from django.urls import path
from apps.reviews.views import CreateReviewAPIView, ListingReviewsAPIView

urlpatterns = [
    path("<int:listing_id>/", ListingReviewsAPIView.as_view()),
    path("<int:listing_id>/create/", CreateReviewAPIView.as_view()),
]