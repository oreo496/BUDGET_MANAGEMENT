from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings
from accounts.models import Admin as AppAdmin


class IsAdminToken(BasePermission):
    """Check for a valid admin JWT in Authorization: Bearer <token>."""

    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        print(f"[IsAdminToken] Auth header: {auth_header[:50]}..." if auth_header else "[IsAdminToken] No auth header")
        
        if not auth_header.startswith('Bearer '):
            print("[IsAdminToken] Auth header doesn't start with 'Bearer '")
            return False
            
        token = auth_header.split(' ', 1)[1].strip()
        print(f"[IsAdminToken] Token extracted, length: {len(token)}")
        
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            print(f"[IsAdminToken] JWT decoded successfully, payload: {payload}")
            
            admin_id = payload.get('admin_id')
            if not admin_id:
                print("[IsAdminToken] No admin_id in payload")
                return False
                
            try:
                admin = AppAdmin.objects.get(id=admin_id)
                print(f"[IsAdminToken] Admin found: {admin.email}")
                request._app_admin = admin
                return True
            except AppAdmin.DoesNotExist:
                print(f"[IsAdminToken] Admin not found with id: {admin_id}")
                return False
        except Exception as e:
            print(f"[IsAdminToken] Exception: {type(e).__name__}: {e}")
            return False
