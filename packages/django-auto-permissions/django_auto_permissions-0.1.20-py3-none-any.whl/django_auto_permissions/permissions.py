from rest_framework.permissions import BasePermission


class PermissionRegistry:
    registry = {}

    @classmethod
    def add_permission(cls, name, permission_class):
        cls.registry[name] = permission_class

    @classmethod
    def get_permission(cls, name):
        return cls.registry.get(name)


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def create_permission_classes_for_model(model, custom_methods):
    model_name = model._meta.model_name.capitalize()

    for method in custom_methods:
        camel_case_method = to_camel_case(method)
        class_name = f"{model_name}{camel_case_method}Permission"
        print("Creating permission class:", class_name)

        new_permission_class = type(
            class_name,
            (BasePermission,),
            {'has_permission': lambda self, request, view: request.method.lower() == method.lower()}
        )
        print("Adding permission class:", new_permission_class)
        PermissionRegistry.add_permission(class_name, new_permission_class)
        print("All permissions:", PermissionRegistry.registry)
