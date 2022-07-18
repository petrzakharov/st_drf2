from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F

from items.models import Item
from users.models import User


class Cart(models.Model):
    items = models.ManyToManyField(
        Item, related_name='cart', through='CartItem'
    )
    users = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)

    def total_cost(self):
        return sum([cart_items_row.total_price() for cart_items_row in CartItem.objects.filter(cart=self)])


class CartItem(models.Model):
    item = models.ForeignKey(Item, related_name='cart_items', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def total_price(self):
        return int(self.quantity) * int(self.price)
