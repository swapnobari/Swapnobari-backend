from rest_framework import serializers
 
from api.serializers import make_slug_field
from api.services import sanitize_html
 
from careers.models import JobApplication, JobPost
 
 
class JobPostListSerializer(serializers.ModelSerializer):
    """Light version for the careers list."""
 
    employment_type_display = serializers.CharField(source="get_employment_type_display", read_only=True)
    is_open = serializers.SerializerMethodField()
 
    class Meta:
        model = JobPost
        fields = [
            "id",
            "title",
            "slug",
            "department",
            "location",
            "employment_type",
            "employment_type_display",
            "vacancies",
            "salary_note",
            "deadline",
            "is_open",
            "is_active",
        ]
        read_only_fields = fields
 
    def get_is_open(self, obj) -> bool:
        return obj.is_open
 
 
class JobPostSerializer(serializers.ModelSerializer):
    """Full job post: used for detail, create and update."""
 
    slug = make_slug_field(JobPost.objects.all())
    employment_type_display = serializers.CharField(source="get_employment_type_display", read_only=True)
    is_open = serializers.SerializerMethodField()
 
    class Meta:
        model = JobPost
        fields = [
            "id",
            "title",
            "slug",
            "department",
            "location",
            "employment_type",
            "employment_type_display",
            "vacancies",
            "description",
            "requirements",
            "salary_note",
            "deadline",
            "is_open",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def get_is_open(self, obj) -> bool:
        return obj.is_open
 
    def validate_description(self, value):
        return sanitize_html(value)
 
    def validate_requirements(self, value):
        return sanitize_html(value)
 
 
class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """What an applicant can send. Status and notes are never accepted."""
    resume = serializers.FileField(
        required=True,
        allow_empty_file=False,
    )
 
    class Meta:
        model = JobApplication
        fields = ["name", "email", "phone", "cover_letter", "resume"]
 
 
class JobApplicationSerializer(serializers.ModelSerializer):
    """Admin view. The job and the resume file cannot be changed."""
 
    job_title = serializers.CharField(source="job.title", read_only=True)
    job_slug = serializers.CharField(source="job.slug", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
 
    class Meta:
        model = JobApplication
        fields = [
            "id",
            "job",
            "job_title",
            "job_slug",
            "name",
            "email",
            "phone",
            "cover_letter",
            "resume",
            "status",
            "status_display",
            "admin_note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "job", "resume", "created_at", "updated_at"]