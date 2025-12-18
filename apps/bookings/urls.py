from django.urls import path

from apps.bookings.views import (
    BookingListAPIView,
    BookingCreateAPIView,
    BookingConfirmAPIView,
    BookingCancelAPIView,
    BookingRejectAPIView,
)

urlpatterns = [
    path("", BookingListAPIView.as_view()),

    path("create/", BookingCreateAPIView.as_view()),

    path("<int:pk>/confirm/", BookingConfirmAPIView.as_view()),
    path("<int:pk>/cancel/", BookingCancelAPIView.as_view()),
    path("<int:pk>/reject/", BookingRejectAPIView.as_view()),
]