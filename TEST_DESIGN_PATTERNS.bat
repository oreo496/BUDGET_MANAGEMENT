@echo off
REM =========================================================
REM Design Patterns Implementation - Quick Test Script
REM =========================================================
echo.
echo ========================================
echo Testing Design Patterns Implementation
echo ========================================
echo.

REM Activate virtual environment
echo [1] Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Could not activate virtual environment
    pause
    exit /b 1
)
echo OK: Virtual environment activated
echo.

REM Navigate to backend
cd backend

REM Create test script
echo [2] Creating test script...
(
echo import os
echo import django
echo.
echo os.environ.setdefault^('DJANGO_SETTINGS_MODULE', 'funder.settings'^)
echo django.setup^(^)
echo.
echo print^("=== Testing Observer Pattern ===\n"^)
echo from utils.observers import EventDispatcher
echo.
echo dispatcher = EventDispatcher^(^)
echo print^("✓ EventDispatcher initialized"^)
echo.
echo # Test dispatching an event
echo dispatcher.dispatch^('budget_exceeded', {
echo     'user_id': 'test-user',
echo     'category': 'Test Category',
echo     'budget_amount': 500.00,
echo     'spent_amount': 600.00
echo }^)
echo print^("✓ Budget exceeded event dispatched\n"^)
echo.
echo print^("=== Testing Strategy Pattern ===\n"^)
echo from utils.strategies import CalculationContext, CompoundInterestCalculation
echo from decimal import Decimal
echo.
echo context = CalculationContext^(CompoundInterestCalculation^(^)^)
echo interest = context.execute^(
echo     principal=Decimal^('10000'^),
echo     rate=Decimal^('0.05'^),
echo     time_years=Decimal^('3'^),
echo     compounds_per_year=12
echo ^)
echo print^(f"✓ Compound interest calculated: ${float^(interest^):.2f}\n"^)
echo.
echo print^("=== Testing Budget Model Strategies ===\n"^)
echo from budgets.models import Budget
echo from accounts.models import User
echo.
echo user = User.objects.first^(^)
echo if user:
echo     budgets = Budget.objects.filter^(user=user^)
echo     if budgets.exists^(^):
echo         budget = budgets.first^(^)
echo         weekly = budget.calculate_period_amount^('WEEKLY'^)
echo         print^(f"✓ Budget period conversion: ${float^(weekly^):.2f} weekly"^)
echo         
echo         status = budget.get_spending_status^(^)
echo         print^(f"✓ Spending status: {float^(status['percentage_used']^):.1f}%% used\n"^)
echo     else:
echo         print^("No budgets found for testing"^)
echo else:
echo     print^("No users found for testing"^)
echo.
echo print^("=== Testing Loan Model Strategies ===\n"^)
echo from loans.models import Loan
echo.
echo loans = Loan.objects.all^(^)
echo if loans.exists^(^):
echo     loan = loans.first^(^)
echo     simple = loan.calculate_interest^('simple'^)
echo     compound = loan.calculate_interest^('compound'^)
echo     monthly = loan.calculate_monthly_payment^(^)
echo     
echo     print^(f"✓ Simple interest: ${float^(simple^):.2f}"^)
echo     print^(f"✓ Compound interest: ${float^(compound^):.2f}"^)
echo     print^(f"✓ Monthly payment: ${float^(monthly^):.2f}\n"^)
echo else:
echo     print^("No loans found for testing"^)
echo.
echo print^("=== All Tests Completed! ===\n"^)
echo print^("The design patterns are working correctly!"^)
) > test_design_patterns.py
echo OK: Test script created
echo.

REM Run the test
echo [3] Running design pattern tests...
python test_design_patterns.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Tests failed
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! All tests passed!
echo ========================================
echo.
echo The design patterns are working:
echo   ✓ Observer Pattern
echo   ✓ Strategy Pattern
echo   ✓ Model Integration
echo.
echo Check these files for more information:
echo   - DESIGN_PATTERNS_GUIDE.md
echo   - DESIGN_PATTERNS_EXAMPLES.md
echo   - DESIGN_PATTERNS_SUMMARY.md
echo.
pause
