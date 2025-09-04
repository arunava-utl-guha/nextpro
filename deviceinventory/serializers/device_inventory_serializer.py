# Import necessary Django REST Framework serializer module
from rest_framework import serializers
# Import path for URL routing (though not used in this snippet)
from django.urls import path
# Import the Organization model from a relative path
from ..models.device_inventory_models import DeviceInventory

# Import translation utility for internationalization
from django.utils.translation import gettext_lazy as _

# Serializer class for SpeciesRecord model, used to convert model instances to JSON
class DeviceInventorySerializer(serializers.ModelSerializer):
    # Read-only fields for tracking creation and update timestamps
    # These fields cannot be modified during serialization
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    
    # Meta class to specify model-specific serializer configuration
    class Meta(object):
        # Specify the model to be serialized
        model = DeviceInventory
        # Define which fields should be included in the serialization
        # Comprehensive list covering taxonomic and location-related information
        fields = ('id', 'device_mac_id', 'device_type', 'qr_code',
            'serial_number', 'firmware_version', 'status', 'organization',
            'organization_name', 'created_at', 'assigned_at', 'last_health_check')
