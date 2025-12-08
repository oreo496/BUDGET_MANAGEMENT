# Funder - Personal Finance Application

A comprehensive personal finance management application built with Django REST Framework (backend) and Next.js (frontend).

## Project Structure

```
funder/
├── backend/              # Django REST API
│   ├── funder/          # Django project settings
│   ├── accounts/        # User authentication & management
│   ├── transactions/    # Transaction management
│   ├── budgets/         # Budget tracking
│   ├── goals/           # Savings goals
│   ├── categories/      # Income/expense categories
│   ├── bank_accounts/   # Bank account integration
│   ├── ai_alerts/       # AI-powered alerts
│   ├── admin_panel/     # Admin functionality
│   ├── utils/           # Utility functions
│   └── database/        # Migrations & seeders
├── frontend/             # Next.js React application
│   ├── src/
│   │   ├── app/         # Next.js app router
│   │   ├── components/ # React components
│   │   ├── lib/         # API client & utilities
│   │   └── store/       # State management
│   └── public/          # Static assets
└── schema.sql           # MySQL database schema
```

## Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **MySQL** - Database
- **JWT** - Authentication
- **bcrypt** - Password hashing
- **cryptography** - Token encryption

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Axios** - HTTP client
- **React Query** - Data fetching

## Database Schema

The database schema is defined in `schema.sql` and includes the following tables:

### Core Tables
- **users** - User accounts with authentication and profile information
- **admins** - Administrator accounts
- **categories** - Income and expense categories (user-specific)
- **bank_accounts** - Tokenized bank account information
- **transactions** - Financial transactions (income/expense)
- **budgets** - Budget tracking (weekly/monthly)
- **goals** - Savings goals with target amounts and deadlines

### Supporting Tables
- **ai_alerts** - AI-generated alerts and recommendations
- **system_logs** - System activity logs for users and admins
- **admin_actions** - Audit trail for administrative actions

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- MySQL 8.0+
- pip & npm

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. Create database:
   ```bash
   mysql -u root -p < ../schema.sql
   ```

6. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. (Optional) Seed database:
   ```bash
   python database/seeders/seed_data.py
   ```

8. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

9. Run development server:
   ```bash
   python manage.py runserver
   ```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URL
   ```

4. Run development server:
   ```bash
   npm run dev
   ```

Frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile/update` - Update user profile

### Transactions
- `GET /api/transactions/` - List transactions
- `POST /api/transactions/` - Create transaction
- `GET /api/transactions/{id}/` - Get transaction
- `PUT /api/transactions/{id}/` - Update transaction
- `DELETE /api/transactions/{id}/` - Delete transaction
- `POST /api/transactions/{id}/flag_fraud/` - Flag transaction as fraud

### Budgets
- `GET /api/budgets/` - List budgets
- `POST /api/budgets/` - Create budget
- `GET /api/budgets/{id}/` - Get budget
- `PUT /api/budgets/{id}/` - Update budget
- `DELETE /api/budgets/{id}/` - Delete budget

### Goals
- `GET /api/goals/` - List goals
- `POST /api/goals/` - Create goal
- `GET /api/goals/{id}/` - Get goal
- `PUT /api/goals/{id}/` - Update goal
- `DELETE /api/goals/{id}/` - Delete goal

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category
- `GET /api/categories/{id}/` - Get category
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Bank Accounts
- `GET /api/bank-accounts/` - List bank accounts
- `POST /api/bank-accounts/` - Add bank account
- `GET /api/bank-accounts/{id}/` - Get bank account
- `DELETE /api/bank-accounts/{id}/` - Remove bank account

### AI Alerts
- `GET /api/ai-alerts/` - List alerts
- `POST /api/ai-alerts/` - Create alert
- `GET /api/ai-alerts/{id}/` - Get alert

### Admin
- `GET /api/admin/logs/` - System logs
- `GET /api/admin/actions/` - Admin actions
- `POST /api/admin/actions/` - Create admin action

## Key Features

- UUID-based primary keys stored as BINARY(16) for efficient storage
- Tokenized bank account data for security
- Fraud detection flagging in transactions
- AI-powered alerts and recommendations
- Comprehensive audit logging
- Support for manual and synced transactions
- Two-factor authentication support
- RESTful API with Django REST Framework
- Modern React frontend with Next.js
- JWT-based authentication

## Database Design Notes

- All IDs use BINARY(16) for UUID storage (more efficient than VARCHAR)
- Foreign keys use appropriate CASCADE and SET NULL behaviors
- Bank account tokens are stored as VARBINARY for encrypted data
- Transactions support both manual entry and bank sync
- Budgets can be set for weekly or monthly periods
- AI alerts support multiple types: budget alerts, spending patterns, fraud detection, and goal recommendations

## Development

### Running Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Code Style
- Backend: Follow PEP 8 Python style guide
- Frontend: ESLint configuration included

## License

ISC

