from django.contrib import admin
from .models import AIAlert


@admin.register(AIAlert)
class AIAlertAdmin(admin.ModelAdmin):
    list_display = ('type', 'user', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('message',)
    readonly_fields = ('id', 'created_at')

