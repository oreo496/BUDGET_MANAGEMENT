from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
import jwt
from accounts.models import User, Admin


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
            
            # For admin tokens, validate against Admin model
            if admin_id:
                try:
                    admin = Admin.objects.get(id=admin_id)
                    # Create a pseudo-user object with admin properties for authentication
                    # This allows admin to pass IsAuthenticated checks
                    admin.is_authenticated = True
                    admin.is_active = True
                    return (admin, token)
                except Admin.DoesNotExist:
                    raise exceptions.AuthenticationFailed('Admin not found')
                
            # For regular user tokens, validate against User model
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                # Log for debugging
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"User not found: user_id={user_id}, type={type(user_id)}")
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
