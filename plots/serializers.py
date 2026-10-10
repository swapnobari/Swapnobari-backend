from rest_framework import serializers
 
from api.serializers import make_slug_field
from api.services import sanitize_html
from projects.models import Project
 
from plots.models import Plot, PlotImage
 
 
class ProjectMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "slug"]
        ref_name = "PlotsProjectMini"
 
 
class PlotImageSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(
        required=True,
        allow_null=False,
    )
    
    class Meta:
        model = PlotImage
        fields = ["id", "image", "caption", "order"]
        read_only_fields = ["id"]
 
 
class PlotListSerializer(serializers.ModelSerializer):
    """Light version for cards and lists."""
 
    project_title = serializers.CharField(source="project.title", read_only=True, default=None)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    
    thumbnail = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    class Meta:
        model = Plot
        fields = [
            "id",
            "title",
            "slug",
            "project",
            "project_title",
            "location",
            "size_katha",
            "price",
            "price_note",
            "status",
            "status_display",
            "thumbnail",
            "is_featured",
            "is_active",
            "order",
        ]
        read_only_fields = fields
 
 
class PlotSerializer(serializers.ModelSerializer):
    """Full plot: used for detail, create and update."""
 
    slug = make_slug_field(Plot.objects.all())
    project_detail = ProjectMiniSerializer(source="project", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    
    thumbnail = serializers.ImageField(
        required=True,
        allow_null=False,
    )
    
    images = PlotImageSerializer(many=True, read_only=True)
 
    class Meta:
        model = Plot
        fields = [
            "id",
            "title",
            "slug",
            "project",
            "project_detail",
            "location",
            "size_katha",
            "facing",
            "road_width",
            "price",
            "price_note",
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