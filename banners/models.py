from django.db import models
from cloudinary.models import CloudinaryField
from api.models import TimeStampedModel
from api.validators import IMAGE_VALIDATORS
 
 
class Banner(TimeStampedModel):
    """One banner per page (the header image + title on inner pages)."""
 
    class Page(models.TextChoices):
        ABOUT = "about", "About Us"
        FOUNDERS_MESSAGE = "founders_message", "Founder's Message"
        TEAM = "team", "Management Team"
        PROJECTS = "projects", "Projects"
        PLOTS = "plots", "Plot Sale"
        FLATS = "flats", "Flat Sale"
        LANDOWNER = "landowner", "Landowner"
        CSR = "csr", "CSR"
        CAREERS = "careers", "Career"
        NEWS = "news", "News & Event"
        CONTACT = "contact", "Contact Us"
        BOOKING = "booking", "Visit Booking"
 
    page = models.CharField(
        max_length=30,
        choices=Page.choices,
        unique=True,
        error_messages={"unique": "A banner for this page already exists."},
    )
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, blank=True)
    image = CloudinaryField(blank=True, null=True, validators=IMAGE_VALIDATORS)
    is_active = models.BooleanField(default=True)
 
    class Meta:
        ordering = ["page"]
 
    def __str__(self):
        return f"{self.get_page_display()} - {self.title}"