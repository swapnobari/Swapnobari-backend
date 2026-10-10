from rest_framework import status, viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
 
from api.mixins import MultipartParserMixin, SingletonMixin
from api.permissions import AllowCreateOrAdmin, IsAdminOrReadOnly
from api.throttles import PublicSubmitThrottle
 
from contact.filters import ContactMessageFilter
from .models import ContactMessage, SiteSettings
from .serializers import (
    ContactMessageCreateSerializer,
    ContactMessageSerializer,
    SiteSettingsSerializer,
)
 
 
class SiteSettingsView(SingletonMixin, MultipartParserMixin, RetrieveUpdateAPIView):
    """GET Visitor: company details, social links, legal texts. PUT / PATCH Admin (multipart)."""
 
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]
 
 
class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    Visitor: POST only (throttled). Returns just a confirmation message.
    Admin: list, retrieve (opening a message marks it as read), update status / notes, delete.
    Filters: is_read, status, date_from, date_to, search.
    """
 
    queryset = ContactMessage.objects.all()
    permission_classes = [AllowCreateOrAdmin]
    filterset_class = ContactMessageFilter
    search_fields = ["name", "email", "phone", "subject", "message"]
    ordering_fields = ["created_at", "status", "is_read"]
 
    def get_throttles(self):
        if self.action == "create":
            return [PublicSubmitThrottle()]
        return super().get_throttles()
 
    def get_serializer_class(self):
        if self.action == "create":
            return ContactMessageCreateSerializer
        return ContactMessageSerializer
 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Thank you for contacting us. We will get back to you soon."},
            status=status.HTTP_201_CREATED,
        )
 
    def retrieve(self, request, *args, **kwargs):
        message = self.get_object()
        if not message.is_read:
            message.is_read = True
            message.save(update_fields=["is_read", "updated_at"])
        return Response(self.get_serializer(message).data)
 