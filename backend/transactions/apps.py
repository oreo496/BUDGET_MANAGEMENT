from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'
    
    def ready(self):
        """Import signal handlers when app is ready."""
        import utils.signals  # This will register all signal handlers

    def ready(self):
        # Import signals
        from . import signals  # noqa: F401

