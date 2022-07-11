from rest_framework import serializers
from carts.models import CartItem, Cart
from rest_framework.fields import SerializerMethodField

from items.models import Item
from items.serializers import ItemSerializer
from django.shortcuts import get_object_or_404


class CartsSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    item_id = serializers.CharField(source='item.id')

    class Meta:
        model = CartItem
        fields = ('id', 'item', 'item_id', 'quantity', 'price', 'total_price')
        # read_only_fields = ('item', 'price', 'total_price',)


class CartTotalSerializer(serializers.ModelSerializer):
    items = CartsSerializer(source='cart_items', many=True, read_only=True)
    total_cost = SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('items', 'total_cost',)

    def get_total_cost(self, obj):
        return self.context['total_cost']


class CartItemSerializer(serializers.ModelSerializer):
    total_price = SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'item', 'quantity', 'price', 'total_price',)
        read_only_fields = ('cart', 'price',)

    def create(self, validated_data):
        request = self.context.get('request')
        item = validated_data['item']
        cart, _ = Cart.objects.get_or_create(
            users=request.user,
        )
        cart_item, _ = CartItem.objects.update_or_create(
            cart=cart,
            item=item,
            defaults={
                'quantity': validated_data['quantity'],
                'price': item.price
            },
        )
        return cart_item

    def get_total_price(self, obj):
        return obj.price * obj.quantity