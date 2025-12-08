from django.contrib import admin
from .models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('institution_name', 'account_type', 'user', 'created_at')
    search_fields = ('institution_name',)
    readonly_fields = ('id', 'created_at', 'token')

