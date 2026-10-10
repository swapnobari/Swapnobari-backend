from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from cloudinary.models import CloudinaryField
from api.models import ActiveOrderModel, SEOModel, SlugModel, TimeStampedModel
from api.storages import raw_media_storage
from api.validators import IMAGE_VALIDATORS, PDF_VALIDATORS
 
 
class ProjectCategory(TimeStampedModel, ActiveOrderModel, SlugModel):
    """Admin-managed project types: Apartment, Land Sharing, Hotel Share..."""
 
    slug_source = "name"
 
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
 
    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Project category"
        verbose_name_plural = "Project categories"
 
    def __str__(self):
        return self.name
 
 
class Project(TimeStampedModel, ActiveOrderModel, SEOModel, SlugModel):
    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
 
    class AreaUnit(models.TextChoices):
        KATHA = "katha", "Katha"
        DECIMAL = "decimal", "Decimal"
        BIGHA = "bigha", "Bigha"
 
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.PROTECT, related_name="projects"
    )
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.UPCOMING)
    short_description = models.CharField(max_length=255, blank=True, help_text="Shown on cards.")
    description = models.TextField(blank=True, help_text="Rich text (HTML).")
 
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
 
    land_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    land_area_unit = models.CharField(max_length=10, choices=AreaUnit.choices, default=AreaUnit.KATHA)
    total_units = models.PositiveIntegerField(blank=True, null=True)
    floors = models.PositiveSmallIntegerField(blank=True, null=True)
    car_parking = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(blank=True, null=True)
    handover_date = models.DateField(blank=True, null=True)
 
    thumbnail = CloudinaryField("swapnobari/projects/", validators=IMAGE_VALIDATORS)
    brochure = CloudinaryField(
        "swapnobari/projects/brochures/",
        validators=PDF_VALIDATORS,
    )
    video_url = models.URLField(blank=True, help_text="YouTube link.")
 
    is_featured = models.BooleanField(default=False, help_text="Show on the Home page.")
    accepts_land_share = models.BooleanField(
        default=False, help_text="Landowners can send a land-share request for this project."
    )
    land_share_terms = models.TextField(
        blank=True, help_text="Owner / developer share terms shown to landowners (HTML)."
    )
 
    class Meta:
        ordering = ["order", "-created_at"]
 
    def __str__(self):
        return self.title
 
 
class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField("swapnobari/projects/gallery/", validators=IMAGE_VALIDATORS)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return f"{self.project.title} - image {self.pk}"
 
 
class ProjectAmenity(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="amenities")
    title = models.CharField(max_length=120)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon name used by the frontend.")
    order = models.PositiveIntegerField(default=0)
 
    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Project amenities"
 
    def __str__(self):
        return f"{self.project.title} - {self.title}"