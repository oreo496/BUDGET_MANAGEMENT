from django.db import models
import uuid
from accounts.models import User


class Budget(models.Model):
    id = models.BinaryField(primary_key=True, max_length=16, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, 
                                  db_column='category_id')
    period = models.CharField(
        max_length=10,
        choices=[('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly')]
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'budgets'
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gte=0), name='amount_non_negative')
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            uuid_obj = uuid.uuid4()
            self.id = uuid_obj.bytes
        super().save(*args, **kwargs)

    def get_uuid_string(self):
        return str(uuid.UUID(bytes=self.id))

    def __str__(self):
        return f"{self.category.name}: ${self.amount} ({self.period})"

