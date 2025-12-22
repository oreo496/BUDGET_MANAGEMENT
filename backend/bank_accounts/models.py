from django.db import models
import uuid
from accounts.models import User
from cryptography.fernet import Fernet
from django.conf import settings


class BankAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    institution_name = models.CharField(max_length=100, blank=True, null=True)
    account_type = models.CharField(max_length=50, blank=True, null=True)
    token = models.BinaryField(max_length=500)  # Encrypted token
    
    # Plaid integration fields
    plaid_access_token = models.BinaryField(max_length=500, blank=True, null=True)  # Encrypted Plaid access token
    plaid_item_id = models.CharField(max_length=100, blank=True, null=True)
    plaid_account_id = models.CharField(max_length=100, blank=True, null=True)
    plaid_cursor = models.TextField(blank=True, null=True)  # For incremental sync
    last_sync = models.DateTimeField(blank=True, null=True)
    auto_sync_enabled = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bank_accounts'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)

    def get_uuid_string(self):
        return str(self.id)

    def encrypt_token(self, plain_token):
        """Encrypt the bank account token."""
        key = settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY
        f = Fernet(key)
        self.token = f.encrypt(plain_token.encode())

    def decrypt_token(self):
        """Decrypt the bank account token."""
        key = settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY
        f = Fernet(key)
        return f.decrypt(self.token).decode()

    def encrypt_plaid_token(self, plain_token):
        """Encrypt the Plaid access token."""
        key = settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY
        f = Fernet(key)
        self.plaid_access_token = f.encrypt(plain_token.encode())

    def decrypt_plaid_token(self):
        """Decrypt the Plaid access token."""
        if not self.plaid_access_token:
            return None
        key = settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY
        f = Fernet(key)
        return f.decrypt(self.plaid_access_token).decode()

    def __str__(self):
        return f"{self.institution_name or 'Unknown'} - {self.account_type or 'N/A'}"

