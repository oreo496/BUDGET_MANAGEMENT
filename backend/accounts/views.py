from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User, Admin
from .serializers import UserSerializer
from .mfa_utils import verify_totp_token, verify_backup_code
from utils.security import sanitize_input, validate_email, sanitize_sql_input
import jwt
from django.conf import settings
from datetime import datetime, timedelta
import secrets


@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request):
    """Change current user's password using Bearer JWT for auth.

    Endpoint: POST /auth/profile/change-password/
    Body: { current_password, new_password }
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith('Bearer '):
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ', 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get('user_id')
        if not user_id:
            raise Exception('user_id missing in token')

        user = User.objects.get(id=user_id)
        data = request.data
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return Response({'detail': 'Current and new password required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({'detail': 'Current password is incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)

        import re
        pw_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^A-Za-z0-9]).{8,}$'
        if not re.match(pw_pattern, new_password):
            return Response({'detail': 'New password must be at least 8 characters and include uppercase, lowercase, number and special character.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': 'Invalid or expired token', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user with input sanitization."""
    # Sanitize input to prevent XSS and SQL injection
    data = request.data.copy()
    username = sanitize_input(data.get('username', ''), max_length=50)
    if not username:
        return Response({'error': 'Username is required and must be unique.'}, status=status.HTTP_400_BAD_REQUEST)
    # Ensure username is unique before hitting DB unique constraint
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists. Please choose another one.'}, status=status.HTTP_400_BAD_REQUEST)
    data['username'] = username
    
    # Sanitize all string fields
    if 'email' in data:
        try:
            data['email'] = validate_email(data['email'])
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    if 'first_name' in data:
        data['first_name'] = sanitize_input(data['first_name'], max_length=50)
    if 'last_name' in data:
        data['last_name'] = sanitize_input(data['last_name'], max_length=50)
    if 'phone' in data:
        from utils.security import validate_phone
        try:
            data['phone'] = validate_phone(data['phone'])
        except Exception:
            data['phone'] = None
    
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User created successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Authenticate user and return token.
    Supports MFA verification.
    Accepts username or email for login.
    """
    # Sanitize input
    username_or_email = sanitize_input(
        request.data.get('identifier') or request.data.get('email') or request.data.get('username', ''),
        max_length=100
    )
    password = request.data.get('password')
    mfa_token = sanitize_input(request.data.get('mfa_token', ''), max_length=6)
    backup_code = sanitize_input(request.data.get('backup_code', ''), max_length=8)

    if not username_or_email or not password:
        return Response(
            {'error': 'Username/Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Try to find user by username or email
        try:
            if '@' in username_or_email:
                user = User.objects.get(email=validate_email(username_or_email))
            else:
                user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.check_password(password) or user.status != 'ACTIVE':
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if MFA is enabled
        if user.two_factor_enabled:
            # If MFA token not provided, request it
            if not mfa_token and not backup_code:
                return Response({
                    'mfa_required': True,
                    'message': 'MFA token required'
                }, status=status.HTTP_200_OK)
            
            # Verify MFA token or backup code
            mfa_valid = False
            
            if mfa_token:
                mfa_valid = verify_totp_token(user.two_factor_secret, mfa_token)
            
            if not mfa_valid and backup_code:
                is_valid, updated_codes = verify_backup_code(user.backup_codes, backup_code)
                if is_valid:
                    user.backup_codes = updated_codes
                    user.save()
                    mfa_valid = True
            
            if not mfa_valid:
                return Response(
                    {'error': 'Invalid MFA token or backup code'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        # Generate JWT token
        token = jwt.encode(
            {
                'user_id': user.get_uuid_string(),
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA)
            },
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return Response({
            'token': token,
            'user': UserSerializer(user).data,
            'mfa_enabled': user.two_factor_enabled
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def profile(request):
    """Get current user profile.

    Supports a simple Bearer JWT in the `Authorization` header for development.
    If no valid token is provided, returns 401.
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith('Bearer '):
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ', 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get('user_id')
        if not user_id:
            raise Exception('user_id missing in token')

        # User.id is a UUIDField; Django accepts the string representation
        user = User.objects.get(id=user_id)
        # Determine if this user is also an admin (by email)
        is_admin = Admin.objects.filter(email=user.email).exists()
        return Response({'user': UserSerializer(user).data, 'is_admin': is_admin}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': 'Invalid or expired token', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def update_profile(request):
    """Update user profile using Bearer JWT in `Authorization` header.

    For development this accepts a JWT and updates the fields present in the request.
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith('Bearer '):
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ', 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get('user_id')
        if not user_id:
            raise Exception('user_id missing in token')

        user = User.objects.get(id=user_id)
        data = request.data.copy()
        # Allow updating first_name, last_name, phone only for now
        for field in ('first_name', 'last_name', 'phone'):
            if field in data:
                setattr(user, field, sanitize_input(data[field], max_length=50))
        user.save()
        is_admin = Admin.objects.filter(email=user.email).exists()
        return Response({'user': UserSerializer(user).data, 'is_admin': is_admin}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': 'Invalid or expired token', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

