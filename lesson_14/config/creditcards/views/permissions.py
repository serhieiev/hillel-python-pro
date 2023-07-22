from rest_framework import permissions


class IsCardOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a card to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the card.
        return obj.owner == request.user
