import random
from products.models import Product


def create_dummy_products(quantity: int = 10) -> None:
    for i in range(quantity):
        price = random.randrange(100, 10000)
        Product.objects.create(
            name=f"Product {i}",
            price=price
        )
