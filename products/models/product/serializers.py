from rest_framework import serializers
from .models import Product
from .. import ProductInventory


class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField('repr_stock')

    def repr_stock(self, obj):
        try:
            inv = ProductInventory.objects.get(product=obj)
        except ProductInventory.DoesNotExist:
            inv = ProductInventory.objects.create(
                product=obj,
                quantity=1000
            )
        return inv.quantity

    class Meta:
        model = Product
        fields = '__all__'
