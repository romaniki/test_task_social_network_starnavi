from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    last_login = models.DateTimeField(null=True)
    last_activity = models.DateTimeField(null=True)
