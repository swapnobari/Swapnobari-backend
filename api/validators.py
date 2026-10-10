"""Reusable validators. Import these in models and serializers."""
import html
import re
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator


MAX_IMAGE_SIZE_MB = 5
MAX_DOCUMENT_SIZE_MB = 10


# Bangladesh mobile numbers:
# 01XXXXXXXXX
# +8801XXXXXXXXX
# 8801XXXXXXXXX
validate_bd_phone = RegexValidator(
    regex=r"^(?:\+?88)?01[3-9]\d{8}$",
    message="Enter a valid Bangladeshi mobile number, e.g. 01712345678.",
)


validate_image_extension = FileExtensionValidator(
    allowed_extensions=["jpg", "jpeg", "png", "webp"]
)


validate_document_extension = FileExtensionValidator(
    allowed_extensions=["pdf", "doc", "docx", "jpg", "jpeg", "png"]
)


def _validate_size(file, max_mb):
    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(
            f"File size must not exceed {max_mb} MB."
        )


def validate_image_size(file):
    _validate_size(file, MAX_IMAGE_SIZE_MB)


def validate_document_size(file):
    _validate_size(file, MAX_DOCUMENT_SIZE_MB)


def validate_not_past_date(value):
    """For booking dates: today or later."""
    if value < date.today():
        raise ValidationError("Date cannot be in the past.")



# Ready-made lists so models/serializers stay short:
IMAGE_VALIDATORS = [validate_image_extension, validate_image_size]
DOCUMENT_VALIDATORS = [validate_document_extension, validate_document_size]

# PDF-only (brochures)
validate_pdf_extension = FileExtensionValidator(allowed_extensions=["pdf"])
PDF_VALIDATORS = [validate_pdf_extension, validate_document_size]

# Resumes / CVs: pdf, doc, docx only
validate_resume_extension = FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])
RESUME_VALIDATORS = [validate_resume_extension, validate_document_size]


# google maps and footer validations
validate_hex_color = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$",
    message="Enter a hex colour like #1a2b3c.",
)
 
_SAFE_LINK_PREFIXES = ("/", "#", "http://", "https://", "mailto:", "tel:")
 
 
def validate_safe_link(value):
    """Menu / button links: site path (/projects), anchor, http(s), mailto, tel.
    Anything else (for example javascript:) is rejected."""
    if value and not value.lower().startswith(_SAFE_LINK_PREFIXES):
        raise ValidationError(
            "Use a site path (/projects), a full https:// link, mailto: or tel:."
        )
 
 
_MAPS_EMBED_PREFIXES = (
    "https://www.google.com/maps",
    "https://maps.google.com/",
    "https://google.com/maps",
)
_MAPS_LINK_PREFIXES = _MAPS_EMBED_PREFIXES + (
    "https://maps.app.goo.gl/",
    "https://goo.gl/maps/",
)
 
 
def extract_google_maps_src(value):
    """Accepts the whole <iframe ...> code Google gives you, or just the src URL,
    and returns the src URL."""
    value = (value or "").strip()
    if "<iframe" in value.lower():
        match = re.search(r"""src\s*=\s*["']([^"']+)["']""", value, re.IGNORECASE)
        if match:
            return html.unescape(match.group(1)).strip()
    return value
 
 
def validate_google_maps_embed(value):
    if value and not value.startswith(_MAPS_EMBED_PREFIXES):
        raise ValidationError(
            "Paste the Google Maps embed code or its src URL "
            "(it starts with https://www.google.com/maps)."
        )
 
 
def validate_google_maps_link(value):
    if value and not value.startswith(_MAPS_LINK_PREFIXES):
        raise ValidationError("Use a Google Maps link (maps.app.goo.gl or google.com/maps).")
 