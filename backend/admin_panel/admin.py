from django.contrib import admin
from .models import SystemLog, AdminAction


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'admin', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('action', 'details')
    readonly_fields = ('id', 'timestamp')


@admin.register(AdminAction)
class AdminActionAdmin(admin.ModelAdmin):
    list_display = ('admin', 'action', 'target_user', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('action',)
    readonly_fields = ('id', 'timestamp')

