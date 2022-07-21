from rest_framework.viewsets import ModelViewSet

from orders.models import Order
from orders.permissions import OnlyAuthorCanEditObject
from orders.serializers import OrderDetailSerializer, OrderSerializer


class OrderViewSet(ModelViewSet):
    http_method_names = ('get', 'put', 'patch', 'post')
    permission_classes = (OnlyAuthorCanEditObject,)

    def get_queryset(self):
        return Order.objects.filter(recipient=self.request.user).prefetch_related('cart__cart_items__item')

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return OrderSerializer
        return OrderDetailSerializer

    def get_throttles(self):
        if self.action == 'create':
            self.throttle_scope = 'create_order'
        return super().get_throttles()
