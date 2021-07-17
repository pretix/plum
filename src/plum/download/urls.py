from django.conf.urls import url

from .views import file, pep503

urlpatterns = [
    url(r'^pip/$', pep503.IndexView.as_view(), name="pep503.index"),
    url(r'^pip/(?P<package>[^/]+)/$', pep503.PackageView.as_view(), name="pep503.package"),
    url(r'^pip/(?P<package>[^/]+)/(?P<version>\d+)/(?P<name>[^/]+)$', pep503.DownloadView.as_view(), name="pep503.download"),
    url(r'^download/(?P<package>[^/]+)/latest$', file.DownloadLatestView.as_view(), name="file.latest"),
    url(r'^download/(?P<package>[^/]+)/(?P<version>\d+)$', file.DownloadView.as_view(), name="file.download"),
]
