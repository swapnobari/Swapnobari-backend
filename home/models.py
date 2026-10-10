from django.db import models
from cloudinary.models import CloudinaryField
from api.models import ActiveOrderModel, TimeStampedModel
from api.validators import IMAGE_VALIDATORS
 
 
class HeroSlide(TimeStampedModel, ActiveOrderModel):
    """Home page slider. Lower `order` shows first."""
 
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, blank=True)
    image = CloudinaryField("swapnobari/home/slides/", null=True, blank=True, validators=IMAGE_VALIDATORS)
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.CharField(
        max_length=255, blank=True, help_text="Site path (/projects) or full URL."
    )
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return self.title
 
 
class HomeSection(TimeStampedModel):
    """Fixed content blocks on the home page, one row per block."""
 
    class Key(models.TextChoices):
        INTRO = "intro", "Intro (Turning dreams into reality)"
        SECURE_INVESTMENT = "secure_investment", "Secure investment for a better tomorrow"
 
    key = models.CharField(
        max_length=30,
        choices=Key.choices,
        unique=True,
        error_messages={"unique": "This section already exists."},
    )
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True, help_text="Rich text (HTML).")
    image = CloudinaryField(
        "swapnobari/home/sections/", null=True, blank=True, validators=IMAGE_VALIDATORS
    )
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
 
    class Meta:
        ordering = ["key"]
 
    def __str__(self):
        return f"{self.get_key_display()}"
 