#!/bin/bash

echo "========================================"
echo "Funder Project Setup Script (Mac/Linux)"
echo "========================================"
echo ""

echo "Step 1: Setting up Backend..."
echo ""

cd backend

echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    echo "Make sure Python 3.8+ is installed"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit backend/.env file with your database credentials!"
    echo ""
fi

echo ""
echo "Step 2: Setting up Frontend..."
echo ""

cd ../frontend

echo "Installing Node dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Node dependencies"
    echo "Make sure Node.js 18+ is installed"
    exit 1
fi

echo ""
echo "Creating .env.local file..."
if [ ! -f .env.local ]; then
    cp .env.example .env.local
    echo ""
    echo "IMPORTANT: Please edit frontend/.env.local file with your API URL!"
    echo ""
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Create MySQL database: mysql -u root -p < schema.sql"
echo "2. Edit backend/.env with database credentials"
echo "3. Edit frontend/.env.local with API URL"
echo "4. Run backend: cd backend && source venv/bin/activate && python manage.py runserver"
echo "5. Run frontend: cd frontend && npm run dev"
echo ""

