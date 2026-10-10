from django.db import models
from django.utils import timezone
 
from api.models import SlugModel, TimeStampedModel
from api.storages import raw_media_storage
from api.validators import RESUME_VALIDATORS, validate_bd_phone
from cloudinary.models import CloudinaryField
 
class JobPost(TimeStampedModel, SlugModel):
    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full time"
        PART_TIME = "part_time", "Part time"
        CONTRACT = "contract", "Contract"
        INTERNSHIP = "internship", "Internship"
 
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=150, blank=True)
    employment_type = models.CharField(
        max_length=12, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME
    )
    vacancies = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True, help_text="Rich text (HTML).")
    requirements = models.TextField(blank=True, help_text="Rich text (HTML).")
    salary_note = models.CharField(max_length=100, blank=True, help_text='e.g. "Negotiable"')
    deadline = models.DateField(blank=True, null=True, help_text="Empty = no deadline.")
    is_active = models.BooleanField(default=True)
 
    class Meta:
        ordering = ["-created_at"]
 
    def __str__(self):
        return self.title
 
    @property
    def is_open(self):
        return self.is_active and (self.deadline is None or self.deadline >= timezone.localdate())
 
 
class JobApplication(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", "New"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"
        HIRED = "hired", "Hired"
 
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="applications")
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[validate_bd_phone])
    cover_letter = models.TextField(blank=True)
    resume = CloudinaryField(
        "resumes",
        resource_type="raw",
        validators=RESUME_VALIDATORS,
    )
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    admin_note = models.TextField(blank=True, help_text="Internal. Never shown to applicants.")
 
    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["job", "status"])]
 
    def __str__(self):
        return f"{self.name} - {self.job.title}"