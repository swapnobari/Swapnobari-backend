import django_filters
from django.utils import timezone
 
from news.models import NewsPost
 
 
class NewsPostFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="published_at", lookup_expr="year")
    upcoming = django_filters.BooleanFilter(
        method="filter_upcoming", help_text="true = events that have not happened yet."
    )
 
    class Meta:
        model = NewsPost
        fields = ["post_type", "is_featured", "is_published", "year", "upcoming"]
 
    def filter_upcoming(self, queryset, name, value):
        if value:
            return queryset.filter(
                post_type=NewsPost.PostType.EVENT, event_date__gte=timezone.now()
            )
        return queryset