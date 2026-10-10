from django.db import models
from cloudinary.models import CloudinaryField
from api.models import ActiveOrderModel, TimeStampedModel
from api.validators import IMAGE_VALIDATORS, validate_bd_phone
 
 
class TeamMember(TimeStampedModel, ActiveOrderModel):
    """Management team. Lower `order` shows first."""
 
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    photo = CloudinaryField(
        "swapnobari/team/", blank=True, null=True, validators=IMAGE_VALIDATORS
    )
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True, validators=[validate_bd_phone])
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return f"{self.name} - {self.designation}"
 