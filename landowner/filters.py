import django_filters
 
from landowner.models import LandShareRequest
 
 
class LandShareRequestFilter(django_filters.FilterSet):
    project_id = django_filters.NumberFilter(field_name="project_id")
    project = django_filters.CharFilter(field_name="project__slug", help_text="Project slug.")
    general = django_filters.BooleanFilter(
        field_name="project", lookup_expr="isnull", help_text="true = general inquiries (no project)."
    )
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="date__gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="date__lte")
 
    class Meta:
        model = LandShareRequest
        fields = ["status", "project", "project_id", "general", "land_size_unit", "date_from", "date_to"]
 