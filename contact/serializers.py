from rest_framework import serializers
 
from api.services import sanitize_html
 
from contact.models import ContactMessage, SiteSettings
 
ALLOWED_MAP_PREFIXES = (
    "https://www.google.com/maps",
    "https://maps.google.com/",
    "https://google.com/maps",
)
 
PUBLIC_FIELDS = [
    "company_name",
    "tagline",
    "logo",
    "logo_bangla",
    "favicon",
    "address",
    "phone_1",
    "phone_2",
    "whatsapp_number",
    "email",
    "working_hours",
    "google_map_embed_url",
    "latitude",
    "longitude",
    "facebook_url",
    "youtube_url",
    "instagram_url",
    "linkedin_url",
    "footer_text",
]
 
 
class SiteSettingsSerializer(serializers.ModelSerializer):
    """Full settings, including the legal pages."""
    
    logo = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    logo_bangla = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    favicon = serializers.ImageField(
        required=False,
        allow_null=True,
    )
 
    class Meta:
        model = SiteSettings
        fields = PUBLIC_FIELDS + ["terms_conditions", "privacy_policy", "updated_at"]
        read_only_fields = ["updated_at"]
 
    def validate_google_map_embed_url(self, value):
        if value and not value.startswith(ALLOWED_MAP_PREFIXES):
            raise serializers.ValidationError(
                "Paste only the src URL of a Google Maps embed (it starts with "
                "https://www.google.com/maps), not the whole <iframe> code."
            )
        return value
 
    def validate_terms_conditions(self, value):
        return sanitize_html(value)
 
    def validate_privacy_policy(self, value):
        return sanitize_html(value)
 
 
class SiteSettingsBriefSerializer(serializers.ModelSerializer):
    """Header / footer / contact data without the long legal texts (used in /api/home/)."""
 
    class Meta:
        model = SiteSettings
        fields = PUBLIC_FIELDS
        read_only_fields = PUBLIC_FIELDS
 
 
class ContactMessageCreateSerializer(serializers.ModelSerializer):
    """What a visitor can send. Status, read flag and notes are never accepted."""
 
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        extra_kwargs = {"message": {"max_length": 5000}}
 
 
class ContactMessageSerializer(serializers.ModelSerializer):
    """Admin view."""
 
    status_display = serializers.CharField(source="get_status_display", read_only=True)
 
    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "subject",
            "message",
            "is_read",
            "status",
            "status_display",
            "admin_note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 