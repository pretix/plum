from django.urls import path, re_path

from .views import file, fdroid, pep503

urlpatterns = [
    path('pip/', pep503.IndexView.as_view(), name="pep503.index"),
    path('pip/<str:package>/', pep503.PackageView.as_view(), name="pep503.package"),
    path('pip/<str:package>/<int:version>/<str:name>', pep503.DownloadView.as_view(),
        name="pep503.download"),
    path('download/<str:package>/latest', file.DownloadLatestView.as_view(), name="file.latest"),
    path('download/<str:package>/<str:version>', file.DownloadView.as_view(), name="file.download"),
    path('fdroid/repo/index-v1.jar', fdroid.IndexView.as_view(), name="fdroid.index.v1"),
    path('fdroid/repo/<str:package>_<str:version>.apk', file.DownloadView.as_view(), name="fdroid.download"),
    re_path(r'^fdroid/repo/icons(-\d+)?/(?P<package>[^/]+).png$', fdroid.IconView.as_view(),
        name="fdroid.icon"),
    path('fdroid/repo/<str:androidpackage>/en-US/phoneScreenshots/<str:id>.png',
        fdroid.ScreenshotView.as_view(),
        name="fdroid.screenshot"),
]
