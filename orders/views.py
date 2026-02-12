from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from .models import Order
from .serializers import OrderSerializer
from .permissions import IsBuyerOrAdminCreateOnly
from users.permissions import IsBuyerOrAdmin

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsBuyerOrAdminCreateOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']  # ?status=completed
    search_fields = ['product__name', 'buyer__email']

    def get_queryset(self):
        user = self.request.user
        if user.role == "seller":
            # Seller sees orders for their products only
            return Order.objects.filter(product__seller=user)
        elif user.role == "buyer":
            # Buyer sees their own orders only
            return Order.objects.filter(buyer=user)
        else:
            # Admin sees all orders
            return Order.objects.all()

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        # Check stock
        if product.stock_quantity < quantity:
            raise ValidationError("Not enough stock available.")

        # Reduce stock
        product.stock_quantity -= quantity
        product.save()

        # Assign logged-in buyer
        serializer.save(buyer=self.request.user)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def monthly_sales(request):
    """
    Returns monthly sales breakdown for all orders.
    """
    sales = (
        Order.objects
        .filter(status='completed')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_sales=Sum('total_price'))
        .order_by('month')
    )

    return Response(list(sales))
