from django.contrib import admin
from django.utils.html import format_html
 
from news.models import NewsImage, NewsPost
 
 
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ("image", "caption", "order")
 
 
@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = (
        "thumb",
        "title",
        "post_type",
        "published_at",
        "event_date",
        "is_featured",
        "is_published",
    )
    list_display_links = ("thumb", "title")
    list_editable = ("is_featured", "is_published")
    list_filter = ("post_type", "is_published", "is_featured", "published_at")
    search_fields = ("title", "excerpt", "content", "event_location")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    inlines = [NewsImageInline]
    readonly_fields = ("cover_preview", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "post_type", "excerpt", "content")}),
        ("Event details", {"fields": ("event_date", "event_location")}),
        ("Media", {"fields": ("cover_image", "cover_preview")}),
        ("Publishing", {"fields": ("published_at", "is_published", "is_featured")}),
        ("SEO", {"classes": ("collapse",), "fields": ("meta_title", "meta_description")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
 
    @admin.display(description="Image")
    def thumb(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" width="80" height="50" style="object-fit:cover;border-radius:4px;" />',
                obj.cover_image.url,
            )
        return "-"
 
    @admin.display(description="Preview")
    def cover_preview(self, obj):
        if obj.pk and obj.cover_image:
            return format_html('<img src="{}" style="max-width:320px;border-radius:6px;" />', obj.cover_image.url)
        return "-"