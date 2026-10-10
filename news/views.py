from django.utils import timezone
from rest_framework import viewsets
 
from api.mixins import GalleryMixin, MultipartParserMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from news.filters import NewsPostFilter
from news.models import NewsPost
from news.serializers import NewsImageSerializer, NewsPostListSerializer, NewsPostSerializer
 
 
class NewsPostViewSet(GalleryMixin, MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: published posts whose publish date has arrived (list + detail).
    Admin: full CRUD (multipart), sees drafts and scheduled posts, and manages gallery
    images under /news/{slug}/images/ (see GalleryMixin).
    Filters: post_type (news / event), is_featured, year, upcoming, search.
    """
 
    queryset = NewsPost.objects.prefetch_related("images")
    serializer_class = NewsPostSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    visibility_field = "is_published"
    filterset_class = NewsPostFilter
    search_fields = ["title", "excerpt", "content", "event_location"]
    ordering_fields = ["published_at", "created_at", "event_date", "title"]
 
    gallery_serializer_class = NewsImageSerializer
    gallery_parent_field = "post"
 
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not (user.is_authenticated and user.is_staff):
            queryset = queryset.filter(published_at__lte=timezone.now())
        return queryset
 
    def get_serializer_class(self):
        if self.action == "list":
            return NewsPostListSerializer
        return super().get_serializer_class()