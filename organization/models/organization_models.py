from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from nextpro.softDeleteModel import SoftDeletionModel

class Organization(SoftDeletionModel):
    ORGANIZATION_TYPES = [
        ('gym', 'Gym'),
        ('business', 'Business'),
        ('standalone', 'Standalone'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('inactive', 'Inactive'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_name = models.CharField(max_length=255)
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPES)
    contact_info = models.JSONField(null=True, blank=True)
    address = models.JSONField(null=True, blank=True)
    subscription_plan = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    end_user_count = models.IntegerField(default=0)
    device_count = models.IntegerField(default=0)
    database_connection_string = models.TextField(null=True, blank=True)
    database_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organizations'
        
    def __str__(self):
        return self.organization_name