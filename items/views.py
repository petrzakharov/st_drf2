from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item


@api_view(http_method_names=['GET'])
def item(request, pk):
    one_item = get_object_or_404(Item, pk=pk)
    return Response({
        "id": one_item.id,
        "title": one_item.title,
        "description": one_item.description,
        "image": str(one_item.image),
        "weight": one_item.weight,
        "price": one_item.price,
    })
