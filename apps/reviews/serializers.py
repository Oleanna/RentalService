from rest_framework import serializers
from django.utils import timezone
from apps.bookings.models import Booking
from apps.reviews.models import Review
from common.enums import BookingStatus


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("user", "listing", "created_at")

    def validate_rating(self, value: int) -> int:
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate(self, attrs):
        request = self.context["request"]
        listing_id = self.context["listing_id"]
        now = timezone.now()

        has_confirmed_booking = Booking.objects.filter(
            listing_id=listing_id,
            renter=request.user,
            status=BookingStatus.CONFIRMED.value,
            check_out__lt=now,
        ).exists()

        if not has_confirmed_booking:
            raise serializers.ValidationError(
                "You can leave a review only after the stay is finished."
            )

        return attrs