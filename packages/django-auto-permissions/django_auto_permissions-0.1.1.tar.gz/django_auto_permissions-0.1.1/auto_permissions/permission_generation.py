# django_auto_permissions/auto_permissions/permission_generation.py

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .viewset_analysis import analyze_registered_viewsets


def generate_permission_codename(viewset_class, method_name):
    """
    Generates a unique permission codename for a given viewset method.

    :param viewset_class: The viewset class.
    :param method_name: The custom method name.
    :return: A string representing the permission codename.
    """
    return f"{viewset_class.__name__.lower()}_{method_name}"


def register_permissions():
    """
    Registers generated permissions with Django's permission system.
    """
    for viewset_class, methods in analyze_registered_viewsets().items():
        for method in methods:
            codename = generate_permission_codename(viewset_class, method)
            name = f"Can {method} {viewset_class.__name__}"

            # Creating and saving the permission
            content_type = ContentType.objects.get_for_model(viewset_class)
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type,
            )

            if created:
                print(f"Created permission: {permission}")
