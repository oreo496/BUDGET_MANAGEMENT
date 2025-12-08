"""
XSS Protection Middleware and Utilities.
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


class XSSProtectionMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers for XSS protection.
    """
    
    def process_response(self, request, response):
        # X-XSS-Protection header (for older browsers)
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Content-Security-Policy (CSP) header
        # Adjust based on your needs
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "  # Adjust for production
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' http://localhost:8000 http://127.0.0.1:8000; "
            "frame-ancestors 'self'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response['Content-Security-Policy'] = csp_policy
        
        # X-Content-Type-Options
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options (already handled by Django, but ensure it's set)
        if 'X-Frame-Options' not in response:
            response['X-Frame-Options'] = 'DENY'
        
        # Referrer-Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions-Policy (formerly Feature-Policy)
        response['Permissions-Policy'] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(), "
            "usb=()"
        )
        
        return response

