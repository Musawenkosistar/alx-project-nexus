from rest_framework import permissions

class IsSellerOrAdmin(permissions.BasePermission):
    """
    Allow sellers to edit only their own products, admins can do anything.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_staff:
            return True

        # Sellers can only edit their own products
        if hasattr(obj, 'seller'):
            return obj.seller == request.user
        return False


class IsBuyerOrAdmin(permissions.BasePermission):
    """
    Allow buyers to create orders only, admins can do anything.
    """

    def has_permission(self, request, view):
        # Admins can do anything
        if request.user.is_staff:
            return True

        # Buyers can create orders
        if request.method == 'POST':
            return request.user.role == 'buyer'
        # Other methods are restricted
        return False

    def has_object_permission(self, request, view, obj):
        # Buyers can see their own orders, admins can see all
        if request.user.is_staff:
            return True
        if hasattr(obj, 'buyer'):
            return obj.buyer == request.user
        return False
