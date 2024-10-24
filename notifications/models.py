from django.db import models


class Notifications(models.Model):
    active = models.BooleanField(default=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from admin to all at {self.timestamp}"
