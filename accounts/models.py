from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    MEMBER = 'member'
    ROLE_CHOICES = [(ADMIN, 'Admin'), (MEMBER, 'Member')]

    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ADMIN
        super().save(*args, **kwargs)