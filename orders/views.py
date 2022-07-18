from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from orders.models import Order
from orders.permissions import OnlyAuthorCanEditObject
from orders.serializers import OrderSerializer, OrderDetailSerializer


class OrderViewSet(ModelViewSet):
    http_method_names = ('get', 'put', 'patch', 'post')
    permission_classes = (OnlyAuthorCanEditObject,)

    def get_queryset(self):
        return Order.objects.filter(recipient=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return OrderSerializer
        return OrderDetailSerializer
