from drf_spectacular.extensions import OpenApiFilterExtension
from rest_framework.filters import OrderingFilter

class CustomOrderingFilterExtension(OpenApiFilterExtension):
    target_class = 'rest_framework.filters.OrderingFilter'
    match_subclasses = True

    def get_schema_operation_parameters(self, auto_schema):
        view = auto_schema.view
        ordering_fields = getattr(view, "ordering_fields", [])

        if ordering_fields:
            enum = ordering_fields + [f"-{field}" for field in ordering_fields]
        else:
            enum = []

        return [{
            'name': 'sortBy',  # 👈 Cambiar el nombre aquí si quieres usar sortBy
            'required': False,
            'in': 'query',
            'description': 'Sort results by one or more fields. Prefix with "-" for descending.',
            'schema': {
                'type': 'string',
                'enum': enum,
                'example': '-created_at',
            }
        }]
