"""
Enhanced authentication views using Strategy pattern.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from utils.strategies import (
    AuthenticationContext,
    PasswordAuthenticationStrategy,
    MFAAuthenticationStrategy,
    TokenAuthenticationStrategy
)
import jwt
from django.conf import settings
from datetime import datetime, timedelta


@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_strategy(request):
    """
    Enhanced login using Strategy pattern for flexible authentication.
    Supports password-only and MFA authentication.
    
    POST /api/auth/login-strategy/
    Body: {
        "email": "user@example.com",
        "password": "password123",
        "mfa_token": "123456"  // optional, required if MFA enabled
    }
    """
    email = request.data.get('email')
    password = request.data.get('password')
    mfa_token = request.data.get('mfa_token')
    
    if not email or not password:
        return Response(
            {'detail': 'Email and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Use MFA strategy (handles both MFA and non-MFA users)
    auth_context = AuthenticationContext(MFAAuthenticationStrategy())
    result = auth_context.authenticate(
        email=email,
        password=password,
        mfa_token=mfa_token
    )
    
    if not result:
        return Response(
            {'detail': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Check if MFA is required but not provided
    if result.get('requires_mfa'):
        return Response(
            {
                'requires_mfa': True,
                'message': 'MFA token required. Please provide your 6-digit code.'
            },
            status=status.HTTP_200_OK
        )
    
    # Generate JWT token
    payload = {
        'user_id': result['user_id'],
        'email': result['email'],
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return Response({
        'token': token,
        'user': {
            'id': result['user_id'],
            'email': result['email'],
            'first_name': result.get('first_name', ''),
            'last_name': result.get('last_name', '')
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """
    Verify JWT token using Token Authentication Strategy.
    
    POST /api/auth/verify-token/
    Body: {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
    """
    token = request.data.get('token')
    
    if not token:
        return Response(
            {'detail': 'Token is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    auth_context = AuthenticationContext(TokenAuthenticationStrategy())
    result = auth_context.authenticate(token=token)
    
    if not result:
        return Response(
            {'detail': 'Invalid or expired token.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response({
        'valid': True,
        'user': result
    }, status=status.HTTP_200_OK)
