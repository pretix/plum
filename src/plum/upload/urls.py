from django.urls import path

from .views import upload

urlpatterns = [
    path('upload/', upload.UploadView.as_view(), name="upload.upload"),
]
