from rest_framework import permissions

class IsBuyerOrAdminCreateOnly(permissions.BasePermission):
    """
    - Buyers can create orders
    - Admin can create orders
    - Sellers cannot create orders
    - Only order owner or admin can edit/view specific order
    """

    def has_permission(self, request, view):

        # Allow read-only if authenticated
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Only buyers or admin can create
        if request.method == "POST":
            return request.user.role in ["buyer", "admin"]

        return False

    def has_object_permission(self, request, view, obj):

        # Admin can access anything
        if request.user.role == "admin":
            return True

        # Buyer can only access their own order
        if request.user.role == "buyer" and obj.buyer == request.user:
            return True

        return False
