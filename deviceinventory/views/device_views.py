from rest_framework import status  # REST framework HTTP status codes
from rest_framework.views import APIView  # Base class for API views
from rest_framework.response import Response  # Standardized API response
from rest_framework.permissions import IsAuthenticated, AllowAny  # Permission classes for view access
from django.core.paginator import Paginator  # Django's pagination utility
from django.db.models import Q  # Complex database query lookups
from django.db import IntegrityError  # Database integrity error handling
from ..models.device_inventory_models import *  # Device inventory model
from ..serializers.device_inventory_serializer import *  # Device serializer


class AddDeviceView(APIView):
    """
    API view to add new devices to inventory without serializers
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Create a new device in inventory
        """
        try:
            # Extract data from request
            device_mac_id = request.data.get('device_mac_id', '').strip()
            device_type = request.data.get('device_type', '').strip()
            serial_number = request.data.get('serial_number', '').strip()
            qr_code = request.data.get('qr_code', '').strip()
            firmware_version = request.data.get('firmware_version', '').strip()
            device_status = request.data.get('status', 'available').strip()
            organization_id = request.data.get('organization')

            # Manual validation
            errors = {}
            
            # Validate required fields
            if not device_mac_id:
                errors['device_mac_id'] = ['This field is required.']
            
            if not device_type:
                errors['device_type'] = ['This field is required.']

            # Check for duplicates
            if device_mac_id and DeviceInventory.objects.filter(device_mac_id=device_mac_id).exists():
                errors['device_mac_id'] = ['Device with this MAC address already exists.']
            
            if serial_number and DeviceInventory.objects.filter(serial_number=serial_number).exists():
                errors['serial_number'] = ['Device with this serial number already exists.']
            
            if qr_code and DeviceInventory.objects.filter(qr_code=qr_code).exists():
                errors['qr_code'] = ['Device with this QR code already exists.']

            # Validate organization if provided
            # organization = None
            # if organization_id:
            #     try:
            #         organization = Organization.objects.get(id=organization_id)
            #     except Organization.DoesNotExist:
            #         errors['organization'] = ['Invalid organization ID.']

            # Return validation errors if any
            if errors:
                return Response({
                    'status': False,
                    'message': 'Validation failed',
                    'errors': errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create device manually
            device_data = {
                'device_mac_id': device_mac_id.upper(),  # Normalize MAC address
                'device_type': device_type,
                'status': device_status,
                
            }

            # Add optional fields if provided
            if serial_number:
                device_data['serial_number'] = serial_number
            if qr_code:
                device_data['qr_code'] = qr_code
            if firmware_version:
                device_data['firmware_version'] = firmware_version
            # if organization:
            #     device_data['organization'] = organization

            # Create the device
            device = DeviceInventory.objects.create(**device_data)

            # Format response manually
            response_data = {
                'id': str(device.id),
                'device_mac_id': device.device_mac_id,
                'device_type': device.device_type,
                'qr_code': device.qr_code,
                'serial_number': device.serial_number,
                'firmware_version': device.firmware_version,
                'status': device.status,
                'organization': str(device.organization.id) if device.organization else None,
                'organization_name': device.organization.name if device.organization else 'UNASSIGNED',
                'created_at': device.created_at.isoformat(),
                'updated_at': device.updated_at.isoformat(),
                'assigned_at': device.assigned_at.isoformat() if device.assigned_at else None,
                'last_health_check': device.last_health_check.isoformat() if device.last_health_check else None
            }

            return Response({
                'status': True,
                'message': 'Device added successfully',
                'records': response_data
            }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({
                'status': False,
                'message': 'Device with this information already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({
                'status': False,
                'message': f'Error adding device: {str(error)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class DeviceListView(APIView):
    """
    API view to list all devices in inventory with pagination, sorting, and search using POST method
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Retrieve devices from inventory with pagination, sorting, and search
        """
        try:
            # Get parameters from request body instead of URL
            page = int(request.data.get('page', 1))
            page_size = int(request.data.get('page_size', 10))
            search = str(request.data.get('search', '')).strip()
            sort_by = str(request.data.get('sort_by', 'created_at'))  # mac, owner, created_time
            order = str(request.data.get('order', 'desc'))  # asc, desc
            
            # Ensure valid values
            page = max(1, page)
            page_size = min(max(1, page_size), 100)  # Limit between 1-100
            
            # Start with all devices
            devices = DeviceInventory.objects.select_related('organization').all()
            
            # Apply search filters
            if search:
                devices = devices.filter(
                    Q(device_mac_id__icontains=search) |  # Search by MAC
                    Q(organization__organization_name__icontains=search)  # Search by Owner/Organization
                )
            
            # Apply sorting - inline sort field mapping
            sort_mapping = {
                'mac': 'device_mac_id',
                'owner': 'organization__organization_name',
                'created_time': 'created_at',
                'device_type': 'device_type',
                'status': 'status'
            }
            sort_field = sort_mapping.get(sort_by, 'created_at')
            
            if order == 'desc':
                sort_field = f'-{sort_field}'
            
            devices = devices.order_by(sort_field)
            
            # Get total count before pagination
            total_count = devices.count()
            
            # Apply pagination
            paginator = Paginator(devices, page_size)
            
            # Validate page number
            if page > paginator.num_pages and paginator.num_pages > 0:
                page = paginator.num_pages
            if page < 1:
                page = 1
                
            devices_page = paginator.get_page(page)
            
            # Check if devices exist
            if total_count > 0:
                # Format devices data manually (no serializer)
                devices_data = []
                for device in devices_page:
                    device_data = {
                        'id': str(device.id),
                        'device_mac_id': device.device_mac_id,
                        'device_type': device.device_type,
                        'qr_code': device.qr_code,
                        'serial_number': device.serial_number,
                        'firmware_version': device.firmware_version,
                        'status': device.status,
                        'organization': str(device.organization.id) if device.organization else None,
                        'organization_name': device.organization.name if device.organization else 'UNASSIGNED',
                        'created_at': device.created_at.isoformat(),
                        'updated_at': device.updated_at.isoformat(),
                        'assigned_at': device.assigned_at.isoformat() if device.assigned_at else None,
                        'last_health_check': device.last_health_check.isoformat() if device.last_health_check else None
                    }
                    devices_data.append(device_data)
                
                return Response({
                    'status': True,
                    'devices': devices_data,
                    'records': {
                        'current_page': page,
                        'page_size': page_size,
                        'total_pages': paginator.num_pages,
                        'total_count': total_count,
                        'has_next': devices_page.has_next(),
                        'has_previous': devices_page.has_previous(),
                        'next_page': devices_page.next_page_number() if devices_page.has_next() else None,
                        'previous_page': devices_page.previous_page_number() if devices_page.has_previous() else None
                    },
                    'filters': {
                        'search': search,
                        'sort_by': sort_by,
                        'order': order
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': False,
                    'message': 'No devices found',
                    'records': {
                        'current_page': 1,
                        'page_size': page_size,
                        'total_pages': 0,
                        'total_count': 0,
                        'has_next': False,
                        'has_previous': False,
                        'next_page': None,
                        'previous_page': None
                    }
                }, status=status.HTTP_404_NOT_FOUND)

        except ValueError as error:
            return Response({
                'status': False,
                'message': 'Invalid page or page_size parameter'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)


class DeviceSetStatusView(APIView):
    """
    API view to set device to specific status (active/inactive)
    """
    permission_classes = (AllowAny,)

    def post(self, request, device_id):
        """
        Set device to specific status
        """
        try:
            device = DeviceInventory.objects.get(id=device_id)
            
            # Get desired status from request
            desired_status = request.data.get('status', '').lower().strip()
            
            if desired_status not in ['active', 'inactive']:
                return Response({
                    'status': False,
                    'message': 'Invalid status. Must be "active" or "inactive".'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if status is already set
            if device.status == desired_status:
                return Response({
                    'status': False,
                    'message': f'Device is already {desired_status}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set the status
            device.status = desired_status
            device.save()
            
            status_text = 'activated' if desired_status == 'active' else 'deactivated'
            
            return Response({
                'status': True,
                'message': f'Device {status_text} successfully',
                'device': {
                    'id': str(device.id),
                    'device_mac_id': device.device_mac_id,
                    'device_type': device.device_type,
                    'status': device.status,
                    'updated_at': device.updated_at.isoformat()
                }
            }, status=status.HTTP_200_OK)
            
        except DeviceInventory.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Device not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as error:
            return Response({
                'status': False,
                'message': f'Error setting device status: {str(error)}'
            }, status=status.HTTP_400_BAD_REQUEST)