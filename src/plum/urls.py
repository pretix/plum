from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include

from .core.admin import site
from .front import urls as fronturls

urlpatterns = [
    url(r'^admin/', site.urls),
    url(r'', include((fronturls, "front"))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
