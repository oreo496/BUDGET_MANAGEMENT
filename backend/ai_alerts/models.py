from django.db import models
import uuid
from accounts.models import User


class AIAlert(models.Model):
    id = models.BinaryField(primary_key=True, max_length=16, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    message = models.TextField()
    type = models.CharField(
        max_length=30,
        choices=[
            ('BUDGET_ALERT', 'Budget Alert'),
            ('SPENDING_PATTERN', 'Spending Pattern'),
            ('FRAUD', 'Fraud'),
            ('GOAL_RECOMMENDATION', 'Goal Recommendation'),
            ('LOAN_REMINDER', 'Loan Reminder'),
            ('GOAL_RISK', 'Goal Risk')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_alerts'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            uuid_obj = uuid.uuid4()
            self.id = uuid_obj.bytes
        super().save(*args, **kwargs)

    def get_uuid_string(self):
        return str(uuid.UUID(bytes=self.id))

    def __str__(self):
        return f"{self.type}: {self.message[:50]}"

