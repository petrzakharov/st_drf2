from django.urls import path
from items.views import item

urlpatterns = [
    path('items/<int:pk>/', item, name='one_item'),
]
