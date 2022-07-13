from django.db.models import F, Sum
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from carts.models import Cart, CartItem

from .serializers import (CartItemSerializer, CartsSerializer,
                          CartTotalSerializer)


class CartsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartTotalSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:  # swagger
            context['total_cost'] = CartItem.objects.filter(
                cart__users=self.request.user
            ).annotate(
                total_price=Sum(F('quantity') * F('price'))
            ).aggregate(total_cost=Sum('total_price'))['total_cost']
            return context


class CartItemModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:  # swagger
            return CartItem.objects.filter(cart__users=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CartItemSerializer
        return CartsSerializer
