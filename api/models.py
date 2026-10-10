from django.db import models
"""
Abstract base models shared by every app.
They create no tables of their own, so `api` needs no migrations.
"""
 
 
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        abstract = True
 
 
class ActiveOrderModel(models.Model):
    """Show/hide switch plus manual ordering (lower number shows first)."""
 
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
 
    class Meta:
        abstract = True
 
 
class SEOModel(models.Model):
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
 
    class Meta:
        abstract = True
 
 
class SingletonModel(models.Model):
    """Exactly one row (pk=1): About page, Founder's message, Site settings...
    Use `Model.load()` to get it; it is created on first use."""
 
    class Meta:
        abstract = True
 
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
 
    def delete(self, *args, **kwargs):
        pass  # the single row can be edited but never deleted
 
    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
    
class SlugModel(models.Model):
    """Adds a unique, auto-generated slug. Set `slug_source` to the field name
    to build it from (default "title"). Generated once, so links never break
    when the title is edited later."""
 
    slug = models.SlugField(max_length=200, unique=True, blank=True, allow_unicode=True)
    slug_source = "title"
 
    class Meta:
        abstract = True
 
    def save(self, *args, **kwargs):
        if not self.slug:
            from .services import unique_slug
 
            self.slug = unique_slug(self, getattr(self, self.slug_source, ""))
        super().save(*args, **kwargs)
        
class ReferenceCodeModel(models.Model):
    """Adds a human-friendly reference code, e.g. SB-L-000123, made from the
    row id right after the first save. Set `reference_prefix` on the model."""
 
    reference_code = models.CharField(
        max_length=20, unique=True, null=True, blank=True, editable=False
    )
    reference_prefix = "SB"
 
    class Meta:
        abstract = True
 
    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)
        if creating and not self.reference_code:
            self.reference_code = f"{self.reference_prefix}-{self.pk:06d}"
            super().save(update_fields=["reference_code"])