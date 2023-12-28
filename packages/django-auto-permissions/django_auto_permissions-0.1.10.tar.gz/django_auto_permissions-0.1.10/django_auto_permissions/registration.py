class ViewsetRegistrar:
    registered_viewsets = []

    @classmethod
    def register(cls, viewset, model):
        cls.registered_viewsets.append((viewset, model))
        cls.register_permissions(viewset, model)

    @classmethod
    def get_custom_methods(cls, viewset):
        standard_methods = {'list', 'create', 'retrieve', 'update', 'partial_update', 'destroy'}
        custom_methods = []
        for attr_name in dir(viewset):
            attr = getattr(viewset, attr_name)
            if callable(attr) and attr_name not in standard_methods:
                custom_methods.append(attr_name)
        return custom_methods

    @classmethod
    def register_permissions(cls, viewset, model):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(model)
        custom_methods = cls.get_custom_methods(viewset)

        for method in custom_methods:
            codename = f"{model._meta.model_name}_{method}"
            name = f"Can {method} {model._meta.verbose_name}"
            Permission.objects.get_or_create(
                codename=codename, name=name, content_type=content_type
            )

    @classmethod
    def process_registrations(cls):
        for viewset, model in cls.registered_viewsets:
            cls.register_permissions(viewset, model)
