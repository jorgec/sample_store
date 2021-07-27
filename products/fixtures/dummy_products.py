import random
from products.models import Product, ProductInventory


def create_dummy_products(quantity: int = 10) -> None:
    for i in range(quantity):
        price = random.randrange(100, 10000)
        Product.objects.create(
            name=f"Product {i}",
            price=price
        )


def add_inventory():
    for p in Product.objects.all():
        try:
            inv = ProductInventory.objects.get(product=p)
            inv.quantity = 1000
            inv.save()
        except ProductInventory.DoesNotExist:
            inv = ProductInventory.objects.create(
                product=p,
                quantity=1000
            )
