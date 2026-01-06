from typing import Any

from rest_framework import serializers
from apps.bookings.models import Booking
from django.utils import timezone

from datetime import date

from common.enums import BookingStatus


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

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        check_in = attrs["check_in"]
        check_out = attrs["check_out"]
        listing = attrs["listing"]

        now = timezone.now()

        if check_in < now or check_out < now:
            raise serializers.ValidationError(
                "Check-in and check-out cannot be in the past."
            )

        if check_in >= check_out:
            raise serializers.ValidationError(
                "Check-out date must be later than check-in date."
            )

        overlapping_booking = Booking.objects.filter(
            renter=user,
            listing=listing,
            status__in=[
                BookingStatus.PENDING.value,
                BookingStatus.CONFIRMED.value,
            ],
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()

        if overlapping_booking:
            raise serializers.ValidationError(
                "You already have a booking for this listing with overlapping dates."
            )

        return attrs