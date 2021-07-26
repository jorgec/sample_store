from rest_framework import serializers

from products.models.product.serializers import ProductSerializer
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = (
            'id',
            'quantity',
            'product',
            'subtotal',
            'subtotal_repr'
        )
