"""
Middleware for security headers including CSP, XSS protection, etc.
"""
from django.utils.deprecation import MiddlewareMixin


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses to protect against XSS and other attacks.
    """
    
    def process_response(self, request, response):
        # Content Security Policy - Prevents XSS attacks
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        # X-Content-Type-Options - Prevents MIME sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options - Prevents clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # X-XSS-Protection - Enables browser XSS filter
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Strict-Transport-Security - Forces HTTPS (uncomment in production with HTTPS)
        # response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Referrer-Policy - Controls referrer information
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions-Policy - Controls browser features
        response['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'payment=()'
        )
        
        return response
