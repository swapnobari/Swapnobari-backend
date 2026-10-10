from django.contrib import admin
from django.utils.html import format_html
 
from api.admin import SingletonAdmin
 
from footer.models import FooterLink, FooterLinkGroup, FooterSettings, FooterSocialLink
 
 
@admin.register(FooterSettings)
class FooterSettingsAdmin(SingletonAdmin):
    list_display = ("__str__", "updated_at")
    readonly_fields = ("logo_preview", "created_at", "updated_at")
    fieldsets = (
        ("Logo", {"fields": ("show_logo", "logo", "logo_preview", "logo_alt_text", "logo_link", "logo_width")}),
        ("About", {"fields": ("show_about", "about_heading", "about_text")}),
        (
            "Contact",
            {
                "fields": (
                    "show_contact",
                    "contact_heading",
                    "address",
                    "phone_1",
                    "phone_2",
                    "whatsapp_number",
                    "email",
                    "working_hours",
                )
            },
        ),
        (
            "Google location",
            {
                "fields": (
                    "show_map",
                    "map_heading",
                    "google_map_embed_url",
                    "google_maps_link",
                    "latitude",
                    "longitude",
                    "map_height",
                )
            },
        ),
        ("Link columns & social", {"fields": ("show_links", "show_social", "social_heading")}),
        ("Bottom bar", {"fields": ("copyright_text", "developed_by_text", "developed_by_url")}),
        ("Look", {"fields": ("background_color", "text_color", "accent_color", "background_image")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
 
    @admin.display(description="Logo preview")
    def logo_preview(self, obj):
        if obj.pk and obj.logo:
            return format_html('<img src="{}" style="max-width:200px;" />', obj.logo.url)
        return "-"
 
 
@admin.register(FooterSocialLink)
class FooterSocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "label", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("platform", "is_active")
    search_fields = ("label", "url")
    ordering = ("order", "id")
    readonly_fields = ("created_at", "updated_at")
 
 
class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ("label", "url", "open_in_new_tab", "order", "is_active")
 
 
@admin.register(FooterLinkGroup)
class FooterLinkGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "placement", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("placement", "is_active")
    search_fields = ("title",)
    ordering = ("order", "id")
    inlines = [FooterLinkInline]
    readonly_fields = ("created_at", "updated_at")