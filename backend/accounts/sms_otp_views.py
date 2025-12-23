"""SMS OTP authentication views."""
import random
import string
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import User, SMSOtp
from .serializers import UserSerializer
from utils.security import sanitize_input, validate_phone


def send_sms_otp(phone: str, code: str) -> bool:
    """Send OTP via SMS using Twilio or print in DEBUG."""
    if settings.DEBUG:
        # In DEBUG, print to console
        print(f"\n[SMS OTP DEBUG] Sending code '{code}' to {phone}")
        return True
    
    try:
        from twilio.rest import Client
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        twilio_number = settings.TWILIO_PHONE_NUMBER
        
        if not all([account_sid, auth_token, twilio_number]):
            print("[SMS OTP] Twilio credentials not configured.")
            return False
        
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your Budget Management OTP is: {code}. Valid for 10 minutes.",
            from_=twilio_number,
            to=phone
        )
        return True
    except Exception as e:
        print(f"[SMS OTP Error] Failed to send SMS: {str(e)}")
        return False


@api_view(['POST'])
@permission_classes([AllowAny])
def request_sms_otp(request):
    """Request SMS OTP for a user. User must be authenticated or identified."""
    # For unauthenticated: require identifier + password to prove identity
    # For authenticated: use the Bearer token
    
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    user = None
    
    if auth_header.startswith('Bearer '):
        # Authenticated request
        import jwt
        token = auth_header.split(' ', 1)[1].strip()
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
        except Exception:
            pass
    
    if not user:
        # Unauthenticated: require identifier and password
        identifier = sanitize_input(
            request.data.get('identifier') or request.data.get('email') or request.data.get('username', ''),
            max_length=100
        )
        password = request.data.get('password', '')
        
        if not identifier or not password:
            return Response(
                {'error': 'Identifier and password required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if '@' in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(username=identifier)
            
            if not user.check_password(password) or user.status != 'ACTIVE':
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.sms_otp_enabled or not user.sms_phone:
        return Response(
            {'error': 'SMS OTP not enabled for this account.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Generate 6-digit OTP
    code = ''.join(random.choices(string.digits, k=6))
    expires_at = timezone.now() + timedelta(minutes=10)
    
    # Delete expired OTPs
    SMSOtp.objects.filter(user=user, expires_at__lte=timezone.now()).delete()
    
    # Create new OTP
    sms_otp = SMSOtp.objects.create(
        user=user,
        code=code,
        expires_at=expires_at
    )
    
    # Send SMS
    success = send_sms_otp(user.sms_phone, code)
    
    if not success:
        sms_otp.delete()
        return Response(
            {'error': 'Failed to send SMS. Please try again later.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({
        'message': f'OTP sent to {user.sms_phone}.',
        'expires_in_seconds': 600
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_sms_otp(request):
    """Verify SMS OTP and return JWT token."""
    identifier = sanitize_input(
        request.data.get('identifier') or request.data.get('email') or request.data.get('username', ''),
        max_length=100
    )
    password = request.data.get('password', '')
    otp_code = sanitize_input(request.data.get('code', ''), max_length=6)
    
    if not identifier or not password or not otp_code:
        return Response(
            {'error': 'Identifier, password, and OTP code required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        if '@' in identifier:
            user = User.objects.get(email=identifier)
        else:
            user = User.objects.get(username=identifier)
        
        if not user.check_password(password) or user.status != 'ACTIVE':
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.sms_otp_enabled:
        return Response(
            {'error': 'SMS OTP not enabled for this account.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get latest OTP
    try:
        sms_otp = SMSOtp.objects.filter(user=user).latest('created_at')
    except SMSOtp.DoesNotExist:
        return Response(
            {'error': 'No OTP requested. Call request-sms-otp first.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check expiry
    if sms_otp.is_expired():
        sms_otp.delete()
        return Response(
            {'error': 'OTP expired. Request a new one.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check attempts
    if sms_otp.is_max_attempts_exceeded():
        sms_otp.delete()
        return Response(
            {'error': 'Too many failed attempts. Request a new OTP.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verify code
    if sms_otp.code != otp_code:
        sms_otp.attempts += 1
        sms_otp.save()
        remaining = max(0, sms_otp.max_attempts - sms_otp.attempts)
        return Response(
            {'error': f'Invalid OTP. {remaining} attempts remaining.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Success: delete OTP and return token
    sms_otp.delete()
    
    import jwt
    from datetime import datetime
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
        'message': 'OTP verified successfully.'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_sms_otp(request):
    """Enable SMS OTP for the authenticated user."""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith('Bearer '):
        return Response(
            {'error': 'Authentication required.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token = auth_header.split(' ', 1)[1].strip()
    try:
        import jwt
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
    except Exception:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    phone = request.data.get('phone', '').strip()
    if not phone:
        return Response({'error': 'Phone number required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        phone = validate_phone(phone)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    user.sms_phone = phone
    user.sms_otp_enabled = True
    user.save()
    
    return Response({
        'message': 'SMS OTP enabled.',
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_sms_otp(request):
    """Disable SMS OTP for the authenticated user."""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith('Bearer '):
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ', 1)[1].strip()
    try:
        import jwt
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
    except Exception:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    user.sms_otp_enabled = False
    user.sms_phone = None
    user.save()
    
    # Clean up any pending OTPs
    SMSOtp.objects.filter(user=user).delete()
    
    return Response({
        'message': 'SMS OTP disabled.',
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)
