"""
Login and logout views for the browsable API.

Add these to your root URLconf if you're using the browsable API and
your API requires authentication:

    urlpatterns = [
        ...
        path('auth/', include('rest_framework_admin.urls'))
    ]

You should make sure your authentication settings include `SessionAuthentication`.
"""

from django.conf.urls.static import static
from django.contrib import admin
from importlib import import_module
from django.conf import settings
from django.urls import path, include
from rest_framework_util.urls import load_urlpatterns


urlpatterns = load_urlpatterns(settings.BACKEND_INSTALLED_APPS, with_app_prefix=True)

if settings.DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
    admin_urlpatterns = [path("admin/", admin.site.urls)]
    docs_urlpatterns = [
        path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
        # Optional UI:
        path(
            'docs/schema/swagger-ui/',
            SpectacularSwaggerView.as_view(
                url_name='schema'),
            name='swagger-ui'),
        path(
            'docs/schema/redoc/',
            SpectacularRedocView.as_view(
                url_name='schema'),
            name='redoc'),
    ]
    static_urlpatterns = static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)

    urlpatterns = admin_urlpatterns + docs_urlpatterns + static_urlpatterns + urlpatterns

