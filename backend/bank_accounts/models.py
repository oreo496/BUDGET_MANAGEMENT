from django.db import models
import uuid
from accounts.models import User
from cryptography.fernet import Fernet
from django.conf import settings


class BankAccount(models.Model):
    id = models.BinaryField(primary_key=True, max_length=16, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    institution_name = models.CharField(max_length=100, blank=True, null=True)
    account_type = models.CharField(max_length=50, blank=True, null=True)
    token = models.BinaryField(max_length=500)  # Encrypted token
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bank_accounts'

    def save(self, *args, **kwargs):
        if not self.id:
            uuid_obj = uuid.uuid4()
            self.id = uuid_obj.bytes
        super().save(*args, **kwargs)

    def get_uuid_string(self):
        return str(uuid.UUID(bytes=self.id))

    def encrypt_token(self, plain_token):
        """Encrypt the bank account token."""
        key = settings.ENCRYPTION_KEY.encode() if hasattr(settings, 'ENCRYPTION_KEY') else b'default-key-32-chars-long!!'
        f = Fernet(key)
        self.token = f.encrypt(plain_token.encode())

    def decrypt_token(self):
        """Decrypt the bank account token."""
        key = settings.ENCRYPTION_KEY.encode() if hasattr(settings, 'ENCRYPTION_KEY') else b'default-key-32-chars-long!!'
        f = Fernet(key)
        return f.decrypt(self.token).decode()

    def __str__(self):
        return f"{self.institution_name or 'Unknown'} - {self.account_type or 'N/A'}"

