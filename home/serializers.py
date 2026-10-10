from django.db.models import Max
from rest_framework import serializers
 
from api.services import sanitize_html
 
from home.models import HeroSlide, HomeSection
 
 
class HeroSlideSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = HeroSlide
        fields = [
            "id",
            "title",
            "subtitle",
            "image",
            "button_text",
            "button_link",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def create(self, validated_data):
        # new slide goes to the end unless an order is given
        if "order" not in validated_data:
            highest = HeroSlide.objects.aggregate(m=Max("order"))["m"]
            validated_data["order"] = 0 if highest is None else highest + 1
        return super().create(validated_data)
 
 
class HomeSectionSerializer(serializers.ModelSerializer):
    key_display = serializers.CharField(source="get_key_display", read_only=True)
 
    class Meta:
        model = HomeSection
        fields = [
            "id",
            "key",
            "key_display",
            "title",
            "subtitle",
            "body",
            "image",
            "button_text",
            "button_link",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def validate_body(self, value):
        return sanitize_html(value)