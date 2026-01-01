from rest_framework import serializers
from apps.listings.models import Listing

class ListingDetailSerializer(serializers.ModelSerializer):#deteil
    class Meta:
        model = Listing
        fields = "__all__"
        read_only_fields = [
            "landlord",
            "created_at",
            "updated_at"
        ]

class ListingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "title",
            "location",
            "price",
        ]

class ListingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "location",
            "price",
            "rooms",
            "property_type",
            "is_active"
        ]
        read_only_fields = ["id", ]