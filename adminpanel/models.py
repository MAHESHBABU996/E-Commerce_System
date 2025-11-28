from django.db import models
from accounts.models import CustomUser

class AdminLog(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.username} - {self.timestamp}"
