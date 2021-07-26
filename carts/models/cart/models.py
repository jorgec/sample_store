from django.apps import apps
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields

from carts.models.cart.constants import CartStateConstants
from common_core.models import AuditBase, IdentityBase
from common_core.models.meta import MetaBase


class Cart(IdentityBase, AuditBase, MetaBase):
    status = models.CharField(
        choices=CartStateConstants.LIST,
        default=CartStateConstants.OPEN,
        max_length=20
    )

    # === Relationship Fields ===
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='user_carts'
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    ################################################################################
    # === Magic Methods ===
    ################################################################################
    def __str__(self):
        return f"{self.user}'s cart"

    ################################################################################
    # === Properties ===
    ################################################################################
    @property
    def product_count(self):
        return self.cart_items.count()

    @property
    def total_items(self):
        return sum([item.quantity for item in self.cart_items.all()])

    @property
    def total_price(self):
        return sum([item.subtotal for item in self.cart_items.all()])

    @property
    def total_price_repr(self):
        return "{:,}".format(self.total_price)
