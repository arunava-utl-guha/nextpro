from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ..models.organization_models import Organization
from ..serializers.organization_serializer import OrganizationSerializer


# ------------------------------
# List Organizations
# ------------------------------
class OrganizationList(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        try:
            organizations = Organization.objects.all().values("id", "name")
            return Response({
                "status": True,
                "data": list(organizations)
            }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                "status": False,
                "message": str(error)
            }, status=status.HTTP_200_OK)


# ------------------------------
# List Organizations (with search, filter, sort, pagination)
# ------------------------------
class OrganizationFilteredList(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        try:
            queryset = Organization.objects.all()

            # -------------------
            # Filters
            # -------------------
            organization_type = request.data.get("organization_type")
            if organization_type:
                queryset = queryset.filter(organization_type=organization_type)

            status_filter = request.data.get("status")
            if status_filter:
                queryset = queryset.filter(status=status_filter)

            # -------------------
            # Field-wise Search
            # -------------------
            search_field = request.data.get("search_field")  # e.g. "organization_name"
            search_value = request.data.get("search_value", "").strip()

            if search_field and search_value:
                # allow only valid fields
                valid_search_fields = [
                    "organization_name", "organization_type",
                    "status", "subscription_plan"
                ]
                if search_field in valid_search_fields:
                    filter_kwargs = {f"{search_field}__icontains": search_value}
                    queryset = queryset.filter(**filter_kwargs)

            # -------------------
            # Sorting (asc/desc)
            # -------------------
            sort_field = request.data.get("sort_field", "created_at")  # default created_at
            sort_order = request.data.get("sort_order", "desc")  # asc / desc

            valid_sort_fields = [
                "organization_name", "organization_type", "status",
                "subscription_plan", "end_user_count", "device_count",
                "created_at", "updated_at"
            ]

            if sort_field in valid_sort_fields:
                if sort_order == "asc":
                    queryset = queryset.order_by(sort_field)
                else:
                    queryset = queryset.order_by(f"-{sort_field}")
            else:
                queryset = queryset.order_by("-created_at")

            # -------------------
            # Pagination
            # -------------------
            page_size = min(int(request.data.get("page_size", 10)), 100)
            page = request.data.get("page", 1)
            paginator = Paginator(queryset, page_size)

            try:
                organizations = paginator.page(page)
            except PageNotAnInteger:
                organizations = paginator.page(1)
            except EmptyPage:
                organizations = paginator.page(paginator.num_pages)

            serializer = OrganizationSerializer(organizations, many=True)

            return Response({
                "status": True,
                "message": "Organizations retrieved successfully",
                "records": serializer.data,
                "pagination": {
                    "current_page": organizations.number,
                    "total_pages": paginator.num_pages,
                    "total_count": paginator.count,
                }
            }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                "status": False,
                "message": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# ------------------------------
# Create Organization
# ------------------------------
class OrganizationCreate(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request):
        try:
            serializer = OrganizationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": True,
                    "message": "Organization created successfully",
                    "record": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                "status": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({
                "status": False,
                "message": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------------
# Organization Detail (Retrieve)
# ------------------------------
class OrganizationDetail(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        try:
            org_id = request.data.get("id")
            organization = get_object_or_404(Organization, pk=org_id)
            serializer = OrganizationSerializer(organization)
            return Response({
                "status": True,
                "message": "Organization retrieved successfully",
                "record": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({
                "status": False,
                "message": str(error)
            }, status=status.HTTP_404_NOT_FOUND)


# ------------------------------
# Update Organization
# ------------------------------
class OrganizationUpdate(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        try:
            org_id = request.data.get("id")
            organization = get_object_or_404(Organization, pk=org_id)
            serializer = OrganizationSerializer(organization, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": True,
                    "message": "Organization updated successfully",
                    "record": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "status": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({
                "status": False,
                "message": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------------
# Update Organization Status
# ------------------------------
class OrganizationStatusUpdate(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        try:
            org_id = request.data.get("id")
            new_status = request.data.get("status")

            organization = get_object_or_404(Organization, pk=org_id)

            valid_statuses = [choice[0] for choice in Organization.STATUS_CHOICES]
            if new_status not in valid_statuses:
                return Response({
                    "status": False,
                    "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            old_status = organization.status
            organization.status = new_status
            organization.save(update_fields=["status", "updated_at"])

            return Response({
                "status": True,
                "message": f'Status changed from "{old_status}" to "{new_status}"'
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({
                "status": False,
                "message": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------------
# Soft Delete Organization
# ------------------------------
class OrganizationDelete(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request):
        try:
            org_id = request.data.get("id")
            org_count = Organization.objects.filter(id=org_id).count()

            if org_count != 0:
                org = Organization.objects.filter(id=org_id).soft_delete()
                if org is not None:
                    return Response({
                        "status": True,
                        "message": "Organization deleted successfully"
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "message": "Organization not found"
                }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                "status": False,
                "message": str(error)
            }, status=status.HTTP_200_OK)


# ------------------------------
# Restore Organization
# ------------------------------
class OrganizationRestore(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request):
        try:
            org_id = request.data.get("id")
            org_count = Organization.all_objects.filter(id=org_id).count()

            if org_count != 0:
                org = Organization.all_objects.filter(id=org_id).restore()
                if org is not None:
                    return Response({
                        "status": True,
                        "message": "Organization restored successfully"
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "message": "Organization not found"
                }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                "status": False,
                "message": str(error)
            }, status=status.HTTP_200_OK)


# ------------------------------
# Hard Delete Organization
# ------------------------------
class OrganizationHardDelete(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request):
        try:
            org_id = request.data.get("id")
            org_count = Organization.all_objects.filter(id=org_id).count()

            if org_count != 0:
                org = Organization.all_objects.filter(id=org_id).hard_delete()
                if org is not None:
                    return Response({
                        "status": True,
                        "message": "Organization deleted permanently"
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "message": "Organization not found"
                }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                "status": False,
                "message": str(error)
            }, status=status.HTTP_200_OK)
