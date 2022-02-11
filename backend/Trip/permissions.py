"""
Object level permission control:
Only logged in user can edit their own profile
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Anybody can view (SAFE_METHODS: GET, HEAD, OPTION)
    User and Admin can view/update
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the User itself
        print("Permission Check: ", obj.user == request.user)
        print("Admin Check: ", request.user.is_staff)
        return obj.user == request.user

class IsAdmin(permissions.BasePermission):
    """
    Admin can view/update
    """

    def has_permission(self, request, view):
        # ONLY admin will have the permission to view/update
        print(request.user)
        return request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Nobody except
    User and Admin can view/update
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the User itself
        return obj.user == request.user or request.user.is_staff
