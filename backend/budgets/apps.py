from django.apps import AppConfig


class BudgetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budgets'
    
    def ready(self):
        """Import signal handlers when app is ready."""
        import utils.signals  # This will register all signal handlers

