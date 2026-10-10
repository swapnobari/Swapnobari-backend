from django.contrib import admin
from django.utils.html import format_html
 
from api.admin import SingletonAdmin
 
from contact.models import ContactMessage, SiteSettings
 
 
@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    list_display = ("company_name", "phone_1", "email", "updated_at")
    readonly_fields = ("logo_preview", "created_at", "updated_at")
    fieldsets = (
        ("Brand", {"fields": ("company_name", "tagline", "logo", "logo_preview", "logo_bangla", "favicon")}),
        ("Contact", {"fields": ("address", "phone_1", "phone_2", "whatsapp_number", "email", "working_hours")}),
        ("Map", {"fields": ("google_map_embed_url", "latitude", "longitude")}),
        ("Social links", {"fields": ("facebook_url", "youtube_url", "instagram_url", "linkedin_url")}),
        ("Footer & legal", {"fields": ("footer_text", "terms_conditions", "privacy_policy")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
 
    @admin.display(description="Logo preview")
    def logo_preview(self, obj):
        if obj.pk and obj.logo:
            return format_html('<img src="{}" style="max-width:200px;" />', obj.logo.url)
        return "-"
 
 
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "email", "phone", "is_read", "status", "created_at")
    list_display_links = ("name", "subject")
    list_editable = ("is_read", "status")
    list_filter = ("is_read", "status", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Message", {"fields": ("name", "email", "phone", "subject", "message")}),
        ("Handling", {"fields": ("is_read", "status", "admin_note")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
 