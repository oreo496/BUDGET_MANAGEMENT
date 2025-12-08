from django.db import models
import uuid
from accounts.models import User


class Goal(models.Model):
    id = models.BinaryField(primary_key=True, max_length=16, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    title = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'goals'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            uuid_obj = uuid.uuid4()
            self.id = uuid_obj.bytes
        super().save(*args, **kwargs)

    def get_uuid_string(self):
        return str(uuid.UUID(bytes=self.id))

    @property
    def progress_percentage(self):
        """Calculate progress percentage."""
        if self.target_amount == 0:
            return 0
        return min(100, (self.current_amount / self.target_amount) * 100)

    def __str__(self):
        return f"{self.title}: ${self.current_amount}/${self.target_amount}"

