from rest_framework import serializers
from .models import Banner
 
 
class BannerSerializer(serializers.ModelSerializer):
    page_display = serializers.CharField(source="get_page_display", read_only=True)
    
    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    class Meta:
        model = Banner
        fields = [
            "id",
            "page",
            "page_display",
            "title",
            "subtitle",
            "image",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 