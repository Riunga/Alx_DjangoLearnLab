from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit or delete objects.
    Non-admin users can only read the data.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS (read-only)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff



