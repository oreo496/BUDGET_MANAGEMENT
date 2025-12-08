from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'amount', 'type', 'date', 'source', 'flagged_fraud')
    list_filter = ('type', 'source', 'flagged_fraud', 'date')
    search_fields = ('merchant',)
    readonly_fields = ('id', 'created_at')

