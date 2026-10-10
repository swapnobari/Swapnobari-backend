from rest_framework import viewsets
 
from api.mixins import MultipartParserMixin, ReorderMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly
 
from testimonials.models import Testimonial
from testimonials.serializers import TestimonialSerializer
 
 
class TestimonialViewSet(ReorderMixin, MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: GET list / detail (active testimonials, in order).
    Admin:   full CRUD (multipart) + POST /reorder/ with {"ids": [...]}.
    """
 
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filterset_fields = ["rating", "is_active"]
    search_fields = ["name", "designation", "message"]
    ordering_fields = ["order", "rating", "created_at"]
 