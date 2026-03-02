from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"


class IsUserRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "USER"