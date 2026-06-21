from django.db import models


class ChatLog(models.Model):
    user_message = models.TextField()
    answer = models.TextField()
    retrieved_sources = models.JSONField(default=list)
    handoff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_message[:80]