# Import necessary Django REST Framework serializer module
from rest_framework import serializers
# Import path for URL routing (though not used in this snippet)
from django.urls import path
# Import the Organization model from a relative path
from ..models.organization_models import Organization

# Import translation utility for internationalization
from django.utils.translation import gettext_lazy as _

# Serializer class for SpeciesRecord model, used to convert model instances to JSON
class OrganizationSerializer(serializers.ModelSerializer):
    # Read-only fields for tracking creation and update timestamps
    # These fields cannot be modified during serialization
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    
    # Meta class to specify model-specific serializer configuration
    class Meta(object):
        # Specify the model to be serialized
        model = Organization
        # Define which fields should be included in the serialization
        # Comprehensive list covering taxonomic and location-related information
        fields = ('id', 'organization_name', 'organization_type',
            'contact_info', 'address', 'subscription_plan', 'status',
            'end_user_count', 'device_count', 'database_connection_string',
            'database_name', 'created_at', 'updated_at')
