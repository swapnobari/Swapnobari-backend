from django.contrib import admin
from django.utils.html import format_html
 
from api.admin import SingletonAdmin
 
from landowner.models import (
    LandDocument,
    LandownerBenefit,
    LandownerPage,
    LandownerStep,
    LandShareRequest,
)
 
 
@admin.register(LandownerPage)
class LandownerPageAdmin(SingletonAdmin):
    list_display = ("title", "updated_at")
    readonly_fields = ("image_preview", "created_at", "updated_at")
    fields = ("title", "subtitle", "description", "image", "image_preview", "created_at", "updated_at")
 
    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="max-width:360px;border-radius:6px;" />', obj.image.url)
        return "-"
 
 
@admin.register(LandownerBenefit)
class LandownerBenefitAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    ordering = ("order", "id")
    readonly_fields = ("created_at", "updated_at")
 
 
@admin.register(LandownerStep)
class LandownerStepAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    ordering = ("order", "id")
    readonly_fields = ("created_at", "updated_at")
 
 
class LandDocumentInline(admin.TabularInline):
    model = LandDocument
    extra = 0
    fields = ("file", "doc_type")
 
 
@admin.register(LandShareRequest)
class LandShareRequestAdmin(admin.ModelAdmin):
    list_display = (
        "reference_code",
        "owner_name",
        "phone",
        "project",
        "land_location",
        "land_size",
        "land_size_unit",
        "status",
        "created_at",
    )
    list_display_links = ("reference_code", "owner_name")
    list_editable = ("status",)
    list_filter = ("status", "project", "land_size_unit", "created_at")
    search_fields = ("reference_code", "owner_name", "phone", "email", "land_location")
    date_hierarchy = "created_at"
    inlines = [LandDocumentInline]
    readonly_fields = ("reference_code", "created_at", "updated_at")
    fieldsets = (
        ("Request", {"fields": ("reference_code", "status", "admin_note")}),
        ("Landowner", {"fields": ("owner_name", "phone", "email")}),
        (
            "Land",
            {"fields": ("project", "land_location", "land_size", "land_size_unit", "land_type", "message")},
        ),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
 