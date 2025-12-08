from django.db import models
import uuid
from accounts.models import Admin, User
from transactions.models import Transaction


class SystemLog(models.Model):
    id = models.BinaryField(primary_key=True, max_length=16, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                            db_column='user_id')
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True,
                             db_column='admin_id')
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'system_logs'
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if not self.id:
            uuid_obj = uuid.uuid4()
            self.id = uuid_obj.bytes
        super().save(*args, **kwargs)

    def get_uuid_string(self):
        return str(uuid.UUID(bytes=self.id))

    def __str__(self):
        return f"{self.action} - {self.timestamp}"


class AdminAction(models.Model):
    id = models.BinaryField(primary_key=True, max_length=16, editable=False)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, db_column='admin_id')
    action = models.CharField(max_length=255)
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    db_column='target_user_id')
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True,
                                   db_column='transaction_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_actions'
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if not self.id:
            uuid_obj = uuid.uuid4()
            self.id = uuid_obj.bytes
        super().save(*args, **kwargs)

    def get_uuid_string(self):
        return str(uuid.UUID(bytes=self.id))

    def __str__(self):
        return f"{self.admin.email}: {self.action}"
