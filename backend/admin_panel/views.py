from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime, timedelta
import jwt

from .models import SystemLog, AdminAction
from .serializers import SystemLogSerializer, AdminActionSerializer
from accounts.models import Admin as AppAdmin, User
from .permissions import IsAdminToken
from loans.models import Loan
from transactions.models import Transaction


class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SystemLogSerializer
    queryset = SystemLog.objects.all()


class AdminActionViewSet(viewsets.ModelViewSet):
    serializer_class = AdminActionSerializer
    queryset = AdminAction.objects.all()


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """Application-level admin login using `accounts.Admin` model.

    POST /api/admin/auth/login/ { email, password }
    Returns JWT token for admin on success.
    """
    data = request.data
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return Response({'detail': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        admin = AppAdmin.objects.get(email=email)
    except AppAdmin.DoesNotExist:
        return Response({'detail': 'Admin account not found. Please create an admin account first.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not admin.check_password(password):
        return Response({'detail': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = jwt.encode({
        'admin_id': admin.get_uuid_string(),
        'email': admin.email,
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA)
    }, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return Response({'token': token, 'admin': {'email': admin.email}}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminToken])
def admin_logout(request):
    # Stateless JWT: logout by client discarding token. Server can record audit if desired.
    return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminToken])
def dashboard(request):
    """Simple admin dashboard: counts of users, loans, transactions."""
    users_count = User.objects.count()
    loans_count = Loan.objects.count()
    transactions_count = Transaction.objects.count()
    return Response({
        'users': users_count,
        'loans': loans_count,
        'transactions': transactions_count,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminToken])
def list_users(request):
    """List all users with basic info."""
    users = User.objects.all().order_by('-created_at')
    users_data = [{
        'id': str(user.id),
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_active': user.status == 'ACTIVE',
        'created_at': user.created_at.isoformat(),
        'phone': user.phone,
    } for user in users]
    return Response(users_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminToken])
def toggle_user_status(request, user_id):
    """Activate or deactivate a user."""
    try:
        user = User.objects.get(id=user_id)
        user.status = 'INACTIVE' if user.status == 'ACTIVE' else 'ACTIVE'
        user.save()
        return Response({'detail': f'User {user.email} status updated to {user.status}'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAdminToken])
def delete_user(request, user_id):
    """Delete a user account."""
    try:
        user = User.objects.get(id=user_id)
        user_email = user.email
        user.delete()
        return Response({'detail': f'User {user_email} deleted successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAdminToken])
def system_stats(request):
    """Get system statistics and health."""
    # Use Django ORM instead of raw SQL to prevent SQL injection
    total_users = User.objects.count()
    total_transactions = Transaction.objects.count()
    total_loans = Loan.objects.count()
    from bank_accounts.models import BankAccount
    total_accounts = BankAccount.objects.count()
    
    return Response({
        'users': {
            'total': total_users,
            'active': User.objects.filter(status='ACTIVE').count(),
            'inactive': User.objects.filter(status='INACTIVE').count(),
        },
        'transactions': {
            'total': total_transactions,
        },
        'loans': {
            'total': total_loans,
            'pending': Loan.objects.filter(status='PENDING').count(),
            'approved': Loan.objects.filter(status='APPROVED').count(),
            'rejected': Loan.objects.filter(status='REJECTED').count(),
        },
        'accounts': {
            'total': total_accounts,
        },
        'system': {
            'database_status': 'Connected',
            'api_version': '1.0.0',
        }
    }, status=status.HTTP_200_OK)

