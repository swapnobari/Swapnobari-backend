import django_filters
 
from contact.models import ContactMessage
 
 
class ContactMessageFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="date__gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="date__lte")
 
    class Meta:
        model = ContactMessage
        fields = ["is_read", "status", "date_from", "date_to"]
 