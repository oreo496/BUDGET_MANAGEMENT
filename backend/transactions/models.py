from django.db import models
import uuid
from accounts.models import User


class Transaction(models.Model):
    id = models.BinaryField(primary_key=True, max_length=16, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL, 
                                 null=True, blank=True, db_column='category_id')
    bank_account = models.ForeignKey('bank_accounts.BankAccount', on_delete=models.SET_NULL,
                                     null=True, blank=True, db_column='bank_account_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=10,
        choices=[('INCOME', 'Income'), ('EXPENSE', 'Expense')]
    )
    merchant = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    source = models.CharField(
        max_length=10,
        choices=[('MANUAL', 'Manual'), ('SYNCED', 'Synced')],
        default='MANUAL'
    )
    flagged_fraud = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            uuid_obj = uuid.uuid4()
            self.id = uuid_obj.bytes
        super().save(*args, **kwargs)

    def get_uuid_string(self):
        return str(uuid.UUID(bytes=self.id))

    def __str__(self):
        return f"{self.type}: ${self.amount} - {self.merchant or 'N/A'}"

