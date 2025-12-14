"""
FunderBot - AI Financial Assistant using Transformers
"""

import os
from typing import Dict, Any

UserFinancialData = Dict[str, Any]

# Global pipeline - lazy loaded
_generator = None

def _get_generator():
    """Lazy load the GPT-2 generator pipeline on first use."""
    global _generator
    if _generator is None:
        try:
            from transformers import pipeline
            _generator = pipeline("text-generation", model="gpt2")
        except Exception:
            _generator = False  # Mark as failed to avoid retrying
    return _generator if _generator else None


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


def get_funderbot_reply(user_message: str, financial_data: UserFinancialData = None) -> str:
    """
    Generate intelligent financial advice using GPT-2 transformer model.
    
    :param user_message: The query text from the user.
    :param financial_data: Optional user financial data for personalized insights.
    """
    msg_lower = user_message.lower()
    
    # Always use rule-based responses first for faster response
    # (GPT-2 model downloads on first use which can take time)
    
    # Greetings
    if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'greetings']):
        return "Hi! I'm FunderBot, your AI financial assistant. Ask me about budgeting, saving, investing, or how to use any feature in Funder!"
    
    # App navigation questions
    if 'login' in msg_lower or 'log in' in msg_lower:
        return "To log in: Go to the login page → Enter your email and password → Click Submit."
    
    if 'account' in msg_lower and ('add' in msg_lower or 'create' in msg_lower):
        return "To add an account: Go to Accounts page → Click 'Add Account' button → Enter account name, type, and initial balance → Save."
    
    if 'budget' in msg_lower and ('create' in msg_lower or 'set' in msg_lower or 'make' in msg_lower):
        return "To create a budget: Go to Budgets page → Click 'Create Budget' → Select category → Set amount and time period → Save."
    
    if 'goal' in msg_lower and ('create' in msg_lower or 'set' in msg_lower):
        return "To create a goal: Go to Goals page → Click 'New Goal' → Enter goal name, target amount, and deadline → Save."
    
    if 'transaction' in msg_lower and 'add' in msg_lower:
        return "To add a transaction: Go to Transactions page → Click 'Add Transaction' → Select account → Enter amount, category, date, description → Save."
    
    if 'card' in msg_lower and ('add' in msg_lower or 'new' in msg_lower):
        return "To add a card: Go to Cards page → Click 'Add Card' → Enter card details → Save."
    
    # Finance advice questions
    if 'save' in msg_lower or 'saving' in msg_lower:
        return "A good rule: Save 20% of your income. Start with a $1,000 emergency fund, then build to 3-6 months of expenses. Use Funder's Goals page to track your progress!"
    
    if 'budget' in msg_lower:
        return "Try the 50/30/20 rule: 50% for needs (rent, food), 30% for wants (fun), 20% for savings/debt. Track everything in Funder's Budgets page!"
    
    if 'debt' in msg_lower or 'pay off' in msg_lower:
        return "Two strategies: Avalanche (pay highest interest first, saves money) or Snowball (pay smallest first, builds motivation). Make minimum payments on all, put extra toward one."
    
    if 'invest' in msg_lower:
        return "Investment basics: Get 401(k) match first, pay off high-interest debt, build emergency fund, then invest in low-cost index funds. Start small and stay consistent!"
    
    if 'emergency' in msg_lower or 'emergency fund' in msg_lower:
        return "Build an emergency fund with 3-6 months of expenses. Start with $1,000, then gradually save more. Keep it in a high-yield savings account for easy access!"
    
    if 'retire' in msg_lower or 'retirement' in msg_lower:
        return "Retirement tips: Start early, contribute to 401(k) (especially if employer matches), consider Roth IRA, aim to save 15% of income. The earlier you start, the more compound interest helps!"
    
    # Default response
    return "I can help you with: budgeting strategies, saving tips, debt payoff, investing basics, or navigating the Funder app (Accounts, Budgets, Goals, Transactions, Cards). What would you like to know?"
    
