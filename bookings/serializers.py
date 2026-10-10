from rest_framework import serializers
 
from api.validators import validate_not_past_date
from flats.models import Flat
from plots.models import Plot
from projects.models import Project
 
from bookings.models import SiteVisitBooking
 
 
class BookingCreateSerializer(serializers.ModelSerializer):
    """What a visitor can send. Status, notes and reference code are never accepted."""
 
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.filter(is_active=True), required=False, allow_null=True
    )
    plot = serializers.PrimaryKeyRelatedField(
        queryset=Plot.objects.filter(is_active=True), required=False, allow_null=True
    )
    flat = serializers.PrimaryKeyRelatedField(
        queryset=Flat.objects.filter(is_active=True), required=False, allow_null=True
    )
 
    class Meta:
        model = SiteVisitBooking
        fields = [
            "name",
            "phone",
            "email",
            "number_of_visitors",
            "visit_type",
            "project",
            "plot",
            "flat",
            "preferred_date",
            "preferred_time_slot",
            "message",
        ]
        extra_kwargs = {"preferred_date": {"validators": [validate_not_past_date]}}
 
    def validate(self, attrs):
        has_target = any(attrs.get(field) for field in ("project", "plot", "flat"))
        if attrs.get("visit_type") != SiteVisitBooking.VisitType.OFFICE and not has_target:
            raise serializers.ValidationError(
                {"project": "Choose a project, plot or flat to visit, or choose an office visit."}
            )
        return attrs
 
 
class BookingSerializer(serializers.ModelSerializer):
    """Admin view: everything."""
 
    project_title = serializers.CharField(source="project.title", read_only=True, default=None)
    plot_title = serializers.CharField(source="plot.title", read_only=True, default=None)
    flat_title = serializers.CharField(source="flat.title", read_only=True, default=None)
    visit_type_display = serializers.CharField(source="get_visit_type_display", read_only=True)
    preferred_time_slot_display = serializers.CharField(
        source="get_preferred_time_slot_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
 
    class Meta:
        model = SiteVisitBooking
        fields = [
            "id",
            "reference_code",
            "name",
            "phone",
            "email",
            "number_of_visitors",
            "visit_type",
            "visit_type_display",
            "project",
            "project_title",
            "plot",
            "plot_title",
            "flat",
            "flat_title",
            "preferred_date",
            "preferred_time_slot",
            "preferred_time_slot_display",
            "message",
            "status",
            "status_display",
            "confirmed_date",
            "confirmed_time",
            "admin_note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reference_code", "created_at", "updated_at"]
 
 
class ConfirmBookingSerializer(serializers.Serializer):
    """Body of POST /bookings/{id}/confirm/ (admin)."""
 
    confirmed_date = serializers.DateField(validators=[validate_not_past_date])
    confirmed_time = serializers.TimeField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=[
            SiteVisitBooking.Status.CONFIRMED,
            SiteVisitBooking.Status.RESCHEDULED,
        ],
        default=SiteVisitBooking.Status.CONFIRMED,
    )
    admin_note = serializers.CharField(required=False, allow_blank=True)
 
 
class BookingStatusQuerySerializer(serializers.Serializer):
    """Query string of the public status lookup."""
 
    code = serializers.CharField(help_text="Reference code, e.g. SB-V-000123")
    phone = serializers.CharField(help_text="Phone number used for the booking")
 
 
class BookingStatusSerializer(serializers.ModelSerializer):
    """What a visitor may see about their own booking. No contact data, no admin note."""
 
    visiting = serializers.SerializerMethodField()
    visit_type_display = serializers.CharField(source="get_visit_type_display", read_only=True)
    preferred_time_slot_display = serializers.CharField(
        source="get_preferred_time_slot_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
 
    class Meta:
        model = SiteVisitBooking
        fields = [
            "reference_code",
            "name",
            "visiting",
            "visit_type",
            "visit_type_display",
            "preferred_date",
            "preferred_time_slot",
            "preferred_time_slot_display",
            "status",
            "status_display",
            "confirmed_date",
            "confirmed_time",
        ]
        read_only_fields = fields
 
    def get_visiting(self, obj) -> str:
        target = obj.project or obj.plot or obj.flat
        return target.title if target else "Office visit"