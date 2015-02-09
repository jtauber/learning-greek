from django.apps import AppConfig as BaseAppConfig
from django.utils.importlib import import_module


class AppConfig(BaseAppConfig):

    name = "learning_greek"

    def ready(self):
        import_module("learning_greek.receivers")
