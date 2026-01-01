from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from apps.listings.filter import ListingFilter
from apps.listings.models import Listing
from apps.listings.serializers import ListingDetailSerializer, ListingListSerializer, ListingCreateUpdateSerializer
from apps.listings.permissions import ListingPermission

class ListingListAPIView(ListAPIView):
    serializer_class = ListingListSerializer
    permission_classes = (ListingPermission,)
    queryset = Listing.objects.select_related("landlord").filter(is_active=True)

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = ListingFilter

    search_fields = ["title", "description",]

    ordering_fields = ["price", "created_at"]
    ordering = ["-price"]

class ListingCreateAPIView(CreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingCreateUpdateSerializer
    permission_classes = (ListingPermission,)

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)

class ListingDetailManageAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.select_related("landlord")
    serializer_class = ListingCreateUpdateSerializer
    permission_classes = (ListingPermission,)
    lookup_field = "id"