from django.contrib import admin
from django.utils.html import format_html
 
from testimonials.models import Testimonial
 
 
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("photo_thumb", "name", "designation", "rating", "order", "is_active")
    list_display_links = ("photo_thumb", "name")
    list_editable = ("rating", "order", "is_active")
    list_filter = ("rating", "is_active")
    search_fields = ("name", "designation", "message")
    ordering = ("order", "id")
    readonly_fields = ("photo_preview", "created_at", "updated_at")
    fields = (
        "name",
        "designation",
        "photo",
        "photo_preview",
        "rating",
        "message",
        "order",
        "is_active",
        "created_at",
        "updated_at",
    )
 
    @admin.display(description="Photo")
    def photo_thumb(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="44" height="44" style="object-fit:cover;border-radius:50%;" />',
                obj.photo.url,
            )
        return "-"
 
    @admin.display(description="Preview")
    def photo_preview(self, obj):
        if obj.pk and obj.photo:
            return format_html('<img src="{}" style="max-width:200px;border-radius:6px;" />', obj.photo.url)
        return "-"
 