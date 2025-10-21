from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    # Allows access to users with role 'admin' or Django is_staff
    def has_permission(self, request, view):
        u = request.user
        if not u or not u.is_authenticated:
            return False
        return getattr(u, "role", None) == "admin" or getattr(u, "is_staff", False)
