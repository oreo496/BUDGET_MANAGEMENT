from rest_framework import serializers
from .models import SystemLog, AdminAction


class SystemLogSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = SystemLog
        fields = ['id', 'user', 'admin', 'action', 'details', 'timestamp']
        read_only_fields = ['id', 'timestamp']

    def get_id(self, obj):
        return obj.get_uuid_string()


class AdminActionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = AdminAction
        fields = ['id', 'admin', 'action', 'target_user', 'transaction', 'timestamp']
        read_only_fields = ['id', 'timestamp']

    def get_id(self, obj):
        return obj.get_uuid_string()

