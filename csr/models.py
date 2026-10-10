from django.db import models
from cloudinary.models import CloudinaryField
from api.models import ActiveOrderModel, SlugModel, TimeStampedModel
from api.validators import IMAGE_VALIDATORS
 
 
class CSRActivity(TimeStampedModel, ActiveOrderModel, SlugModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Rich text (HTML).")
    cover_image = CloudinaryField("swapnobari/csr/", null=True, blank=True, validators=IMAGE_VALIDATORS)
    activity_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
 
    class Meta:
        ordering = ["order", "-activity_date", "-created_at"]
        verbose_name = "CSR activity"
        verbose_name_plural = "CSR activities"
 
    def __str__(self):
        return self.title
 
 
class CSRImage(TimeStampedModel):
    activity = models.ForeignKey(CSRActivity, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField("swapnobari/csr/gallery/", null=True, blank=True, validators=IMAGE_VALIDATORS)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return f"{self.activity.title} - image {self.pk}"
 