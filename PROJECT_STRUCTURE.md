# Funder Project Structure

## Overview

This document describes the complete project structure for the Funder personal finance application.

## Directory Structure

```
funder/
├── backend/                    # Django REST API Backend
│   ├── funder/                # Main Django project
│   │   ├── __init__.py
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # Root URL configuration
│   │   ├── wsgi.py            # WSGI configuration
│   │   └── asgi.py            # ASGI configuration
│   │
│   ├── accounts/              # User authentication & management
│   │   ├── models.py          # User & Admin models
│   │   ├── views.py           # Authentication views
│   │   ├── serializers.py     # User serializers
│   │   ├── urls.py            # Account routes
│   │   ├── admin.py           # Django admin config
│   │   └── tests.py           # Account tests
│   │
│   ├── transactions/          # Transaction management
│   │   ├── models.py          # Transaction model
│   │   ├── views.py          # Transaction viewsets
│   │   ├── serializers.py    # Transaction serializers
│   │   ├── urls.py           # Transaction routes
│   │   └── admin.py          # Admin config
│   │
│   ├── budgets/               # Budget tracking
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── goals/                 # Savings goals
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── categories/            # Income/expense categories
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── bank_accounts/         # Bank account integration
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── ai_alerts/             # AI-powered alerts
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── admin_panel/           # Admin functionality
│   │   ├── models.py          # SystemLog & AdminAction models
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── utils/                 # Utility functions
│   │   ├── uuid_helpers.py   # UUID conversion utilities
│   │   └── jwt_auth.py        # JWT authentication helpers
│   │
│   ├── database/              # Database scripts
│   │   ├── migrations/        # Django migrations
│   │   └── seeders/          # Seed data scripts
│   │       └── seed_data.py
│   │
│   ├── manage.py              # Django management script
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   ├── pytest.ini            # Pytest configuration
│   └── setup.py              # Setup script
│
├── frontend/                   # Next.js React Frontend
│   ├── src/
│   │   ├── app/              # Next.js app router
│   │   │   ├── layout.tsx    # Root layout
│   │   │   ├── page.tsx      # Home page
│   │   │   └── globals.css   # Global styles
│   │   │
│   │   ├── components/       # React components
│   │   │   └── README.md
│   │   │
│   │   ├── lib/              # Utilities
│   │   │   └── api.ts        # API client
│   │   │
│   │   └── store/            # State management
│   │       └── authStore.ts  # Authentication store
│   │
│   ├── public/                # Static assets
│   ├── package.json          # Node dependencies
│   ├── tsconfig.json          # TypeScript config
│   ├── next.config.js        # Next.js config
│   ├── tailwind.config.js    # Tailwind CSS config
│   ├── postcss.config.js     # PostCSS config
│   └── .env.example          # Environment variables template
│
├── schema.sql                 # MySQL database schema
├── README.md                  # Main project documentation
├── PROJECT_STRUCTURE.md       # This file
└── .gitignore                # Git ignore rules
```

## Backend Architecture

### Django Apps

Each Django app follows a standard structure:
- **models.py**: Database models (Django ORM)
- **views.py**: API endpoints (Django REST Framework)
- **serializers.py**: Data serialization
- **urls.py**: URL routing
- **admin.py**: Django admin interface configuration
- **tests.py**: Unit tests

### Key Features

1. **UUID Storage**: All primary keys use BINARY(16) for efficient UUID storage
2. **JWT Authentication**: Token-based authentication
3. **RESTful API**: Django REST Framework for API endpoints
4. **Admin Panel**: Django admin for data management
5. **Encryption**: Bank account tokens are encrypted using Fernet

## Frontend Architecture

### Next.js Structure

- **App Router**: Using Next.js 14 app directory structure
- **TypeScript**: Full type safety
- **Tailwind CSS**: Utility-first CSS framework
- **State Management**: Zustand for global state
- **API Client**: Axios with interceptors for authentication

### Key Features

1. **Server-Side Rendering**: Next.js SSR capabilities
2. **Type Safety**: TypeScript throughout
3. **Modern UI**: Tailwind CSS for styling
4. **State Management**: Zustand for client state
5. **API Integration**: Centralized API client

## Database Schema

See `schema.sql` for the complete database schema. Key points:

- All tables use BINARY(16) for UUID primary keys
- Foreign keys with appropriate CASCADE/SET NULL behaviors
- Indexes on frequently queried fields
- Constraints for data integrity

## Development Workflow

1. **Backend Development**:
   - Make changes to models/views/serializers
   - Run migrations: `python manage.py makemigrations && migrate`
   - Test endpoints using Django admin or API client

2. **Frontend Development**:
   - Create components in `src/components/`
   - Add pages in `src/app/`
   - Update API calls in `src/lib/api.ts`

3. **Database Changes**:
   - Update models in Django
   - Generate migrations
   - Apply migrations
   - Update schema.sql if needed

## Testing

- Backend: Pytest with pytest-django
- Frontend: Jest (to be configured)
- Run tests: `pytest` (backend) or `npm test` (frontend)

## Deployment Considerations

- Environment variables in `.env` files
- Database migrations must be run
- Static files collection for Django
- Next.js build for production
- CORS configuration for API access
- Security headers and HTTPS

