from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken
 
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    initial = serializers.SerializerMethodField()

    avatar = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "phone",
            "avatar",
            "initial",
            "is_active",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "email",
            "is_active",
            "is_staff",
            "date_joined",
            "initial",
        ]
        ref_name = "CustomUser"

    def get_initial(self, obj):
        return obj.full_name[0].upper() if obj.full_name else "?"
 
 
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password],
    )

    avatar = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "phone",
            "avatar",
            "password",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        return user
 
class UserProfileSerializer(serializers.ModelSerializer):
    
    avatar = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "phone", "avatar", "is_staff", "date_joined"]
        read_only_fields = ["id", "email", "is_staff", "date_joined"]
 
 
class LoginSerializer(TokenObtainPairSerializer):
    """Email + password. Only admin (is_staff) accounts can log in."""
 
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["full_name"] = user.full_name
        token["is_admin"] = user.is_staff
        return token
 
    def validate(self, attrs):
        data = super().validate(attrs)  # raises if credentials are wrong
        if not self.user.is_staff:
            raise AuthenticationFailed("This account does not have admin access.")
        data["user"] = UserProfileSerializer(self.user, context=self.context).data
        return data
 
 
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
 
    def save(self, **kwargs):
        try:
            RefreshToken(self.validated_data["refresh"]).blacklist()
        except TokenError:
            raise serializers.ValidationError({"refresh": "Invalid or expired token."})
 
 
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
 
    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
 
    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        if attrs["new_password"] == attrs["old_password"]:
            raise serializers.ValidationError(
                {"new_password": "New password must be different from the old one."}
            )
        validate_password(attrs["new_password"], self.context["request"].user)
        return attrs
 
    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        # sign out every device: blacklist all refresh tokens of this user
        for token in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=token)
        return user