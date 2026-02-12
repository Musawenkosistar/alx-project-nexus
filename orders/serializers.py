from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    buyer_email = serializers.ReadOnlyField(source='buyer.email')

    class Meta:
        model = Order
        fields = ['id', 'product', 'product_name', 'buyer', 'buyer_email', 'quantity', 'total_price', 'status', 'created_at']
        read_only_fields = ['id', 'product_name', 'buyer_email', 'total_price', 'created_at']
