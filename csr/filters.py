import django_filters
 
from csr.models import CSRActivity
 
 
class CSRActivityFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="activity_date", lookup_expr="year")
 
    class Meta:
        model = CSRActivity
        fields = ["year", "is_active"]
