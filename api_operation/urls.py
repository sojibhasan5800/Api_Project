"""
URL configuration for api_operation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
schema_view = get_schema_view(
   openapi.Info(
      title="Courier & E-commerce API",
      default_version='v1',
      description="API documentation for User, Profile, Order, Payment, Delivery system",
      terms_of_service="https://www.yourcompany.com/terms/",
      contact=openapi.Contact(email="support@yourcompany.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   authentication_classes=[JWTAuthentication], 
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # API Endpoints
    # path('api/v1/', include('api.urls')),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/categories/', include('categories.urls')),
    path('api/v1/cart/', include('cart.urls')),
    path('api/v1/store/', include('store.urls')),
    path('api/v1/order/', include('order.urls')),

    # Swagger urls
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

