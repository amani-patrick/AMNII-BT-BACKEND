from django.db import models
from django.contrib.auth.models import User

class Strategy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='strategies')
    name = models.CharField(max_length=100)
    description = models.TextField()
    parameters = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
