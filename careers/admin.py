from django.contrib import admin
from django.db.models import Count
 
from careers.models import JobApplication, JobPost
 
 
@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "department",
        "location",
        "employment_type",
        "vacancies",
        "deadline",
        "application_count",
        "is_active",
    )
    list_editable = ("is_active",)
    list_filter = ("employment_type", "department", "is_active")
    search_fields = ("title", "department", "location", "description")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "department", "location", "employment_type", "vacancies")}),
        ("Details", {"fields": ("description", "requirements", "salary_note", "deadline")}),
        ("Display", {"fields": ("is_active",)}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
 
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_applications=Count("applications"))
 
    @admin.display(description="Applications", ordering="_applications")
    def application_count(self, obj):
        return obj._applications
 
 
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "job", "email", "phone", "status", "created_at")
    list_display_links = ("name",)
    list_editable = ("status",)
    list_filter = ("status", "job", "created_at")
    search_fields = ("name", "email", "phone", "job__title")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Application", {"fields": ("job", "status", "admin_note")}),
        ("Applicant", {"fields": ("name", "email", "phone", "cover_letter", "resume")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )