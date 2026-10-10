"""Shared helpers used by more than one app."""
import nh3
from django.utils.text import slugify


def sanitize_html(value: str) -> str:
    """Strip scripts, event handlers and other unsafe markup from rich-text
    (HTML) fields while keeping normal formatting tags."""
    if not value:
        return value
    return nh3.clean(value)


def unique_slug(instance, source_value, slug_field="slug"):
    """Unicode-friendly slug (Bangla titles work) that is unique for the model.
    Adds -2, -3 ... when the slug is already taken."""
    model = instance.__class__
    max_length = model._meta.get_field(slug_field).max_length or 50
    base = slugify(source_value or "", allow_unicode=True)[: max_length - 8]
    base = base or model.__name__.lower()
    slug, number = base, 2
    while model.objects.filter(**{slug_field: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base}-{number}"
        number += 1
    return slug

def next_order(queryset):
    """Next free position (max order + 1) in a queryset that has an `order` field."""
    from django.db.models import Max
 
    highest = queryset.aggregate(m=Max("order"))["m"]
    return 0 if highest is None else highest + 1

def normalize_phone(value):
    """Last 10 digits, so 01712345678, +8801712345678 and 8801712345678 all match."""
    import re
 
    return re.sub(r"\D", "", value or "")[-10:]
 