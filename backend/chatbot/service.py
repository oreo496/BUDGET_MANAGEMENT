# -*- coding: utf-8 -*-
"""
Chatbot service using transformers for NLP.
Handles chat interactions and AI responses.
"""

try:
    from transformers import pipeline
except ImportError:
    pipeline = None
    print("Warning: transformers not installed. Chatbot will use fallback responses.")

# ==== NLP Section ====
_generator = None

def _get_generator():
    """Lazy load the generator pipeline on first use. Returns None if torch/model unavailable."""
    global _generator
    if _generator is not None:
        return _generator
    
    if pipeline is None:
        return None
    try:
        import torch  # noqa: F401  # ensure torch is present
        from transformers import pipeline
        _generator = pipeline("text-generation", model="gpt2")
    except Exception:
        _generator = None
    return _generator

INTERNAL_PROMPT = (
    "You are FunderBot, an AI chatbot for the Funder app. "
    "If asked about Funder/app features and you do NOT have a live connection, reply: "
    "'Sorry, I can't answer app-specific questions right now. Please connect FunderBot to your app for those.' "
    "For general finance or budgeting, provide short best advice possible. "
    "Never make up details about the Funder app or anything related to Funder. "
    "You can answer questions about using the Funder app AND general finance or budgeting topics. "
    "Never perform actions or change user data. "
    "Give advice, explain finance concepts, budgeting help, Funder features, and navigation. "
    "If asked about changing email/data, explain the steps ONLY. "
    "If the question is completely unrelated or irrelevant, reply: 'I answer questions about Funder and finance topics.' "
    "If the user asks about the Funder app and you do NOT have a live connection or data, respond: 'Sorry, I can't answer app-specific questions right now.' "
    "Otherwise, for general finance or budgeting questions, answer as best as you can. "
)

APP_KEYWORDS = [
    "dashboard", "profile", "funder", "change my email",
    "transactions", "settings", "api", "account",
    "login", "signup", "frontend", "backend"
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


def get_funderbot_reply(user_message: str) -> str:
    """
    Generate a reply from FunderBot based on user message.
    
    If an app/Funder keyword is detected, return fixed response.
    Otherwise, use NLP model for finance/budgeting advice.
    """
    # If an app/Funder keyword is detected, return your fixed response.
    if any(keyword in user_message.lower() for keyword in APP_KEYWORDS):
        return "Sorry, I can't answer app-specific questions right now. Please connect FunderBot to your app for those."
    
    prompt = INTERNAL_PROMPT + " User: " + user_message + " FunderBot:"
    generator = _get_generator()
    if generator is None:
        return "AI model is warming up. For now: start by listing your monthly income, fixed bills, savings target, and cap discretionary to what's left."

    response = generator(prompt, max_length=80)
    reply = response[0]['generated_text'].split("FunderBot:")[-1].strip()
    return clean_reply(reply)
