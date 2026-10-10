from django.contrib import admin
from django.utils.html import format_html
 
from partners.models import Partner
 
 
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("logo_thumb", "name", "website_url", "order", "is_active")
    list_display_links = ("logo_thumb", "name")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "website_url")
    ordering = ("order", "id")
    readonly_fields = ("logo_preview", "created_at", "updated_at")
    fields = (
        "name",
        "logo",
        "logo_preview",
        "website_url",
        "order",
        "is_active",
        "created_at",
        "updated_at",
    )
 
    @admin.display(description="Logo")
    def logo_thumb(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="70" height="40" style="object-fit:contain;" />', obj.logo.url
            )
        return "-"
 
    @admin.display(description="Preview")
    def logo_preview(self, obj):
        if obj.pk and obj.logo:
            return format_html('<img src="{}" style="max-width:240px;" />', obj.logo.url)
        return "-"