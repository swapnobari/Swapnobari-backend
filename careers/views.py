from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
 
from api.mixins import VisibilityMixin
from api.permissions import IsAdmin, IsAdminOrReadOnly
from api.throttles import PublicSubmitThrottle
 
from careers.filters import JobApplicationFilter
from careers.models import JobApplication, JobPost
from careers.serializers import (
    JobApplicationCreateSerializer,
    JobApplicationSerializer,
    JobPostListSerializer,
    JobPostSerializer,
)
 
 
class JobPostViewSet(VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: active jobs whose deadline has not passed (list + detail),
             POST /jobs/{slug}/apply/ (multipart, throttled).
    Admin: full CRUD, sees inactive and expired jobs too.
    Filters: employment_type, department, search.
    """
 
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filterset_fields = ["employment_type", "department", "is_active"]
    search_fields = ["title", "department", "location", "description"]
    ordering_fields = ["created_at", "deadline", "title"]
 
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not (user.is_authenticated and user.is_staff):
            today = timezone.localdate()
            queryset = queryset.filter(Q(deadline__isnull=True) | Q(deadline__gte=today))
        return queryset
 
    def get_serializer_class(self):
        if self.action == "list":
            return JobPostListSerializer
        return super().get_serializer_class()
 
    def get_throttles(self):
        if self.action == "apply":
            return [PublicSubmitThrottle()]
        return super().get_throttles()
 
    @swagger_auto_schema(
        request_body=JobApplicationCreateSerializer,
        responses={201: "Application received.", 400: "Validation error or already applied."},
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[AllowAny],
        parser_classes=[MultiPartParser, FormParser],
    )
    def apply(self, request, slug=None):
        """Apply for an open job. Resume (pdf / doc / docx) is sent as multipart/form-data."""
        job = self.get_object()  # inactive or expired jobs are a 404 for visitors
        serializer = JobApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        email = serializer.validated_data["email"]
        if JobApplication.objects.filter(job=job, email__iexact=email).exists():
            raise ValidationError({"email": "You have already applied for this job."})
 
        serializer.save(job=job)
        return Response(
            {"detail": "Your application has been received. Thank you for applying."},
            status=status.HTTP_201_CREATED,
        )
 
 
class JobApplicationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Admin only: list, retrieve, update (status, admin note, applicant details), delete.
    Applications are created by visitors through POST /jobs/{slug}/apply/.
    Filters: job (slug), job_id, status, date_from, date_to, search.
    """
 
    queryset = JobApplication.objects.select_related("job")
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAdmin]
    filterset_class = JobApplicationFilter
    search_fields = ["name", "email", "phone", "job__title"]
    ordering_fields = ["created_at", "status"]