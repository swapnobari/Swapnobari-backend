from rest_framework import viewsets
 
from api.mixins import MultipartParserMixin, ReorderMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from team.models import TeamMember
from team.serializers import TeamMemberSerializer
 
 
class TeamMemberViewSet(ReorderMixin, MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: GET list / detail (active members, in order).
    Admin:   full CRUD (multipart) + POST /reorder/ with {"ids": [...]}.
    """
 
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filterset_fields = ["is_active"]
    search_fields = ["name", "designation"]
    ordering_fields = ["order", "name", "created_at"]