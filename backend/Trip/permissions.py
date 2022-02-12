"""
Object level permission control:
Only logged in user can edit their own profile
"""
from .models import Itinerary
from rest_framework import permissions
from django.http import Http404


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
        return request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Nobody except
    User and Admin can view/update
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the User itself
        return obj.user == request.user or request.user.is_staff


class IsTripEventOwnerOrAdminUpdate(permissions.BasePermission):
    """
    Nobody except
    User and Admin can create
    This is different from IsOwnerOrAdmin by that it checks for the owner of the Itinerary
        that this trip event belongs to (because trip event don't have owner)
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the User itself or Admin
        itin = Itinerary.objects.get(id=obj.itin.id)
        print(f"=> UPDATE <== ITIN USER: {itin.user}, CURR USER: {request.user}, IS-STAFF: {request.user.is_staff}")

        return itin.user == request.user or request.user.is_staff


class IsTripEventOwnerOrAdminCreate(permissions.BasePermission):
    """
    Nobody except
    User and Admin can view/update
    This is different from IsOwnerOrAdmin by that it checks for the owner of the Itinerary
        that this trip event belongs to (because trip event don't have owner)
    """

    def has_permission(self, request, view):
        # Check if Itinerary to be created is belonged to this user or not
        try:
            itin = Itinerary.objects.get(id=request.data['itin'])
        except:
            raise Http404
        print(f"=> CREATE <= ITIN USER: {itin.user}, CURR USER: {request.user}, IS-STAFF: {request.user.is_staff}")

        return itin.user == request.user or request.user.is_staff
