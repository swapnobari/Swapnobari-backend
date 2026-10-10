from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
 
from api.mixins import MultipartParserMixin
from api.permissions import IsAdmin
 
from users.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserProfileSerializer,
)
 
 
class LoginView(TokenObtainPairView):
    """POST email + password -> access, refresh, user."""
 
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"
 
 
class LogoutView(GenericAPIView):
    """POST refresh token -> blacklisted. Open to any caller so an expired
    access token cannot block logout."""
 
    serializer_class = LogoutSerializer
    permission_classes = [AllowAny]
 
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
 
 
class ProfileView(MultipartParserMixin, RetrieveUpdateAPIView):
    """GET / PUT / PATCH own profile. Avatar goes as multipart/form-data."""
 
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdmin]
 
    def get_object(self):
        return self.request.user
 
 
class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAdmin]
 
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password changed. Please log in again."},
            status=status.HTTP_200_OK,
        )