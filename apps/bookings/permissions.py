from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from apps.bookings.models import Booking
from common.enums.roles_user import Roles


class IsBookingLandlordOwner(BasePermission):
   def has_object_permission(self, request: Request, view, obj: Booking,) -> bool:
        return (
            request.user.is_authenticated
            and request.user.role == Roles.LANDLORD.value
            and obj.listing.landlord_id == request.user.id
        )


class CanCancelBooking(BasePermission):
    def has_object_permission(self, request: Request, view, obj: Booking,) -> bool:
        return (
            request.user.is_authenticated
            and request.user.role == Roles.RENTER.value
            and obj.renter_id == request.user.id
        )

class IsRenter(BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return (
            request.user.is_authenticated
            and request.user.role == Roles.RENTER.value
        )
