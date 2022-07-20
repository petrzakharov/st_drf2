from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from users.views import CurrentUserView, RegisterView

app_name = 'users'

urlpatterns = [
    path('users/auth/login/', obtain_auth_token),
    path('users/auth/register/', RegisterView.as_view(), name='register'),
    path('users/current/', CurrentUserView.as_view({'get': 'list', 'put': 'update', 'patch': 'partial_update'}),
         name='general-viewset'),
]
