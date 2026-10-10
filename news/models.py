from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
from api.models import SEOModel, SlugModel, TimeStampedModel
from api.validators import IMAGE_VALIDATORS
 
 
class NewsPost(TimeStampedModel, SEOModel, SlugModel):
    class PostType(models.TextChoices):
        NEWS = "news", "News"
        EVENT = "event", "Event"
 
    title = models.CharField(max_length=200)
    post_type = models.CharField(max_length=10, choices=PostType.choices, default=PostType.NEWS)
    excerpt = models.CharField(max_length=300, blank=True, help_text="Short summary for cards.")
    content = models.TextField(blank=True, help_text="Rich text (HTML).")
    cover_image = CloudinaryField("swapnobari/news/", null=True, blank=True, validators=IMAGE_VALIDATORS)
 
    published_at = models.DateTimeField(
        default=timezone.now, help_text="A future date schedules the post."
    )
    event_date = models.DateTimeField(blank=True, null=True, help_text="Events only.")
    event_location = models.CharField(max_length=255, blank=True, help_text="Events only.")
 
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
 
    class Meta:
        ordering = ["-published_at", "-id"]
        verbose_name = "News / Event"
        verbose_name_plural = "News & Events"
        indexes = [models.Index(fields=["is_published", "published_at"])]
 
    def __str__(self):
        return self.title
 
 
class NewsImage(TimeStampedModel):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField("swapnobari/news/gallery/", null=True, blank=True, validators=IMAGE_VALIDATORS)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
 
    class Meta:
        ordering = ["order", "id"]
 
    def __str__(self):
        return f"{self.post.title} - image {self.pk}"