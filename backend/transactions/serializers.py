from rest_framework import serializers
from .models import Transaction
from ai_alerts.models import AIAlert


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    ai_alert_message = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'bank_account', 'amount', 'type',
                  'merchant', 'date', 'source', 'flagged_fraud', 'ai_alert_message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_id(self, obj):
        return obj.get_uuid_string()

    def get_ai_alert_message(self, obj):
        # Find latest alert with embedded txn id if present
        txn_id = obj.get_uuid_string()
        alert = AIAlert.objects.filter(user=obj.user, message__contains=f"txn:{txn_id}").order_by('-created_at').first()
        return alert.message if alert else None

