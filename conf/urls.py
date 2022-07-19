from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path as url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="My test API",
        default_version='v1',
        description="Документация",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('items.urls')),
    path('api/v1/', include('carts.urls')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('reviews.urls')),
    path('api/v1/', include('orders.urls')),
]

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
