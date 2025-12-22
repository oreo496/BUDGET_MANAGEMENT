from datetime import timedelta
from decimal import Decimal
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transactions.models import Transaction
from utils.strategies import NotificationContext, MultiChannelNotificationStrategy
from .models import Goal
from .serializers import GoalSerializer


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    notification_context = NotificationContext(MultiChannelNotificationStrategy())

    def get_queryset(self):
        user = getattr(self.request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            return Goal.objects.filter(user=user).order_by('-created_at')
        return Goal.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def insights(self, request, pk=None):
        """Provide AI-style insights for a goal and notify on risk."""
        try:
            goal = self.get_object()
            today = timezone.now().date()
            start_range = today - timedelta(days=30)

            # Aggregate recent income/expense
            txns = Transaction.objects.filter(user=request.user, date__range=(start_range, today))
            income = sum((txn.amount for txn in txns if txn.type == 'INCOME'), Decimal('0'))
            expense = sum((txn.amount for txn in txns if txn.type == 'EXPENSE'), Decimal('0'))
            monthly_surplus = Decimal(income) - Decimal(expense)

            target_remaining = Decimal(goal.target_amount) - Decimal(goal.current_amount)
            if goal.deadline:
                days_left = max((goal.deadline - today).days, 1)
            else:
                days_left = 180  # assume six months if no deadline
            months_left = max(Decimal(days_left) / Decimal(30), Decimal('1'))
            required_monthly = target_remaining / months_left

            progress_pct = float(goal.progress_percentage)
            risk = monthly_surplus < required_monthly
            notification_created = False
            if risk:
                subject = f"Goal risk: {goal.title}"
                message = (
                    f"You need about ${required_monthly:.2f} per month to hit this goal, "
                    f"but your last 30 days surplus was ${monthly_surplus:.2f}."
                )
                notification_created = self.notification_context.notify(
                    recipient=str(request.user.id),
                    subject=subject,
                    message=message
                )

            return Response({
                'progress_percentage': progress_pct,
                'monthly_surplus': float(monthly_surplus),
                'required_monthly': float(required_monthly),
                'risk': risk,
                'notification_created': bool(notification_created),
                'days_left': days_left
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # Return a user-friendly error instead of 500
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

