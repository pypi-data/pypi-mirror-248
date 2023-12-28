from .viewset_analysis import get_custom_methods


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
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    for viewset_class, model_class in registered_viewsets_models:
        content_type = ContentType.objects.get_for_model(model_class)
        for method in get_custom_methods(viewset_class):
            codename = f"{viewset_class.__name__.lower()}_{method}"
            name = f"Can {method} {model_class.__name__}"

            # Creating and saving the permission
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type,
            )
            if created:
                print(f"Created permission: {permission}")
