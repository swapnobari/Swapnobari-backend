from django.contrib import admin
from django.utils.html import format_html
 
from .models import Banner
 
 
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("image_thumb", "page", "title", "is_active", "updated_at")
    list_display_links = ("image_thumb", "page")
    list_editable = ("is_active",)
    list_filter = ("is_active", "page")
    search_fields = ("title", "subtitle")
    readonly_fields = ("image_preview", "created_at", "updated_at")
    fields = ("page", "title", "subtitle", "image", "image_preview", "is_active", "created_at", "updated_at")
 
    @admin.display(description="Image")
    def image_thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="90" height="40" style="object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return "-"
 
    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="max-width:420px;border-radius:6px;" />', obj.image.url)
        return "-"
 