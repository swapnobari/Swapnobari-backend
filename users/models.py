from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from api.validators import IMAGE_VALIDATORS, validate_bd_phone
 
from .manager import UserManager
 
 
class User(AbstractUser):
    """
    Admin account. Logs in with email + password.
    Admin = is_staff and is_active. Visitors never have an account.
    """
 
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
 
    email = models.EmailField(
        unique=True,
        error_messages={"unique": "An account with this email already exists."},
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, validators=[validate_bd_phone])
    avatar = CloudinaryField(
        "swapnobari/users/",
        blank=True,
        null=True,
        validators=IMAGE_VALIDATORS,
    )
 
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]
 
    objects = UserManager()
 
    class Meta:
        ordering = ["-date_joined"]
 
    def __str__(self):
        return self.email
 
    def get_full_name(self):
        return self.full_name
 
    def get_short_name(self):
        return self.full_name.split(" ")[0] if self.full_name else self.email