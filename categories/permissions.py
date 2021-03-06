from rest_framework import permissions


class HasAdminRoleOrRead(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if (request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_superuser is True):
            return True
