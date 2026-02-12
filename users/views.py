from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from users.models import User
from products.models import Product
from orders.models import Order
from django.db.models.functions import ExtractMonth, ExtractYear
from collections import OrderedDict

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):

    # Only admin allowed
    if request.user.role != "admin":
        return Response({"detail": "Not authorized."}, status=403)

    total_users = User.objects.count()
    total_buyers = User.objects.filter(role="buyer").count()
    total_sellers = User.objects.filter(role="seller").count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()

    total_sales = Order.objects.filter(status="completed").aggregate(
        total=Sum('total_price')
    )['total'] or 0

    data = {
        "total_users": total_users,
        "total_buyers": total_buyers,
        "total_sellers": total_sellers,
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_sales": total_sales
    }

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_sales(request):
    # Only admin allowed
    if request.user.role != "admin":
        return Response({"detail": "Not authorized."}, status=403)

    # Aggregate total sales by month and year
    sales_data = (
        Order.objects.filter(status="completed")
        .annotate(year=ExtractYear('created_at'), month=ExtractMonth('created_at'))
        .values('year', 'month')
        .annotate(total_sales=Sum('total_price'))
        .order_by('year', 'month')
    )

    # Format data for clarity
    result = []
    for entry in sales_data:
        result.append({
            "year": entry['year'],
            "month": entry['month'],
            "total_sales": float(entry['total_sales'])
        })

    return Response(result)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    # Only admin can access
    if request.user.role != "admin":
        return Response({"detail": "Not authorized."}, status=403)

    # Total counts
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_sales = Order.objects.filter(status="completed").aggregate(
        total_sales=Sum('total_price')
    )['total_sales'] or 0.0

    # Monthly sales breakdown
    sales_data = (
        Order.objects.filter(status="completed")
        .annotate(year=ExtractYear('created_at'), month=ExtractMonth('created_at'))
        .values('year', 'month')
        .annotate(total_sales=Sum('total_price'))
        .order_by('year', 'month')
    )

    monthly_sales = []
    for entry in sales_data:
        monthly_sales.append({
            "year": entry['year'],
            "month": entry['month'],
            "total_sales": float(entry['total_sales'])
        })

    # Combine into a single response
    dashboard = {
        "total_users": total_users,
        "total_products": total_products,
        "total_sales": float(total_sales),
        "monthly_sales": monthly_sales
    }

    return Response(dashboard)
