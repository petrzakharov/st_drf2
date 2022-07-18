from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from users.views import CurrentUserView, RegisterView

urlpatterns = [
    path('users/auth/login/', obtain_auth_token),
    path('users/auth/register/', RegisterView.as_view()),
    path('users/current/', CurrentUserView.as_view({'get': 'list', 'put': 'update', 'patch': 'partial_update'})),
]
