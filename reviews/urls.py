from django.urls import path

from reviews.views import ReviewsViewset

urlpatterns = [
    path('reviews/', ReviewsViewset.as_view()),
]


