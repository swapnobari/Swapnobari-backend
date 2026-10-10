from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from cloudinary.models import CloudinaryField       
from api.models import ActiveOrderModel, SingletonModel, TimeStampedModel
from api.validators import (
    IMAGE_VALIDATORS,
    validate_bd_phone,
    validate_google_maps_embed,
    validate_google_maps_link,
    validate_hex_color,
    validate_safe_link,
)
 
 
class FooterSettings(SingletonModel, TimeStampedModel):
    """Everything in the website footer. Blank colours = the site's default theme."""
 
    # logo
    show_logo = models.BooleanField(default=True)
    logo = CloudinaryField(
        "swapnobari/footer/", blank=True, null=True, validators=IMAGE_VALIDATORS
    )
    logo_alt_text = models.CharField(max_length=150, blank=True)
    logo_link = models.CharField(max_length=255, default="/", validators=[validate_safe_link])
    logo_width = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(20), MaxValueValidator(600)],
        help_text="Pixels. Empty = automatic.",
    )
 
    # about
    show_about = models.BooleanField(default=True)
    about_heading = models.CharField(max_length=100, blank=True)
    about_text = models.TextField(blank=True, help_text="Short company description.")
 
    # contact
    show_contact = models.BooleanField(default=True)
    contact_heading = models.CharField(max_length=100, default="Contact Us", blank=True)
    address = models.TextField(blank=True)
    phone_1 = models.CharField(max_length=30, blank=True)
    phone_2 = models.CharField(max_length=30, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    working_hours = models.CharField(max_length=150, blank=True)
 
    # Google location
    show_map = models.BooleanField(default=True)
    map_heading = models.CharField(max_length=100, default="Find Us", blank=True)
    google_map_embed_url = models.URLField(
        max_length=2000,
        blank=True,
        validators=[validate_google_maps_embed],
        help_text="Google Maps > Share > Embed a map. The API also accepts the whole iframe code.",
    )
    google_maps_link = models.URLField(
        max_length=500,
        blank=True,
        validators=[validate_google_maps_link],
        help_text='Link for an "Open in Google Maps" / "Get directions" button.',
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    map_height = models.PositiveSmallIntegerField(
        default=250, validators=[MinValueValidator(100), MaxValueValidator(600)], help_text="Pixels."
    )
 
    # link columns and social
    show_links = models.BooleanField(default=True, help_text="Show the link columns.")
    show_social = models.BooleanField(default=True)
    social_heading = models.CharField(max_length=100, default="Follow Us", blank=True)
 
    # bottom bar 
    copyright_text = models.CharField(
        max_length=255,
        default="© {year} Swapno Bari Housing Ltd. All rights reserved.",
        blank=True,
        help_text="{year} is replaced by the current year.",
    )
    developed_by_text = models.CharField(max_length=150, blank=True)
    developed_by_url = models.CharField(max_length=255, blank=True, validators=[validate_safe_link])
 
    # look
    background_color = models.CharField(max_length=7, blank=True, validators=[validate_hex_color])
    text_color = models.CharField(max_length=7, blank=True, validators=[validate_hex_color])
    accent_color = models.CharField(max_length=7, blank=True, validators=[validate_hex_color])
    background_image = CloudinaryField(
        "swapnobari/footer/", blank=True, null=True, validators=IMAGE_VALIDATORS
    )
 
    class Meta:
        verbose_name = "Footer settings"
        verbose_name_plural = "Footer settings"
 
    def __str__(self):
        return "Footer settings"
 
 
class FooterSocialLink(TimeStampedModel, ActiveOrderModel):
    class Platform(models.TextChoices):
        FACEBOOK = "facebook", "Facebook"
        YOUTUBE = "youtube", "YouTube"
        INSTAGRAM = "instagram", "Instagram"
        LINKEDIN = "linkedin", "LinkedIn"
        X = "x", "X (Twitter)"
        TIKTOK = "tiktok", "TikTok"
        WHATSAPP = "whatsapp", "WhatsApp"
        TELEGRAM = "telegram", "Telegram"
        OTHER = "other", "Other"
 
    platform = models.CharField(max_length=15, choices=Platform.choices)
    label = models.CharField(max_length=60, blank=True, help_text="Shown on hover / for screen readers.")
    url = models.URLField(max_length=500)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return self.label or self.get_platform_display()
 
 
class FooterLinkGroup(TimeStampedModel, ActiveOrderModel):
    class Placement(models.TextChoices):
        COLUMN = "column", "Footer column"
        BOTTOM_BAR = "bottom_bar", "Bottom bar (next to copyright)"
 
    title = models.CharField(max_length=100, help_text='e.g. "Quick Links", "Our Projects".')
    placement = models.CharField(max_length=12, choices=Placement.choices, default=Placement.COLUMN)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return self.title
 
 
class FooterLink(TimeStampedModel, ActiveOrderModel):
    group = models.ForeignKey(FooterLinkGroup, on_delete=models.CASCADE, related_name="links")
    label = models.CharField(max_length=100)
    url = models.CharField(
        max_length=500, validators=[validate_safe_link], help_text="/projects, https://..., mailto:..., tel:..."
    )
    open_in_new_tab = models.BooleanField(default=False)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return f"{self.group.title}: {self.label}"