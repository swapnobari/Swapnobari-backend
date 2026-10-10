import django_filters

from projects.models import Project
 
 
class ProjectFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", help_text="Category slug.")
    category_id = django_filters.NumberFilter(field_name="category_id")
 
    class Meta:
        model = Project
        fields = ["category", "category_id", "status", "is_featured", "accepts_land_share", "is_active"]
 