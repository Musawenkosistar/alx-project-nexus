from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsSellerOwnerOrAdmin

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSellerOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user

        # Admin sees everything
        if user.role == "admin":
            return Product.objects.all()

        # Seller sees only their products
        if user.role == "seller":
            return Product.objects.filter(seller=user)

        # Buyer sees all products (read-only)
        if user.role == "buyer":
            return Product.objects.all()

        return Product.objects.none()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
