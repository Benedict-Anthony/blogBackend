from rest_framework import permissions

class IsAuthorORPubisher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_publisher:
                return True
            if obj.author == request.user:
                return True
            return False
        return False

class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if obj.author == request.user:
                return True
            return False
        return False