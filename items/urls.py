from django.urls import include, path
from rest_framework.routers import DefaultRouter

from items.views import ItemViewSet

router = DefaultRouter()
router.register('items', ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls))
]
