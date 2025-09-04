from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from nextpro.softDeleteModel import SoftDeletionModel
from organization.models.organization_models import Organization
from organization.models.organization_admin_models import OrganizationAdmin
    
    
class OrganizationSetting(SoftDeletionModel):
    SETTING_CATEGORIES = [
        ('billing', 'Billing'),
        ('service_provider', 'Service Provider'),
        ('notification', 'Notification'),
        ('security', 'Security'),
        ('general', 'General'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    setting_category = models.CharField(max_length=50, choices=SETTING_CATEGORIES)
    setting_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(OrganizationAdmin, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organization_settings'
        unique_together = ['organization', 'setting_category']
        
    def __str__(self):
        return f"{self.organization.organization_name} - {self.setting_category}"