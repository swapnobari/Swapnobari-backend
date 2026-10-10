from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from cloudinary.models import CloudinaryField
from api.models import ActiveOrderModel, TimeStampedModel
from api.validators import IMAGE_VALIDATORS
 
 
class Testimonial(TimeStampedModel, ActiveOrderModel):
    """Customer review shown on the home page. Lower `order` shows first."""
 
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150, blank=True, help_text="e.g. Flat owner, Landowner")
    photo = CloudinaryField(
        "swapnobari/testimonials/", blank=True, null=True, validators=IMAGE_VALIDATORS
    )
    rating = models.PositiveSmallIntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    message = models.TextField()
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return f"{self.name} ({self.rating}/5)"