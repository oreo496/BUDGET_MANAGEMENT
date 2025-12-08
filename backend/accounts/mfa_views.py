"""
Multi-Factor Authentication views.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .mfa_serializers import (
    MFASetupSerializer,
    MFAVerifySerializer,
    MFADisableSerializer
)
from .mfa_utils import (
    generate_totp_secret,
    get_totp_uri,
    generate_qr_code,
    verify_totp_token,
    generate_backup_codes,
    save_backup_codes,
    verify_backup_code
)
from utils.security import sanitize_input, validate_email


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_mfa(request):
    """
    Setup MFA for the authenticated user.
    Returns QR code and backup codes.
    """
    # Get user from request (would need custom auth middleware)
    # For now, using email from request data
    email = sanitize_input(request.data.get('email'), max_length=100)
    
    try:
        user = User.objects.get(email=email)
        
        if user.two_factor_enabled:
            return Response(
                {'error': 'MFA is already enabled for this user'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate TOTP secret
        secret = generate_totp_secret()
        user.two_factor_secret = secret
        
        # Generate backup codes
        backup_codes = generate_backup_codes()
        user.backup_codes = save_backup_codes(backup_codes)
        
        # Generate QR code
        totp_uri = get_totp_uri(user.email, secret)
        qr_code = generate_qr_code(totp_uri)
        
        # Don't save yet - user needs to verify first
        # Store temporarily in session or return for verification
        
        return Response({
            'secret': secret,
            'qr_code': qr_code,
            'backup_codes': backup_codes,
            'message': 'Scan QR code with authenticator app, then verify with a token'
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_mfa_setup(request):
    """
    Verify MFA setup by confirming a token.
    This enables MFA for the user.
    """
    email = sanitize_input(request.data.get('email'), max_length=100)
    token = sanitize_input(request.data.get('token'), max_length=6)
    secret = sanitize_input(request.data.get('secret'), max_length=32)
    
    if not token or not secret:
        return Response(
            {'error': 'Token and secret are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        
        # Verify token
        if verify_totp_token(secret, token):
            # Enable MFA
            user.two_factor_secret = secret
            user.two_factor_enabled = True
            user.save()
            
            return Response({
                'message': 'MFA enabled successfully',
                'mfa_enabled': True
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid token. Please try again.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_mfa(request):
    """
    Disable MFA for the authenticated user.
    Requires password confirmation.
    """
    email = sanitize_input(request.data.get('email'), max_length=100)
    password = request.data.get('password')
    
    if not password:
        return Response(
            {'error': 'Password is required to disable MFA'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        
        # Verify password
        if not user.check_password(password):
            return Response(
                {'error': 'Invalid password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Disable MFA
        user.two_factor_enabled = False
        user.two_factor_secret = None
        user.backup_codes = None
        user.save()
        
        return Response({
            'message': 'MFA disabled successfully',
            'mfa_enabled': False
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mfa_status(request):
    """Get MFA status for the authenticated user."""
    email = sanitize_input(request.GET.get('email'), max_length=100)
    
    try:
        user = User.objects.get(email=email)
        return Response({
            'mfa_enabled': user.two_factor_enabled,
            'has_backup_codes': bool(user.backup_codes)
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

