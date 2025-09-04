# Importing serializers module from rest_framework
from rest_framework import serializers

# Importing all models from parent directory's models module
from ..models import *

# Importing translation utility from Django
from django.utils.translation import gettext_lazy as _

from authentication.models import User

# Defining UserSerializer class inheriting from serializers.ModelSerializer
class UserSerializer(serializers.ModelSerializer):
    
    # Read-only field for created_at timestamp
    created_at = serializers.ReadOnlyField()
    
    # Read-only field for updated_at timestamp
    updated_at = serializers.ReadOnlyField()

    # Meta class for additional options
    class Meta(object):
        # Specifying the model to be serialized
        model = User
        
        # Defining the fields to be included in the serialization
        fields = (
            'id', 'username', 'email', 'password_hash',
            'full_name', 'permissions', 'status', 'created_at', 'last_login', 'updated_at'
        )
        # Making the password write-only
        extra_kwargs = {'password': {'write_only': True}}

    # Method to create a new user
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# Defining ChangePasswordSerializer class inheriting from serializers.Serializer
class ChangePasswordSerializer(serializers.Serializer):
    
    # CharField for username, required
    username = serializers.CharField(required=True)
    
    # CharField for password, required
    password = serializers.CharField(required=True)
    
    # CharField for confirm password, required
    confirm_password = serializers.CharField(required=True)
