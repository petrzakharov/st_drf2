import django_filters

from .models import Item


class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = {
            'price': ['lt', 'lte', 'gt', 'gte'],
            'weight': ['lt', 'lte', 'gt', 'gte']
        }
