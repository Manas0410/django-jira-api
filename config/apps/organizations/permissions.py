from rest_framework.permissions import BasePermission

class IsOrgAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.memberships.filter(
            user=request.user,
            role="admin"
        ).exists()