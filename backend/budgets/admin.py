from django.contrib import admin
from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'period', 'amount', 'user', 'created_at')
    list_filter = ('period', 'created_at')
    search_fields = ('category__name',)

