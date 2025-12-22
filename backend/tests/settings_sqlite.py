from funder.settings import *  # noqa

# Use SQLite for tests to avoid MySQL-specific constraints on BLOB primary keys
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Ensure faster hashing during tests (optional)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Allow all origins in tests
CORS_ALLOW_ALL_ORIGINS = True
