from django.db import models
from accounts.models import User


class ChatMessage(models.Model):
    """Store chat message history."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField(help_text="User's message")
    response = models.TextField(help_text="FunderBot's response")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name}: {self.message[:50]}"
