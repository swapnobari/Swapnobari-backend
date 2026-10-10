from cloudinary_storage.storage import RawMediaCloudinaryStorage


def raw_media_storage():
    """Callable (not an instance) so migrations can serialise it.
    Used by FileFields that hold PDFs/documents instead of images."""
    return RawMediaCloudinaryStorage()