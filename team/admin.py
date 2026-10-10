from django.contrib import admin
from django.utils.html import format_html
 
from .models import TeamMember
 
 
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("photo_thumb", "name", "designation", "order", "is_active")
    list_display_links = ("photo_thumb", "name")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "designation", "email", "phone")
    ordering = ("order", "id")
    readonly_fields = ("photo_preview", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "designation", "bio", "photo", "photo_preview")}),
        ("Contact & social", {"fields": ("email", "phone", "facebook_url", "linkedin_url")}),
        ("Display", {"fields": ("order", "is_active")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
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
            return format_html('<img src="{}" style="max-width:240px;border-radius:6px;" />', obj.photo.url)
        return "-"