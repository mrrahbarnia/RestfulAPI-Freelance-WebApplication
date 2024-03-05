from rest_framework import permissions
# from portfolio.models import Portfolio


class IsOwnerOrReadOnly(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.profile.user == request.user
