from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow reading to every users but
    allow writing only to admin users.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.is_admin:
            return True
        else:
            return False


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)