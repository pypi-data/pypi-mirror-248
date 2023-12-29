import sys
from rest_framework.permissions import BasePermission

def create_permission_classes_for_model(model, custom_methods):
    model_name = model._meta.model_name.capitalize()

    for method in custom_methods:
        # Define class name based on the model and method
        class_name = f"{model_name}{method.capitalize()}Permission"

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