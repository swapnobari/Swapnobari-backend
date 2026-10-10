from rest_framework import serializers
 
from api.serializers import make_slug_field
from api.services import sanitize_html
 
from csr.models import CSRActivity, CSRImage
 
 
class CSRImageSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = CSRImage
        fields = ["id", "image", "caption", "order"]
        read_only_fields = ["id"]
 
 
class CSRActivityListSerializer(serializers.ModelSerializer):
    """Light version for cards and lists."""
    
    cover_image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    class Meta:
        model = CSRActivity
        fields = [
            "id",
            "title",
            "slug",
            "cover_image",
            "activity_date",
            "location",
            "is_active",
            "order",
        ]
        read_only_fields = fields
 
 
class CSRActivitySerializer(serializers.ModelSerializer):
    """Full activity: used for detail, create and update."""
 
    slug = make_slug_field(CSRActivity.objects.all())
    
    cover_image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    images = CSRImageSerializer(many=True, read_only=True)
 
    class Meta:
        model = CSRActivity
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "cover_image",
            "activity_date",
            "location",
            "is_active",
            "order",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def validate_description(self, value):
        return sanitize_html(value)
 