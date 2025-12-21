"""
FunderBot - AI Financial Assistant using Transformers + Deep Learning Predictions
"""

import os
import requests
from typing import Dict, Any

try:
    from transformers import pipeline
except ImportError:
    pipeline = None
    print("Warning: transformers not installed. Chatbot will use fallback responses.")

UserFinancialData = Dict[str, Any]

# Global pipeline - lazy loaded
_generator = None

def _get_generator():
    """Lazy load the GPT-2 generator pipeline on first use."""
    global _generator
    if _generator is not None:
        return _generator
    
    if pipeline is None:
        return None
    try:
        import torch  # noqa: F401  # ensure torch is present
        from transformers import pipeline as _pipeline
        _generator = _pipeline("text-generation", model="gpt2")
    except Exception:
        _generator = None
    return _generator

INTERNAL_PROMPT = (
    "You are FunderBot, an AI financial advisor for Funder app with pages: "
    "Dashboard (overview), Accounts (manage bank accounts), Transactions (track spending), "
    "Budgets (set limits), Goals (savings targets), Investments (portfolio), Cards (manage cards), Settings (profile). "
    "For app questions, explain navigation steps clearly. "
    "For finance questions, give practical budgeting and saving advice. "
    "Keep responses under 100 words. Be helpful and friendly."
)

APP_KEYWORDS = [
    "dashboard", "profile", "funder", "change my email", "how to use",
    "transactions", "settings", "api", "account", "where is",
    "login", "signup", "frontend", "backend", "navigate", "find"
]


def clean_reply(reply: str) -> str:
    """Remove repeated sentences and strip whitespace."""
    sentences = reply.split('. ')
    seen = set()
    cleaned = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and sentence not in seen:
            cleaned.append(sentence)
            seen.add(sentence)
    return '. '.join(cleaned).strip()


def call_ai_prediction(endpoint: str, data: dict) -> dict:
    """
    Helper function to call AI prediction endpoints.
    Returns prediction result or None if error.
    """
    try:
        from django.conf import settings
        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
        response = requests.post(
            f"{base_url}/api/ai-alerts/{endpoint}/",
            json=data,
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"AI prediction error: {e}")
    return None


def get_funderbot_reply(user_message: str, financial_data: UserFinancialData = None) -> str:
    """
    Generate intelligent financial advice using GPT-2 transformer model + Deep Learning predictions.
    
    :param user_message: The query text from the user.
    :param financial_data: Optional user financial data for personalized insights.
    """
    msg_lower = user_message.lower()
    
    # ========== AI-POWERED PREDICTIONS ==========
    
    # Budget risk analysis
    if any(word in msg_lower for word in ['budget risk', 'overspend', 'overrun', 'budget alert']):
        if financial_data and 'budget_data' in financial_data:
            result = call_ai_prediction('predict/budget-risk', financial_data['budget_data'])
            if result and result.get('success'):
                risk = result['risk_probability']
                level = result['risk_level']
                recommended = result['recommended_budget']
                daily_cap = result['daily_spending_cap']
                
                return (f"Budget Risk Analysis: {level} risk ({risk*100:.1f}% probability). "
                        f"I recommend increasing your budget to ${recommended:.2f} and limiting daily spending to ${daily_cap:.2f}. "
                        f"Would you like tips on reducing expenses?")
        
        return "I can analyze your budget risk! Share your spending data: total spent, monthly budget, days passed, and transaction count."
    
    # Savings goal prediction
    if any(word in msg_lower for word in ['goal', 'save', 'saving', 'savings goal']):
        if financial_data and 'goal_data' in financial_data:
            result = call_ai_prediction('predict/goal-success', financial_data['goal_data'])
            if result and result.get('success'):
                prob = result['success_probability']
                confidence = result['confidence_level']
                monthly_needed = result['recommended_monthly_contribution']
                
                if prob > 0.8:
                    return (f"Great news! You have a {prob*100:.1f}% chance of reaching your goal ({confidence} confidence). "
                            f"Keep contributing ${monthly_needed:.2f}/month and you're on track! 🎯")
                elif prob > 0.5:
                    return (f"You have a {prob*100:.1f}% chance of success ({confidence} confidence). "
                            f"To improve your odds, try increasing monthly contributions to ${monthly_needed:.2f}.")
                else:
                    return (f"Your current plan has a {prob*100:.1f}% success rate. Consider: "
                            f"1) Increase monthly savings to ${monthly_needed:.2f}, "
                            f"2) Extend your timeline, or 3) Reduce non-essential expenses.")
        
        return "I can predict your savings goal success! Tell me: goal amount, current savings, months remaining, monthly income & expenses."
    
    # Transaction prediction
    if any(word in msg_lower for word in ['categorize', 'transaction type', 'what category', 'classify transaction']):
        if financial_data and 'transaction_data' in financial_data:
            result = call_ai_prediction('predict/transaction', financial_data['transaction_data'])
            if result and result.get('success'):
                predicted_type = result['predicted_type']
                confidence = result['confidence']
                
                return (f"AI Prediction: This transaction is likely '{predicted_type}' "
                        f"(confidence: {confidence*100:.1f}%). The model analyzed amount, merchant, "
                        f"category, and payment method to make this prediction.")
        
        return "I can categorize transactions using AI! Share the transaction details: amount, merchant, category, payment method."
    
    # Fraud detection
    if any(word in msg_lower for word in ['suspicious', 'fraud', 'flagged', 'unusual transaction']):
        if financial_data and 'transaction_data' in financial_data:
            result = call_ai_prediction('predict/flagged', financial_data['transaction_data'])
            if result and result.get('success'):
                is_flagged = result['is_flagged']
                risk_score = result['risk_score']
                
                if is_flagged:
                    return (f"⚠️ ALERT: This transaction is flagged as suspicious (risk score: {risk_score*100:.1f}%). "
                            f"I recommend reviewing it carefully. Unusual patterns detected in amount, location, or timing.")
                else:
                    return (f"✓ This transaction looks normal (risk score: {risk_score*100:.1f}%). "
                            f"No suspicious patterns detected. You're good to go!")
        
        return "I can detect suspicious transactions! Share the transaction details and I'll analyze it for fraud risk."
    
    # ========== RULE-BASED RESPONSES ==========
    
    # Greetings
    if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'greetings']):
        return "Hi! I'm FunderBot, your AI financial assistant powered by deep learning. Ask me about budgeting, saving, investing, AI predictions, or how to use Funder!"
    
    # App navigation questions
    if 'login' in msg_lower or 'log in' in msg_lower:
        return "To log in: Go to the login page → Enter your email and password → Click Submit."
    
    if 'account' in msg_lower and ('add' in msg_lower or 'create' in msg_lower):
        return "To add an account: Go to Accounts page → Click 'Add Account' button → Enter account name, type, and initial balance → Save."
    
    if 'budget' in msg_lower and ('create' in msg_lower or 'set' in msg_lower or 'make' in msg_lower):
        return "To create a budget: Go to Budgets page → Click 'Create Budget' → Select category → Set amount and time period → Save. Want me to analyze your budget risk with AI?"
    
    if 'goal' in msg_lower and ('create' in msg_lower or 'set' in msg_lower):
        return "To create a goal: Go to Goals page → Click 'New Goal' → Enter goal name, target amount, and deadline → Save. I can predict your success probability using AI!"
    
    if 'transaction' in msg_lower and 'add' in msg_lower:
        return "To add a transaction: Go to Transactions page → Click 'Add Transaction' → Select account → Enter amount, category, date, description → Save. I can auto-categorize transactions with AI!"
    
    if 'card' in msg_lower and ('add' in msg_lower or 'new' in msg_lower):
        return "To add a card: Go to Cards page → Click 'Add Card' → Enter card details → Save."
    
    # Finance advice questions
    if 'emergency' in msg_lower or 'emergency fund' in msg_lower:
        return "Build an emergency fund with 3-6 months of expenses. Start with $1,000, then gradually save more. Keep it in a high-yield savings account for easy access!"
    
    if 'debt' in msg_lower or 'pay off' in msg_lower:
        return "Two strategies: Avalanche (pay highest interest first, saves money) or Snowball (pay smallest first, builds motivation). Make minimum payments on all, put extra toward one."
    
    if 'invest' in msg_lower:
        return "Investment basics: Get 401(k) match first, pay off high-interest debt, build emergency fund, then invest in low-cost index funds. Start small and stay consistent!"
    
    if 'retire' in msg_lower or 'retirement' in msg_lower:
        return "Retirement tips: Start early, contribute to 401(k) (especially if employer matches), consider Roth IRA, aim to save 15% of income. The earlier you start, the more compound interest helps!"
    
    # AI capabilities
    if 'ai' in msg_lower or 'predict' in msg_lower or 'machine learning' in msg_lower:
        return "I use deep learning models to: 1) Predict budget overrun risk, 2) Estimate savings goal success, 3) Auto-categorize transactions, 4) Detect fraudulent transactions. Ask me to analyze your data!"
    
    # Default response
    return "I can help you with: budgeting strategies, saving tips, debt payoff, investing basics, AI predictions (budget risk, goal success, transaction categorization, fraud detection), or navigating the Funder app. What would you like to know?"
    
