"""
Transaction-specific observers for monitoring transaction events.
"""
from decimal import Decimal
from typing import Dict, Any
from utils.observers import Observer
from utils.strategies import NotificationContext, MultiChannelNotificationStrategy


class FraudDetectionObserver(Observer):
    """
    Observer that monitors transactions for potential fraud.
    """
    
    def __init__(self):
        self.notification_context = NotificationContext(
            MultiChannelNotificationStrategy()
        )
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle fraud-related events."""
        if event_type == 'potential_fraud':
            self._handle_potential_fraud(data)
        elif event_type == 'fraud_confirmed':
            self._handle_fraud_confirmed(data)
    
    def _handle_potential_fraud(self, data: Dict[str, Any]) -> None:
        """Handle potential fraud detection."""
        user_id = data.get('user_id')
        transaction_id = data.get('transaction_id')
        amount = data.get('amount', 0)
        description = data.get('description', 'Unknown')
        reason = data.get('reason', 'Unusual activity')
        
        subject = "Potential Fraudulent Activity Detected"
        message = (
            f"We detected a potentially fraudulent transaction:\n"
            f"Amount: ${abs(amount):.2f}\n"
            f"Description: {description}\n"
            f"Reason: {reason}\n"
            f"Transaction ID: {transaction_id}\n\n"
            f"Please review this transaction immediately."
        )
        
        self.notification_context.notify(
            recipient=str(user_id),
            subject=subject,
            message=message
        )
    
    def _handle_fraud_confirmed(self, data: Dict[str, Any]) -> None:
        """Handle confirmed fraud."""
        user_id = data.get('user_id')
        transaction_id = data.get('transaction_id')
        
        subject = "Fraud Confirmed - Action Required"
        message = (
            f"A transaction has been confirmed as fraudulent.\n"
            f"Transaction ID: {transaction_id}\n"
            f"We've flagged this transaction and recommend contacting your bank."
        )
        
        self.notification_context.notify(
            recipient=str(user_id),
            subject=subject,
            message=message
        )


class TransactionCategorizationObserver(Observer):
    """
    Observer that automatically categorizes transactions.
    """
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle transaction categorization events."""
        if event_type == 'transaction_created':
            self._auto_categorize(data)
    
    def _auto_categorize(self, data: Dict[str, Any]) -> None:
        """Automatically categorize transaction based on description."""
        from transactions.models import Transaction
        from categories.models import Category
        
        transaction_id = data.get('transaction_id')
        description = data.get('description', '').lower()
        user_id = data.get('user_id')
        
        # Simple categorization logic
        category_keywords = {
            'groceries': ['grocery', 'supermarket', 'food', 'walmart', 'kroger'],
            'dining': ['restaurant', 'cafe', 'coffee', 'starbucks', 'mcdonald'],
            'transportation': ['gas', 'uber', 'lyft', 'taxi', 'parking'],
            'utilities': ['electric', 'water', 'internet', 'phone', 'utility'],
            'entertainment': ['movie', 'netflix', 'spotify', 'game', 'concert'],
            'shopping': ['amazon', 'store', 'mall', 'shop'],
        }
        
        detected_category = None
        for category_name, keywords in category_keywords.items():
            if any(keyword in description for keyword in keywords):
                detected_category = category_name
                break
        
        if detected_category:
            try:
                transaction = Transaction.objects.get(id=transaction_id)
                category, _ = Category.objects.get_or_create(
                    user_id=user_id,
                    name=detected_category.title(),
                    type='EXPENSE'
                )
                transaction.category = category
                transaction.save()
            except Exception as e:
                print(f"Error auto-categorizing transaction: {e}")


class LargeTransactionObserver(Observer):
    """
    Observer that monitors large transactions.
    """
    
    def __init__(self, threshold: Decimal = Decimal('1000.00')):
        self.threshold = threshold
        self.notification_context = NotificationContext()
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle transaction events."""
        if event_type == 'transaction_created':
            self._check_large_transaction(data)
    
    def _check_large_transaction(self, data: Dict[str, Any]) -> None:
        """Check if transaction is unusually large."""
        amount = abs(Decimal(str(data.get('amount', 0))))
        user_id = data.get('user_id')
        description = data.get('description', 'Unknown')
        transaction_type = data.get('type', 'EXPENSE')
        
        if amount >= self.threshold:
            subject = f"Large {transaction_type.title()} Detected"
            message = (
                f"A large {transaction_type.lower()} of ${amount:.2f} was recorded.\n"
                f"Description: {description}\n"
                f"Please verify this transaction is correct."
            )
            
            self.notification_context.notify(
                recipient=str(user_id),
                subject=subject,
                message=message
            )


class RecurringTransactionObserver(Observer):
    """
    Observer that detects recurring transactions.
    """
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle recurring transaction detection."""
        if event_type == 'recurring_detected':
            self._handle_recurring_detected(data)
    
    def _handle_recurring_detected(self, data: Dict[str, Any]) -> None:
        """Handle recurring transaction detection."""
        user_id = data.get('user_id')
        description = data.get('description')
        amount = data.get('amount', 0)
        frequency = data.get('frequency', 'monthly')
        
        notification_context = NotificationContext()
        
        subject = "Recurring Transaction Detected"
        message = (
            f"We detected a recurring {frequency} transaction:\n"
            f"Amount: ${abs(amount):.2f}\n"
            f"Description: {description}\n"
            f"Consider setting up a budget for this recurring expense."
        )
        
        notification_context.notify(
            recipient=str(user_id),
            subject=subject,
            message=message
        )
