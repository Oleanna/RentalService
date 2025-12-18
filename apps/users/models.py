from __future__ import annotations
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils import timezone

from common.enums.roles_user import Roles


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email", unique=True)
    first_name = models.CharField("first name", max_length=50)
    last_name = models.CharField("last name", max_length=50)
    role = models.CharField(
        max_length=50,
        choices=Roles.choices(),
        default=Roles.RENTER
        )
    birthday = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, region="DE")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    data_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email






