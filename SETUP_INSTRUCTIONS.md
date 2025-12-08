# Funder - Complete Setup Instructions

## ⚠️ IMPORTANT NOTES

### Backend Technology
- **Backend**: Django (Python) - NOT JavaScript
- **Frontend**: Next.js (TypeScript/JavaScript) - This is standard for modern web apps

If you want PHP instead of Django, let me know and I'll recreate the backend in PHP.

### Database Setup
Since we're using **BINARY(16) for UUIDs** (which Django doesn't natively support well), you have two options:

**Option 1: Use Existing Schema (Recommended)**
1. Create the database using the SQL schema first
2. Then use `--fake-initial` for migrations

**Option 2: Let Django Create Tables**
- Django will create tables, but UUIDs will be stored differently
- You may need to adjust the models

## Step-by-Step Setup

### 1. Database Setup

```bash
# Create the database using the SQL schema
mysql -u root -p < schema.sql
```

### 2. Backend Setup (Django - Python)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your database credentials:
# DB_NAME=funder
# DB_USER=root
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=3306

# Generate encryption key for bank tokens
python -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())"
# Copy the output to your .env file

# Since tables already exist, fake the initial migrations
python manage.py migrate --fake-initial

# Create Django superuser (for admin panel)
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

Backend will run at: `http://localhost:8000`

### 3. Frontend Setup (Next.js - TypeScript)

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Run development server
npm run dev
```

Frontend will run at: `http://localhost:3000`

## What's Implemented

### ✅ Fully Implemented:
- All Django models matching your database schema
- REST API endpoints for all resources
- JWT authentication structure
- Database seeders
- Admin panel configuration
- Frontend structure with Next.js

### ⚠️ Needs Configuration:
- Database connection (edit .env)
- Encryption key generation
- JWT secret key
- CORS settings (if needed)

### 🔧 May Need Adjustments:
- Django migrations with BINARY(16) - use `--fake-initial` if tables exist
- Foreign key relationships - verify they work with your existing schema
- Authentication middleware - may need custom JWT middleware

## Testing the Setup

### Test Backend:
```bash
cd backend
python manage.py runserver
# Visit http://localhost:8000/admin
# Visit http://localhost:8000/api/auth/register
```

### Test Frontend:
```bash
cd frontend
npm run dev
# Visit http://localhost:3000
```

## Common Issues

### Issue: Django migrations fail
**Solution**: Use `--fake-initial` since tables already exist:
```bash
python manage.py migrate --fake-initial
```

### Issue: MySQL connection error
**Solution**: Check your .env file has correct database credentials

### Issue: Module not found
**Solution**: Make sure virtual environment is activated and dependencies installed

### Issue: BINARY(16) field issues
**Solution**: The models use BinaryField which should work, but if you get errors, you may need to use raw SQL migrations

## Next Steps After Setup

1. **Test API endpoints** using Postman or curl
2. **Seed database** with test data: `python database/seeders/seed_data.py`
3. **Build frontend components** in `frontend/src/components/`
4. **Add authentication middleware** for JWT tokens
5. **Implement business logic** in views/serializers

## Want PHP Instead?

If you prefer PHP for the backend instead of Django, I can:
- Create a PHP/Laravel or PHP/Slim backend
- Match the same database schema
- Create REST API endpoints
- Set up authentication

Just let me know!

