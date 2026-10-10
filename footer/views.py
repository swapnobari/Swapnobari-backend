from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView
 
from api.mixins import MultipartParserMixin, ReorderMixin, SingletonMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from footer.models import FooterLink, FooterLinkGroup, FooterSettings, FooterSocialLink
from footer.serializers import (
    FooterLinkGroupSerializer,
    FooterLinkSerializer,
    FooterSettingsSerializer,
    FooterSocialLinkSerializer,
)
 
 
class FooterView(SingletonMixin, MultipartParserMixin, RetrieveUpdateAPIView):
    """
    GET   Visitor: the whole footer in one payload (settings + active social links +
          active link groups with their active links).
    PUT / PATCH   Admin (multipart: logo, background image, text, colours, Google map...).
    Social links and link columns are managed through their own endpoints.
    """
 
    queryset = FooterSettings.objects.all()
    serializer_class = FooterSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]
 
 
class FooterSocialLinkViewSet(ReorderMixin, VisibilityMixin, viewsets.ModelViewSet):
    """Visitor: read active. Admin: full CRUD + POST /reorder/."""
 
    queryset = FooterSocialLink.objects.all()
    serializer_class = FooterSocialLinkSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filterset_fields = ["platform", "is_active"]
 
 
class FooterLinkGroupViewSet(ReorderMixin, VisibilityMixin, viewsets.ModelViewSet):
    """Footer columns / bottom-bar groups, each with its links.
    Visitor: read active. Admin: full CRUD + POST /reorder/."""
 
    queryset = FooterLinkGroup.objects.prefetch_related("links")
    serializer_class = FooterLinkGroupSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filterset_fields = ["placement", "is_active"]
 
 
class FooterLinkViewSet(ReorderMixin, VisibilityMixin, viewsets.ModelViewSet):
    """Single links inside a group. Filter with ?group=<group id>.
    Visitor: read active links of active groups. Admin: full CRUD + POST /reorder/."""
 
    queryset = FooterLink.objects.select_related("group")
    serializer_class = FooterLinkSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filterset_fields = ["group", "is_active"]
 
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not (user.is_authenticated and user.is_staff):
            queryset = queryset.filter(group__is_active=True)
        return queryset