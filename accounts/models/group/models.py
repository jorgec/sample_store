from django.contrib.auth.models import Permission
from django.db import models
from django_extensions.db.fields import AutoSlugField

from common_core.models import IdentityBase, AuditBase
from common_core.models.meta import MetaBase
from .managers import GroupManager


class UserGroup(IdentityBase, AuditBase, MetaBase):
    slug = AutoSlugField(unique=True, max_length=200, populate_from="name")
    name = models.CharField('name', max_length=150, unique=True)

    dashboard_url = models.CharField(blank=True, null=True, default=None, max_length=200)

    permissions = models.ManyToManyField(
        Permission,
        related_name='account_permissions',
        verbose_name='Account Permissions',
        blank=True,
    )

    objects = GroupManager()

    class Meta:
        verbose_name = 'Account UserGroup'
        verbose_name_plural = 'account groups'

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name,


class GroupMembership(IdentityBase, AuditBase, MetaBase):
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=False)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, null=False)
    is_owner = models.BooleanField(default=False)

    class Meta:
        unique_together = ['group', 'account']

    def __str__(self):
        return f"{self.group}: {self.account}"
