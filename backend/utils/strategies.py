"""
Strategy Pattern Implementation for Funder Application
This module provides base classes and implementations for various strategies.
"""
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Dict, Optional
from datetime import datetime, timedelta


# ============================================================================
# CALCULATION STRATEGIES
# ============================================================================

class CalculationStrategy(ABC):
    """Base class for calculation strategies."""
    
    @abstractmethod
    def calculate(self, **kwargs) -> Decimal:
        """Execute the calculation."""
        pass


class MonthlyBudgetCalculation(CalculationStrategy):
    """Calculate monthly budget allowance."""
    
    def calculate(self, annual_amount: Decimal = None, monthly_amount: Decimal = None, **kwargs) -> Decimal:
        if monthly_amount:
            return Decimal(str(monthly_amount))
        if annual_amount:
            return Decimal(str(annual_amount)) / 12
        return Decimal('0.00')


class WeeklyBudgetCalculation(CalculationStrategy):
    """Calculate weekly budget allowance."""
    
    def calculate(self, annual_amount: Decimal = None, monthly_amount: Decimal = None, **kwargs) -> Decimal:
        if monthly_amount:
            return Decimal(str(monthly_amount)) * 12 / 52
        if annual_amount:
            return Decimal(str(annual_amount)) / 52
        return Decimal('0.00')


class SimpleInterestCalculation(CalculationStrategy):
    """Calculate simple interest."""
    
    def calculate(self, principal: Decimal, rate: Decimal, time_years: Decimal, **kwargs) -> Decimal:
        """
        Simple Interest = Principal × Rate × Time
        
        Args:
            principal: Principal amount
            rate: Interest rate (as decimal, e.g., 0.05 for 5%)
            time_years: Time period in years
        """
        return Decimal(str(principal)) * Decimal(str(rate)) * Decimal(str(time_years))


class CompoundInterestCalculation(CalculationStrategy):
    """Calculate compound interest."""
    
    def calculate(self, principal: Decimal, rate: Decimal, time_years: Decimal, 
                  compounds_per_year: int = 12, **kwargs) -> Decimal:
        """
        Compound Interest = Principal × (1 + rate/n)^(n×t) - Principal
        
        Args:
            principal: Principal amount
            rate: Annual interest rate (as decimal)
            time_years: Time period in years
            compounds_per_year: Number of times interest compounds per year
        """
        p = Decimal(str(principal))
        r = Decimal(str(rate))
        t = Decimal(str(time_years))
        n = Decimal(str(compounds_per_year))
        
        # Calculate (1 + r/n)
        rate_per_period = 1 + (r / n)
        # Calculate n*t
        total_periods = n * t
        
        # Using power calculation
        amount = p * (rate_per_period ** float(total_periods))
        return amount - p


class GoalProgressCalculation(CalculationStrategy):
    """Calculate goal progress percentage."""
    
    def calculate(self, current_amount: Decimal, target_amount: Decimal, **kwargs) -> Decimal:
        """Calculate progress as percentage."""
        if target_amount == 0:
            return Decimal('0.00')
        
        progress = (Decimal(str(current_amount)) / Decimal(str(target_amount))) * 100
        return min(progress, Decimal('100.00'))


# ============================================================================
# NOTIFICATION STRATEGIES
# ============================================================================

class NotificationStrategy(ABC):
    """Base class for notification strategies."""
    
    @abstractmethod
    def send(self, recipient: str, subject: str, message: str, **kwargs) -> bool:
        """Send notification to recipient."""
        pass


class EmailNotificationStrategy(NotificationStrategy):
    """Send notifications via email."""
    
    def send(self, recipient: str, subject: str, message: str, **kwargs) -> bool:
        """Send email notification."""
        # TODO: Implement actual email sending (SMTP, SendGrid, etc.)
        print(f"[EMAIL] To: {recipient}")
        print(f"[EMAIL] Subject: {subject}")
        print(f"[EMAIL] Message: {message}")
        
        # For now, just log it
        return True


class SMSNotificationStrategy(NotificationStrategy):
    """Send notifications via SMS."""
    
    def send(self, recipient: str, subject: str, message: str, **kwargs) -> bool:
        """Send SMS notification."""
        # TODO: Implement actual SMS sending (Twilio, etc.)
        print(f"[SMS] To: {recipient}")
        print(f"[SMS] Message: {message}")
        
        return True


class InAppNotificationStrategy(NotificationStrategy):
    """Send in-app notifications (store in database)."""
    
    def send(self, recipient: str, subject: str, message: str, **kwargs) -> bool:
        """Create in-app notification."""
        from ai_alerts.models import AIAlert
        from accounts.models import User

        try:
            # recipient should be user_id
            user = User.objects.get(id=recipient)

            # Determine alert type from subject
            subject_lower = subject.lower()
            alert_type = 'BUDGET_ALERT'
            if 'fraud' in subject_lower:
                alert_type = 'FRAUD'
            elif 'goal' in subject_lower:
                alert_type = 'GOAL_RECOMMENDATION'
                if 'risk' in subject_lower or 'overspend' in subject_lower:
                    # Some databases may not include GOAL_RISK in enum; fall back safely
                    alert_type = 'GOAL_RECOMMENDATION'
            elif 'loan' in subject_lower:
                # Some databases may not include LOAN_REMINDER in enum; fall back safely
                alert_type = 'BUDGET_ALERT'
            elif 'spending' in subject_lower or 'pattern' in subject_lower:
                alert_type = 'SPENDING_PATTERN'

            AIAlert.objects.create(
                user=user,
                message=f"{subject}: {message}",
                type=alert_type
            )
            return True
        except Exception as e:
            print(f"Error creating in-app notification: {e}")
            return False


class PushNotificationStrategy(NotificationStrategy):
    """Send push notifications."""
    
    def send(self, recipient: str, subject: str, message: str, **kwargs) -> bool:
        """Send push notification."""
        # TODO: Implement push notifications (Firebase, OneSignal, etc.)
        print(f"[PUSH] To: {recipient}")
        print(f"[PUSH] Title: {subject}")
        print(f"[PUSH] Body: {message}")
        
        return True


class MultiChannelNotificationStrategy(NotificationStrategy):
    """Send notifications through multiple channels."""
    
    def __init__(self, strategies: list = None):
        self.strategies = strategies or [
            InAppNotificationStrategy(),
            EmailNotificationStrategy()
        ]
    
    def send(self, recipient: str, subject: str, message: str, **kwargs) -> bool:
        """Send notification through all configured channels."""
        results = []
        for strategy in self.strategies:
            try:
                result = strategy.send(recipient, subject, message, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"Error with notification strategy {strategy.__class__.__name__}: {e}")
                results.append(False)
        
        # Return True if at least one channel succeeded
        return any(results)


# ============================================================================
# AUTHENTICATION STRATEGIES
# ============================================================================

class AuthenticationStrategy(ABC):
    """Base class for authentication strategies."""
    
    @abstractmethod
    def authenticate(self, **credentials) -> Optional[Dict[str, Any]]:
        """Authenticate user with given credentials."""
        pass


class PasswordAuthenticationStrategy(AuthenticationStrategy):
    """Standard password-based authentication."""
    
    def authenticate(self, email: str, password: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Authenticate using email and password."""
        from accounts.models import User
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return {
                    'user_id': str(user.id),
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
        except User.DoesNotExist:
            pass
        
        return None





class TokenAuthenticationStrategy(AuthenticationStrategy):
    """Token-based authentication strategy."""
    
    def authenticate(self, token: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Authenticate using JWT token."""
        import jwt
        from django.conf import settings
        from accounts.models import User
        
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get('user_id')
            
            if user_id:
                user = User.objects.get(id=user_id)
                return {
                    'user_id': str(user.id),
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
        except (jwt.InvalidTokenError, User.DoesNotExist):
            pass
        
        return None


# ============================================================================
# STRATEGY CONTEXT CLASSES
# ============================================================================

class CalculationContext:
    """Context class for calculation strategies."""
    
    def __init__(self, strategy: CalculationStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: CalculationStrategy) -> None:
        """Change the calculation strategy at runtime."""
        self._strategy = strategy
    
    def execute(self, **kwargs) -> Decimal:
        """Execute the current strategy."""
        return self._strategy.calculate(**kwargs)


class NotificationContext:
    """Context class for notification strategies."""
    
    def __init__(self, strategy: NotificationStrategy = None):
        self._strategy = strategy or InAppNotificationStrategy()
    
    def set_strategy(self, strategy: NotificationStrategy) -> None:
        """Change the notification strategy at runtime."""
        self._strategy = strategy
    
    def notify(self, recipient: str, subject: str, message: str, **kwargs) -> bool:
        """Send notification using current strategy."""
        return self._strategy.send(recipient, subject, message, **kwargs)


class AuthenticationContext:
    """Context class for authentication strategies."""
    
    def __init__(self, strategy: AuthenticationStrategy = None):
        self._strategy = strategy or PasswordAuthenticationStrategy()
    
    def set_strategy(self, strategy: AuthenticationStrategy) -> None:
        """Change the authentication strategy at runtime."""
        self._strategy = strategy
    
    def authenticate(self, **credentials) -> Optional[Dict[str, Any]]:
        """Authenticate using current strategy."""
        return self._strategy.authenticate(**credentials)
