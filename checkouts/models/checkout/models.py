from django.apps import apps
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields

from carts.models.cart.constants import CartStateConstants
from checkouts.models.checkout.constants import CheckoutPaymentStatusConstants, CheckoutStatusConstants
from common_core.models import AuditBase, IdentityBase
from common_core.models.meta import MetaBase


class Checkout(IdentityBase, AuditBase, MetaBase):
    payment_status = models.CharField(choices=CheckoutPaymentStatusConstants.LIST,
                                      default=CheckoutPaymentStatusConstants.PROCESSING, max_length=32)
    status = models.CharField(choices=CheckoutStatusConstants.LIST, default=CheckoutStatusConstants.OPEN, max_length=32)

    # Relations
    cart = models.ForeignKey(
        'carts.Cart',
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )

    user = models.ForeignKey(
        'accounts.Account',
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )
