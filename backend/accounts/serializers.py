from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=True)
    # Exclude sensitive MFA fields from response
    two_factor_secret = serializers.CharField(read_only=True, required=False)
    backup_codes = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 
                  'two_factor_enabled', 'status', 'created_at', 'password',
                  'two_factor_secret', 'backup_codes']
        read_only_fields = ['id', 'created_at', 'two_factor_secret', 'backup_codes']
        extra_kwargs = {
            'two_factor_secret': {'write_only': False},
            'backup_codes': {'write_only': False},
        }

    def get_id(self, obj):
        """Convert binary ID to UUID string."""
        return obj.get_uuid_string()

    def to_representation(self, instance):
        """Remove sensitive fields from response."""
        data = super().to_representation(instance)
        # Never expose secret or backup codes in API responses
        data.pop('two_factor_secret', None)
        data.pop('backup_codes', None)
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

