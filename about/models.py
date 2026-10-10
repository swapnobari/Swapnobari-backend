from django.db import models
from cloudinary.models import CloudinaryField
 
from api.models import ActiveOrderModel, SingletonModel, TimeStampedModel
from api.validators import IMAGE_VALIDATORS
 
 
class AboutPage(SingletonModel, TimeStampedModel):
    title = models.CharField(max_length=150, default="About Us")
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, help_text="Rich text (HTML).")
    image = CloudinaryField(
        blank=True, null=True, validators=IMAGE_VALIDATORS
    )
    # optional counters shown on the page
    established_year = models.PositiveSmallIntegerField(blank=True, null=True)
    years_of_experience = models.PositiveSmallIntegerField(blank=True, null=True)
    total_projects_delivered = models.PositiveIntegerField(blank=True, null=True)
    happy_families = models.PositiveIntegerField(blank=True, null=True)
 
    class Meta:
        verbose_name = "About page"
        verbose_name_plural = "About page"
 
    def __str__(self):
        return "About page"
 
 
class FoundersMessage(SingletonModel, TimeStampedModel):
    founder_name = models.CharField(max_length=150, blank=True)
    designation = models.CharField(max_length=150, blank=True)
    message = models.TextField(blank=True, help_text="Rich text (HTML).")
    image = CloudinaryField(
        blank=True, null=True, validators=IMAGE_VALIDATORS
    )
 
    class Meta:
        verbose_name = "Founder's message"
        verbose_name_plural = "Founder's message"
 
    def __str__(self):
        return "Founder's message"
 
 
class MissionVision(TimeStampedModel):
    class Type(models.TextChoices):
        MISSION = "mission", "Mission"
        VISION = "vision", "Vision"
 
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        unique=True,
        error_messages={"unique": "This already exists. Edit it instead."},
    )
    title = models.CharField(max_length=150)
    description = models.TextField(help_text="Rich text (HTML).")
    image = CloudinaryField(
        blank=True, null=True, validators=IMAGE_VALIDATORS,
    )
    is_active = models.BooleanField(default=True)
 
    class Meta:
        ordering = ["type"]  # mission, then vision
        verbose_name = "Mission / Vision"
        verbose_name_plural = "Mission & Vision"
 
    def __str__(self):
        return self.get_type_display()
 
 
class CoreValue(TimeStampedModel, ActiveOrderModel):
    """Integrity, Quality, Innovation... shown as a list on the About page."""
 
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return self.title
 