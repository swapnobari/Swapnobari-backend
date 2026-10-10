from django.contrib import admin
 
from bookings.models import SiteVisitBooking
 
 
@admin.register(SiteVisitBooking)
class SiteVisitBookingAdmin(admin.ModelAdmin):
    list_display = (
        "reference_code",
        "name",
        "phone",
        "visiting",
        "visit_type",
        "preferred_date",
        "preferred_time_slot",
        "status",
        "created_at",
    )
    list_display_links = ("reference_code", "name")
    list_editable = ("status",)
    list_filter = ("status", "visit_type", "preferred_time_slot", "project", "preferred_date")
    search_fields = ("reference_code", "name", "phone", "email")
    date_hierarchy = "preferred_date"
    readonly_fields = ("reference_code", "created_at", "updated_at")
    actions = ["mark_confirmed", "mark_completed", "mark_cancelled"]
    fieldsets = (
        ("Booking", {"fields": ("reference_code", "status", "confirmed_date", "confirmed_time", "admin_note")}),
        ("Visitor", {"fields": ("name", "phone", "email", "number_of_visitors")}),
        (
            "Visit",
            {"fields": ("visit_type", "project", "plot", "flat", "preferred_date", "preferred_time_slot", "message")},
        ),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
 
    @admin.display(description="Visiting")
    def visiting(self, obj):
        target = obj.project or obj.plot or obj.flat
        return target.title if target else "Office"
 
    @admin.action(description="Mark selected as confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status=SiteVisitBooking.Status.CONFIRMED)
 
    @admin.action(description="Mark selected as completed")
    def mark_completed(self, request, queryset):
        queryset.update(status=SiteVisitBooking.Status.COMPLETED)
 
    @admin.action(description="Mark selected as cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(status=SiteVisitBooking.Status.CANCELLED)