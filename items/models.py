from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=300, unique=True)
    description = models.TextField(unique=True)
    image = models.ImageField(upload_to='pictures/', blank=True, null=True)
    weight = models.PositiveSmallIntegerField()
    price = models.DecimalField(validators=[MinValueValidator(1)], decimal_places=2, max_digits=8)
