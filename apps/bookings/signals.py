from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.bookings.models import Booking
from common.enums import BookingStatus


@receiver(post_save, sender=Booking)
def cancel_overlapping_bookings(sender, instance: Booking, created, **kwargs):
    if instance.status != BookingStatus.CONFIRMED.value:
        return

    Booking.objects.filter(
        listing=instance.listing,
        status=BookingStatus.PENDING.value,
        check_in__lt=instance.check_out,
        check_out__gt=instance.check_in,
    ).exclude(id=instance.id).update(
        status=BookingStatus.CANCELED.value
    )
