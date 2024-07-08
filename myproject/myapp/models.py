from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)


class Message(models.Model):
    user = models.ForeignKey('myapp.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
