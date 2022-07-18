import datetime

from rest_framework import serializers

from carts.models import Cart
from carts.serializers import CartTotalSerializer
from orders.models import Order


class ValidationForOrderSerializer:
    def validate_delivery_at(self, value):
        if value.timestamp() < (datetime.datetime.now() + datetime.timedelta(days=1)).timestamp():
            raise serializers.ValidationError('Дата доставки должна быть больше, чем дата + 24 часа')
        return value

    def validate_status(self, value):
        if value != 'ca':
            # тут погуглить, поидее нужно принимать и ca и cancelled, но c cancelled не происходит
            # сохранение в бд. Можно заменить в choices
            raise serializers.ValidationError("Передан некорректный статус заказа")
        return value


class OrderSerializer(serializers.ModelSerializer, ValidationForOrderSerializer):
    # list и create
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'cart', 'status', 'total_cost', 'address', 'delivery_at', 'created_at')
        read_only_fields = ('total_cost', 'created_at', 'cart',)

    def create(self, validated_data):
        request = self.context.get('request')
        try:
            cart_without_order = Cart.objects.get(order=None, users=request.user)
            items = Cart.items  # в корзине должны быть товары, как лучше организовать проверку
            # Добавить товар, удалить товар, попробовать создать заказ. (корзина создалась при добавлении первого
            # заказа, но не удалилась при удалениее товара. Возможно при удалении заказа товара проверять,
            # что он последний в корзине и удалять такую корзину, описать метод delete в сериалайзере CartItems)
        except Cart.DoesNotExist:
            raise serializers.ValidationError({"detail": "У вас нет корзины с товарами, чтобы совершить заказ!"})
            # что, если добавить здесь permission для post запроса, который проверяет, есть ли у пользователя корзина
            # в которой есть товары, но нет заказа ???
        order = Order.objects.create(
            delivery_at=validated_data['delivery_at'],
            recipient=request.user,
            address=validated_data['address'],
            cart=cart_without_order,
            total_cost=cart_without_order.total_cost()
        )
        return order

    # def validate_delivery_at(self, value):
    #     if value.timestamp() < (datetime.datetime.now() + datetime.timedelta(days=1)).timestamp():
    #         raise serializers.ValidationError('Дата доставки должна быть больше, чем дата + 24 часа')
    #     return value


class OrderDetailSerializer(serializers.ModelSerializer, ValidationForOrderSerializer):
    cart = CartTotalSerializer(read_only=True)
    # status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = ('id', 'cart', 'status', 'recipient', 'total_cost', 'address', 'delivery_at', 'created_at',)
        read_only_fields = ('recipient', 'total_cost', 'created_at',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = instance.get_status_display()
        return representation


    # def update(self, instance, validated_data):
    #     # тут нужен пермишн, который разрешает статус update (put, patch) только если заказ в статусе created
    #     # еще один пермишн - заказ может изменять только его владелец (put, patch)
    #     instance.de