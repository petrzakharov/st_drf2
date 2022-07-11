from rest_framework import serializers
from .models import Item
from carts.models import CartItem, Cart
from rest_framework.fields import SerializerMethodField
from django.db.models import Sum, F


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'title', 'description', 'image', 'weight', 'price')
