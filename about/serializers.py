from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from api.services import sanitize_html
 
from about.models import AboutPage, CoreValue, FoundersMessage, MissionVision
 
 
class MissionVisionSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    
    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    class Meta:
        model = MissionVision
        fields = [
            "id",
            "type",
            "type_display",
            "title",
            "description",
            "image",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def validate_description(self, value):
        return sanitize_html(value)
 
 
class CoreValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreValue
        fields = [
            "id",
            "title",
            "description",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
 
class AboutPageSerializer(serializers.ModelSerializer):
    """The page itself (editable) + mission/vision and values (read-only, active only)."""
 
    mission_vision = serializers.SerializerMethodField()
    values = serializers.SerializerMethodField()
    
    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    class Meta:
        model = AboutPage
        fields = [
            "title",
            "subtitle",
            "description",
            "image",
            "established_year",
            "years_of_experience",
            "total_projects_delivered",
            "happy_families",
            "mission_vision",
            "values",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]
 
    def validate_description(self, value):
        return sanitize_html(value)
 
    @swagger_serializer_method(serializer_or_field=MissionVisionSerializer(many=True))
    def get_mission_vision(self, obj):
        queryset = MissionVision.objects.filter(is_active=True)
        return MissionVisionSerializer(queryset, many=True, context=self.context).data
 
    @swagger_serializer_method(serializer_or_field=CoreValueSerializer(many=True))
    def get_values(self, obj):
        queryset = CoreValue.objects.filter(is_active=True)
        return CoreValueSerializer(queryset, many=True, context=self.context).data
 
 
class FoundersMessageSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = FoundersMessage
        fields = ["founder_name", "designation", "message", "image", "updated_at"]
        read_only_fields = ["updated_at"]
 
    def validate_message(self, value):
        return sanitize_html(value)
 