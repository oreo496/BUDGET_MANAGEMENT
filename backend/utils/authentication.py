from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
import jwt
from accounts.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT Authentication for DRF views.
    Expects Authorization header: Bearer <token>
    """
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return None
            
        try:
            # Expected format: "Bearer <token>"
            parts = auth_header.split()
            
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return None
                
            token = parts[1]
            
            # Decode JWT token
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            # Check if this is an admin token or user token
            user_id = payload.get('user_id')
            admin_id = payload.get('admin_id')
            
            if not user_id and not admin_id:
                raise exceptions.AuthenticationFailed('Invalid token payload')
            
            # For admin tokens, we don't validate against User model
            # Admin authentication is handled separately
            if admin_id:
                return (None, token)  # Return None for user, just validate token
                
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('User not found')
                
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')
    
    def authenticate_header(self, request):
        return 'Bearer'
