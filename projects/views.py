from django.db import transaction
from django.db.models import Count, Max, Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from django.db.models import ProtectedError
 
from api.mixins import MultipartParserMixin, ReorderMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from .filters import ProjectFilter
from projects.models import Project, ProjectCategory
from projects.serializers import (
    ProjectAmenitySerializer,
    ProjectCategorySerializer,
    ProjectImageSerializer,
    ProjectListSerializer,
    ProjectSerializer,
)
 
 
def _next_order(queryset):
    highest = queryset.aggregate(m=Max("order"))["m"]
    return 0 if highest is None else highest + 1
 
 
class ProjectCategoryViewSet(ReorderMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: read active categories (with active project count).
    Admin: full CRUD + POST /reorder/. A category that still has projects cannot be deleted.
    Detail URL uses the slug.
    """
 
    queryset = ProjectCategory.objects.annotate(
        project_count=Count("projects", filter=Q(projects__is_active=True), distinct=True)
    )
    serializer_class = ProjectCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    lookup_field = "slug"
    filterset_fields = ["is_active"]
    search_fields = ["name"]
 
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "This category still has projects. Move or delete them first."},
                status=status.HTTP_400_BAD_REQUEST,
            )
 
 
class ProjectViewSet(ReorderMixin, MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: list (light cards) and detail (full) of active projects.
    Admin: full CRUD (multipart), reorder, plus gallery images and amenities
    under /projects/{slug}/images/ and /projects/{slug}/amenities/.
    Filters: category (slug), category_id, status, is_featured, accepts_land_share, search.
    """
 
    queryset = Project.objects.select_related("category").prefetch_related("images", "amenities")
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filterset_class = ProjectFilter
    search_fields = ["title", "short_description", "location"]
    ordering_fields = ["order", "created_at", "title", "handover_date"]
 
    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer
 
    # Gallery images:  GET (visitor) / POST (admin) /projects/{slug}/images/
    
    @swagger_auto_schema(method="get", responses={200: ProjectImageSerializer(many=True)})
    @swagger_auto_schema(
        method="post",
        request_body=ProjectImageSerializer,
        responses={201: ProjectImageSerializer(many=True)},
        operation_description=(
            "Upload one image with `image`, or several at once by repeating the "
            "`images` field. `caption` is applied to every uploaded file."
        ),
    )
    @action(detail=True, methods=["get", "post"], url_path="images")
    def images(self, request, slug=None):
        project = self.get_object()
        context = self.get_serializer_context()
 
        if request.method == "GET":
            return Response(ProjectImageSerializer(project.images.all(), many=True, context=context).data)
 
        files = request.FILES.getlist("images")
        if not files and "image" in request.FILES:
            files = [request.FILES["image"]]
        if not files:
            raise ValidationError({"image": "Upload at least one image."})
 
        caption = request.data.get("caption", "")
        next_order = _next_order(project.images)
        created = []
        with transaction.atomic():
            for file in files:
                serializer = ProjectImageSerializer(
                    data={"image": file, "caption": caption, "order": next_order}, context=context
                )
                serializer.is_valid(raise_exception=True)
                created.append(serializer.save(project=project))
                next_order += 1
        return Response(
            ProjectImageSerializer(created, many=True, context=context).data,
            status=status.HTTP_201_CREATED,
        )
 
    @swagger_auto_schema(method="patch", request_body=ProjectImageSerializer)
    @action(
        detail=True,
        methods=["patch", "delete"],
        url_path=r"images/(?P<image_id>\d+)",
    )
    def image_detail(self, request, slug=None, image_id=None):
        """PATCH caption / order / replace image, or DELETE one gallery image (admin)."""
        project = self.get_object()
        image = get_object_or_404(project.images, pk=image_id)
        if request.method == "DELETE":
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = ProjectImageSerializer(
            image, data=request.data, partial=True, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
 
    
    # Amenities:  GET (visitor) / POST (admin) /projects/{slug}/amenities/
  
    @swagger_auto_schema(method="get", responses={200: ProjectAmenitySerializer(many=True)})
    @swagger_auto_schema(
        method="post", request_body=ProjectAmenitySerializer, responses={201: ProjectAmenitySerializer}
    )
    @action(
        detail=True,
        methods=["get", "post"],
        url_path="amenities",
        parser_classes=[JSONParser, FormParser, MultiPartParser],
    )
    def amenities(self, request, slug=None):
        project = self.get_object()
        if request.method == "GET":
            return Response(ProjectAmenitySerializer(project.amenities.all(), many=True).data)
 
        serializer = ProjectAmenitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data.get("order")
        serializer.save(
            project=project,
            order=_next_order(project.amenities) if not order else order,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
    @swagger_auto_schema(method="patch", request_body=ProjectAmenitySerializer)
    @action(
        detail=True,
        methods=["patch", "delete"],
        url_path=r"amenities/(?P<amenity_id>\d+)",
        parser_classes=[JSONParser, FormParser, MultiPartParser],
    )
    def amenity_detail(self, request, slug=None, amenity_id=None):
        """PATCH or DELETE one amenity (admin)."""
        project = self.get_object()
        amenity = get_object_or_404(project.amenities, pk=amenity_id)
        if request.method == "DELETE":
            amenity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = ProjectAmenitySerializer(amenity, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)