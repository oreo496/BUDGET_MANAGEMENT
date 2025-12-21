from django.db import models
import uuid
from accounts.models import User
from decimal import Decimal
from datetime import timedelta


class Budget(models.Model):
    id = models.BinaryField(primary_key=True, max_length=16, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, 
                                  db_column='category_id')
    period = models.CharField(
        max_length=10,
        choices=[('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly')]
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'budgets'
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gte=0), name='amount_non_negative')
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            uuid_obj = uuid.uuid4()
            self.id = uuid_obj.bytes
        super().save(*args, **kwargs)

    def get_uuid_string(self):
        return str(uuid.UUID(bytes=self.id))
    
    def calculate_period_amount(self, target_period: str = None) -> Decimal:
        """
        Calculate budget amount for different periods using Strategy pattern.
        
        Args:
            target_period: 'WEEKLY', 'MONTHLY', or 'ANNUAL'
        
        Returns:
            Calculated amount for the target period
        """
        from utils.strategies import (
            CalculationContext,
            WeeklyBudgetCalculation,
            MonthlyBudgetCalculation
        )
        
        target_period = target_period or self.period
        
        if target_period == 'WEEKLY':
            context = CalculationContext(WeeklyBudgetCalculation())
            if self.period == 'MONTHLY':
                return context.execute(monthly_amount=self.amount)
            else:
                return self.amount
        elif target_period == 'MONTHLY':
            context = CalculationContext(MonthlyBudgetCalculation())
            if self.period == 'WEEKLY':
                # Convert weekly to monthly
                return self.amount * 52 / 12
            else:
                return self.amount
        elif target_period == 'ANNUAL':
            if self.period == 'MONTHLY':
                return self.amount * 12
            else:  # WEEKLY
                return self.amount * 52
        
        return self.amount
    
    def get_spending_status(self) -> dict:
        """Get current spending status for this budget."""
        from transactions.models import Transaction
        from django.db.models import Sum
        from datetime import date
        
        today = date.today()
        
        # Determine date range based on period
        if self.period == 'MONTHLY':
            start_date = date(today.year, today.month, 1)
        else:  # WEEKLY
            # Get start of current week (Monday)
            start_date = today - timedelta(days=today.weekday())
        
        # Calculate total spending
        total_spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            type='EXPENSE',
            date__gte=start_date,
            date__lte=today
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        total_spent = abs(total_spent)
        remaining = self.amount - total_spent
        percentage = (total_spent / self.amount * 100) if self.amount > 0 else Decimal('0.00')
        
        return {
            'budget_amount': self.amount,
            'spent_amount': total_spent,
            'remaining_amount': remaining,
            'percentage_used': percentage,
            'is_exceeded': total_spent > self.amount,
            'period': self.period
        }

    def __str__(self):
        return f"{self.category.name}: ${self.amount} ({self.period})"

