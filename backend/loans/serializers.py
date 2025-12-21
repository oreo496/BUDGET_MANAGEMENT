from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'user', 'lender_name', 'amount', 'term_months', 'interest_rate', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'created_at']

    def get_id(self, obj):
        return obj.get_uuid_string()

    def get_user(self, obj):
        return obj.user.get_uuid_string()
