from django.contrib import admin
from django.utils.html import format_html
 
from csr.models import CSRActivity, CSRImage
 
 
class CSRImageInline(admin.TabularInline):
    model = CSRImage
    extra = 1
    fields = ("image", "caption", "order")
 
 
@admin.register(CSRActivity)
class CSRActivityAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "activity_date", "location", "order", "is_active")
    list_display_links = ("thumb", "title")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "activity_date")
    search_fields = ("title", "location", "description")
    date_hierarchy = "activity_date"
    ordering = ("order", "-activity_date")
    inlines = [CSRImageInline]
    readonly_fields = ("cover_preview", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "description", "activity_date", "location")}),
        ("Media", {"fields": ("cover_image", "cover_preview")}),
        ("Display", {"fields": ("is_active", "order")}),
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