import django_filters
 
from bookings.models import SiteVisitBooking
 
 
class BookingFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="preferred_date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="preferred_date", lookup_expr="lte")
 
    class Meta:
        model = SiteVisitBooking
        fields = [
            "status",
            "visit_type",
            "preferred_time_slot",
            "project",
            "plot",
            "flat",
            "preferred_date",
            "date_from",
            "date_to",
        ]
 