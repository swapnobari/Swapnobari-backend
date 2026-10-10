from django.contrib import admin
from django.utils.html import format_html
 
from plots.models import Plot, PlotImage
 
 
class PlotImageInline(admin.TabularInline):
    model = PlotImage
    extra = 1
    fields = ("image", "caption", "order")
 
 
@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = (
        "thumb",
        "title",
        "project",
        "size_katha",
        "price",
        "status",
        "is_featured",
        "order",
        "is_active",
    )
    list_display_links = ("thumb", "title")
    list_editable = ("status", "is_featured", "order", "is_active")
    list_filter = ("status", "project", "is_featured", "is_active")
    search_fields = ("title", "location", "description")
    ordering = ("order", "-created_at")
    inlines = [PlotImageInline]
    readonly_fields = ("thumb_preview", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "project", "status", "description")}),
        ("Plot details", {"fields": ("location", "size_katha", "facing", "road_width")}),
        ("Price", {"fields": ("price", "price_note")}),
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