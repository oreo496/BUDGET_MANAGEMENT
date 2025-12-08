# Testing Guide for Funder Application

This guide explains how to run tests for both backend and frontend.

## Backend Testing (Django/Python)

### Test Structure

Backend tests are organized by Django apps:
- `accounts/tests.py` - User and Admin model/API tests
- `transactions/tests.py` - Transaction model/API tests
- `budgets/tests.py` - Budget model tests
- `goals/tests.py` - Goal model tests
- `tests/test_integration.py` - Integration tests

### Running Backend Tests

#### Using Django's Test Runner
```bash
cd backend
python manage.py test
```

#### Run specific test file
```bash
python manage.py test accounts.tests
python manage.py test transactions.tests
```

#### Run specific test class
```bash
python manage.py test accounts.tests.UserModelTestCase
```

#### Run specific test method
```bash
python manage.py test accounts.tests.UserModelTestCase.test_user_creation
```

#### Using Pytest (Recommended)
```bash
cd backend
pytest
```

#### Run with coverage
```bash
pytest --cov=. --cov-report=html
```

#### Run specific test file
```bash
pytest accounts/tests.py
pytest tests/test_integration.py
```

### Test Examples

#### Model Tests
- Test user creation and password hashing
- Test UUID string conversion
- Test data validation and constraints

#### API Tests
- Test user registration endpoint
- Test login endpoint
- Test transaction creation
- Test authentication requirements

#### Integration Tests
- Test complete user workflows
- Test data cascade deletion
- Test relationships between models

### Example Test Output

```
backend$ pytest
======================== test session starts ========================
platform win32 -- Python 3.11.0
collected 15 items

accounts/tests.py::UserModelTestCase::test_user_creation PASSED
accounts/tests.py::UserModelTestCase::test_user_uuid_string PASSED
accounts/tests.py::UserAPITestCase::test_register_user PASSED
...
======================== 15 passed in 2.34s ========================
```

## Frontend Testing (Next.js/React)

### Test Structure

Frontend tests use Jest and React Testing Library:
- `src/components/**/__tests__/*.test.tsx` - Component tests
- `src/app/**/__tests__/*.test.tsx` - Page tests
- `src/lib/__tests__/*.test.ts` - Utility tests
- `src/store/__tests__/*.test.ts` - State management tests

### Running Frontend Tests

#### Run all tests
```bash
cd frontend
npm test
```

#### Run in watch mode
```bash
npm run test:watch
```

#### Run with coverage
```bash
npm run test:coverage
```

#### Run specific test file
```bash
npm test -- Sidebar.test.tsx
```

### Test Examples

#### Component Tests
- Test component rendering
- Test user interactions
- Test conditional rendering
- Test props handling

#### Page Tests
- Test page layout
- Test navigation
- Test form interactions
- Test data display

#### Store Tests
- Test state initialization
- Test state updates
- Test persistence

### Example Test Output

```
frontend$ npm test

> funder-frontend@1.0.0 test
> jest

 PASS  src/components/Layout/__tests__/Sidebar.test.tsx
 PASS  src/components/Layout/__tests__/Header.test.tsx
 PASS  src/components/Cards/__tests__/CreditCard.test.tsx
 PASS  src/app/__tests__/page.test.tsx
 PASS  src/app/transactions/__tests__/page.test.tsx
 PASS  src/lib/__tests__/api.test.ts
 PASS  src/store/__tests__/authStore.test.ts

Test Suites: 7 passed, 7 total
Tests:       25 passed, 25 total
Snapshots:   0 total
Time:        3.456 s
```

## Test Coverage Goals

### Backend
- Models: 90%+
- Views/API: 80%+
- Utils: 100%

### Frontend
- Components: 80%+
- Pages: 70%+
- Utils: 100%

## Writing New Tests

### Backend Test Template

```python
from django.test import TestCase
from .models import YourModel

class YourModelTestCase(TestCase):
    def setUp(self):
        # Set up test data
        pass
    
    def test_something(self):
        # Your test logic
        self.assertEqual(actual, expected)
```

### Frontend Test Template

```typescript
import { render, screen } from '@testing-library/react';
import YourComponent from '../YourComponent';

describe('YourComponent', () => {
  it('renders correctly', () => {
    render(<YourComponent />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
});
```

## Continuous Integration

Tests should be run:
- Before committing code
- In CI/CD pipeline
- Before deploying to production

## Troubleshooting

### Backend Tests Failing
- Ensure database is set up correctly
- Check that migrations are applied
- Verify test database settings

### Frontend Tests Failing
- Ensure all dependencies are installed
- Check Jest configuration
- Verify test environment setup

