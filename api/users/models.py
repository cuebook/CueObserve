from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime
from .managers import CustomUserManager
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def convertToLowerCase(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).convertToLowerCase(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = LowercaseEmailField(_("email address"), unique=True)
    name = models.CharField(max_length=200, null=False, default="User")
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default="Inactive")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email
