from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from nextpro.softDeleteModel import SoftDeletionModel
from organization.models.organization_models import Organization

class DeviceInventory(SoftDeletionModel):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('faulty', 'Faulty'),
        ('maintenance', 'Maintenance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_mac_id = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=100)
    qr_code = models.CharField(max_length=255, unique=True, null=True, blank=True)
    serial_number = models.CharField(max_length=255, unique=True, null=True, blank=True)
    firmware_version = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_at = models.DateTimeField(null=True, blank=True)
    last_health_check = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'device_inventory'
        
    def __str__(self):
        return f"{self.device_type} - {self.device_mac_id}"