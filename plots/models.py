from django.core.validators import MinValueValidator
from django.db import models
from cloudinary.models import CloudinaryField
from api.models import ActiveOrderModel, SEOModel, SlugModel, TimeStampedModel
from api.validators import IMAGE_VALIDATORS
 
 
class Plot(TimeStampedModel, ActiveOrderModel, SEOModel, SlugModel):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        BOOKED = "booked", "Booked"
        SOLD = "sold", "Sold"
 
    title = models.CharField(max_length=200)
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="plots",
        help_text="Optional: the project this plot belongs to.",
    )
    location = models.CharField(max_length=255)
    size_katha = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    facing = models.CharField(max_length=50, blank=True)
    road_width = models.CharField(max_length=50, blank=True, help_text="e.g. 30 ft")
    price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    price_note = models.CharField(
        max_length=100, blank=True, help_text='e.g. "Contact for price"'
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.AVAILABLE)
    description = models.TextField(blank=True, help_text="Rich text (HTML).")
    thumbnail = CloudinaryField("swapnobari/plots/", validators=IMAGE_VALIDATORS)
    is_featured = models.BooleanField(default=False, help_text="Show on the Home page.")
 
    class Meta:
        ordering = ["order", "-created_at"]
 
    def __str__(self):
        return self.title
 
 
class PlotImage(TimeStampedModel):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField("swapnobari/plots/gallery/", validators=IMAGE_VALIDATORS)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return f"{self.plot.title} - image {self.pk}"