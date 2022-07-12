from .filters import ItemFilter
from .models import Item
from carts.models import Cart, CartItem
from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ItemSerializer
from django.db.models import Sum, F


class ItemViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering = ['title']
    filterset_class = ItemFilter
