from rest_framework import serializers
from .models import AIAlert


class AIAlertSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = AIAlert
        fields = ['id', 'user', 'message', 'type', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_id(self, obj):
        return obj.get_uuid_string()

