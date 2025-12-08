from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ['id', 'user', 'category', 'period', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_id(self, obj):
        return obj.get_uuid_string()

