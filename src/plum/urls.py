from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from .core.admin import site

urlpatterns = [
    url(r'^admin/', site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
