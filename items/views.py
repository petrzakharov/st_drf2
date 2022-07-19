from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from .filters import ItemFilter
from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering = ['title']
    filterset_class = ItemFilter
    permission_classes = (AllowAny,)
