from rest_framework.throttling import SimpleRateThrottle
 
 
class PublicSubmitThrottle(SimpleRateThrottle):
    """Limits public form submissions (land-share, booking, contact, job
    applications) per IP. Rate comes from DEFAULT_THROTTLE_RATES["public_submit"].
    Logged-in admins are never limited."""
 
    scope = "public_submit"
 
    def get_cache_key(self, request, view):
        user = request.user
        if user and user.is_authenticated and user.is_staff:
            return None  # no limit
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}
    
class BookingLookupThrottle(PublicSubmitThrottle):
    """Limits the public booking-status lookup (stops guessing of reference codes).
    Rate comes from DEFAULT_THROTTLE_RATES["booking_lookup"]."""
 
    scope = "booking_lookup"