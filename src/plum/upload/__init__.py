from django.apps import AppConfig


class UlConfig(AppConfig):
    name = 'plum.upload'
    verbose_name = 'Upload'


default_app_config = 'plum.upload.UlConfig'
