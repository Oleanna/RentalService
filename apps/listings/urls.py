from django.urls import path

from apps.listings.views import (
    ListingListAPIView,
    ListingCreateAPIView,
    ListingDetailManageAPIView,
)

urlpatterns = [
    path("", ListingListAPIView.as_view()),
    path("create/", ListingCreateAPIView.as_view()),
    path("<int:id>/", ListingDetailManageAPIView.as_view()),
]