"""
Security utilities for SQL injection and XSS protection.
"""
import re
import html
from django.utils.html import escape
from django.core.exceptions import ValidationError


def sanitize_input(value, max_length=None, allow_html=False):
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        value: Input value to sanitize
        max_length: Maximum allowed length
        allow_html: If True, allows safe HTML (not recommended)
    
    Returns:
        Sanitized string
    """
    if value is None:
        return None
    
    # Convert to string
    value = str(value).strip()
    
    # Check length
    if max_length and len(value) > max_length:
        raise ValidationError(f"Input exceeds maximum length of {max_length}")
    
    # Escape HTML to prevent XSS
    if not allow_html:
        value = escape(value)
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    return value


def sanitize_sql_input(value):
    """
    Additional validation for SQL injection prevention.
    Note: Django ORM already protects against SQL injection,
    but this adds extra validation for suspicious patterns.
    """
    if value is None:
        return None
    
    value = str(value)
    
    # List of dangerous SQL patterns
    dangerous_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|SCRIPT)\b)",
        r"(--|#|\/\*|\*\/)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"(\b(OR|AND)\s+['\"].*['\"]\s*=\s*['\"].*['\"])",
        r"(\b(OR|AND)\s+['\"]\s*=\s*['\"])",
    ]
    
    # Check for dangerous patterns (case-insensitive)
    for pattern in dangerous_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError("Invalid input detected")
    
    return value


def validate_email(email):
    """Validate and sanitize email address."""
    if not email:
        return None
    
    email = sanitize_input(email, max_length=100)
    
    # Basic email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationError("Invalid email format")
    
    return email.lower()


def validate_phone(phone):
    """Validate and sanitize phone number."""
    if not phone:
        return None
    
    phone = sanitize_input(phone, max_length=20)
    
    # Remove non-digit characters except +, -, spaces, parentheses
    phone = re.sub(r'[^\d\+\-\(\)\s]', '', phone)
    
    return phone


def validate_amount(amount):
    """Validate monetary amount."""
    try:
        amount = float(amount)
        if amount < 0:
            raise ValidationError("Amount cannot be negative")
        if amount > 999999999.99:
            raise ValidationError("Amount exceeds maximum limit")
        return round(amount, 2)
    except (ValueError, TypeError):
        raise ValidationError("Invalid amount format")


def sanitize_text_field(text, max_length=1000):
    """Sanitize text fields (descriptions, notes, etc.)."""
    if not text:
        return ""
    
    text = sanitize_input(text, max_length=max_length)
    
    # Remove script tags and event handlers
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
    
    return text


def validate_uuid(uuid_string):
    """Validate UUID format."""
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, uuid_string, re.IGNORECASE):
        raise ValidationError("Invalid UUID format")
    return uuid_string


def sanitize_for_logging(value):
    """Sanitize values before logging to prevent log injection."""
    if value is None:
        return None
    
    value = str(value)
    # Remove newlines and control characters
    value = re.sub(r'[\r\n\t]', ' ', value)
    value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
    return value[:500]  # Limit log entry length

