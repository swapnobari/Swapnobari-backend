from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView
 
from api.mixins import MultipartParserMixin, ReorderMixin, SingletonMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from about.models import AboutPage, CoreValue, FoundersMessage, MissionVision
from about.serializers import (
    AboutPageSerializer,
    CoreValueSerializer,
    FoundersMessageSerializer,
    MissionVisionSerializer,
)
 
 
class AboutPageView(SingletonMixin, MultipartParserMixin, RetrieveUpdateAPIView):
    """
    GET   Visitor: page content + active mission/vision + active values in one payload.
    PUT / PATCH   Admin: edit the page (multipart). Mission/vision and values
    are managed through their own endpoints.
    """
 
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    permission_classes = [IsAdminOrReadOnly]
 
 
class FoundersMessageView(SingletonMixin, MultipartParserMixin, RetrieveUpdateAPIView):
    """GET: Visitor. PUT / PATCH: Admin (multipart)."""
 
    queryset = FoundersMessage.objects.all()
    serializer_class = FoundersMessageSerializer
    permission_classes = [IsAdminOrReadOnly]
 
 
class MissionVisionViewSet(MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """Visitor: read active. Admin: full CRUD. Detail URL uses the type (mission / vision)."""
 
    queryset = MissionVision.objects.all()
    serializer_class = MissionVisionSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    lookup_field = "type"
    filterset_fields = ["type", "is_active"]
 
 
class CoreValueViewSet(ReorderMixin, VisibilityMixin, viewsets.ModelViewSet):
    """Visitor: read active values in order. Admin: full CRUD + POST /reorder/.
    Text only, so JSON or form data both work."""
 
    queryset = CoreValue.objects.all()
    serializer_class = CoreValueSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filterset_fields = ["is_active"]
 