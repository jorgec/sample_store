from django.apps import apps
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields

from carts.models.cart.constants import CartStateConstants
from checkouts.models.checkout.constants import CheckoutPaymentStatusConstants
from common_core.models import AuditBase, IdentityBase
from common_core.models.meta import MetaBase


class CheckoutItem(IdentityBase, AuditBase, MetaBase):
    product_name = models.CharField(max_length=128)
    product_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])

    # Relations
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )

    checkout = models.ForeignKey(
        'checkouts.Checkout',
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )

    class Meta:
        unique_together = ["checkout", "product"]

    ################################################################################
    # === Magic Methods ===
    ################################################################################
    def __str__(self):
        return self.product_name

    ################################################################################
    # === Properties ===
    ################################################################################
    @property
    def subtotal(self):
        return self.product_price * self.quantity

    @property
    def subtotal_repr(self):
        return "{:,}".format(self.subtotal)
