from rest_framework import permissions

class IsSellerOwnerOrAdmin(permissions.BasePermission):
    """
    - Admin can do anything
    - Seller can edit/delete only their own products
    - Buyers can only read
    """

    def has_permission(self, request, view):
        # Allow read-only requests for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Must be authenticated for write actions
        if not request.user.is_authenticated:
            return False

        # Admin can do anything
        if request.user.role == "admin":
            return True

        # Sellers can create products
        if request.method == "POST" and request.user.role == "seller":
            return True

        return True

    def has_object_permission(self, request, view, obj):
        # Allow read-only
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admin can edit anything
        if request.user.role == "admin":
            return True

        # Seller can only edit their own product
        if request.user.role == "seller" and obj.seller == request.user:
            return True

        return False
