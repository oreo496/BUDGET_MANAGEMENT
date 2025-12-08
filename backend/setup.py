"""
Setup script for Funder backend.
Run this to set up the development environment.
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e.stderr}")
        return False

def main():
    print("=" * 50)
    print("Funder Backend Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8+ is required")
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("\nSetup failed. Please check the errors above.")
        sys.exit(1)
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("\n⚠ Warning: .env file not found")
        print("Please copy .env.example to .env and configure it")
    else:
        print("\n✓ .env file found")
    
    print("\n" + "=" * 50)
    print("Setup completed!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Configure .env file with your database credentials")
    print("2. Create database: mysql -u root -p < ../schema.sql")
    print("3. Run migrations: python manage.py makemigrations && python manage.py migrate")
    print("4. Create superuser: python manage.py createsuperuser")
    print("5. Run server: python manage.py runserver")

if __name__ == '__main__':
    main()

