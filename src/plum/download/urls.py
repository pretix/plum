from django.conf.urls import url

from .views import file, fdroid, pep503

urlpatterns = [
    url(r'^pip/$', pep503.IndexView.as_view(), name="pep503.index"),
    url(r'^pip/(?P<package>[^/]+)/$', pep503.PackageView.as_view(), name="pep503.package"),
    url(r'^pip/(?P<package>[^/]+)/(?P<version>\d+)/(?P<name>[^/]+)$', pep503.DownloadView.as_view(),
        name="pep503.download"),
    url(r'^download/(?P<package>[^/]+)/latest$', file.DownloadLatestView.as_view(), name="file.latest"),
    url(r'^download/(?P<package>[^/]+)/(?P<version>[^/]+)$', file.DownloadView.as_view(), name="file.download"),
    url(r'^fdroid/repo/index-v1.jar$', fdroid.IndexView.as_view(), name="fdroid.index.v1"),
    url(r'^fdroid/repo/(?P<package>[^/]+)_(?P<version>[^/]+).apk$', file.DownloadView.as_view(), name="fdroid.download"),
    url(r'^fdroid/repo/icons(-\d+)?/(?P<package>[^/]+).png$', fdroid.IconView.as_view(),
        name="fdroid.icon"),
    url(r'fdroid/repo/(?P<androidpackage>[^/]+)/en-US/phoneScreenshots/(?P<id>[^/]+).png$',
        fdroid.ScreenshotView.as_view(),
        name="fdroid.screenshot"),
]
