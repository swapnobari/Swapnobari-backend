from rest_framework import serializers
 
from api.serializers import make_slug_field
from api.services import sanitize_html
from projects.models import Project
 
from flats.models import Flat, FlatImage
 
 
class ProjectMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "slug"]
        ref_name = "FlatsProjectMini"
 
 
class FlatImageSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = FlatImage
        fields = ["id", "image", "caption", "order"]
        read_only_fields = ["id"]
 
 
class FlatListSerializer(serializers.ModelSerializer):
    """Light version for cards and lists."""
 
    project_title = serializers.CharField(source="project.title", read_only=True, default=None)
    flat_type_display = serializers.CharField(source="get_flat_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    
    thumbnail = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    class Meta:
        model = Flat
        fields = [
            "id",
            "title",
            "slug",
            "project",
            "project_title",
            "flat_type",
            "flat_type_display",
            "location",
            "price_per_sft",
            "size_sft",
            "total_land",
            "total_land_unit",
            "number_of_units",
            "car_parking",
            "status",
            "status_display",
            "thumbnail",
            "is_featured",
            "is_active",
            "order",
        ]
        read_only_fields = fields
 
 
class FlatSerializer(serializers.ModelSerializer):
    """Full flat: used for detail, create and update."""
 
    slug = make_slug_field(Flat.objects.all())
    project_detail = ProjectMiniSerializer(source="project", read_only=True)
    flat_type_display = serializers.CharField(source="get_flat_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    
    thumbnail = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    images = FlatImageSerializer(many=True, read_only=True)
 
    class Meta:
        model = Flat
        fields = [
            "id",
            "title",
            "slug",
            "project",
            "project_detail",
            "flat_type",
            "flat_type_display",
            "location",
            "price_per_sft",
            "size_sft",
            "total_land",
            "total_land_unit",
            "number_of_units",
            "car_parking",
            "floor",
            "bedrooms",
            "bathrooms",
            "balconies",
            "facing",
            "handover_date",
            "status",
            "status_display",
            "description",
            "thumbnail",
            "is_featured",
            "meta_title",
            "meta_description",
            "is_active",
            "order",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def validate_description(self, value):
        return sanitize_html(value)