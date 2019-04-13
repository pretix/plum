from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'plum.core'
    verbose_name = 'Core'


default_app_config = 'plum.core.CoreConfig'
