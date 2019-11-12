from django.conf.urls import url

from .views import upload

urlpatterns = [
    url(r'^upload/$', upload.UploadView.as_view(), name="upload.upload"),
]
