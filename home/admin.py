from django.contrib import admin
from django.utils.html import format_html
 
from .models import HeroSlide, HomeSection
 
 
def _thumb(image):
    if image:
        return format_html(
            '<img src="{}" width="110" height="50" style="object-fit:cover;border-radius:4px;" />',
            image.url,
        )
    return "-"
 
 
@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "order", "is_active", "updated_at")
    list_display_links = ("thumb", "title")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")
    ordering = ("order", "id")
    readonly_fields = ("preview", "created_at", "updated_at")
    fields = (
        "title",
        "subtitle",
        "image",
        "preview",
        "button_text",
        "button_link",
        "order",
        "is_active",
        "created_at",
        "updated_at",
    )
 
    @admin.display(description="Image")
    def thumb(self, obj):
        return _thumb(obj.image)
 
    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="max-width:420px;border-radius:6px;" />', obj.image.url)
        return "-"
 
 
@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ("thumb", "key", "title", "is_active", "updated_at")
    list_display_links = ("thumb", "key")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle", "body")
    readonly_fields = ("created_at", "updated_at")
 
    @admin.display(description="Image")
    def thumb(self, obj):
        return _thumb(obj.image)