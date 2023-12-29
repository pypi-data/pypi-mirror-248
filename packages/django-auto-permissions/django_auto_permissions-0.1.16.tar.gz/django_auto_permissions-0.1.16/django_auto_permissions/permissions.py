import sys

from rest_framework.permissions import BasePermission


def create_permission_classes_for_viewset(viewset, custom_methods):
    viewset_name = viewset.__name__

    for method in custom_methods:
        # Define class name
        class_name = f"{viewset_name}{method.capitalize()}Permission"

        # Define the permission class dynamically
        new_permission_class = type(
            class_name,
            (BasePermission,),
            {
                'has_permission': lambda self, request, view: request.method.lower() == method.lower()
                # Define more methods or override as needed
            }
        )

        # Add the new class to the permissions module
        setattr(sys.modules[__name__], class_name, new_permission_class)
