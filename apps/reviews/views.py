from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer
from apps.listings.models import Listing

class CreateReviewAPIView(CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["listing_id"] = self.kwargs.get("listing_id")
        return context

    def perform_create(self, serializer):
        listing = Listing.objects.get(id=self.kwargs["listing_id"])
        serializer.save(user=self.request.user, listing=listing)

class ListingReviewsAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        listing_id = self.kwargs.get("listing_id")
        return Review.objects.filter(listing_id=listing_id)