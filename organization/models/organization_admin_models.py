from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from nextpro.softDeleteModel import SoftDeletionModel
from organization.models.organization_models import Organization
    
class OrganizationAdmin(SoftDeletionModel):
    ADMIN_TYPES = [
        ('gym_portal', 'Gym Portal'),
        ('business_manager', 'Business Manager'),
        ('standalone', 'Standalone'),
    ]
    
    ADMIN_LEVELS = [
        ('property_manager', 'Property Manager'),
        ('sub_account', 'Sub Account'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
        ('deactivated', 'Deactivated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    admin_type = models.CharField(max_length=50, choices=ADMIN_TYPES)
    admin_level = models.CharField(max_length=20, choices=ADMIN_LEVELS, default='property_manager')
    parent_admin = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    permissions = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'organization_admins'
        unique_together = ['organization', 'email']
        
    def __str__(self):
        return f"{self.username} - {self.organization.organization_name}"
    
