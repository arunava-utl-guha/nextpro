from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from nextpro.softDeleteModel import SoftDeletionModel
    
class FirmwareVersion(SoftDeletionModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deprecated', 'Deprecated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    version_log = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'firmware_versions'
        unique_together = ['version', 'model']
        
    def __str__(self):
        return f"{self.model} v{self.version}"
    
