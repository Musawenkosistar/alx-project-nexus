from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    seller_email = serializers.ReadOnlyField(source='seller.email')

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock_quantity', 'seller', 'seller_email']
        read_only_fields = ['id', 'seller_email']
