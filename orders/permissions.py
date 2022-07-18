from rest_framework import permissions


class OnlyAuthorCanEditObject(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT'):
            if obj.status == 'cr':
                return obj.recipient == request.user
            return False
        return obj.recipient == request.user
