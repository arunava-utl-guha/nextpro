from django.urls import path
from .views.device_views import *

urlpatterns = [
    # Device CRUD operations
    path('add/', AddDeviceView.as_view(), name='add_device'),
    path('list/', DeviceListView.as_view(), name='device_list'),
    
    # Device status operations
    path('change-status/<uuid:device_id>', DeviceSetStatusView.as_view(), name='toggle_device_status'),
]