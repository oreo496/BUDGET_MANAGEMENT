from django.db import models
import uuid
from decimal import Decimal


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='loans')
    lender_name = models.CharField(max_length=100, default='Funder Bank')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    term_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    status = models.CharField(
        max_length=12,
        choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'loans'

    def get_uuid_string(self):
        return str(self.id)
    
    def calculate_interest(self, calculation_type: str = 'simple') -> Decimal:
        """
        Calculate loan interest using Strategy pattern.
        
        Args:
            calculation_type: 'simple' or 'compound'
        
        Returns:
            Total interest amount
        """
        from utils.strategies import (
            CalculationContext,
            SimpleInterestCalculation,
            CompoundInterestCalculation
        )
        
        rate_decimal = self.interest_rate / 100  # Convert percentage to decimal
        time_years = Decimal(str(self.term_months)) / 12
        
        if calculation_type == 'compound':
            context = CalculationContext(CompoundInterestCalculation())
            return context.execute(
                principal=self.amount,
                rate=rate_decimal,
                time_years=time_years,
                compounds_per_year=12
            )
        else:  # simple interest
            context = CalculationContext(SimpleInterestCalculation())
            return context.execute(
                principal=self.amount,
                rate=rate_decimal,
                time_years=time_years
            )
    
    def calculate_monthly_payment(self) -> Decimal:
        """Calculate monthly loan payment."""
        if self.term_months == 0:
            return Decimal('0.00')
        
        # Calculate using compound interest for more accurate monthly payment
        total_interest = self.calculate_interest('compound')
        total_amount = self.amount + total_interest
        monthly_payment = total_amount / self.term_months
        
        return monthly_payment.quantize(Decimal('0.01'))
    
    def get_loan_summary(self) -> dict:
        """Get comprehensive loan summary."""
        monthly_payment = self.calculate_monthly_payment()
        simple_interest = self.calculate_interest('simple')
        compound_interest = self.calculate_interest('compound')
        
        return {
            'principal': float(self.amount),
            'interest_rate': float(self.interest_rate),
            'term_months': self.term_months,
            'monthly_payment': float(monthly_payment),
            'total_interest_simple': float(simple_interest),
            'total_interest_compound': float(compound_interest),
            'total_amount': float(self.amount + compound_interest),
            'status': self.status
        }

    def __str__(self):
        return f"Loan {self.id} - {self.user.email} - {self.amount}"
