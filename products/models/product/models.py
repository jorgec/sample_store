from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields

from common_core.models import AuditBase, IdentityBase
from common_core.models.meta import MetaBase


class Product(IdentityBase, AuditBase, MetaBase):
    name = models.CharField(max_length=128, unique=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    ################################################################################
    # === Properties ===
    ################################################################################
    @property
    def stock(self):
        try:
            return self.product_inventory.quantity
        except AttributeError:
            return 0

    ################################################################################
    # === Model-specific methods ===
    ################################################################################
    def get_price(self):
        """
        Tax computations, etc
        """

        return self.price


################################################################################
# === Signals ===
################################################################################
@receiver(post_save, sender=Product)
def scaffold_post_save(sender, instance=None, created=False, **kwargs):
    pass


@receiver(pre_save, sender=Product)
def scaffold_pre_save(sender, instance=None, created=False, **kwargs):
    pass
