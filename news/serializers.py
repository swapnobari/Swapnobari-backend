from rest_framework import serializers
 
from api.serializers import make_slug_field
from api.services import sanitize_html
 
from news.models import NewsImage, NewsPost
 
 
class NewsImageSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = NewsImage
        fields = ["id", "image", "caption", "order"]
        read_only_fields = ["id"]
 
 
class NewsPostListSerializer(serializers.ModelSerializer):
    """Light version for cards and lists."""
 
    post_type_display = serializers.CharField(source="get_post_type_display", read_only=True)
    
    cover_image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    class Meta:
        model = NewsPost
        fields = [
            "id",
            "title",
            "slug",
            "post_type",
            "post_type_display",
            "excerpt",
            "cover_image",
            "published_at",
            "event_date",
            "event_location",
            "is_featured",
            "is_published",
        ]
        read_only_fields = fields
 
 
class NewsPostSerializer(serializers.ModelSerializer):
    """Full post: used for detail, create and update."""
 
    slug = make_slug_field(NewsPost.objects.all())
    post_type_display = serializers.CharField(source="get_post_type_display", read_only=True)
    
    cover_image = serializers.ImageField(
        required=False,  
        allow_null=True,
    )
    
    images = NewsImageSerializer(many=True, read_only=True)
 
    class Meta:
        model = NewsPost
        fields = [
            "id",
            "title",
            "slug",
            "post_type",
            "post_type_display",
            "excerpt",
            "content",
            "cover_image",
            "published_at",
            "event_date",
            "event_location",
            "is_published",
            "is_featured",
            "meta_title",
            "meta_description",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def validate_content(self, value):
        return sanitize_html(value)