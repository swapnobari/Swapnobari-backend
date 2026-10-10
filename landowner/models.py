from django.core.validators import MinValueValidator
from django.db import models
from cloudinary.models import CloudinaryField
from api.models import ActiveOrderModel, ReferenceCodeModel, SingletonModel, TimeStampedModel
from api.storages import raw_media_storage
from api.validators import DOCUMENT_VALIDATORS, IMAGE_VALIDATORS, validate_bd_phone
 
 
class LandownerPage(SingletonModel, TimeStampedModel):
    title = models.CharField(max_length=150, default="Landowner")
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, help_text="Rich text (HTML).")
    image = CloudinaryField(
        "swapnobari/landowner/", blank=True, null=True, validators=IMAGE_VALIDATORS
    )
 
    class Meta:
        verbose_name = "Landowner page"
        verbose_name_plural = "Landowner page"
 
    def __str__(self):
        return "Landowner page"
 
 
class LandownerBenefit(TimeStampedModel, ActiveOrderModel):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon name used by the frontend.")
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return self.title
 
 
class LandownerStep(TimeStampedModel, ActiveOrderModel):
    """'How it works' steps, shown in order."""
 
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return self.title
 
 
class LandShareRequest(TimeStampedModel, ReferenceCodeModel):
    """A landowner offering land. With a project it is a land-share request for
    that project; without one it is a general landowner inquiry."""
 
    reference_prefix = "SB-L"
 
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        UNDER_REVIEW = "under_review", "Under review"
        SITE_INSPECTED = "site_inspected", "Site inspected"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
 
    class SizeUnit(models.TextChoices):
        KATHA = "katha", "Katha"
        DECIMAL = "decimal", "Decimal"
        BIGHA = "bigha", "Bigha"
 
    owner_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, validators=[validate_bd_phone])
    email = models.EmailField(blank=True)
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="land_share_requests",
        help_text="Empty = general landowner inquiry.",
    )
    land_location = models.CharField(max_length=255)
    land_size = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    land_size_unit = models.CharField(max_length=10, choices=SizeUnit.choices, default=SizeUnit.KATHA)
    land_type = models.CharField(max_length=100, blank=True, help_text="Current use of the land.")
    message = models.TextField(blank=True, help_text="Proposed arrangement or notes.")
 
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    admin_note = models.TextField(blank=True, help_text="Internal. Never shown to visitors.")
 
    class Meta:
        ordering = ["-created_at"]
 
    def __str__(self):
        return f"{self.reference_code or 'new'} - {self.owner_name}"
 
 
class LandDocument(TimeStampedModel):
    class DocType(models.TextChoices):
        DEED = "deed", "Deed"
        MAP = "map", "Map"
        KHATIAN = "khatian", "Khatian"
        OTHER = "other", "Other"
 
    land_request = models.ForeignKey(
        LandShareRequest, on_delete=models.CASCADE, related_name="documents"
    )
    file = CloudinaryField(
        "swapnobari/landowner/documents/",
        null=True,
        blank=True,
        resource_type="raw",
        validators=DOCUMENT_VALIDATORS,
    )
    doc_type = models.CharField(max_length=10, choices=DocType.choices, default=DocType.OTHER)
 
    class Meta:
        ordering = ["id"]
 
    def __str__(self):
        return f"{self.land_request.reference_code} - {self.get_doc_type_display()}"