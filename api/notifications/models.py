from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    title = models.CharField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title} - {self.user.username}"
