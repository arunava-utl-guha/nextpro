# Import necessary Django REST Framework serializer module
from rest_framework import serializers
# Import path for URL routing (though not used in this snippet)
from django.urls import path
# Import the Organization model from a relative path
from ..models.organization_admin_models import OrganizationAdmin

# Import translation utility for internationalization
from django.utils.translation import gettext_lazy as _

# Serializer class for SpeciesRecord model, used to convert model instances to JSON
class OrganizationAdminSerializer(serializers.ModelSerializer):
    # Read-only fields for tracking creation and update timestamps
    # These fields cannot be modified during serialization
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    
    # Meta class to specify model-specific serializer configuration
    class Meta(object):
        # Specify the model to be serialized
        model = OrganizationAdmin
        # Define which fields should be included in the serialization
        # Comprehensive list covering taxonomic and location-related information
        fields = ('id', 'organization', 'organization_name', 'username',
            'email', 'password_hash', 'full_name', 'admin_type', 'admin_level',
            'parent_admin', 'parent_admin_name', 'permissions', 'status',
            'created_at', 'updated_at', 'last_login')
        # Making the password write-only
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }
