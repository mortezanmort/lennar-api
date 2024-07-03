from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404


class NestedObjectMixin:
    parent_model = None
    parent_object_lookup_field = "pk"

    def get_parent_model(self):
        if self.parent_model is None:
            raise ImproperlyConfigured("parent model should be defined")

        return self.parent_model

    def get_parent_object(self):
        return get_object_or_404(self.get_parent_model(), **{"pk": self.kwargs[self.parent_object_lookup_field]})

    @property
    def look_up_field_value(self):
        return self.kwargs[self.parent_object_lookup_field]
