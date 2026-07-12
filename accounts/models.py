from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Utente'),
        ('coach', 'Coach'),
    )
    role = models.CharField(max_length = 10, choices = ROLE_CHOICES, default = 'user')
    bio = models.TextField(blank = True)
    birth_date = models.DateField(null = True, blank = True)

    groups = models.ManyToManyField (
        'auth.Group',
        related_name = 'customuser_set',
        blank = True
    )
    user_permissions = models.ManyToManyField (
        'auth.Permission',
        related_name = 'customuser_set',
        blank = True
    )

    def __str__(self):
        return self.username