from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings
from accounts.models import User, Admin


class IsOwnerOrAdmin(BasePermission):
    """Allow access only to the object's owner or an admin user.

    This permission expects a Bearer JWT in `Authorization` header with
    a `user_id` payload (string UUID). It stores decoded values on the
    request for reuse.
    """

    def _decode_token(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None, False
        token = auth_header.split(' ', 1)[1].strip()
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get('user_id')
            if not user_id:
                return None, False
            try:
                user = User.objects.get(id=user_id)
            except Exception:
                return None, False
            is_admin = Admin.objects.filter(email=user.email).exists()
            return user, is_admin
        except Exception:
            return None, False

    def has_permission(self, request, view):
        user, is_admin = self._decode_token(request)
        if not user:
            return False
        # attach for later use
        request._auth_user = user
        request._auth_is_admin = is_admin
        return True

    def has_object_permission(self, request, view, obj):
        # Admins have all permissions
        if getattr(request, '_auth_is_admin', False):
            return True
        user = getattr(request, '_auth_user', None)
        if not user:
            return False
        # Owner may act on their own object
        try:
            return str(obj.user.get_uuid_string()) == str(user.get_uuid_string())
        except Exception:
            return False
