from rest_framework import viewsets
 
from api.mixins import GalleryMixin, MultipartParserMixin, ReorderMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from csr.filters import CSRActivityFilter
from csr.models import CSRActivity
from csr.serializers import CSRActivityListSerializer, CSRActivitySerializer, CSRImageSerializer
 
 
class CSRActivityViewSet(GalleryMixin, ReorderMixin, MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: list (light cards) and detail (full) of active CSR activities.
    Admin: full CRUD (multipart), reorder, and gallery images under
    /csr/{slug}/images/ (see GalleryMixin).
    Filters: year, search.
    """
 
    queryset = CSRActivity.objects.prefetch_related("images")
    serializer_class = CSRActivitySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filterset_class = CSRActivityFilter
    search_fields = ["title", "location", "description"]
    ordering_fields = ["order", "activity_date", "created_at"]
 
    gallery_serializer_class = CSRImageSerializer
    gallery_parent_field = "activity"
 
    def get_serializer_class(self):
        if self.action == "list":
            return CSRActivityListSerializer
        return super().get_serializer_class()
 