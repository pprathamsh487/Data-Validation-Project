from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    You can add extra fields here, e.g., mobile, company, etc.
    """
    mobile = models.CharField(max_length=15, blank=True, null=True)
    # Add more fields as needed

    def __str__(self):
        return self.username
    class Meta:
        db_table = "USERS"

