from django.db import models

from carts.models import Cart
from users.models import User


class Order(models.Model):
    STATUSES = [
        ('cr', 'Created'),
        ('de', 'Delivered'),
        ('pr', 'Processed'),
        ('ca', 'Cancelled'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_at = models.DateTimeField()
    recipient = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    cart = models.ForeignKey(Cart, related_name='order', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=STATUSES, default='cr')
    total_cost = models.DecimalField(decimal_places=2, max_digits=8)
