from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
 
from api.services import sanitize_html
from projects.models import Project
 
from landowner.models import (
    LandDocument,
    LandownerBenefit,
    LandownerPage,
    LandownerStep,
    LandShareRequest,
)
 
 
#page content
class LandownerBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandownerBenefit
        fields = ["id", "title", "description", "icon", "order", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
 
 
class LandownerStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandownerStep
        fields = ["id", "title", "description", "order", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
 
 
class LandownerPageSerializer(serializers.ModelSerializer):
    """The page (editable) + active benefits and steps (read-only)."""
    
    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    benefits = serializers.SerializerMethodField()
    steps = serializers.SerializerMethodField()
 
    class Meta:
        model = LandownerPage
        fields = ["title", "subtitle", "description", "image", "benefits", "steps", "updated_at"]
        read_only_fields = ["updated_at"]
 
    def validate_description(self, value):
        return sanitize_html(value)
 
    @swagger_serializer_method(serializer_or_field=LandownerBenefitSerializer(many=True))
    def get_benefits(self, obj):
        queryset = LandownerBenefit.objects.filter(is_active=True)
        return LandownerBenefitSerializer(queryset, many=True, context=self.context).data
 
    @swagger_serializer_method(serializer_or_field=LandownerStepSerializer(many=True))
    def get_steps(self, obj):
        queryset = LandownerStep.objects.filter(is_active=True)
        return LandownerStepSerializer(queryset, many=True, context=self.context).data
 
 
#land-share requests
class LandDocumentSerializer(serializers.ModelSerializer):
    
    file = serializers.FileField(
        required=False,
        allow_null=True,
        allow_empty_file=False,
    )
    
    doc_type_display = serializers.CharField(source="get_doc_type_display", read_only=True)
 
    class Meta:
        model = LandDocument
        fields = ["id", "file", "doc_type", "doc_type_display", "created_at"]
        read_only_fields = ["id", "created_at"]
 
 
class ProjectMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "slug"]
 
 
class LandShareRequestCreateSerializer(serializers.ModelSerializer):
    """What a visitor can send. Status, notes and reference code are never accepted.
    Documents are sent as repeated `documents` files (or one `document`) in the same
    multipart request; the view handles them."""
 
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.filter(is_active=True, accepts_land_share=True),
        required=False,
        allow_null=True,
        error_messages={
            "does_not_exist": "This project is not accepting land-share requests.",
        },
    )
 
    class Meta:
        model = LandShareRequest
        fields = [
            "owner_name",
            "phone",
            "email",
            "project",
            "land_location",
            "land_size",
            "land_size_unit",
            "land_type",
            "message",
        ]
 
 
class LandShareRequestSerializer(serializers.ModelSerializer):
    """Admin view: everything, including documents, status and internal note."""
 
    project_detail = ProjectMiniSerializer(source="project", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    land_size_unit_display = serializers.CharField(source="get_land_size_unit_display", read_only=True)
    documents = LandDocumentSerializer(many=True, read_only=True)
 
    class Meta:
        model = LandShareRequest
        fields = [
            "id",
            "reference_code",
            "owner_name",
            "phone",
            "email",
            "project",
            "project_detail",
            "land_location",
            "land_size",
            "land_size_unit",
            "land_size_unit_display",
            "land_type",
            "message",
            "status",
            "status_display",
            "admin_note",
            "documents",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reference_code", "created_at", "updated_at"]