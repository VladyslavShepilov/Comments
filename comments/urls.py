from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from debug_toolbar import urls as debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("captcha/", include("captcha.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("", include("user.urls")),
    path("__debug__/", include(debug_toolbar_urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
