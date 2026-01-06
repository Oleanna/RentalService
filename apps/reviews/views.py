from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer
from apps.listings.models import Listing
from django.shortcuts import get_object_or_404

class CreateReviewAPIView(CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["listing"] = get_object_or_404(
            Listing, id=self.kwargs["listing_id"], is_active=True
        )
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            listing=self.get_serializer_context()["listing"]
        )

class ListingReviewsAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        listing = get_object_or_404(Listing, id=self.kwargs["listing_id"])

        if not listing.is_active:
            raise ValidationError("Listing not found")

        return Review.objects.filter(listing=listing)