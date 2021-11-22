from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Add additional fields to the standard user model provided by django
    to track the time of the last login and activities"""
    last_login = models.DateTimeField(null=True)
    last_activity = models.DateTimeField(null=True)
