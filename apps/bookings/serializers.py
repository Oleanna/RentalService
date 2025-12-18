from typing import Any

from rest_framework import serializers
from apps.bookings.models import Booking
from django.utils import timezone

from datetime import date

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "listing",
            "check_in",
            "check_out",
        ]
