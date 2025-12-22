from rest_framework import serializers
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    progress_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Goal
        fields = ['id', 'user', 'title', 'target_amount', 'current_amount',
                  'deadline', 'progress_percentage', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def get_id(self, obj):
        return obj.get_uuid_string()

