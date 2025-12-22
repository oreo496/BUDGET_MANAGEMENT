from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsOwnerOrAdmin
from .models import Loan
from .serializers import LoanSerializer
import jwt
from django.conf import settings
from accounts.models import User
from ai_alerts.models import AIAlert
from utils.strategies import NotificationContext, MultiChannelNotificationStrategy


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    permission_classes = [IsOwnerOrAdmin]
    notification_context = NotificationContext(MultiChannelNotificationStrategy())

    def get_queryset(self):
        # If Authorization Bearer JWT present, return loans for that user
        request = self.request
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1].strip()
            try:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                user_id = payload.get('user_id')
                if user_id:
                    loans = Loan.objects.filter(user__id=user_id).order_by('-created_at')
                    self._ensure_loan_notifications(loans)
                    return loans
            except Exception:
                return Loan.objects.none()
        # Otherwise return none for security
        return Loan.objects.none()

    def _ensure_loan_notifications(self, loans):
        """Create reminders based on loan timelines."""
        today = timezone.now().date()
        for loan in loans:
            due_date = loan.created_at.date() + timedelta(days=loan.term_months * 30)
            days_remaining = (due_date - today).days
            loan_key = loan.get_uuid_string()

            # Avoid spamming by only sending one reminder per day per loan
            already_sent = AIAlert.objects.filter(
                user=loan.user,
                type='LOAN_REMINDER',
                message__contains=f"loan:{loan_key}",
                created_at__date=today
            ).exists()
            if already_sent:
                continue

            if days_remaining in (30, 14, 7, 1, 0) or days_remaining < 0:
                status_label = "overdue" if days_remaining < 0 else f"due in {days_remaining} days"
                subject = f"Loan reminder: {loan.lender_name}"
                message = (
                    f"Loan loan:{loan_key} for ${loan.amount} is {status_label}. "
                    f"Monthly payment is about ${loan.calculate_monthly_payment():.2f}."
                )
                self.notification_context.notify(
                    recipient=str(loan.user.id),
                    subject=subject,
                    message=message
                )

    def create(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        token = auth_header.split(' ', 1)[1].strip()
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get('user_id')
            if not user_id:
                raise Exception('user_id missing')
            user = User.objects.get(id=user_id)
        except Exception as e:
            return Response({'detail': 'Invalid token', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        serializer = LoanSerializer(data=data)
        if serializer.is_valid():
            loan = Loan(
                user=user,
                amount=serializer.validated_data['amount'],
                lender_name=serializer.validated_data.get('lender_name', 'Funder Bank'),
                term_months=serializer.validated_data['term_months'],
                interest_rate=serializer.validated_data.get('interest_rate', 0.0),
            )
            loan.save()
            return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
