from common_core.models import IdentityBase, AuditBase
from common_core.models.meta import MetaBase
from django.db import models


class ProductInventory(IdentityBase, AuditBase, MetaBase):
    quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)

    # Relations
    product = models.OneToOneField(
        'products.Product',
        on_delete=models.CASCADE,
        related_name="product_inventory"
    )

    def reduce(self, quantity):
        if quantity > self.quantity:
            quantity = self.quantity

        self.quantity = self.quantity - quantity
        self.save(force_update=True)
