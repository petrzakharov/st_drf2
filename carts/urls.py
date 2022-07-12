from django.urls import path, include
from carts.views import CartsViewSet, CartItemModelViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('carts', CartsViewSet, basename='carts')
router.register('carts/items', CartItemModelViewSet, basename='carts-item')


urlpatterns = [
    path('', include(router.urls)),
]
