from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
 
from api.mixins import MultipartParserMixin, ReorderMixin, SingletonMixin, VisibilityMixin
from api.permissions import AllowCreateOrAdmin, IsAdminOrReadOnly
from api.throttles import PublicSubmitThrottle
 
from landowner.filters import LandShareRequestFilter
from landowner.models import (
    LandDocument,
    LandownerBenefit,
    LandownerPage,
    LandownerStep,
    LandShareRequest,
)
from landowner.serializers import (
    LandDocumentSerializer,
    LandownerBenefitSerializer,
    LandownerPageSerializer,
    LandownerStepSerializer,
    LandShareRequestCreateSerializer,
    LandShareRequestSerializer,
)
 
MAX_DOCUMENTS = 5
 
 
class LandownerPageView(SingletonMixin, MultipartParserMixin, RetrieveUpdateAPIView):
    """GET Visitor: page + active benefits + active steps. PUT / PATCH Admin (multipart)."""
 
    queryset = LandownerPage.objects.all()
    serializer_class = LandownerPageSerializer
    permission_classes = [IsAdminOrReadOnly]
 
 
class LandownerBenefitViewSet(ReorderMixin, VisibilityMixin, viewsets.ModelViewSet):
    """Visitor: read active benefits. Admin: full CRUD + POST /reorder/."""
 
    queryset = LandownerBenefit.objects.all()
    serializer_class = LandownerBenefitSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filterset_fields = ["is_active"]
 
 
class LandownerStepViewSet(ReorderMixin, VisibilityMixin, viewsets.ModelViewSet):
    """Visitor: read active steps. Admin: full CRUD + POST /reorder/."""
 
    queryset = LandownerStep.objects.all()
    serializer_class = LandownerStepSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filterset_fields = ["is_active"]
 
 
class LandShareRequestViewSet(MultipartParserMixin, viewsets.ModelViewSet):
    """
    Visitor: POST only (multipart, throttled). Returns just a message and the reference code.
        Optional files: repeat `documents` (max 5), or send one `document`;
        `doc_type` (deed / map / khatian / other) applies to all files of that submission.
    Admin: list, retrieve, update status / notes, delete.
    Filters: status, project (slug), project_id, general, land_size_unit, date_from, date_to, search.
    """
 
    queryset = LandShareRequest.objects.select_related("project").prefetch_related("documents")
    permission_classes = [AllowCreateOrAdmin]
    filterset_class = LandShareRequestFilter
    search_fields = ["reference_code", "owner_name", "phone", "email", "land_location"]
    ordering_fields = ["created_at", "status", "land_size"]
 
    def get_throttles(self):
        if self.action == "create":
            return [PublicSubmitThrottle()]
        return super().get_throttles()
 
    def get_serializer_class(self):
        if self.action == "create":
            return LandShareRequestCreateSerializer
        return LandShareRequestSerializer
 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        # collect and validate documents BEFORE saving anything
        files = request.FILES.getlist("documents")
        if not files and "document" in request.FILES:
            files = [request.FILES["document"]]
        if len(files) > MAX_DOCUMENTS:
            raise ValidationError({"documents": f"You can upload at most {MAX_DOCUMENTS} files."})
 
        doc_type = request.data.get("doc_type") or LandDocument.DocType.OTHER
        document_serializers = []
        for file in files:
            document_serializer = LandDocumentSerializer(data={"file": file, "doc_type": doc_type})
            document_serializer.is_valid(raise_exception=True)
            document_serializers.append(document_serializer)
 
        with transaction.atomic():
            land_request = serializer.save()
            for document_serializer in document_serializers:
                document_serializer.save(land_request=land_request)
 
        return Response(
            {
                "detail": "Your request has been received. We will contact you soon.",
                "reference_code": land_request.reference_code,
            },
            status=status.HTTP_201_CREATED,
        )