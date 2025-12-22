from rest_framework import serializers
from .models import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    token = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = BankAccount
        fields = ['id', 'institution_name', 'account_type', 'token', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_id(self, obj):
        return obj.get_uuid_string()

    def create(self, validated_data):
        # Extract token and user
        token = validated_data.pop('token')
        # User is already in validated_data from serializer.save(user=...)
        bank_account = BankAccount(**validated_data)
        bank_account.encrypt_token(token)
        bank_account.save()
        return bank_account

