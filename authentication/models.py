from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from nextpro.softDeleteModel import SoftDeletionModel

class UserManager(BaseUserManager):
    
    
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a new user with the given email and password.
        """
        # Raise an error if the username is not provided
        if not username:
            raise ValueError(_('The username field must be set.'))
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.
        """

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin,SoftDeletionModel):
    """
    Custom User model based on the provided database schema
    """
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    permissions = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # Linking the UserManager to the User model
    objects = UserManager()
    
    # Defining the field that will be used for logging in
    USERNAME_FIELD = 'username'
    
    # Defining additional required fields
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    # Meta class for additional options
    class Meta:
        # Human-readable name for the object in singular form
        verbose_name = _('User')
        # Human-readable name for the object in plural form
        verbose_name_plural = _('Users')
