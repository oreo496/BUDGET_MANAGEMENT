"""
Budget-specific observers for monitoring budget events.
"""
from decimal import Decimal
from typing import Dict, Any
from utils.observers import Observer
from utils.strategies import NotificationContext, MultiChannelNotificationStrategy


class BudgetExceededObserver(Observer):
    """
    Observer that monitors when budgets are exceeded.
    Sends notifications when spending exceeds budget limits.
    """
    
    def __init__(self):
        self.notification_context = NotificationContext(
            MultiChannelNotificationStrategy()
        )
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle budget-related events."""
        if event_type == 'budget_exceeded':
            self._handle_budget_exceeded(data)
        elif event_type == 'budget_warning':
            self._handle_budget_warning(data)
    
    def _handle_budget_exceeded(self, data: Dict[str, Any]) -> None:
        """Handle budget exceeded event."""
        user_id = data.get('user_id')
        category = data.get('category')
        budget_amount = data.get('budget_amount', 0)
        spent_amount = data.get('spent_amount', 0)
        
        subject = f"Budget Exceeded: {category}"
        message = (
            f"Your {category} budget of ${budget_amount:.2f} has been exceeded. "
            f"You've spent ${spent_amount:.2f} so far."
        )
        
        self.notification_context.notify(
            recipient=str(user_id),
            subject=subject,
            message=message
        )
    
    def _handle_budget_warning(self, data: Dict[str, Any]) -> None:
        """Handle budget warning event (e.g., 80% threshold)."""
        user_id = data.get('user_id')
        category = data.get('category')
        budget_amount = data.get('budget_amount', 0)
        spent_amount = data.get('spent_amount', 0)
        percentage = (spent_amount / budget_amount * 100) if budget_amount > 0 else 0
        
        subject = f"Budget Warning: {category}"
        message = (
            f"You've used {percentage:.0f}% of your {category} budget. "
            f"${spent_amount:.2f} of ${budget_amount:.2f} spent."
        )
        
        self.notification_context.notify(
            recipient=str(user_id),
            subject=subject,
            message=message
        )


class SpendingPatternObserver(Observer):
    """
    Observer that analyzes spending patterns and provides insights.
    """
    
    def __init__(self):
        self.notification_context = NotificationContext()
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle spending pattern events."""
        if event_type == 'unusual_spending':
            self._handle_unusual_spending(data)
        elif event_type == 'spending_trend':
            self._handle_spending_trend(data)
    
    def _handle_unusual_spending(self, data: Dict[str, Any]) -> None:
        """Handle unusual spending detected."""
        user_id = data.get('user_id')
        amount = data.get('amount', 0)
        category = data.get('category', 'Unknown')
        average = data.get('average', 0)
        
        subject = "Unusual Spending Detected"
        message = (
            f"We detected an unusual transaction of ${amount:.2f} in {category}. "
            f"This is significantly higher than your average of ${average:.2f}."
        )
        
        self.notification_context.notify(
            recipient=str(user_id),
            subject=subject,
            message=message
        )
    
    def _handle_spending_trend(self, data: Dict[str, Any]) -> None:
        """Handle spending trend analysis."""
        user_id = data.get('user_id')
        trend = data.get('trend', 'stable')
        category = data.get('category', 'overall')
        
        if trend == 'increasing':
            subject = f"Spending Trend Alert: {category}"
            message = f"Your {category} spending has been increasing over the past month."
            
            self.notification_context.notify(
                recipient=str(user_id),
                subject=subject,
                message=message
            )


class GoalProgressObserver(Observer):
    """
    Observer that monitors savings goal progress.
    """
    
    def __init__(self):
        self.notification_context = NotificationContext()
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle goal-related events."""
        if event_type == 'goal_milestone':
            self._handle_goal_milestone(data)
        elif event_type == 'goal_achieved':
            self._handle_goal_achieved(data)
        elif event_type == 'goal_deadline_approaching':
            self._handle_deadline_approaching(data)
    
    def _handle_goal_milestone(self, data: Dict[str, Any]) -> None:
        """Handle goal milestone achievement (25%, 50%, 75%)."""
        user_id = data.get('user_id')
        goal_title = data.get('goal_title')
        percentage = data.get('percentage', 0)
        current_amount = data.get('current_amount', 0)
        target_amount = data.get('target_amount', 0)
        
        subject = f"Goal Milestone: {goal_title}"
        message = (
            f"Congratulations! You've reached {percentage:.0f}% of your {goal_title} goal. "
            f"${current_amount:.2f} of ${target_amount:.2f} saved."
        )
        
        self.notification_context.notify(
            recipient=str(user_id),
            subject=subject,
            message=message
        )
    
    def _handle_goal_achieved(self, data: Dict[str, Any]) -> None:
        """Handle goal achievement."""
        user_id = data.get('user_id')
        goal_title = data.get('goal_title')
        amount = data.get('amount', 0)
        
        subject = f"Goal Achieved: {goal_title}"
        message = f"🎉 Congratulations! You've achieved your {goal_title} goal of ${amount:.2f}!"
        
        self.notification_context.notify(
            recipient=str(user_id),
            subject=subject,
            message=message
        )
    
    def _handle_deadline_approaching(self, data: Dict[str, Any]) -> None:
        """Handle goal deadline approaching."""
        user_id = data.get('user_id')
        goal_title = data.get('goal_title')
        days_remaining = data.get('days_remaining', 0)
        progress = data.get('progress_percentage', 0)
        
        subject = f"Goal Deadline Approaching: {goal_title}"
        message = (
            f"Your {goal_title} goal deadline is in {days_remaining} days. "
            f"You're currently at {progress:.0f}% completion."
        )
        
        self.notification_context.notify(
            recipient=str(user_id),
            subject=subject,
            message=message
        )
