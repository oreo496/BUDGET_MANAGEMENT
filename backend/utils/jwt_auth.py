"""
JWT Authentication utilities.
"""
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from accounts.models import User


def generate_token(user):
    """Generate JWT token for user."""
    payload = {
        'user_id': user.get_uuid_string(),
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token):
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_from_token(token):
    """Get user object from JWT token."""
    payload = verify_token(token)
    if not payload:
        return None
    
    try:
        user = User.objects.get(email=payload['email'])
        return user
    except User.DoesNotExist:
        return None

