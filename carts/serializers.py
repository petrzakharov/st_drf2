from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from carts.models import Cart, CartItem
from items.serializers import ItemSerializer


class CartsSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    item_id = serializers.CharField(source='item.id')

    class Meta:
        model = CartItem
        fields = ('id', 'item', 'item_id', 'quantity', 'price', 'total_price')


class CartTotalSerializer(serializers.ModelSerializer):
    items = CartsSerializer(source='cart_items', many=True, read_only=True)
    total_cost = SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_cost',)

    @staticmethod
    def get_total_cost(obj):
        return obj.total_cost()


class CartItemSerializer(serializers.ModelSerializer):
    total_price = SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'item', 'quantity', 'price', 'total_price',)
        read_only_fields = ('cart', 'price',)

    def create(self, validated_data):
        request = self.context.get('request')
        item = validated_data['item']
        try:
            cart = Cart.objects.get(
                users=request.user,
                order=None
            )
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                users=request.user
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

    def update(self, instance, validated_data):
        instance.price = instance.item.price
        instance.quantity = validated_data['quantity']
        instance.save()
        return instance

    @staticmethod
    def get_total_price(obj):
        return obj.total_price()
