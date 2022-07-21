import logging

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from carts.models import Cart, CartItem
from .permissions import OnlyCartWithoutOrderIsEditable
from .serializers import (
    CartItemSerializer, CartsSerializer, CartTotalSerializer,
)


class CartsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartTotalSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_authenticated:  # swagger
            return Cart.objects.filter(users=self.request.user).prefetch_related('items')


class CartItemModelViewSet(ModelViewSet):
    permission_classes = (OnlyCartWithoutOrderIsEditable,)
    queryset = CartItem.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:  # swagger
            return CartItem.objects.filter(cart__users=self.request.user).select_related('item')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CartItemSerializer
        return CartsSerializer
