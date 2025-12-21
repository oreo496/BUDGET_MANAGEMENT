# Design Patterns Examples

## Real-World Usage Examples

### Example 1: Creating a Transaction with Auto-Notifications

```python
# When a user creates a transaction, the system automatically:
# 1. Categorizes it (TransactionCategorizationObserver)
# 2. Checks for fraud (FraudDetectionObserver)
# 3. Checks if it's large (LargeTransactionObserver)
# 4. Updates budget status (Budget signals)

from transactions.models import Transaction
from categories.models import Category

# Create transaction
transaction = Transaction.objects.create(
    user_id='user-uuid',
    amount=-750.00,  # Negative for expense
    type='EXPENSE',
    description='Amazon purchase - electronics',
    date='2025-12-21'
)

# Automatically triggers:
# - transaction_created event → auto-categorization
# - transaction_created event → large transaction check
# - Budget check → may trigger budget_exceeded or budget_warning
```

### Example 2: Calculating Loan Payments with Different Strategies

```python
from loans.models import Loan

# Create a loan
loan = Loan.objects.create(
    user=user,
    amount=10000.00,
    term_months=36,
    interest_rate=5.0,
    lender_name='Bank ABC'
)

# Calculate using simple interest
simple_interest = loan.calculate_interest('simple')
print(f"Simple Interest: ${simple_interest}")

# Calculate using compound interest
compound_interest = loan.calculate_interest('compound')
print(f"Compound Interest: ${compound_interest}")

# Get monthly payment
monthly_payment = loan.calculate_monthly_payment()
print(f"Monthly Payment: ${monthly_payment}")

# Get full summary
summary = loan.get_loan_summary()
print(summary)
# Output:
# {
#     'principal': 10000.0,
#     'interest_rate': 5.0,
#     'term_months': 36,
#     'monthly_payment': 299.71,
#     'total_interest_simple': 1500.0,
#     'total_interest_compound': 1589.45,
#     'total_amount': 11589.45,
#     'status': 'PENDING'
# }
```

### Example 3: Budget Period Conversions

```python
from budgets.models import Budget

# Create monthly budget
budget = Budget.objects.create(
    user=user,
    category=groceries_category,
    period='MONTHLY',
    amount=500.00
)

# Convert to different periods
weekly_equivalent = budget.calculate_period_amount('WEEKLY')
print(f"Weekly: ${weekly_equivalent}")  # ~115.38

annual_equivalent = budget.calculate_period_amount('ANNUAL')
print(f"Annual: ${annual_equivalent}")  # 6000.00

# Get current spending status
status = budget.get_spending_status()
print(status)
# Output:
# {
#     'budget_amount': Decimal('500.00'),
#     'spent_amount': Decimal('450.00'),
#     'remaining_amount': Decimal('50.00'),
#     'percentage_used': Decimal('90.00'),
#     'is_exceeded': False,
#     'period': 'MONTHLY'
# }
```

### Example 4: Multi-Channel Notifications

```python
from utils.strategies import (
    NotificationContext,
    MultiChannelNotificationStrategy,
    EmailNotificationStrategy,
    SMSNotificationStrategy,
    InAppNotificationStrategy
)

# Send notification via multiple channels
multi_strategy = MultiChannelNotificationStrategy([
    InAppNotificationStrategy(),
    EmailNotificationStrategy(),
    SMSNotificationStrategy()
])

context = NotificationContext(multi_strategy)
context.notify(
    recipient='user-uuid',
    subject='Budget Alert',
    message='You have exceeded your monthly grocery budget of $500'
)

# This will:
# 1. Create an AI Alert in the database
# 2. Send an email (when configured)
# 3. Send an SMS (when configured)
```

### Example 5: Custom Authentication Flow

```python
from utils.strategies import AuthenticationContext, MFAAuthenticationStrategy

# Authenticate with MFA
auth_context = AuthenticationContext(MFAAuthenticationStrategy())

# First attempt without MFA token
result = auth_context.authenticate(
    email='user@example.com',
    password='SecurePass123!'
)

if result.get('requires_mfa'):
    # User has MFA enabled, prompt for token
    print("MFA token required")
    mfa_token = input("Enter 6-digit code: ")
    
    # Retry with MFA token
    result = auth_context.authenticate(
        email='user@example.com',
        password='SecurePass123!',
        mfa_token=mfa_token
    )

if result and not result.get('requires_mfa'):
    print(f"Authenticated: {result['email']}")
    # Generate JWT token...
```

### Example 6: React Component with Observer Hooks

```typescript
// BudgetDashboard.tsx
import React from 'react';
import { useBudgetObserver, useAlertObserver } from '@/hooks/useObserver';
import { formatCurrency, calculateBudgetForPeriod } from '@/lib/strategies';

export default function BudgetDashboard() {
  const { budgets, exceededBudgets, loading, refresh } = useBudgetObserver(60000);
  const { alerts, unreadCount } = useAlertObserver(30000);

  if (loading) return <div>Loading budgets...</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Budget Dashboard</h1>
        <div className="flex items-center gap-4">
          <span className="text-red-600 font-semibold">
            {exceededBudgets.length} Exceeded
          </span>
          <span className="bg-blue-600 text-white px-3 py-1 rounded-full">
            {unreadCount} Alerts
          </span>
          <button onClick={refresh} className="btn-primary">
            Refresh
          </button>
        </div>
      </div>

      {/* Budget Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {budgets.map(budget => {
          const weeklyAmount = calculateBudgetForPeriod(
            budget.amount,
            budget.period,
            'WEEKLY'
          );
          
          return (
            <div key={budget.id} className="bg-white p-4 rounded-lg shadow">
              <h3 className="font-semibold">{budget.category?.name}</h3>
              <p className="text-2xl text-blue-600">
                {formatCurrency(budget.amount, 'EGP')}
              </p>
              <p className="text-sm text-gray-500">
                ~{formatCurrency(weeklyAmount, 'EGP')}/week
              </p>
            </div>
          );
        })}
      </div>

      {/* Recent Alerts */}
      <div className="mt-6">
        <h2 className="text-xl font-bold mb-3">Recent Alerts</h2>
        {alerts.slice(0, 5).map(alert => (
          <div key={alert.id} className="bg-yellow-50 p-3 mb-2 rounded">
            <span className="font-semibold">{alert.type}</span>
            <p className="text-sm">{alert.message}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Example 7: Creating a Custom Observer

```python
# backend/transactions/observers.py

from utils.observers import Observer
from utils.strategies import NotificationContext, InAppNotificationStrategy
from typing import Dict, Any

class MonthlyReportObserver(Observer):
    """
    Sends monthly spending reports to users.
    Triggered by a scheduled task.
    """
    
    def __init__(self):
        self.notification = NotificationContext(InAppNotificationStrategy())
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        if event_type == 'monthly_report_due':
            self._generate_and_send_report(data)
    
    def _generate_and_send_report(self, data: Dict[str, Any]) -> None:
        user_id = data.get('user_id')
        month = data.get('month')
        year = data.get('year')
        
        # Calculate spending by category
        from transactions.models import Transaction
        from django.db.models import Sum
        from datetime import date
        
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        spending = Transaction.objects.filter(
            user_id=user_id,
            type='EXPENSE',
            date__gte=start_date,
            date__lt=end_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        message = (
            f"Your {month}/{year} spending report:\n"
            f"Total Expenses: ${abs(spending):.2f}\n"
            f"View detailed breakdown in the app."
        )
        
        self.notification.notify(
            recipient=str(user_id),
            subject="Monthly Spending Report",
            message=message
        )

# Register the observer
from utils.signals import dispatcher
monthly_report_observer = MonthlyReportObserver()
dispatcher.subscribe('monthly_report_due', monthly_report_observer)

# Trigger from a scheduled task
# dispatcher.dispatch('monthly_report_due', {
#     'user_id': 'user-uuid',
#     'month': 12,
#     'year': 2025
# })
```

### Example 8: Frontend Loan Calculator Component

```typescript
// LoanCalculator.tsx
import React, { useState } from 'react';
import { calculateLoanPayment, formatCurrency } from '@/lib/strategies';

export default function LoanCalculator() {
  const [principal, setPrincipal] = useState<string>('10000');
  const [rate, setRate] = useState<string>('5.0');
  const [term, setTerm] = useState<string>('36');
  const [useCompound, setUseCompound] = useState<boolean>(true);

  const monthlyPayment = calculateLoanPayment(
    parseFloat(principal) || 0,
    (parseFloat(rate) || 0) / 100,
    parseInt(term) || 1,
    useCompound
  );

  const totalPayment = monthlyPayment * (parseInt(term) || 1);
  const totalInterest = totalPayment - (parseFloat(principal) || 0);

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-4">Loan Calculator</h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Principal Amount</label>
          <input
            type="number"
            value={principal}
            onChange={(e) => setPrincipal(e.target.value)}
            className="w-full px-3 py-2 border rounded"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Interest Rate (%)</label>
          <input
            type="number"
            step="0.1"
            value={rate}
            onChange={(e) => setRate(e.target.value)}
            className="w-full px-3 py-2 border rounded"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Term (months)</label>
          <input
            type="number"
            value={term}
            onChange={(e) => setTerm(e.target.value)}
            className="w-full px-3 py-2 border rounded"
          />
        </div>

        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={useCompound}
            onChange={(e) => setUseCompound(e.target.checked)}
            id="compound"
          />
          <label htmlFor="compound" className="text-sm">
            Use Compound Interest
          </label>
        </div>
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded">
        <div className="flex justify-between mb-2">
          <span className="font-medium">Monthly Payment:</span>
          <span className="text-xl font-bold text-blue-600">
            {formatCurrency(monthlyPayment, 'EGP')}
          </span>
        </div>
        <div className="flex justify-between mb-2">
          <span className="text-sm text-gray-600">Total Payment:</span>
          <span className="text-sm">{formatCurrency(totalPayment, 'EGP')}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm text-gray-600">Total Interest:</span>
          <span className="text-sm text-red-600">
            {formatCurrency(totalInterest, 'EGP')}
          </span>
        </div>
      </div>
    </div>
  );
}
```

### Example 9: Triggering Events Manually

```python
# From a Django management command or view

from utils.observers import EventDispatcher

dispatcher = EventDispatcher()

# Trigger unusual spending alert
dispatcher.dispatch('unusual_spending', {
    'user_id': 'user-uuid',
    'amount': 1500.00,
    'category': 'Entertainment',
    'average': 200.00
})

# Trigger goal milestone
dispatcher.dispatch('goal_milestone', {
    'user_id': 'user-uuid',
    'goal_title': 'Emergency Fund',
    'percentage': 50,
    'current_amount': 5000.00,
    'target_amount': 10000.00
})

# Trigger fraud alert
dispatcher.dispatch('potential_fraud', {
    'transaction_id': 'trans-uuid',
    'user_id': 'user-uuid',
    'amount': 5000.00,
    'description': 'Unknown merchant',
    'reason': 'Transaction amount exceeds $5000'
})
```

### Example 10: Strategy Pattern for Different User Preferences

```python
# backend/accounts/views.py

from utils.strategies import NotificationContext
from utils.strategies import (
    EmailNotificationStrategy,
    SMSNotificationStrategy,
    InAppNotificationStrategy,
    MultiChannelNotificationStrategy
)

def send_notification_based_on_preference(user, subject, message):
    """
    Send notification using strategy based on user preferences.
    """
    # Get user notification preferences
    preferences = {
        'email': user.preferences.get('notify_email', True),
        'sms': user.preferences.get('notify_sms', False),
        'in_app': user.preferences.get('notify_in_app', True)
    }
    
    # Build strategy list based on preferences
    strategies = []
    if preferences['in_app']:
        strategies.append(InAppNotificationStrategy())
    if preferences['email']:
        strategies.append(EmailNotificationStrategy())
    if preferences['sms']:
        strategies.append(SMSNotificationStrategy())
    
    # Create notification context with selected strategies
    if len(strategies) > 1:
        strategy = MultiChannelNotificationStrategy(strategies)
    elif len(strategies) == 1:
        strategy = strategies[0]
    else:
        # Default to in-app
        strategy = InAppNotificationStrategy()
    
    context = NotificationContext(strategy)
    return context.notify(
        recipient=str(user.id),
        subject=subject,
        message=message
    )
```

---

## Testing the Patterns

### Test Script (Python)

```python
# test_patterns.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from utils.observers import EventDispatcher
from utils.strategies import CalculationContext, CompoundInterestCalculation
from budgets.models import Budget
from loans.models import Loan
from accounts.models import User

# Test Observer Pattern
print("=== Testing Observer Pattern ===")
dispatcher = EventDispatcher()
dispatcher.dispatch('budget_exceeded', {
    'user_id': 'test-user',
    'category': 'Test Category',
    'budget_amount': 500.00,
    'spent_amount': 600.00
})
print("✓ Budget exceeded event dispatched")

# Test Strategy Pattern - Calculations
print("\n=== Testing Strategy Pattern - Calculations ===")
context = CalculationContext(CompoundInterestCalculation())
interest = context.execute(
    principal=10000,
    rate=0.05,
    time_years=3,
    compounds_per_year=12
)
print(f"✓ Compound interest calculated: ${interest:.2f}")

# Test Budget Strategy Methods
print("\n=== Testing Budget Model Strategies ===")
user = User.objects.first()
if user:
    budget = Budget.objects.filter(user=user).first()
    if budget:
        weekly = budget.calculate_period_amount('WEEKLY')
        print(f"✓ Budget period conversion: ${weekly:.2f} weekly")
        
        status = budget.get_spending_status()
        print(f"✓ Spending status: {status['percentage_used']}% used")

# Test Loan Strategy Methods
print("\n=== Testing Loan Model Strategies ===")
loan = Loan.objects.first()
if loan:
    simple = loan.calculate_interest('simple')
    compound = loan.calculate_interest('compound')
    monthly = loan.calculate_monthly_payment()
    
    print(f"✓ Simple interest: ${simple:.2f}")
    print(f"✓ Compound interest: ${compound:.2f}")
    print(f"✓ Monthly payment: ${monthly:.2f}")

print("\n=== All tests completed! ===")
```

Run with: `python test_patterns.py`

---

These examples demonstrate real-world usage of both Observer and Strategy patterns in your Funder application!
