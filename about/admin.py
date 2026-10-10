from django.contrib import admin
from django.utils.html import format_html
 
from api.admin import SingletonAdmin
 
from .models import AboutPage, CoreValue, FoundersMessage, MissionVision
 
 
def _preview(obj, field="image"):
    image = getattr(obj, field)
    if obj.pk and image:
        return format_html('<img src="{}" style="max-width:360px;border-radius:6px;" />', image.url)
    return "-"
 
 
@admin.register(AboutPage)
class AboutPageAdmin(SingletonAdmin):
    list_display = ("title", "updated_at")
    readonly_fields = ("image_preview", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "subtitle", "description", "image", "image_preview")}),
        (
            "Counters (optional)",
            {
                "fields": (
                    "established_year",
                    "years_of_experience",
                    "total_projects_delivered",
                    "happy_families",
                )
            },
        ),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
 
    @admin.display(description="Preview")
    def image_preview(self, obj):
        return _preview(obj)
 
 
@admin.register(FoundersMessage)
class FoundersMessageAdmin(SingletonAdmin):
    list_display = ("founder_name", "designation", "updated_at")
    readonly_fields = ("image_preview", "created_at", "updated_at")
    fields = ("founder_name", "designation", "message", "image", "image_preview", "created_at", "updated_at")
 
    @admin.display(description="Preview")
    def image_preview(self, obj):
        return _preview(obj)
 
 
@admin.register(MissionVision)
class MissionVisionAdmin(admin.ModelAdmin):
    list_display = ("type", "title", "is_active", "updated_at")
    list_editable = ("is_active",)
    list_filter = ("is_active", "type")
    search_fields = ("title", "description")
    readonly_fields = ("image_preview", "created_at", "updated_at")
    fields = ("type", "title", "description", "image", "image_preview", "is_active", "created_at", "updated_at")
 
    @admin.display(description="Preview")
    def image_preview(self, obj):
        return _preview(obj)
 
 
@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active", "updated_at")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    ordering = ("order", "id")
    readonly_fields = ("created_at", "updated_at")
 