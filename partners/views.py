from rest_framework import viewsets
 
from api.mixins import MultipartParserMixin, ReorderMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from partners.models import Partner
from partners.serializers import PartnerSerializer
 
 
class PartnerViewSet(ReorderMixin, MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: GET list / detail (active partners, in order).
    Admin:   full CRUD (multipart) + POST /reorder/ with {"ids": [...]}.
    """
 
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filterset_fields = ["is_active"]
    search_fields = ["name"]
    ordering_fields = ["order", "name", "created_at"]
 