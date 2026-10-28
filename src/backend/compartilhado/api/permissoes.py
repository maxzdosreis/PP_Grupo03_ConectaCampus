from rest_framework.permissions import BasePermission


class ApenasGestor(BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request.user, "eh_gestor", False))
