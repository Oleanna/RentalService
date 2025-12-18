from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from common.enums import Roles
from .models import Listing


class ListingPermission(BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return (request.user
                and request.user.is_authenticated
                and request.user.role == Roles.LANDLORD.value)



    def has_object_permission(self, request: Request, view, obj: Listing) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.landlord_id == request.user.id
