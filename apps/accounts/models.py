from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier for auth."""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        ADMIN = 'admin', 'Store Administrator'

    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField('email address', unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    # Shipping profile fields
    phone_number = models.CharField(max_length=20, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True, verbose_name="County / Sector")
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=60, default='Romania')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email.split('@')[0]

    @property
    def is_store_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
