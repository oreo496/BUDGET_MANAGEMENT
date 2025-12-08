from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'bank_account', 'amount', 'type',
                  'merchant', 'date', 'source', 'flagged_fraud', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_id(self, obj):
        return obj.get_uuid_string()

