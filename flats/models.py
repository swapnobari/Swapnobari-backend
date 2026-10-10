from django.core.validators import MinValueValidator
from django.db import models
from cloudinary.models import CloudinaryField
from api.models import ActiveOrderModel, SEOModel, SlugModel, TimeStampedModel
from api.validators import IMAGE_VALIDATORS
 
 
class Flat(TimeStampedModel, ActiveOrderModel, SEOModel, SlugModel):
    class FlatType(models.TextChoices):
        RESIDENTIAL = "residential", "Residential"
        COMMERCIAL = "commercial", "Commercial"
 
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        BOOKED = "booked", "Booked"
        SOLD = "sold", "Sold"
 
    class LandUnit(models.TextChoices):
        DECIMAL = "decimal", "Decimal"
        KATHA = "katha", "Katha"
        BIGHA = "bigha", "Bigha"
 
    title = models.CharField(max_length=200)
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="flats",
        help_text="Optional: the project this flat belongs to.",
    )
    flat_type = models.CharField(max_length=15, choices=FlatType.choices, default=FlatType.RESIDENTIAL)
    location = models.CharField(max_length=255)
 
    price_per_sft = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], help_text="Taka per sq ft."
    )
    size_sft = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_land = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_land_unit = models.CharField(max_length=10, choices=LandUnit.choices, default=LandUnit.DECIMAL)
    number_of_units = models.PositiveIntegerField(blank=True, null=True)
    car_parking = models.CharField(max_length=100, blank=True, help_text='e.g. "15 Nos +"')
 
    floor = models.PositiveSmallIntegerField(blank=True, null=True)
    bedrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    bathrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    balconies = models.PositiveSmallIntegerField(blank=True, null=True)
    facing = models.CharField(max_length=50, blank=True)
    handover_date = models.DateField(blank=True, null=True)
 
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.AVAILABLE)
    description = models.TextField(blank=True, help_text="Rich text (HTML).")
    thumbnail = CloudinaryField("swapnobari/flats/", null=True, blank=True, validators=IMAGE_VALIDATORS)
    is_featured = models.BooleanField(default=False, help_text="Show on the Home page.")
 
    class Meta:
        ordering = ["order", "-created_at"]
 
    def __str__(self):
        return self.title
 
 
class FlatImage(TimeStampedModel):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField("swapnobari/flats/gallery/", null=True, blank=True, validators=IMAGE_VALIDATORS)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return f"{self.flat.title} - image {self.pk}"