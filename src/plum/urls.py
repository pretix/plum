from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static
from django.urls import include

from .core.admin import site
from .front import urls as fronturls
from .download import urls as dlurls
from .upload import urls as upurls

urlpatterns = [
    re_path(r'^admin/', site.urls),
    path('', include((dlurls, "download"))),
    path('', include((upurls, "upload"))),
    path('', include((fronturls, "front"))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
