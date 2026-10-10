from django.contrib import admin
from django.utils.html import format_html
 
from flats.models import Flat, FlatImage
 
 
class FlatImageInline(admin.TabularInline):
    model = FlatImage
    extra = 1
    fields = ("image", "caption", "order")
 
 
@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    list_display = (
        "thumb",
        "title",
        "project",
        "flat_type",
        "price_per_sft",
        "status",
        "is_featured",
        "order",
        "is_active",
    )
    list_display_links = ("thumb", "title")
    list_editable = ("status", "is_featured", "order", "is_active")
    list_filter = ("status", "flat_type", "project", "is_featured", "is_active")
    search_fields = ("title", "location", "description")
    ordering = ("order", "-created_at")
    inlines = [FlatImageInline]
    readonly_fields = ("thumb_preview", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "project", "flat_type", "status", "description")}),
        ("Location & building", {"fields": ("location", "total_land", "total_land_unit", "number_of_units", "car_parking", "handover_date")}),
        ("Flat details", {"fields": ("size_sft", "floor", "bedrooms", "bathrooms", "balconies", "facing")}),
        ("Price", {"fields": ("price_per_sft",)}),
        ("Media", {"fields": ("thumbnail", "thumb_preview")}),
        ("Display", {"fields": ("is_featured", "is_active", "order")}),
        ("SEO", {"classes": ("collapse",), "fields": ("meta_title", "meta_description")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
 
    @admin.display(description="Image")
    def thumb(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="80" height="50" style="object-fit:cover;border-radius:4px;" />',
                obj.thumbnail.url,
            )
        return "-"
 
    @admin.display(description="Preview")
    def thumb_preview(self, obj):
        if obj.pk and obj.thumbnail:
            return format_html('<img src="{}" style="max-width:320px;border-radius:6px;" />', obj.thumbnail.url)
        return "-"