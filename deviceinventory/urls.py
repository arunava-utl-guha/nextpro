from django.urls import path
from .views.device_views import *

urlpatterns = [
    # Device CRUD operations
    path('add/', AddDeviceView.as_view(), name='add_device'),
    path('list/', DeviceListView.as_view(), name='device_list'),
    path('bulk-upload-csv/', BulkDeviceCSVUploadView.as_view(), name='bulk_device_csv_upload'),
    # Device status operations
    path('change-status/<uuid:device_id>', DeviceSetStatusView.as_view(), name='toggle_device_status'),
]