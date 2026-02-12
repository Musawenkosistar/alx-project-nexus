import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created/Updated: {path}")

# ----------------------------
# USERS SERIALIZER
# ----------------------------
users_serializer = """from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_active', 'is_staff', 'created_at']
        read_only_fields = ['id', 'created_at']
"""
write_file(os.path.join(BASE_DIR, "users", "serializers.py"), users_serializer)

# ----------------------------
# PRODUCTS SERIALIZER
# ----------------------------
products_serializer = """from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    seller_email = serializers.ReadOnlyField(source='seller.email')

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock_quantity', 'seller', 'seller_email']
        read_only_fields = ['id', 'seller_email']
"""
write_file(os.path.join(BASE_DIR, "products", "serializers.py"), products_serializer)

# ----------------------------
# ORDERS SERIALIZER
# ----------------------------
orders_serializer = """from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    buyer_email = serializers.ReadOnlyField(source='buyer.email')

    class Meta:
        model = Order
        fields = ['id', 'product', 'product_name', 'buyer', 'buyer_email', 'quantity', 'total_price', 'status', 'created_at']
        read_only_fields = ['id', 'product_name', 'buyer_email', 'total_price', 'created_at']
"""
write_file(os.path.join(BASE_DIR, "orders", "serializers.py"), orders_serializer)

# ----------------------------
# USERS VIEW
# ----------------------------
users_view = """from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
"""
write_file(os.path.join(BASE_DIR, "users", "views.py"), users_view)

# ----------------------------
# PRODUCTS VIEW
# ----------------------------
products_view = """from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
"""
write_file(os.path.join(BASE_DIR, "products", "views.py"), products_view)

# ----------------------------
# ORDERS VIEW
# ----------------------------
orders_view = """from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
"""
write_file(os.path.join(BASE_DIR, "orders", "views.py"), orders_view)

# ----------------------------
# PROJECT URLS
# ----------------------------
project_name = "LibraryProject"  # Change if your project folder name is different

urls_content = f"""from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from products.views import ProductViewSet
from orders.views import OrderViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
"""
write_file(os.path.join(BASE_DIR, project_name, "urls.py"), urls_content)

print("\\nStep 6 setup complete ✅")
