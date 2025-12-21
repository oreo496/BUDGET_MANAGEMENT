# Design Patterns Implementation Guide

## Overview

The Funder application has been enhanced with two major design patterns:
1. **Observer Pattern** - For event-driven notifications and real-time updates
2. **Strategy Pattern** - For flexible calculations, notifications, and authentication

---

## 🔍 Observer Pattern Implementation

### Backend (Django)

#### Architecture

```
EventDispatcher (Singleton)
    ├── BudgetExceededObserver
    ├── SpendingPatternObserver
    ├── GoalProgressObserver
    ├── FraudDetectionObserver
    ├── TransactionCategorizationObserver
    ├── LargeTransactionObserver
    └── RecurringTransactionObserver
```

#### Key Components

**1. Event Dispatcher** (`backend/utils/observers.py`)
- Singleton class managing all observers
- Supports subscribe/unsubscribe operations
- Dispatches events to registered observers

**2. Observer Base Class** (`backend/utils/observers.py`)
```python
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        pass
```

**3. Signal Integration** (`backend/utils/signals.py`)
- Django signals connected to Observer pattern
- Auto-registers observers on app startup
- Monitors: Transaction, Budget, Goal models

#### Observers Implemented

| Observer | Events | Purpose |
|----------|--------|---------|
| BudgetExceededObserver | `budget_exceeded`, `budget_warning` | Alerts when budgets are exceeded or approaching limit |
| SpendingPatternObserver | `unusual_spending`, `spending_trend` | Detects unusual spending patterns |
| GoalProgressObserver | `goal_milestone`, `goal_achieved`, `goal_deadline_approaching` | Tracks savings goal progress |
| FraudDetectionObserver | `potential_fraud`, `fraud_confirmed` | Monitors suspicious transactions |
| TransactionCategorizationObserver | `transaction_created` | Auto-categorizes transactions |
| LargeTransactionObserver | `transaction_created` | Alerts on large transactions |

#### Usage Example

```python
from utils.observers import EventDispatcher

# Get dispatcher instance
dispatcher = EventDispatcher()

# Dispatch an event
dispatcher.dispatch('budget_exceeded', {
    'user_id': '12345',
    'category': 'Groceries',
    'budget_amount': 500.00,
    'spent_amount': 550.00
})

# All subscribed observers will be notified automatically
```

### Frontend (React/Next.js)

#### Custom Hooks (`frontend/src/hooks/useObserver.ts`)

**1. useAlertObserver**
```typescript
const { alerts, unreadCount, loading, refresh } = useAlertObserver(30000);
// Polls for new alerts every 30 seconds
```

**2. useBudgetObserver**
```typescript
const { budgets, exceededBudgets, loading, refresh } = useBudgetObserver(60000);
// Monitors budget status
```

**3. useTransactionObserver**
```typescript
const { transactions, newTransactions, loading, refresh } = useTransactionObserver(30000);
// Detects new transactions
```

**4. useGoalObserver**
```typescript
const { goals, achievedGoals, loading, refresh } = useGoalObserver(60000);
// Tracks goal progress
```

**5. Event Emitter**
```typescript
import { appEvents } from '@/hooks/useObserver';

// Emit event
appEvents.emit('notification_received', { message: 'New alert!' });

// Listen to event
appEvents.on('notification_received', (data) => {
  console.log(data.message);
});
```

---

## 🎯 Strategy Pattern Implementation

### Backend (Django)

#### Calculation Strategies (`backend/utils/strategies.py`)

**Available Strategies:**

1. **Budget Calculations**
   - `MonthlyBudgetCalculation` - Calculate monthly allowances
   - `WeeklyBudgetCalculation` - Calculate weekly allowances

2. **Interest Calculations**
   - `SimpleInterestCalculation` - Simple interest formula
   - `CompoundInterestCalculation` - Compound interest with configurable periods

3. **Goal Progress**
   - `GoalProgressCalculation` - Calculate percentage completion

**Usage in Models:**

```python
# In Budget model
def calculate_period_amount(self, target_period='MONTHLY'):
    from utils.strategies import CalculationContext, MonthlyBudgetCalculation
    
    context = CalculationContext(MonthlyBudgetCalculation())
    return context.execute(monthly_amount=self.amount)

# In Loan model
def calculate_interest(self, calculation_type='simple'):
    from utils.strategies import CalculationContext, SimpleInterestCalculation
    
    context = CalculationContext(SimpleInterestCalculation())
    return context.execute(
        principal=self.amount,
        rate=self.interest_rate/100,
        time_years=self.term_months/12
    )
```

#### Notification Strategies (`backend/utils/strategies.py`)

**Available Strategies:**

1. `EmailNotificationStrategy` - Send via email (SMTP)
2. `SMSNotificationStrategy` - Send via SMS (Twilio)
3. `InAppNotificationStrategy` - Create AI Alert in database
4. `PushNotificationStrategy` - Send push notifications (Firebase)
5. `MultiChannelNotificationStrategy` - Combine multiple channels

**Usage:**

```python
from utils.strategies import NotificationContext, MultiChannelNotificationStrategy

# Use multi-channel notifications
context = NotificationContext(MultiChannelNotificationStrategy())
context.notify(
    recipient='user_id_123',
    subject='Budget Alert',
    message='You have exceeded your budget'
)
```

#### Authentication Strategies (`backend/utils/strategies.py`)

**Available Strategies:**

1. `PasswordAuthenticationStrategy` - Standard email/password
2. `MFAAuthenticationStrategy` - Multi-factor authentication
3. `TokenAuthenticationStrategy` - JWT token validation

**Usage:**

```python
from utils.strategies import AuthenticationContext, MFAAuthenticationStrategy

# Authenticate with MFA
context = AuthenticationContext(MFAAuthenticationStrategy())
result = context.authenticate(
    email='user@example.com',
    password='secret123',
    mfa_token='123456'
)
```

### Frontend (React/Next.js)

#### Calculation Strategies (`frontend/src/lib/strategies.ts`)

**Available Functions:**

```typescript
// Budget calculations
calculateBudgetForPeriod(amount, 'MONTHLY', 'WEEKLY')

// Loan calculations
calculateLoanPayment(10000, 0.05, 36, true) // compound interest

// Goal progress
calculateGoalProgress(5000, 10000) // Returns 50%

// Currency formatting
formatCurrency(1500.50, 'EGP') // Returns "E£1,500.50"

// Percentage formatting
formatPercentage(85.5, 1) // Returns "85.5%"
```

**Usage in Components:**

```typescript
import { calculateLoanPayment, formatCurrency } from '@/lib/strategies';

const monthlyPayment = calculateLoanPayment(
  parseFloat(amount),
  parseFloat(interestRate) / 100,
  parseInt(termMonths),
  true
);

const formatted = formatCurrency(monthlyPayment, 'EGP');
```

---

## 📋 Event Types Reference

### Budget Events
- `budget_exceeded` - Budget limit exceeded
- `budget_warning` - 80% of budget used

### Transaction Events
- `transaction_created` - New transaction added
- `potential_fraud` - Suspicious activity detected
- `fraud_confirmed` - Fraud flag set
- `recurring_detected` - Recurring transaction pattern found

### Goal Events
- `goal_milestone` - Reached 25%, 50%, or 75%
- `goal_achieved` - Goal completed (100%)
- `goal_deadline_approaching` - Less than 7 days remaining

### Spending Events
- `unusual_spending` - Significantly higher than average
- `spending_trend` - Increasing spending pattern

---

## 🚀 Getting Started

### Backend Setup

1. **Activate signal handlers** (already configured in apps.py files)
```python
# budgets/apps.py, transactions/apps.py, goals/apps.py
def ready(self):
    import utils.signals
```

2. **Use strategies in views**
```python
from utils.strategies import NotificationContext, InAppNotificationStrategy

notification = NotificationContext(InAppNotificationStrategy())
notification.notify(user_id, "Alert", "Your budget is exceeded")
```

3. **Create custom observers**
```python
from utils.observers import Observer

class MyCustomObserver(Observer):
    def update(self, event_type: str, data: dict):
        # Handle event
        pass

# Register it
from utils.signals import dispatcher
dispatcher.subscribe('my_event', MyCustomObserver())
```

### Frontend Setup

1. **Use observer hooks in components**
```typescript
import { useAlertObserver } from '@/hooks/useObserver';

function MyComponent() {
  const { alerts, unreadCount } = useAlertObserver(30000);
  
  return (
    <div>
      <p>Unread alerts: {unreadCount}</p>
      {alerts.map(alert => <div key={alert.id}>{alert.message}</div>)}
    </div>
  );
}
```

2. **Use calculation strategies**
```typescript
import { calculateLoanPayment, formatCurrency } from '@/lib/strategies';

const payment = calculateLoanPayment(10000, 0.05, 36);
const formatted = formatCurrency(payment, 'EGP');
```

---

## 🧪 Testing

### Test Observer Pattern

```python
# Test event dispatching
from utils.observers import EventDispatcher

dispatcher = EventDispatcher()
dispatcher.dispatch('budget_exceeded', {
    'user_id': 'test_user',
    'category': 'Test',
    'budget_amount': 100,
    'spent_amount': 150
})

# Check AI Alerts table for notification
```

### Test Strategy Pattern

```python
# Test calculation strategies
from budgets.models import Budget

budget = Budget.objects.get(id='...')
weekly_amount = budget.calculate_period_amount('WEEKLY')
monthly_amount = budget.calculate_period_amount('MONTHLY')

# Test loan calculations
from loans.models import Loan

loan = Loan.objects.get(id='...')
simple_interest = loan.calculate_interest('simple')
compound_interest = loan.calculate_interest('compound')
```

---

## 📊 Benefits

### Observer Pattern Benefits
✅ Decoupled notification system  
✅ Easy to add new observers without modifying existing code  
✅ Real-time event processing  
✅ Automatic alerts and notifications  
✅ Extensible event system  

### Strategy Pattern Benefits
✅ Flexible calculation methods  
✅ Easy to swap algorithms at runtime  
✅ Clean separation of concerns  
✅ Testable calculation logic  
✅ Consistent interfaces  

---

## 🔧 Extending the Patterns

### Adding a New Observer

1. Create observer class:
```python
from utils.observers import Observer

class MyNewObserver(Observer):
    def update(self, event_type: str, data: dict):
        # Implementation
        pass
```

2. Register in `utils/signals.py`:
```python
my_observer = MyNewObserver()
dispatcher.subscribe('my_event_type', my_observer)
```

### Adding a New Strategy

1. Create strategy class:
```python
from utils.strategies import CalculationStrategy

class MyNewCalculation(CalculationStrategy):
    def calculate(self, **kwargs):
        # Implementation
        return result
```

2. Use in context:
```python
from utils.strategies import CalculationContext

context = CalculationContext(MyNewCalculation())
result = context.execute(**params)
```

---

## 📚 Files Created/Modified

### New Files
- `backend/utils/observers.py` - Observer base classes
- `backend/utils/strategies.py` - Strategy implementations
- `backend/utils/signals.py` - Django signal handlers
- `backend/budgets/observers.py` - Budget observers
- `backend/transactions/observers.py` - Transaction observers
- `backend/accounts/auth_strategies.py` - Authentication strategy views
- `frontend/src/hooks/useObserver.ts` - React observer hooks
- `frontend/src/lib/strategies.ts` - Frontend strategies

### Modified Files
- `backend/budgets/models.py` - Added strategy methods
- `backend/loans/models.py` - Added calculation strategies
- `backend/budgets/apps.py` - Signal registration
- `backend/transactions/apps.py` - Signal registration
- `backend/goals/apps.py` - Signal registration

---

## 🎓 Design Pattern Summary

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| **Observer** | Event notifications | EventDispatcher + Django Signals |
| **Strategy** | Flexible algorithms | Context classes + Strategy interfaces |
| **Singleton** | EventDispatcher | Single instance for all observers |
| **Factory** | Django models | Model creation patterns |

---

**Your application now follows best practices with Observer and Strategy design patterns fully implemented!** 🎉
