
"""Reusable validators. Import these in models and serializers."""

import html
import re
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


MAX_IMAGE_SIZE_MB = 5
MAX_DOCUMENT_SIZE_MB = 10


# Bangladesh mobile numbers:
# 01XXXXXXXXX
# +8801XXXXXXXXX
# 8801XXXXXXXXX
validate_bd_phone = RegexValidator(
    regex=r"^(?:01[3-9]\d{8}|(?:\+?880)1[3-9]\d{8})$",
    message="Enter a valid Bangladeshi mobile number, e.g. 01712345678.",
)


# ---------------------------------------------------------
# File extension and size validation
# Compatible with uploaded files and existing Cloudinary
# resources that do not expose the usual .name attribute.
# ---------------------------------------------------------

def _get_file_extension(value):
    """Return a lowercase extension when it can be determined."""
    # Normal Django UploadedFile / FieldFile
    name = getattr(value, "name", None)

    # Cloudinary resources can expose format/public_id instead.
    if not name:
        file_format = getattr(value, "format", None)
        if file_format:
            return str(file_format).lower().lstrip(".")

        name = getattr(value, "public_id", None)

    if not name:
        return None

    name = str(name).rsplit("/", 1)[-1]

    if "." not in name:
        return None

    return name.rsplit(".", 1)[-1].lower()


def _validate_extension(value, allowed_extensions, label):
    extension = _get_file_extension(value)

    if extension is None:
        # Existing Cloudinary resources may not expose their extension.
        # Allow them to be retained when their format cannot be determined.
        if getattr(value, "public_id", None):
            return

        raise ValidationError(
            f"Could not determine the file extension. "
            f"Allowed formats: {', '.join(sorted(allowed_extensions))}."
        )

    if extension not in allowed_extensions:
        raise ValidationError(
            f"{label} must be one of: "
            f"{', '.join(sorted(allowed_extensions))}."
        )


def validate_image_extension(value):
    _validate_extension(
        value,
        {"jpg", "jpeg", "png", "webp"},
        "Image",
    )


def validate_document_extension(value):
    _validate_extension(
        value,
        {"pdf", "doc", "docx", "jpg", "jpeg", "png"},
        "Document",
    )


def validate_pdf_extension(value):
    _validate_extension(value, {"pdf"}, "File")


def validate_resume_extension(value):
    _validate_extension(
        value,
        {"pdf", "doc", "docx"},
        "Resume",
    )


def _validate_size(file, max_mb):
    """Check size when the object exposes a usable size attribute."""
    size = getattr(file, "size", None)

    # Some Cloudinary resources do not expose their remote file size.
    # Uploaded files normally expose .size and are validated below.
    if size is None:
        return

    if size > max_mb * 1024 * 1024:
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


# Ready-made validator lists
IMAGE_VALIDATORS = [
    validate_image_extension,
    validate_image_size,
]

DOCUMENT_VALIDATORS = [
    validate_document_extension,
    validate_document_size,
]

# PDF-only (brochures)
PDF_VALIDATORS = [
    validate_pdf_extension,
    validate_document_size,
]

# Resumes / CVs: PDF, DOC, DOCX only
RESUME_VALIDATORS = [
    validate_resume_extension,
    validate_document_size,
]


# ---------------------------------------------------------
# Google Maps and footer validations
# ---------------------------------------------------------

validate_hex_color = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$",
    message="Enter a hex colour like #1a2b3c.",
)


_SAFE_LINK_PREFIXES = (
    "/",
    "#",
    "http://",
    "https://",
    "mailto:",
    "tel:",
)


def validate_safe_link(value):
    """Allow site paths, anchors, HTTP(S), mailto and tel links."""
    if value and not value.lower().startswith(_SAFE_LINK_PREFIXES):
        raise ValidationError(
            "Use a site path (/projects), a full https:// link, "
            "mailto: or tel:."
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
    """Accept an iframe snippet or a Google Maps embed URL."""
    value = (value or "").strip()

    if "<iframe" in value.lower():
        match = re.search(
            r"""src\s*=\s*["']([^"']+)["']""",
            value,
            re.IGNORECASE,
        )
        if match:
            return html.unescape(match.group(1)).strip()

    return value


def validate_google_maps_embed(value):
    if value and not value.startswith(_MAPS_EMBED_PREFIXES):
        raise ValidationError(
            "Paste a Google Maps embed URL starting with "
            "https://www.google.com/maps, or the complete iframe code."
        )


def validate_google_maps_link(value):
    if value and not value.startswith(_MAPS_LINK_PREFIXES):
        raise ValidationError(
            "Use a Google Maps link "
            "(maps.app.goo.gl or google.com/maps)."
        )
