from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    )

    telephone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    is_approved = models.BooleanField(default=False)

    full_name = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    bank_name = models.CharField(max_length=255, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.username

# Create your models here.
