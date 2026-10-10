from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
 
from api.models import ReferenceCodeModel, TimeStampedModel
from api.validators import validate_bd_phone
 
 
class SiteVisitBooking(TimeStampedModel, ReferenceCodeModel):
    reference_prefix = "SB-V"
 
    class VisitType(models.TextChoices):
        SITE = "site", "Site visit"
        OFFICE = "office", "Office visit"
 
    class TimeSlot(models.TextChoices):
        MORNING = "morning", "Morning"
        NOON = "noon", "Noon"
        AFTERNOON = "afternoon", "Afternoon"
        EVENING = "evening", "Evening"
 
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        RESCHEDULED = "rescheduled", "Rescheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
 
    # visitor
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, validators=[validate_bd_phone])
    email = models.EmailField(blank=True)
    number_of_visitors = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(50)]
    )
 
    # what they want to visit
    project = models.ForeignKey(
        "projects.Project", on_delete=models.SET_NULL, blank=True, null=True, related_name="visit_bookings"
    )
    plot = models.ForeignKey(
        "plots.Plot", on_delete=models.SET_NULL, blank=True, null=True, related_name="visit_bookings"
    )
    flat = models.ForeignKey(
        "flats.Flat", on_delete=models.SET_NULL, blank=True, null=True, related_name="visit_bookings"
    )
    visit_type = models.CharField(max_length=10, choices=VisitType.choices, default=VisitType.SITE)
 
    # when they want to come
    preferred_date = models.DateField()
    preferred_time_slot = models.CharField(
        max_length=10, choices=TimeSlot.choices, default=TimeSlot.MORNING
    )
    message = models.TextField(blank=True)
 
    # admin side
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    confirmed_date = models.DateField(blank=True, null=True)
    confirmed_time = models.TimeField(blank=True, null=True)
    admin_note = models.TextField(blank=True, help_text="Internal. Never shown to visitors.")
 
    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "preferred_date"])]
 
    def __str__(self):
        return f"{self.reference_code or 'new'} - {self.name}"
 