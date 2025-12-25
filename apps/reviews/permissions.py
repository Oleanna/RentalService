from __future__ import annotations

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReviewAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return obj.user_id == request.user.id