from django.contrib import admin

# Register your models here.
from .models.organization_models import Organization

from models.organization_admin_models import OrganizationAdmin

from .models.organization_settings_models import OrganizationSetting


admin.site.register(Organization)
admin.site.register(OrganizationAdmin)
admin.site.register(OrganizationSetting)