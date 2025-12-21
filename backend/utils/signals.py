"""
Django signals integration with Observer pattern.
This module connects Django's signal system with our custom observers.
"""
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from utils.observers import EventDispatcher
from budgets.observers import BudgetExceededObserver, SpendingPatternObserver, GoalProgressObserver
from transactions.observers import (
    FraudDetectionObserver, 
    TransactionCategorizationObserver,
    LargeTransactionObserver,
    RecurringTransactionObserver
)


# Initialize event dispatcher
dispatcher = EventDispatcher()

# Register observers
budget_exceeded_observer = BudgetExceededObserver()
spending_pattern_observer = SpendingPatternObserver()
goal_progress_observer = GoalProgressObserver()
fraud_detection_observer = FraudDetectionObserver()
transaction_categorization_observer = TransactionCategorizationObserver()
large_transaction_observer = LargeTransactionObserver(threshold=Decimal('500.00'))
recurring_transaction_observer = RecurringTransactionObserver()

# Subscribe observers to events
dispatcher.subscribe('budget_exceeded', budget_exceeded_observer)
dispatcher.subscribe('budget_warning', budget_exceeded_observer)
dispatcher.subscribe('unusual_spending', spending_pattern_observer)
dispatcher.subscribe('spending_trend', spending_pattern_observer)
dispatcher.subscribe('goal_milestone', goal_progress_observer)
dispatcher.subscribe('goal_achieved', goal_progress_observer)
dispatcher.subscribe('goal_deadline_approaching', goal_progress_observer)
dispatcher.subscribe('potential_fraud', fraud_detection_observer)
dispatcher.subscribe('fraud_confirmed', fraud_detection_observer)
dispatcher.subscribe('transaction_created', transaction_categorization_observer)
dispatcher.subscribe('transaction_created', large_transaction_observer)
dispatcher.subscribe('recurring_detected', recurring_transaction_observer)


# ============================================================================
# TRANSACTION SIGNALS
# ============================================================================

@receiver(post_save, sender='transactions.Transaction')
def transaction_post_save(sender, instance, created, **kwargs):
    """Handle transaction creation and updates."""
    if created:
        # Dispatch transaction created event
        dispatcher.dispatch('transaction_created', {
            'transaction_id': instance.get_uuid_string(),
            'user_id': str(instance.user_id),
            'amount': float(instance.amount),
            'type': instance.type,
            'description': instance.description or '',
            'category': instance.category.name if instance.category else None,
            'date': str(instance.date)
        })
        
        # Check for potential fraud
        if _is_potential_fraud(instance):
            dispatcher.dispatch('potential_fraud', {
                'transaction_id': instance.get_uuid_string(),
                'user_id': str(instance.user_id),
                'amount': float(instance.amount),
                'description': instance.description or '',
                'reason': 'Unusual transaction pattern'
            })
        
        # Update budget spending if applicable
        if instance.category and instance.type == 'EXPENSE':
            _check_budget_status(instance)


def _is_potential_fraud(transaction) -> bool:
    """Simple fraud detection logic."""
    from transactions.models import Transaction
    from datetime import timedelta
    from django.utils import timezone
    
    # Check for multiple large transactions in short time
    recent_transactions = Transaction.objects.filter(
        user=transaction.user,
        date__gte=timezone.now().date() - timedelta(hours=1),
        type='EXPENSE'
    ).exclude(id=transaction.id)
    
    # Flag if multiple large transactions (>$500) in last hour
    large_recent = [t for t in recent_transactions if abs(t.amount) > 500]
    if len(large_recent) >= 2 and abs(transaction.amount) > 500:
        return True
    
    # Flag if transaction is unusually large (>$5000)
    if abs(transaction.amount) > 5000:
        return True
    
    return False


def _check_budget_status(transaction):
    """Check if transaction causes budget to be exceeded."""
    from budgets.models import Budget
    from transactions.models import Transaction
    from django.db.models import Sum
    
    try:
        # Find applicable budgets
        budgets = Budget.objects.filter(
            user=transaction.user,
            category=transaction.category
        )
        
        for budget in budgets:
            # Calculate total spending for this budget period
            # For simplicity, using current month
            from datetime import date
            today = date.today()
            start_of_month = date(today.year, today.month, 1)
            
            total_spent = Transaction.objects.filter(
                user=transaction.user,
                category=transaction.category,
                type='EXPENSE',
                date__gte=start_of_month,
                date__lte=today
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            
            total_spent = abs(total_spent)
            
            # Check if budget exceeded
            if total_spent > budget.amount:
                dispatcher.dispatch('budget_exceeded', {
                    'user_id': str(transaction.user_id),
                    'category': budget.category.name,
                    'budget_amount': float(budget.amount),
                    'spent_amount': float(total_spent)
                })
            # Check if warning threshold (80%)
            elif total_spent >= budget.amount * Decimal('0.80'):
                dispatcher.dispatch('budget_warning', {
                    'user_id': str(transaction.user_id),
                    'category': budget.category.name,
                    'budget_amount': float(budget.amount),
                    'spent_amount': float(total_spent)
                })
    except Exception as e:
        print(f"Error checking budget status: {e}")


# ============================================================================
# GOAL SIGNALS
# ============================================================================

@receiver(post_save, sender='goals.Goal')
def goal_post_save(sender, instance, created, **kwargs):
    """Handle goal updates."""
    if not created:
        # Check progress milestones
        progress = float(instance.progress_percentage)
        
        # Check for milestone achievements
        milestones = [25, 50, 75]
        for milestone in milestones:
            if progress >= milestone and progress < milestone + 5:  # 5% buffer
                dispatcher.dispatch('goal_milestone', {
                    'user_id': str(instance.user_id),
                    'goal_title': instance.title,
                    'percentage': milestone,
                    'current_amount': float(instance.current_amount),
                    'target_amount': float(instance.target_amount)
                })
                break
        
        # Check if goal achieved
        if progress >= 100:
            dispatcher.dispatch('goal_achieved', {
                'user_id': str(instance.user_id),
                'goal_title': instance.title,
                'amount': float(instance.target_amount)
            })
        
        # Check deadline approaching
        if instance.deadline:
            from datetime import date
            days_remaining = (instance.deadline - date.today()).days
            if days_remaining <= 7 and progress < 100:
                dispatcher.dispatch('goal_deadline_approaching', {
                    'user_id': str(instance.user_id),
                    'goal_title': instance.title,
                    'days_remaining': days_remaining,
                    'progress_percentage': progress
                })


# ============================================================================
# BUDGET SIGNALS
# ============================================================================

@receiver(post_save, sender='budgets.Budget')
def budget_post_save(sender, instance, created, **kwargs):
    """Handle budget creation and updates."""
    if created:
        # Could dispatch budget_created event if needed
        pass


# ============================================================================
# FRAUD FLAG SIGNALS
# ============================================================================

@receiver(post_save, sender='transactions.Transaction')
def fraud_flag_handler(sender, instance, **kwargs):
    """Handle fraud flag updates."""
    if instance.flagged_fraud:
        dispatcher.dispatch('fraud_confirmed', {
            'transaction_id': instance.get_uuid_string(),
            'user_id': str(instance.user_id)
        })
