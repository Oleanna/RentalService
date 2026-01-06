from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.exceptions import ValidationError

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.bookings.models import Booking
from apps.bookings.permissions import IsRenter, IsBookingLandlordOwner, CanCancelBooking
from apps.bookings.serializers import BookingSerializer, BookingCreateSerializer
from common.enums import BookingStatus


class BookingListAPIView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Booking.objects.select_related("listing", "renter", "listing__landlord",)

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        if user.role == "renter":
            return qs.filter(renter=user)

        if user.role == "landlord":
            return qs.filter(listing__landlord=user)

        return qs.none()


class BookingCreateAPIView(CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = (IsAuthenticated, IsRenter)
    queryset = Booking.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            renter=self.request.user,
            status = BookingStatus.PENDING.value
        )


class BookingConfirmAPIView(UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated, IsBookingLandlordOwner)
    queryset = Booking.objects.select_related("listing__landlord")

    def update(self, request, *args, **kwargs):
        booking = self.get_object()

        if booking.status != BookingStatus.PENDING.value:
            raise ValidationError(
                "Only bookings with status PENDING can be confirmed"
            )

        booking.status = BookingStatus.CONFIRMED.value
        booking.save(update_fields=["status"])

        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_200_OK,
        )

class BookingCancelAPIView(UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated, CanCancelBooking)
    queryset = Booking.objects.select_related("renter")

    def update(self, request, *args, **kwargs):
        booking = self.get_object()

        if booking.status == BookingStatus.CANCELED.value:
            raise ValidationError("Booking already canceled")

        now = timezone.now()
        time_before_check_in = booking.check_in - now

        if time_before_check_in < timedelta(days=2):
            raise ValidationError(
                "Booking cannot be canceled less than 2 days before check-in."
            )

        booking.status = BookingStatus.CANCELED.value
        booking.save(update_fields=["status"])

        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_200_OK,
        )

class BookingRejectAPIView(UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated, IsBookingLandlordOwner,)
    queryset = Booking.objects.select_related("listing__landlord")

    def update(self, request, *args, **kwargs):
        booking = self.get_object()

        if booking.status != BookingStatus.PENDING.value:
            raise ValidationError(
                "Only bookings with status PENDING can be rejected"
            )

        booking.status = BookingStatus.CANCELED.value
        booking.save(update_fields=["status"])

        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_200_OK,
        )
