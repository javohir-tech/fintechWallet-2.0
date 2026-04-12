# =================== PYTHON =====================
import uuid
from random import randint
from datetime import timedelta

# ================== DJANGO =====================
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import identify_hasher

# ================= SHARED ======================
from shared.models import BaseModel

# ================= REST FRAMEWORK ==============
from rest_framework_simplejwt.tokens import RefreshToken


def is_hashed(password):
    try:
        identify_hasher(password)
        return True
    except:
        return False


class AuthType(models.TextChoices):
    VIA_EMAIL = "via_email", "VIA EMAIL"
    VIA_PHONE = "via_phone", "VIA PHONE"


class AuthStatus(models.TextChoices):
    NEW = "new", "NEW"
    VERIFYED = "verifed", "VERIFED"
    DONE = "done", "DONE"
    PHOTO = "photo_done", "PHOTO DONE"
    LOGOUT = "logout", "LOGOUT"


class User(BaseModel, AbstractUser):

    email = models.EmailField(max_length=64, unique=True, null=True)
    phone_number = models.CharField(max_length=36, unique=True, null=True)
    avatar = models.ImageField(upload_to="users/avatar", null=True)
    auth_type = models.CharField(
        max_length=9, choices=AuthType.choices, default=AuthType.VIA_EMAIL
    )
    auth_status = models.CharField(
        max_length=10, choices=AuthStatus.choices, default=AuthStatus.NEW
    )

    def create_code(self, auth_type):
        UserConfirmation.objects.filter(user=self, is_confirmed=False).delete()
        
        while True:
            try :
                code = "".join([str(randint(1, 10000) % 10) for _ in range(4)])
                UserConfirmation.objects.create(user=self, code=code, auth_type=auth_type)
                return code
            except IntegrityError:
                continue
                



    def check_username(self):
        temp_user = f"wallet_username_{uuid.uuid4().__str__().split("=")[-1]}"

        while User.objects.filter(username=temp_user).exists():
            temp_user = f"{temp_user}{randint(1, 9)}"
            self.username = temp_user

    def check_password(self):
        temp_password = f"wallet_passsword_{uuid.uuid4().__str__().split("-")[-1]}"
        self.password = temp_password

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()
            self.email = normalize_email

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

    def password_hesh(self):
        if not is_hashed(self.password):
            self.set_password(self.password)

    def clean(self):
        self.check_password()
        self.check_username()
        self.check_email()
        self.password_hesh()

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.clean()
        else:
            self.check_email()

            if self.password and not is_hashed(self.password):
                self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email or self.phone_number


EXPIRE_EMAIL = 5
EXPIRE_PHONE = 2


class UserConfirmation(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="verify_codes"
    )
    auth_type = models.CharField(
        max_length=9, choices=AuthType.choices, default=AuthType.VIA_EMAIL
    )
    code = models.CharField(max_length=4)
    expire_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.auth_type == AuthType.VIA_EMAIL:
                self.expire_time = timezone.now() + timedelta(minutes=EXPIRE_EMAIL)
            elif self.auth_type == AuthType.VIA_PHONE:
                self.expire_time = timezone.now() + timedelta(minutes=EXPIRE_PHONE)

        super().save(*args, **kwargs)

    def check_expire(self):
        if self.check_expire is None:
            return True

        return timezone.now() > self.expire_time

    def can_verify(self):

        if self.expire_time():
            return False
        if self.is_confirmed:
            return False

        return True

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "code"],
                condition=Q(is_confirmed=True),
                name="unique_used_code_per_user",
            )
        ]


# Create your models here.
