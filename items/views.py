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



"""
Сериалайзер

items = serializers.SerializerMethodField()

def get_items(self, obj):
    
    

"""


"""
CARTS (все корзины для текущего пользователя)

/carts/  get

Список товаров + общая стоимость всей корзины (2 совмещенных сериалайзера, наследование, + 1 расчетное поле ?)

{
  "id": 0,
  "items": [
    # список по каждому товару
    {
      "id": 0, # айдишник корзины
      
      "item": {
        "id": 0,
        "title": "string",
        "description": "string",
        "image": "string",
        "weight": 2147483647,
        "price": "string"
      },
    
      # инфа об одном товаре инфа из корзины
      "item_id": "string", 
      "quantity": 2147483647,
      "price": "string",
      "total_price": "string"
    }
  ],
  "total_cost": "string" # общая стоимость всей корзины, с учетом количества каждой позиции
}


-------------------------------------------------------


/carts/items/       get, post

GET: получаем список товаров в корзине
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [ # список товаров
    { 
    # инфа об одном товаре (вложенный сериалайзер Item)
      "id": 0,
      "item": {
        "id": 0,
        "title": "string",
        "description": "string",
        "image": "string",
        "weight": 2147483647,
        "price": "string"
      },
    # инфа об одном товаре инфа из корзины
      "item_id": "string",
      "quantity": 2147483647,
      "price": "string",
      "total_price": "string"
    }
  ]
}



-------------------------------------------------------


При запросе на этот эндпоинт получаю информациб об одном товаре из корзины и подробно о товаре
/carts/items/{id}/   get, put, patch, delete

GET

{
  "id": 0, (айдишник корзины текущего пользователя)
  "item": { # тут данные по определенному айтему (вложенный сериалайзер для модели Item)
    "id": 0,
    "title": "string",
    "description": "string",
    "image": "string",
    "weight": 2147483647,
    "price": "string"
  },
  "item_id": "string", # айтем айди в корзине
  "quantity": 2147483647, # количество товара в корзине
  "price": "string", # стоимость товара в корзине
  "total_price": "string" # стоимость товара в корзине умноженного на количество в корзине
}



-------------------------------------------------------
"""