# AI Model Quick Test Script
# Run this after exporting models from notebook to verify integration

import requests
import json

BASE_URL = "http://localhost:8000"

def test_transaction_prediction():
    """Test transaction type prediction"""
    print("\n" + "="*70)
    print("TEST 1: Transaction Type Prediction")
    print("="*70)
    
    data = {
        "amount": 150.00,
        "category": "Food",
        "payment_method": "Credit Card",
        "merchant_name": "Restaurant XYZ",
        "transaction_type": "Expense",
        "is_recurring": 0,
        "is_flagged": 0,
        "monthly_budget": 500,
        "spent_in_category_month": 300,
        "over_budget_percentage": 0.6
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai-alerts/predict/transaction/",
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ SUCCESS")
            print(f"  Predicted Type: {result.get('predicted_type')}")
            print(f"  Confidence: {result.get('confidence', 0)*100:.1f}%")
            print(f"  Model Votes: {result.get('model_votes')}")
        else:
            print(f"✗ FAILED: Status {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")


def test_budget_risk():
    """Test budget overrun risk prediction"""
    print("\n" + "="*70)
    print("TEST 2: Budget Overrun Risk Prediction")
    print("="*70)
    
    data = {
        "total_spent": 1200.00,
        "monthly_budget": 1500.00,
        "days_passed": 20,
        "transaction_count": 45,
        "avg_transaction_size": 26.67,
        "recent_trend": 50.00
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai-alerts/predict/budget-risk/",
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ SUCCESS")
            print(f"  Risk Level: {result.get('risk_level')}")
            print(f"  Risk Probability: {result.get('risk_probability', 0)*100:.1f}%")
            print(f"  Recommended Budget: ${result.get('recommended_budget', 0):.2f}")
            print(f"  Daily Spending Cap: ${result.get('daily_spending_cap', 0):.2f}")
        else:
            print(f"✗ FAILED: Status {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")


def test_goal_success():
    """Test savings goal success prediction"""
    print("\n" + "="*70)
    print("TEST 3: Savings Goal Success Prediction")
    print("="*70)
    
    data = {
        "goal_amount": 10000.00,
        "current_savings": 3000.00,
        "months_remaining": 12,
        "monthly_income": 5000.00,
        "monthly_expenses": 3500.00,
        "past_contributions": 200.00,
        "contribution_consistency": 0.75,
        "income_stability": 0.80,
        "past_goal_success_rate": 0.65
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai-alerts/predict/goal-success/",
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ SUCCESS")
            print(f"  Goal Achievable: {result.get('goal_achievable')}")
            print(f"  Success Probability: {result.get('success_probability', 0)*100:.1f}%")
            print(f"  Confidence: {result.get('confidence_level')}")
            print(f"  Recommended Monthly: ${result.get('recommended_monthly_contribution', 0):.2f}")
        else:
            print(f"✗ FAILED: Status {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")


def test_flagged_transaction():
    """Test fraudulent transaction detection"""
    print("\n" + "="*70)
    print("TEST 4: Fraudulent Transaction Detection")
    print("="*70)
    
    data = {
        "amount": 2500.00,
        "category": "Shopping",
        "payment_method": "Credit Card",
        "merchant_name": "Unknown Merchant",
        "transaction_type": "Expense",
        "is_recurring": 0,
        "monthly_budget": 500,
        "spent_in_category_month": 300,
        "over_budget_percentage": 5.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai-alerts/predict/flagged/",
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ SUCCESS")
            print(f"  Is Flagged: {result.get('is_flagged')}")
            print(f"  Confidence: {result.get('confidence', 0)*100:.1f}%")
            print(f"  Risk Score: {result.get('risk_score', 0)*100:.1f}%")
        else:
            print(f"✗ FAILED: Status {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")


def test_chatbot():
    """Test chatbot with AI capabilities"""
    print("\n" + "="*70)
    print("TEST 5: Chatbot Integration")
    print("="*70)
    
    messages = [
        "Hi FunderBot!",
        "What can you help me with?",
        "Tell me about AI predictions"
    ]
    
    for msg in messages:
        try:
            response = requests.post(
                f"{BASE_URL}/api/chatbot/send_message/",
                json={"message": msg},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n  User: {msg}")
                print(f"  Bot: {result.get('bot_response')}")
            else:
                print(f"✗ FAILED: Status {response.status_code}")
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            break


if __name__ == "__main__":
    print("\n" + "="*70)
    print("AI MODEL INTEGRATION TEST SUITE")
    print("="*70)
    print(f"Testing API at: {BASE_URL}")
    print("\nNOTE: Make sure Django server is running!")
    print("Run: python manage.py runserver")
    
    input("\nPress Enter to start tests...")
    
    # Run all tests
    test_transaction_prediction()
    test_budget_risk()
    test_goal_success()
    test_flagged_transaction()
    test_chatbot()
    
    print("\n" + "="*70)
    print("TEST SUITE COMPLETE")
    print("="*70)
    print("\nIf all tests passed (✓), your AI models are fully integrated!")
    print("Check AI_INTEGRATION_GUIDE.md for detailed documentation.")
