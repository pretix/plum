from django.conf.urls import url

from .views import pep503

urlpatterns = [
    url(r'^pip/$', pep503.IndexView.as_view(), name="pep503.index"),
    url(r'^pip/(?P<package>[^/]+)/$', pep503.PackageView.as_view(), name="pep503.package"),
    url(r'^pip/(?P<package>[^/]+)/(?P<version>\d+)/(?P<name>[^/]+)$', pep503.DownloadView.as_view(), name="pep503.download"),
]
