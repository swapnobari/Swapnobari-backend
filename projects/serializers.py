from rest_framework import serializers
 
from api.serializers import make_slug_field
from api.services import sanitize_html
 
from projects.models import Project, ProjectAmenity, ProjectCategory, ProjectImage
 
 
class ProjectCategorySerializer(serializers.ModelSerializer):
    slug = make_slug_field(ProjectCategory.objects.all())
    project_count = serializers.IntegerField(read_only=True, help_text="Active projects in this category.")
 
    class Meta:
        model = ProjectCategory
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "order",
            "is_active",
            "project_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
 
class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ["id", "name", "slug"]
 
 
class ProjectImageSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(
        required=True,
        allow_null=False,
    )
    
    class Meta:
        model = ProjectImage
        fields = ["id", "image", "caption", "order"]
        read_only_fields = ["id"]
 
 
class ProjectAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAmenity
        fields = ["id", "title", "icon", "order"]
        read_only_fields = ["id"]
 
 
class ProjectListSerializer(serializers.ModelSerializer):
    """Light version for cards and lists."""
 
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    
    thumbnail = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "category_name",
            "category_slug",
            "status",
            "status_display",
            "short_description",
            "location",
            "land_area",
            "land_area_unit",
            "handover_date",
            "thumbnail",
            "is_featured",
            "accepts_land_share",
            "is_active",
            "order",
        ]
        read_only_fields = fields
 
 
class ProjectSerializer(serializers.ModelSerializer):
    """Full project: used for detail, create and update."""
 
    slug = make_slug_field(Project.objects.all())
    category_detail = CategoryMiniSerializer(source="category", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    
    thumbnail = serializers.ImageField(
        required=True,
        allow_null=False,
    )
    brochure = serializers.FileField(
        required=True,
        allow_empty_file=False,
    )
    
    images = ProjectImageSerializer(many=True, read_only=True)
    amenities = ProjectAmenitySerializer(many=True, read_only=True)
 
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "category_detail",
            "status",
            "status_display",
            "short_description",
            "description",
            "location",
            "latitude",
            "longitude",
            "land_area",
            "land_area_unit",
            "total_units",
            "floors",
            "car_parking",
            "start_date",
            "handover_date",
            "thumbnail",
            "brochure",
            "video_url",
            "is_featured",
            "accepts_land_share",
            "land_share_terms",
            "meta_title",
            "meta_description",
            "is_active",
            "order",
            "images",
            "amenities",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def validate_description(self, value):
        return sanitize_html(value)
 
    def validate_land_share_terms(self, value):
        return sanitize_html(value)
 
    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        handover = attrs.get("handover_date", getattr(self.instance, "handover_date", None))
        if start and handover and handover < start:
            raise serializers.ValidationError(
                {"handover_date": "Handover date cannot be before the start date."}
            )
        return attrs