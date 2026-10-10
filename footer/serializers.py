from django.db.models import Max
from django.utils import timezone
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
 
from api.validators import extract_google_maps_src, validate_google_maps_embed
 
from footer.models import FooterLink, FooterLinkGroup, FooterSettings, FooterSocialLink
 
 
class FooterSocialLinkSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(source="get_platform_display", read_only=True)
 
    class Meta:
        model = FooterSocialLink
        fields = [
            "id",
            "platform",
            "platform_display",
            "label",
            "url",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def create(self, validated_data):
        if "order" not in validated_data:
            highest = FooterSocialLink.objects.aggregate(m=Max("order"))["m"]
            validated_data["order"] = 0 if highest is None else highest + 1
        return super().create(validated_data)
 
 
class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = [
            "id",
            "group",
            "label",
            "url",
            "open_in_new_tab",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def create(self, validated_data):
        # new link goes to the end of its group unless an order is given
        if "order" not in validated_data:
            highest = FooterLink.objects.filter(group=validated_data["group"]).aggregate(
                m=Max("order")
            )["m"]
            validated_data["order"] = 0 if highest is None else highest + 1
        return super().create(validated_data)
 
 
class FooterLinkGroupSerializer(serializers.ModelSerializer):
    placement_display = serializers.CharField(source="get_placement_display", read_only=True)
    links = serializers.SerializerMethodField()
 
    class Meta:
        model = FooterLinkGroup
        fields = [
            "id",
            "title",
            "placement",
            "placement_display",
            "order",
            "is_active",
            "links",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def create(self, validated_data):
        if "order" not in validated_data:
            highest = FooterLinkGroup.objects.aggregate(m=Max("order"))["m"]
            validated_data["order"] = 0 if highest is None else highest + 1
        return super().create(validated_data)
 
    @swagger_serializer_method(serializer_or_field=FooterLinkSerializer(many=True))
    def get_links(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        is_admin = bool(user and user.is_authenticated and user.is_staff)
        links = obj.links.all()  # prefetched by the views
        if self.context.get("public_only") or not is_admin:
            links = [link for link in links if link.is_active]
        return FooterLinkSerializer(links, many=True, context=self.context).data
 
 
class FooterSettingsSerializer(serializers.ModelSerializer):
    """The footer in one payload: settings + active social links + active link groups."""
    
    logo = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    background_image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    google_map_embed_url = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=5000,
        help_text="Paste the whole Google Maps <iframe> code or only its src URL.",
    )
    copyright_display = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()
    link_groups = serializers.SerializerMethodField()
 
    class Meta:
        model = FooterSettings
        fields = [
            # logo
            "show_logo",
            "logo",
            "logo_alt_text",
            "logo_link",
            "logo_width",
            # about
            "show_about",
            "about_heading",
            "about_text",
            # contact
            "show_contact",
            "contact_heading",
            "address",
            "phone_1",
            "phone_2",
            "whatsapp_number",
            "email",
            "working_hours",
            # google location
            "show_map",
            "map_heading",
            "google_map_embed_url",
            "google_maps_link",
            "latitude",
            "longitude",
            "map_height",
            # links and social
            "show_links",
            "show_social",
            "social_heading",
            # bottom bar
            "copyright_text",
            "copyright_display",
            "developed_by_text",
            "developed_by_url",
            # look
            "background_color",
            "text_color",
            "accent_color",
            "background_image",
            # read-only extras
            "social_links",
            "link_groups",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]
 
    def validate_google_map_embed_url(self, value):
        value = extract_google_maps_src(value)
        validate_google_maps_embed(value)
        if len(value) > 2000:
            raise serializers.ValidationError("The map URL is too long.")
        return value
 
    def get_copyright_display(self, obj) -> str:
        return obj.copyright_text.replace("{year}", str(timezone.localdate().year))
 
    @swagger_serializer_method(serializer_or_field=FooterSocialLinkSerializer(many=True))
    def get_social_links(self, obj):
        queryset = FooterSocialLink.objects.filter(is_active=True)
        return FooterSocialLinkSerializer(queryset, many=True, context=self.context).data
 
    @swagger_serializer_method(serializer_or_field=FooterLinkGroupSerializer(many=True))
    def get_link_groups(self, obj):
        groups = FooterLinkGroup.objects.filter(is_active=True).prefetch_related("links")
        context = {**self.context, "public_only": True}
        return FooterLinkGroupSerializer(groups, many=True, context=context).data