from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'BackendCode'

    def ready(self):
        import BackendCode.signals
