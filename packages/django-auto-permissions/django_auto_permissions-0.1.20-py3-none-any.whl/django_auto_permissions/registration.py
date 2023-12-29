class ViewsetRegistrar:
    registered_viewsets = []

    @classmethod
    def register(cls, viewset, model):
        print("Registering viewset:", viewset, model)
        cls.registered_viewsets.append((viewset, model))
        print("Registered viewsets post registration:", cls.registered_viewsets)
        cls.register_permissions(viewset, model)

    @classmethod
    def get_custom_methods(cls, viewset_class):
        from django.views import View
        from rest_framework.viewsets import ViewSet, GenericViewSet
        standard_methods = {'list', 'create', 'retrieve', 'update', 'partial_update', 'destroy'}
        base_attributes = set(dir(type('dummy', (object,), {})))  # Python base object attributes
        view_attributes = set(dir(View))  # Attributes from Django's View
        viewset_attributes = set(dir(ViewSet))  # Attributes from DRF's ViewSet
        generic_viewset_attributes = set(dir(GenericViewSet))  # Attributes from DRF's GenericViewSet

        # Combine all inherited attributes
        inherited_attributes = base_attributes.union(
            view_attributes, viewset_attributes, generic_viewset_attributes
        )

        custom_methods = []
        for attr_name in dir(viewset_class):
            if attr_name in standard_methods or attr_name in inherited_attributes:
                continue
            attr = getattr(viewset_class, attr_name)
            if callable(attr) and attr.__qualname__.startswith(viewset_class.__name__ + '.'):
                custom_methods.append(attr_name)

        return custom_methods

    @classmethod
    def register_permissions(cls, viewset, model):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from .permissions import create_permission_classes_for_model
        print("Registering permissions for:", viewset, model)
        content_type = ContentType.objects.get_for_model(model)
        custom_methods = cls.get_custom_methods(viewset)
        print("Custom methods:", custom_methods)
        for method in custom_methods:
            codename = f"{model._meta.model_name}_{method}"
            name = f"Can {method} {model._meta.verbose_name}"
            Permission.objects.get_or_create(
                codename=codename, name=name, content_type=content_type
            )
            print(f"Registered permission: {codename}")
        # Create dynamic permission classes and add them to the module
        create_permission_classes_for_model(model, custom_methods)

    @classmethod
    def process_registrations(cls):
        for viewset, model in cls.registered_viewsets:
            cls.register_permissions(viewset, model)
