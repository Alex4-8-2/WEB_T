# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    failed_login_attempts = models.IntegerField(default=0)
    lock_until = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    # audit fields already in AbstractUser (last_login, date_joined)

    def is_locked(self):
        if self.lock_until and self.lock_until > timezone.now():
            return True
        return False
