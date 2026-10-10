from django.db import models
from cloudinary.models import CloudinaryField
from api.models import ActiveOrderModel, TimeStampedModel
from api.validators import IMAGE_VALIDATORS
 
 
class Partner(TimeStampedModel, ActiveOrderModel):
    """Strategic partner logo shown on the home page. Lower `order` shows first."""
 
    name = models.CharField(max_length=150)
    logo = CloudinaryField("swapnobari/partners/", null=True, blank=True, validators=IMAGE_VALIDATORS)
    website_url = models.URLField(blank=True)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return self.name
 