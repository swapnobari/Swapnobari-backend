from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from cloudinary.models import CloudinaryField
from api.models import SingletonModel, TimeStampedModel
from api.validators import IMAGE_VALIDATORS, validate_bd_phone
 
 
class SiteSettings(SingletonModel, TimeStampedModel):
    """Company-wide settings used by the header, footer, contact page and legal pages."""
 
    # brand
    company_name = models.CharField(max_length=150, default="Swapno Bari Housing Ltd.")
    tagline = models.CharField(max_length=255, blank=True)
    logo = CloudinaryField(
        "logos", blank=True, null=True, validators=IMAGE_VALIDATORS
    )
    logo_bangla = CloudinaryField(
        "logos/bangla", blank=True, null=True, validators=IMAGE_VALIDATORS
    )
    favicon = CloudinaryField(
        "logos/favicons", blank=True, null=True, validators=IMAGE_VALIDATORS
    )
 
    # contact
    address = models.TextField(blank=True)
    phone_1 = models.CharField(max_length=30, blank=True)
    phone_2 = models.CharField(max_length=30, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    working_hours = models.CharField(max_length=150, blank=True)
 
    # map
    google_map_embed_url = models.URLField(
        max_length=1000, blank=True, help_text="Only the src URL of the Google Maps embed."
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
 
    # social
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
 
    # footer / legal
    footer_text = models.CharField(max_length=255, blank=True)
    terms_conditions = models.TextField(blank=True, help_text="Rich text (HTML).")
    privacy_policy = models.TextField(blank=True, help_text="Rich text (HTML).")
 
    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"
 
    def __str__(self):
        return "Site settings"
 
 
class ContactMessage(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", "New"
        REPLIED = "replied", "Replied"
        CLOSED = "closed", "Closed"
 
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, validators=[validate_bd_phone])
    subject = models.CharField(max_length=200)
    message = models.TextField()
 
    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NEW)
    admin_note = models.TextField(blank=True, help_text="Internal. Never shown to visitors.")
 
    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_read", "status"])]
 
    def __str__(self):
        return f"{self.name} - {self.subject}"
 