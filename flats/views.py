from rest_framework import viewsets
 
from api.mixins import GalleryMixin, MultipartParserMixin, ReorderMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from flats.filters import FlatFilter
from flats.models import Flat
from flats.serializers import FlatImageSerializer, FlatListSerializer, FlatSerializer
 
 
class FlatViewSet(GalleryMixin, ReorderMixin, MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: list (light cards) and detail (full) of active flats.
    Admin: full CRUD (multipart), reorder, and gallery images under
    /flats/{slug}/images/ (see GalleryMixin).
    Filters: project (slug), project_id, status, flat_type, bedrooms, min_price,
    max_price, min_size, max_size, is_featured, search.
    """
 
    queryset = Flat.objects.select_related("project").prefetch_related("images")
    serializer_class = FlatSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filterset_class = FlatFilter
    search_fields = ["title", "location", "description"]
    ordering_fields = ["order", "created_at", "price_per_sft", "size_sft"]
 
    gallery_serializer_class = FlatImageSerializer
    gallery_parent_field = "flat"
 
    def get_serializer_class(self):
        if self.action == "list":
            return FlatListSerializer
        return super().get_serializer_class()