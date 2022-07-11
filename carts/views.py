from rest_framework.permissions import IsAuthenticated
from carts.models import Cart, CartItem
from rest_framework import viewsets, mixins
from rest_framework.viewsets import ModelViewSet
from django.db.models import Sum, F
from rest_framework.response import Response
from items.models import Item
from .serializers import CartsSerializer, CartTotalSerializer, CartItemSerializer


class CartsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartTotalSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['total_cost'] = CartItem.objects.filter(
            cart__users=self.request.user
        ).annotate(total_price=Sum(F('quantity') * F('price'))).aggregate(total_cost=Sum('total_price'))['total_cost']
        return context


class CartItemModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CartItem.objects.filter(cart__users=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemSerializer
        return CartsSerializer

    # def update(self, request, *args, **kwargs):
    #     kwargs['pk'] айдишник CartItem

    #     instance = CartItem.objects.get(
    #         cart__user=request.user,
    #         item=Item.objects.get(pk=request.data['item'])
    #     )
    #     print(instance)
    #     data = {'quantity': request.data['quantity']}
    #     serializer = self.get_serializer_class()(instance, data=data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
