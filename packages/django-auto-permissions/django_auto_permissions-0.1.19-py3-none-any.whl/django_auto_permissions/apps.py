from django.apps import AppConfig

class AutoPermissionsConfig(AppConfig):
    name = 'django_auto_permissions'

    def ready(self):
        from .registration import ViewsetRegistrar
        ViewsetRegistrar.process_registrations()