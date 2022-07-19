from rest_framework import permissions

from carts.models import Cart


class OnlyCartWithoutOrderIsEditable(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT', 'DELETE'):
            if Cart.objects.filter(cart_items=obj, order=None, users=request.user):
                return obj.cart.users == request.user
            return False
        return obj.cart.users == request.user
