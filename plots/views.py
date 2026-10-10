from rest_framework import viewsets
 
from api.mixins import GalleryMixin, MultipartParserMixin, ReorderMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from plots.filters import PlotFilter
from plots.models import Plot
from plots.serializers import PlotImageSerializer, PlotListSerializer, PlotSerializer
 
 
class PlotViewSet(GalleryMixin, ReorderMixin, MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: list (light cards) and detail (full) of active plots.
    Admin: full CRUD (multipart), reorder, and gallery images under
    /plots/{slug}/images/ (see GalleryMixin).
    Filters: project (slug), project_id, status, size_katha, min_size, max_size,
    is_featured, search.
    """
 
    queryset = Plot.objects.select_related("project").prefetch_related("images")
    serializer_class = PlotSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filterset_class = PlotFilter
    search_fields = ["title", "location", "description"]
    ordering_fields = ["order", "created_at", "size_katha", "price"]
 
    gallery_serializer_class = PlotImageSerializer
    gallery_parent_field = "plot"
 
    def get_serializer_class(self):
        if self.action == "list":
            return PlotListSerializer
        return super().get_serializer_class()