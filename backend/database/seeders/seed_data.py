"""
Database seeder script for development/testing.
"""
import os
import sys
import django
import random
from datetime import date, timedelta

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from accounts.models import User, Admin
from categories.models import Category
from transactions.models import Transaction
from budgets.models import Budget
from goals.models import Goal


def seed_users():
    """Create sample users."""
    user1 = User.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='1234567890',
        status='ACTIVE'
    )
    user1.set_password('password123')
    user1.save()
    
    user2 = User.objects.create(
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@example.com',
        phone='0987654321',
        status='ACTIVE'
    )
    user2.set_password('password123')
    user2.save()
    
    print("✓ Created sample users")
    return user1, user2


def seed_categories(user):
    """Create sample categories for a user."""
    categories = [
        {'name': 'Salary', 'type': 'INCOME'},
        {'name': 'Freelance', 'type': 'INCOME'},
        {'name': 'Groceries', 'type': 'EXPENSE'},
        {'name': 'Transportation', 'type': 'EXPENSE'},
        {'name': 'Entertainment', 'type': 'EXPENSE'},
    ]
    
    created = []
    for cat_data in categories:
        cat = Category.objects.create(
            user=user,
            name=cat_data['name'],
            type=cat_data['type']
        )
        created.append(cat)
    
    print(f"✓ Created {len(created)} categories for user")
    return created


def seed_transactions(user, categories):
    """Create sample transactions."""
    
    expense_cats = [c for c in categories if c.type == 'EXPENSE']
    income_cats = [c for c in categories if c.type == 'INCOME']
    
    transactions = []
    for i in range(20):
        is_income = random.choice([True, False])
        category = random.choice(income_cats if is_income else expense_cats)
        
        transaction = Transaction.objects.create(
            user=user,
            category=category,
            amount=random.uniform(10, 500) if is_income else random.uniform(5, 200),
            type='INCOME' if is_income else 'EXPENSE',
            merchant=f'Merchant {i+1}',
            date=date.today() - timedelta(days=random.randint(0, 30)),
            source=random.choice(['MANUAL', 'SYNCED'])
        )
        transactions.append(transaction)
    
    print(f"✓ Created {len(transactions)} transactions")
    return transactions


def seed_budgets(user, categories):
    """Create sample budgets."""
    expense_cats = [c for c in categories if c.type == 'EXPENSE']
    
    budgets = []
    for cat in expense_cats[:3]:  # Create budgets for first 3 expense categories
        budget = Budget.objects.create(
            user=user,
            category=cat,
            period=random.choice(['WEEKLY', 'MONTHLY']),
            amount=random.uniform(50, 500)
        )
        budgets.append(budget)
    
    print(f"✓ Created {len(budgets)} budgets")
    return budgets


def seed_goals(user):
    """Create sample goals."""
    
    goals = [
        {
            'title': 'Emergency Fund',
            'target_amount': 10000,
            'current_amount': 2500,
            'deadline': date.today() + timedelta(days=365)
        },
        {
            'title': 'Vacation',
            'target_amount': 3000,
            'current_amount': 800,
            'deadline': date.today() + timedelta(days=180)
        }
    ]
    
    created = []
    for goal_data in goals:
        goal = Goal.objects.create(
            user=user,
            **goal_data
        )
        created.append(goal)
    
    print(f"✓ Created {len(created)} goals")
    return created


def main():
    """Run all seeders."""
    print("Starting database seeding...\n")
    
    # Clear existing data (optional - comment out if you want to keep data)
    # User.objects.all().delete()
    
    # Seed data
    user1, user2 = seed_users()
    categories1 = seed_categories(user1)
    transactions1 = seed_transactions(user1, categories1)
    budgets1 = seed_budgets(user1, categories1)
    goals1 = seed_goals(user1)
    
    print("\n✓ Database seeding completed!")


if __name__ == '__main__':
    main()

