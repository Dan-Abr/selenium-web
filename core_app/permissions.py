# third-party
from rest_framework import permissions


class IsUser(permissions.IsAuthenticated):
    """ Custom permission class to allow only the logged-in user to access the view.
    """
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and obj.user == request.user