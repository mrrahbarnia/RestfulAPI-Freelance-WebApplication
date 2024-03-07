from rest_framework import permissions
# from portfolio.models import Portfolio


class IsOwnerOrReadOnly(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.profile.user == request.user


class IsOwner(permissions.BasePermission):
    """
    This custom permission set for deleting
    portfolio's comments only by their owners.
    """
    def has_object_permission(self, request, view, obj):

        return obj.user == request.user