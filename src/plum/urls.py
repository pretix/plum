from decorator_include import decorator_include
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static
from django.urls import include
from multifactor.decorators import multifactor_protected

from .core.admin import site
from .front import urls as fronturls
from .download import urls as dlurls
from .upload import urls as upurls

urlpatterns = [
    path('multifactor/', include('multifactor.urls')),
    re_path(r'^admin/', decorator_include(multifactor_protected(factors=1, advertise=False), site.urls)),
    path('', include((dlurls, "download"))),
    path('', include((upurls, "upload"))),
    path('', decorator_include(multifactor_protected(factors=0, advertise=False), (fronturls, "front"))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
