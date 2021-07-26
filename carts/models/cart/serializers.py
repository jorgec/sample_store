from rest_framework import serializers

from .models import Cart
from ..cart_item.serializers import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('repr_items')

    def repr_items(self, obj):
        return CartItemSerializer(obj.cart_items.all(), many=True).data

    class Meta:
        model = Cart
        fields = (
            'id',
            'status',
            'user',
            'product_count',
            'total_items',
            'total_price',
            'total_price_repr',
            'cart_items',
            'items'
        )

