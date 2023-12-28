from django.apps import AppConfig

from .permission_generation import register_permissions
from .viewset_analysis import analyze_registered_viewsets, register_viewset


class AutoPermissionsConfig(AppConfig):
    name = 'django_auto_permissions'

    def ready(self):
        # Example usage - this should ideally be done by the user of your library

        # Mock model class
        custom_methods = analyze_registered_viewsets()
        print("Custom Methods:", custom_methods)

        # Register generated permissions
        register_permissions()
