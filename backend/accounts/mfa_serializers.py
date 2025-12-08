"""
Serializers for Multi-Factor Authentication.
"""
from rest_framework import serializers
from .models import User
from .mfa_utils import (
    generate_totp_secret,
    get_totp_uri,
    generate_qr_code,
    verify_totp_token,
    generate_backup_codes,
    save_backup_codes,
    verify_backup_code,
    load_backup_codes
)


class MFASetupSerializer(serializers.Serializer):
    """Serializer for MFA setup response."""
    secret = serializers.CharField(read_only=True)
    qr_code = serializers.CharField(read_only=True)
    backup_codes = serializers.ListField(
        child=serializers.CharField(),
        read_only=True
    )


class MFAVerifySerializer(serializers.Serializer):
    """Serializer for MFA verification."""
    token = serializers.CharField(
        required=True,
        max_length=6,
        min_length=6,
        help_text="6-digit code from authenticator app"
    )
    
    def validate_token(self, value):
        """Validate token format."""
        if not value.isdigit():
            raise serializers.ValidationError("Token must be numeric")
        if len(value) != 6:
            raise serializers.ValidationError("Token must be 6 digits")
        return value


class MFALoginSerializer(serializers.Serializer):
    """Serializer for MFA verification during login."""
    token = serializers.CharField(
        required=True,
        max_length=6,
        min_length=6
    )
    backup_code = serializers.CharField(
        required=False,
        max_length=8,
        min_length=8,
        help_text="Optional backup code if token is not available"
    )
    
    def validate(self, attrs):
        """Validate that either token or backup_code is provided."""
        if not attrs.get('token') and not attrs.get('backup_code'):
            raise serializers.ValidationError(
                "Either token or backup_code must be provided"
            )
        return attrs


class MFADisableSerializer(serializers.Serializer):
    """Serializer for disabling MFA."""
    password = serializers.CharField(
        required=True,
        help_text="User password to confirm MFA disable"
    )

