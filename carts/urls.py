from django.urls import include, path
from rest_framework.routers import DefaultRouter

from carts.views import CartItemModelViewSet, CartsViewSet

router = DefaultRouter()
router.register('carts', CartsViewSet, basename='carts')
router.register('carts/items', CartItemModelViewSet, basename='carts-item')


urlpatterns = [
    path('', include(router.urls)),
]
