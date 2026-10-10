from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
 
from api.permissions import AllowCreateOrAdmin, IsAdmin
from api.services import normalize_phone
from api.throttles import BookingLookupThrottle, PublicSubmitThrottle
 
from bookings.filters import BookingFilter
from bookings.models import SiteVisitBooking
from bookings.serializers import (
    BookingCreateSerializer,
    BookingSerializer,
    BookingStatusQuerySerializer,
    BookingStatusSerializer,
    ConfirmBookingSerializer,
)
 
 
class BookingViewSet(viewsets.ModelViewSet):
    """
    Visitor:
      POST  /bookings/                    create a booking (throttled). Returns message + reference code.
      GET   /bookings/status/?code=&phone=   check own booking (limited fields, throttled).
    Admin:
      GET / PATCH / PUT / DELETE  /bookings/ and /bookings/{id}/
      POST  /bookings/{id}/confirm/       confirm or reschedule with date and time.
    Filters: status, visit_type, preferred_time_slot, project, plot, flat (ids),
    preferred_date, date_from, date_to, search.
    """
 
    queryset = SiteVisitBooking.objects.select_related("project", "plot", "flat")
    permission_classes = [AllowCreateOrAdmin]
    filterset_class = BookingFilter
    search_fields = ["reference_code", "name", "phone", "email"]
    ordering_fields = ["created_at", "preferred_date", "status"]
 
    def get_throttles(self):
        if self.action == "create":
            return [PublicSubmitThrottle()]
        return super().get_throttles()
 
    def get_serializer_class(self):
        if self.action == "create":
            return BookingCreateSerializer
        return BookingSerializer
 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response(
            {
                "detail": "Your visit request has been received. We will confirm it shortly.",
                "reference_code": booking.reference_code,
            },
            status=status.HTTP_201_CREATED,
        )
 
    @swagger_auto_schema(
        query_serializer=BookingStatusQuerySerializer,
        responses={200: BookingStatusSerializer, 404: "No booking found with these details."},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="status",
        url_name="status",
        permission_classes=[AllowAny],
        throttle_classes=[BookingLookupThrottle],
    )
    def check_status(self, request):
        query = BookingStatusQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        code = query.validated_data["code"].strip()
        phone = normalize_phone(query.validated_data["phone"])
 
        booking = (
            SiteVisitBooking.objects.select_related("project", "plot", "flat")
            .filter(reference_code__iexact=code)
            .first()
        )
        # same answer for "wrong code" and "wrong phone" so codes cannot be probed
        if not booking or normalize_phone(booking.phone) != phone:
            return Response(
                {"detail": "No booking found with these details."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(BookingStatusSerializer(booking).data)
 
    @swagger_auto_schema(request_body=ConfirmBookingSerializer, responses={200: BookingSerializer})
    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if booking.status in (
            SiteVisitBooking.Status.COMPLETED,
            SiteVisitBooking.Status.CANCELLED,
        ):
            raise ValidationError(
                {"detail": f"A {booking.get_status_display().lower()} booking cannot be confirmed."}
            )
 
        serializer = ConfirmBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
 
        booking.status = data["status"]
        booking.confirmed_date = data["confirmed_date"]
        booking.confirmed_time = data.get("confirmed_time")
        if "admin_note" in data:
            booking.admin_note = data["admin_note"]
        booking.save()
        return Response(BookingSerializer(booking, context=self.get_serializer_context()).data)
 