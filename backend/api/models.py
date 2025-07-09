from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, display_name, password, **extra_fields):
        """
        A helper function to create the user

        Args:
            email (str): the user's email
            display_name (str): the user's display name
            password (str): the user's password
        """
        if not display_name:
            raise ValueError("A display name must be set.")
        if not email:
            raise ValueError("An email must be set.")
        if not password:
            raise ValueError("A password must be set.")

        email = self.normalize_email(email)
        display_name = self.model.normalize_username(display_name)
        user = self.model(email=email, display_name=display_name, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, display_name, password, **extra_fields):
        """
        A function that creates a regular(non super) user

        Args:
            email (str): the user's email
            display_name (str): the user's display name
            password (str): the user's password
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, display_name, password, **extra_fields)

    def create_superuser(self, email, display_name, password, **extra_fields):
        """
        A function that creates a super user

        Args:
            email (str): the user's email
            display_name (str): the user's display name
            password (str): the user's password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, display_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Users in this app are represented by this model.

    email, display_name and password are all required.
    """

    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        ("email address"),
        unique=True,
        error_messages={
            "unique": ("An email with that username already exists."),
        },
    )  # email used for authentication

    display_name = models.CharField(
        ("display name"),
        max_length=150,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
    )  # display name

    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["display_name"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        """Returns the user's display name"""
        return self.display_name

    def clean(self):
        """Calls the normalize function on the email and display_name"""
        setattr(self, self.USERNAME_FIELD, self.normalize_email(self.get_username()))
        self.display_name = self.normalize_username(self.display_name)

