from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from users import views
from users.views import RegisterView, CurrentUserView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register('users/current', CurrentUserView, basename='users-current')


urlpatterns = [
    # path('users/auth/login/', views.LoginView.as_view()),
    path('users/auth/login/', obtain_auth_token),
    path('users/auth/register/', RegisterView.as_view()),
    path('users/current/', CurrentUserView.as_view({'get': 'list', 'put': 'update', 'patch': 'partial_update'})),
]
