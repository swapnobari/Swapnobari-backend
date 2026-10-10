import django_filters
 
from plots.models import Plot
 
 
class PlotFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name="project__slug", help_text="Project slug.")
    project_id = django_filters.NumberFilter(field_name="project_id")
    min_size = django_filters.NumberFilter(field_name="size_katha", lookup_expr="gte", help_text="Katha, minimum.")
    max_size = django_filters.NumberFilter(field_name="size_katha", lookup_expr="lte", help_text="Katha, maximum.")
 
    class Meta:
        model = Plot
        fields = [
            "project",
            "project_id",
            "status",
            "size_katha",
            "min_size",
            "max_size",
            "is_featured",
            "is_active",
        ]
 