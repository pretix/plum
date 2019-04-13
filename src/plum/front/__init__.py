from django.apps import AppConfig


class FrontConfig(AppConfig):
    name = 'plum.front'
    verbose_name = 'Front'


default_app_config = 'plum.front.FrontConfig'
