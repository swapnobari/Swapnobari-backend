import django_filters
 
from careers.models import JobApplication
 
 
class JobApplicationFilter(django_filters.FilterSet):
    job_id = django_filters.NumberFilter(field_name="job_id")
    job = django_filters.CharFilter(field_name="job__slug", help_text="Job slug.")
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="date__gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="date__lte")
 
    class Meta:
        model = JobApplication
        fields = ["job", "job_id", "status", "date_from", "date_to"]
