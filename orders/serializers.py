import datetime

from rest_framework import serializers

from carts.models import Cart
from carts.serializers import CartTotalSerializer
from orders.models import Order


class ValidationForOrderSerializer:
    @staticmethod
    def validate_delivery_at(value):
        if value.timestamp() < (datetime.datetime.now() + datetime.timedelta(days=1)).timestamp():
            raise serializers.ValidationError('Дата доставки должна быть больше, чем дата + 24 часа')
        return value

    @staticmethod
    def validate_status(value):
        if value != 'ca':
            raise serializers.ValidationError("Передан некорректный статус заказа")
        return value


class OrderSerializer(serializers.ModelSerializer, ValidationForOrderSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'cart', 'status', 'total_cost', 'address', 'delivery_at', 'created_at')
        read_only_fields = ('total_cost', 'created_at', 'cart',)

    def create(self, validated_data):
        request = self.context.get('request')
        try:
            cart_without_order = Cart.objects.get(order=None, users=request.user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError({"detail": "У вас нет корзины с товарами, чтобы совершить заказ!"})
        order = Order.objects.create(
            delivery_at=validated_data['delivery_at'],
            recipient=request.user,
            address=validated_data['address'],
            cart=cart_without_order,
            total_cost=cart_without_order.total_cost()
        )
        return order


class OrderDetailSerializer(serializers.ModelSerializer, ValidationForOrderSerializer):
    cart = CartTotalSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'cart', 'status', 'recipient', 'total_cost', 'address', 'delivery_at', 'created_at',)
        read_only_fields = ('recipient', 'total_cost', 'created_at',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = instance.get_status_display()
        return representation
