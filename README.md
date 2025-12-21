# 💰 Funder - AI-Powered Personal Finance Application

A comprehensive personal finance management application with AI-powered predictions built with Django REST Framework (backend) and Next.js (frontend).

## 🚀 Quick Start

See **AI_INTEGRATION_COMPLETE.md** for complete setup guide and **schema.sql** for database schema.

### Windows Quick Start
`atch
QUICK_START.bat
`

### Manual Setup

**Backend:**
`ash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
`

**Frontend:**
`ash
cd frontend
npm install
npm run dev
`

**AI Models:**
`ash
code backend/AI_DL_MODEL.ipynb
# Run all cells (1-17)
cd backend
python test_ai_integration.py
`

## 🧠 AI Features

- **Transaction Classification** - 89%+ ensemble accuracy
- **Budget Overrun Prediction** - 88%+ accuracy  
- **Savings Goal Success** - 91%+ accuracy
- **Fraud Detection** - 82%+ accuracy
- **FunderBot Chatbot** - AI-powered financial advisor

## 🛠️ Tech Stack

**Backend:** Django 4.2, DRF, PyTorch, TabNet, Transformers, MySQL, JWT+MFA  
**Frontend:** Next.js 14, TypeScript, Tailwind CSS, Zustand

## 📡 API Endpoints

- /api/accounts/ - Authentication (register, login, MFA)
- /api/transactions/ - Transaction management
- /api/budgets/ - Budget tracking
- /api/goals/ - Savings goals
- /api/ai-alerts/predict/* - AI predictions
- /api/chatbot/ - AI chatbot

## 📚 Documentation

- **Full Setup Guide:** [AI_INTEGRATION_COMPLETE.md](AI_INTEGRATION_COMPLETE.md)
- **Database Schema:** [schema.sql](schema.sql)
- **AI Training:** [backend/AI_DL_MODEL.ipynb](backend/AI_DL_MODEL.ipynb)

## 🎯 Project Structure

`
BUDGET_MANAGEMENT/
├── backend/              # Django + AI models
├── frontend/             # Next.js React app
├── Funder_AiModel/       # AI research
└── .venv/               # Python virtual environment
`

---

**Made with ❤️ by Shahin Lap**
