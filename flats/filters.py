import django_filters
 
from flats.models import Flat
 
 
class FlatFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name="project__slug", help_text="Project slug.")
    project_id = django_filters.NumberFilter(field_name="project_id")
    min_price = django_filters.NumberFilter(field_name="price_per_sft", lookup_expr="gte", help_text="Taka per sft.")
    max_price = django_filters.NumberFilter(field_name="price_per_sft", lookup_expr="lte", help_text="Taka per sft.")
    min_size = django_filters.NumberFilter(field_name="size_sft", lookup_expr="gte", help_text="Sq ft.")
    max_size = django_filters.NumberFilter(field_name="size_sft", lookup_expr="lte", help_text="Sq ft.")
 
    class Meta:
        model = Flat
        fields = [
            "project",
            "project_id",
            "status",
            "flat_type",
            "bedrooms",
            "min_price",
            "max_price",
            "min_size",
            "max_size",
            "is_featured",
            "is_active",
        ]