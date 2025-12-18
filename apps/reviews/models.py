from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.users.models import User
from apps.listings.models import Listing


class Review(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review {self.rating} for {self.listing.title}"