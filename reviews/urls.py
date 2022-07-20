from django.urls import path

from reviews.views import ReviewsViewset

app_name = 'reviews'

urlpatterns = [
    path('reviews/', ReviewsViewset.as_view(), name='general-viewset'),
]


