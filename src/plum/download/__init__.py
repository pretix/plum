from django.apps import AppConfig


class DlConfig(AppConfig):
    name = 'plum.download'
    verbose_name = 'Download'


default_app_config = 'plum.download.DlConfig'
