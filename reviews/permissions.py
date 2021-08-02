from rest_framework import permissions


class IsAuthorModeratorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        roles = ['moderator', 'admin']
        if (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role in roles):
            return True
