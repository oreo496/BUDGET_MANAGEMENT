"""
Test script for Funder API prediction endpoint
Run: python manage.py shell < test_funder_api.py
"""
import requests
import json
import os

# Set base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("\n" + "="*70)
    print("TEST 1: Health Check (GET)")
    print("="*70)
    try:
        response = requests.get(f"{BASE_URL}/health/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_predict_transaction_authenticated(token):
    """Test transaction prediction endpoint"""
    print("\n" + "="*70)
    print("TEST 2: Predict Transaction Type (POST with Auth)")
    print("="*70)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    transaction_data = {
        "amount": 45.50,
        "merchant_category": "food",
        "is_recurring": 0,
        "day_of_week": 3,
        "hour_of_day": 19
    }
    
    print(f"Request body: {json.dumps(transaction_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/predict/",
            headers=headers,
            json=transaction_data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_predict_without_auth():
    """Test that endpoint requires authentication"""
    print("\n" + "="*70)
    print("TEST 3: Predict Transaction (POST without Auth - Should Fail)")
    print("="*70)
    
    transaction_data = {
        "amount": 25.00,
        "merchant_category": "transport",
        "is_recurring": 1,
        "day_of_week": 1,
        "hour_of_day": 8
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/predict/",
            json=transaction_data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 401  # Should be unauthorized
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_predict_invalid_data():
    """Test with invalid/missing data"""
    print("\n" + "="*70)
    print("TEST 4: Predict with Missing Required Fields")
    print("="*70)
    
    # Missing 'amount' field
    transaction_data = {
        "merchant_category": "food",
        "day_of_week": 3
    }
    
    headers = {
        'Authorization': 'Bearer test-token',  # This would fail auth anyway
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/predict/",
            json=transaction_data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [400, 401]  # Bad request or unauthorized
    except Exception as e:
        print(f"Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "FUNDER API PREDICTION TESTS" + " "*26 + "║")
    print("╚" + "="*68 + "╝")
    
    results = {}
    
    # Test 1: Health check (no auth required)
    results['health_check'] = test_health_check()
    
    # Test 2: Prediction without auth (should fail)
    results['predict_without_auth'] = test_predict_without_auth()
    
    # Test 3: Invalid data
    results['predict_invalid_data'] = test_predict_invalid_data()
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:30s}: {status}")
    
    total_passed = sum(1 for v in results.values() if v)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ {total_tests - total_passed} test(s) failed")
        print("\nNote: For authenticated tests, you need to:")
        print("1. Log in to get a JWT token")
        print("2. Include it in the Authorization header")


if __name__ == '__main__':
    print("\n" + "!"*70)
    print("IMPORTANT: Start the backend with 'python manage.py runserver'")
    print("Then run this script: python test_funder_api.py")
    print("!"*70)
    
    # For now, just show what to do
    print("\nTo run authenticated tests with actual token:")
    print("""
    1. Get a token from login endpoint:
       curl -X POST http://localhost:8000/api/auth/login/ \\
         -H "Content-Type: application/json" \\
         -d '{"username":"user","password":"pass"}'
    
    2. Use the token in requests:
       curl -X POST http://localhost:8000/api/predict/ \\
         -H "Authorization: Bearer YOUR_TOKEN" \\
         -H "Content-Type: application/json" \\
         -d '{"amount":50,"merchant_category":"food"}'
    """)
