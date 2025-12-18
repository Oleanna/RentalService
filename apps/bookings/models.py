from django.db import models
from apps.users.models import User
from apps.listings.models import Listing
from common.enums.status_booking import BookingStatus


class Booking(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    renter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices(),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "booking"
        unique_together = ("listing", "renter", "check_in", "check_out")


    def __str__(self):
        return f"Booking {self.renter.email} | {self.listing.title}"
