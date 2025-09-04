from django.urls import path
from .views.organization_views import *


urlpatterns = [
    # List APIs
    path("list/", OrganizationList.as_view(), name="organization-list"),
    path("filter/list/", OrganizationFilteredList.as_view(), name="organization-filtered-list"),

    # CRUD APIs
    path("create/", OrganizationCreate.as_view(), name="organization-create"),
    path("detail/", OrganizationDetail.as_view(), name="organization-detail"),
    path("update/", OrganizationUpdate.as_view(), name="organization-update"),

    # Status update
    path("status/update/", OrganizationStatusUpdate.as_view(), name="organization-status-update"),

    # Delete / Restore APIs
    path("delete/", OrganizationDelete.as_view(), name="organization-delete"),
    path("restore/", OrganizationRestore.as_view(), name="organization-restore"),
    path("hard-delete/", OrganizationHardDelete.as_view(), name="organization-hard-delete"),
]
