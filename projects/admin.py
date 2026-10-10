from django.contrib import admin
from django.utils.html import format_html
 
from projects.models import Project, ProjectAmenity, ProjectCategory, ProjectImage
 
 
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
 
 
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "caption", "order")
 
 
class ProjectAmenityInline(admin.TabularInline):
    model = ProjectAmenity
    extra = 1
    fields = ("title", "icon", "order")
 
 
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "thumb",
        "title",
        "category",
        "status",
        "is_featured",
        "accepts_land_share",
        "order",
        "is_active",
    )
    list_display_links = ("thumb", "title")
    list_editable = ("status", "is_featured", "order", "is_active")
    list_filter = ("category", "status", "is_featured", "accepts_land_share", "is_active")
    search_fields = ("title", "location", "short_description")
    ordering = ("order", "-created_at")
    inlines = [ProjectImageInline, ProjectAmenityInline]
    readonly_fields = ("thumb_preview", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "status", "short_description", "description")}),
        ("Location", {"fields": ("location", "latitude", "longitude")}),
        (
            "Details",
            {
                "fields": (
                    "land_area",
                    "land_area_unit",
                    "total_units",
                    "floors",
                    "car_parking",
                    "start_date",
                    "handover_date",
                )
            },
        ),
        ("Media", {"fields": ("thumbnail", "thumb_preview", "brochure", "video_url")}),
        ("Land sharing", {"fields": ("accepts_land_share", "land_share_terms")}),
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