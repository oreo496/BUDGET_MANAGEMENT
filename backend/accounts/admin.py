from django.contrib import admin
from .models import User, Admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id', 'created_at')


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('id', 'created_at')

