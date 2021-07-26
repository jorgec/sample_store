from django.apps import apps
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields

from carts.models.cart.constants import CartStateConstants
from common_core.models import AuditBase, IdentityBase
from common_core.models.meta import MetaBase


class CartItem(IdentityBase, AuditBase, MetaBase):
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])

    # === Relationship Fields ===
    cart = models.ForeignKey(
        'carts.Cart',
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='product_cart_items'
    )

    class Meta:
        ordering = ('cart', 'id')
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ("cart", "product")

    ################################################################################
    # === Magic Methods ===
    ################################################################################
    def __str__(self):
        return f"{self.product}"

    ################################################################################
    # === Properties ===
    ################################################################################
    @property
    def subtotal(self):
        return self.product.get_price() * self.quantity

    @property
    def subtotal_repr(self):
        return "{:,}".format(self.subtotal)