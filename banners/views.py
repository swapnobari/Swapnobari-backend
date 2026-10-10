from rest_framework import viewsets
 
from api.mixins import MultipartParserMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from banners.models import Banner
from banners.serializers import BannerSerializer
 
 
class BannerViewSet(MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: GET list / GET /banners/<page>/  (active banners only)
    Admin:   full CRUD, sees inactive banners too. Send data as multipart/form-data.
 
    Pagination is off because `?page=about` would clash with the page-number param,
    and there are only ~12 banners in total.
    """
 
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    lookup_field = "page"
    filterset_fields = ["page", "is_active"]
    search_fields = ["title", "subtitle"]
    ordering_fields = ["page", "created_at"]