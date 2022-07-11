from django.urls import path, include
from items.views import ItemViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('items', ItemViewSet, basename='item')

urlpatterns = [
    # path('items/<int:pk>/', item, name='one_item'),
    path('', include(router.urls))
]
