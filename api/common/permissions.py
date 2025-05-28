from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsInGroup(BasePermission):
    """
    Checks if the user belongs to one of the required groups.

    This class provides a method to determine whether a user is a member of
    specific groups required for accessing a view. It extends the BasePermission
    class from Django's permissions system. The permission check ensures that the
    user is authenticated and belongs to at least one of the allowed groups
    specified by the view's 'required_groups' attribute.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        allowed_groups = getattr(view, "required_groups", [])
        return request.user.groups.filter(name__in=allowed_groups).exists()