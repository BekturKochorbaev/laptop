from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from laptop.yasg import urlpatterns as yasg


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
] + yasg

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
