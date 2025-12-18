from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils import timezone
from apps.users.models import User
from common.enums.type_property import PropertyType


class Listing(models.Model):
    landlord = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)

    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    rooms = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    property_type = models.CharField(
        max_length=30,
        choices=PropertyType.choices(),
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'listings'

    def __str__(self):
        return f"{self.title} | {self.landlord}"