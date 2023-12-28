def get_custom_methods(viewset_class):
    """
    Identifies custom methods in a given viewset class that are not part of the standard DRF viewsets.

    :param viewset_class: The viewset class to analyze.
    :return: A list of custom method names.
    """
    # Standard methods in DRF viewsets
    standard_methods = {'list', 'create', 'retrieve', 'update', 'partial_update', 'destroy'}

    # Introspect viewset class and find custom methods
    custom_methods = []
    for attr_name in dir(viewset_class):
        attr = getattr(viewset_class, attr_name)
        if callable(attr) and attr_name not in standard_methods:
            custom_methods.append(attr_name)

    return custom_methods


# django_auto_permissions/auto_permissions/viewset_analysis.py

# Existing imports and get_custom_methods function

# New code for registration
registered_viewsets_models = []


def register_viewset(viewset_class, model_class):
    """
    Registers a viewset class and its corresponding model class for permission analysis.

    :param viewset_class: The viewset class to register.
    :param model_class: The Django model class associated with the viewset.
    """
    registered_viewsets_models.append((viewset_class, model_class))


def analyze_registered_viewsets():
    """
    Analyzes all registered viewsets and returns a dictionary of custom methods.

    :return: Dictionary of viewset classes to their custom methods.
    """
    custom_methods_per_viewset = {}
    for viewset_class, _ in registered_viewsets_models:
        custom_methods = get_custom_methods(viewset_class)
        custom_methods_per_viewset[viewset_class] = custom_methods
    return custom_methods_per_viewset
