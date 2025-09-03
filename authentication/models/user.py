from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid

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

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model based on the provided database schema
    """
    
    # Primary Key - UUID as shown in the schema
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Unique identifier for the user"
    )

    # CharField for username with maximum length of 30, unique
    username = models.CharField(max_length=30, unique=True)
    
    # Organization relationship
    organization_id = models.UUIDField(
        null=True,
        blank=True,
        help_text="Organization this user belongs to"
    )
    
    # Core authentication field
    email = models.CharField(
        max_length=255,
        unique=True,
        help_text="User's email address (used for login)"
    )
    
    # Password field (Django will handle hashing)
    password_hash = models.CharField(
        max_length=255,
        help_text="Hashed password",
        db_column='password_hash'
    )
    
    # User information
    full_name = models.CharField(
        max_length=255,
        help_text="User's full name"
    )
    
    phone_number = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text="User's phone number"
    )
    
    # User classification
    user_type = models.CharField(
        max_length=50,
        help_text="User's role type (ADMIN, MANAGER, EMPLOYEE, HR, etc.)"
    )
    
    status = models.CharField(
        max_length=50,
        help_text="User's current status (ACTIVE, INACTIVE, SUSPENDED, etc.)"
    )
    
    # JSON fields for flexible data
    subscription_details = models.JSONField(
        default=dict,
        blank=True,
        help_text="User's subscription information"
    )
    
    emergency_contact = models.JSONField(
        default=dict,
        blank=True,
        help_text="Emergency contact information"
    )
    
    # Media field
    profile_image_url = models.TextField(
        null=True,
        blank=True,
        help_text="URL to user's profile image"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp when user was created"
    )
    
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last login timestamp"
    )
    
    # Audit field
    created_by = models.UUIDField(
        null=True,
        blank=True,
        help_text="ID of user who created this account"
    )

    # Django required fields for authentication
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    # Meta class for additional options
    class Meta:
        # Human-readable name for the object in singular form
        verbose_name = _('User')
        # Human-readable name for the object in plural form
        verbose_name_plural = _('Users')
