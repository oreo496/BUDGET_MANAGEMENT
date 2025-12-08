from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'current_amount', 'target_amount', 'deadline', 'user')
    search_fields = ('title',)
    readonly_fields = ('id', 'created_at', 'progress_percentage')

