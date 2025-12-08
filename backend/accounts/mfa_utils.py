"""
Multi-Factor Authentication utilities using TOTP (Time-based One-Time Password).
"""
import pyotp
import qrcode
import io
import base64
import json
import secrets
from django.conf import settings


def generate_totp_secret():
    """Generate a new TOTP secret for a user."""
    return pyotp.random_base32()


def get_totp_uri(user_email, secret, issuer_name="Funder"):
    """
    Generate TOTP URI for QR code generation.
    
    Args:
        user_email: User's email address
        secret: TOTP secret
        issuer_name: Name of the service
    
    Returns:
        TOTP URI string
    """
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=user_email,
        issuer_name=issuer_name
    )


def generate_qr_code(uri):
    """
    Generate QR code image as base64 string.
    
    Args:
        uri: TOTP URI
    
    Returns:
        Base64-encoded PNG image string
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def verify_totp_token(secret, token):
    """
    Verify a TOTP token.
    
    Args:
        secret: User's TOTP secret
        token: 6-digit token from authenticator app
    
    Returns:
        True if token is valid, False otherwise
    """
    if not secret or not token:
        return False
    
    try:
        totp = pyotp.TOTP(secret)
        # Allow tokens from current and previous time window (for clock skew)
        return totp.verify(token, valid_window=1)
    except Exception:
        return False


def generate_backup_codes(count=10):
    """
    Generate backup codes for MFA.
    
    Args:
        count: Number of backup codes to generate
    
    Returns:
        List of backup codes
    """
    codes = []
    for _ in range(count):
        # Generate 8-digit code
        code = ''.join([str(secrets.randbelow(10)) for _ in range(8)])
        codes.append(code)
    return codes


def save_backup_codes(codes):
    """Convert backup codes list to JSON string for storage."""
    return json.dumps(codes)


def load_backup_codes(backup_codes_json):
    """Load backup codes from JSON string."""
    if not backup_codes_json:
        return []
    try:
        return json.loads(backup_codes_json)
    except (json.JSONDecodeError, TypeError):
        return []


def verify_backup_code(backup_codes_json, code):
    """
    Verify a backup code and remove it if valid.
    
    Args:
        backup_codes_json: JSON string of backup codes
        code: Backup code to verify
    
    Returns:
        Tuple (is_valid, updated_backup_codes_json)
    """
    codes = load_backup_codes(backup_codes_json)
    
    if code in codes:
        codes.remove(code)
        return True, save_backup_codes(codes)
    
    return False, backup_codes_json

