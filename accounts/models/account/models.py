"""
Account model

---
Jorge Cosgayon
"""
import logging

from django.apps import apps
from django.contrib.auth.models import (
    AbstractBaseUser, Group, Permission
)
from django.core.validators import RegexValidator
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from common_core.models import IdentityBase, AuditBase
from common_core.models.meta import MetaBase
from .constants import USERNAME_REGEX
from .managers import AccountManager

logger = logging.getLogger(__name__)


class Account(IdentityBase, AuditBase, MetaBase, AbstractBaseUser):
    """
    Base Account model
    Fields:
        - username: CharField
        - email: EmailField
        - is_active: BooleanField
        - is_admin: BooleanField
        - user_settings: JSONField
    """
    # Fields
    username = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username can only contain alphanumeric characters and the following characters: . -',
                code='Invalid Username'
            )
        ],
        unique=True,

    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=False
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perms):
        UserGroup = apps.get_model('accounts.UserGroup')

        if isinstance(perms, str):
            p = perms.split(",")
        elif isinstance(perms, Permission):
            p = [perms]
        elif isinstance(perms, tuple):
            p = perms
        else:
            raise TypeError("Must be a comma-separated string, tuple, or Permission object")

        has_permission = False

        for perm in p:
            if isinstance(p, Permission):
                groups = UserGroup.objects.filter(permissions=perm)
            else:
                groups = UserGroup.objects.filter(permissions__codename=perm)

            if self.groupmembership_set.filter(group__in=groups).count() > 0:
                has_permission = True
                break
        return has_permission

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        ordering = ('username', '-created',)

    ################################################################################
    # Model methods


@receiver(post_save, sender=Account)
def scaffold_account(sender, instance=None, created=False, **kwargs):
    if created:
        Profile = apps.get_model('profiles.Profile')
        Token.objects.create(user=instance)
        try:
            profile = Profile.objects.create(
                account=instance
            )
            logger.info(f"{profile} created for {instance}")
        except IntegrityError as e:
            logger.error(f"IntegriyError: {e} for {instance}")
            pass

