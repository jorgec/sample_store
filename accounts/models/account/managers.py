import string

import random
from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import IntegrityError
from django.db.models import QuerySet


class AccountQuerySet(QuerySet):
    def actives(self):
        return self.filter(is_active=True)


class AccountManager(BaseUserManager):
    def actives(self):
        return AccountQuerySet(self.model, using=self._db).actives()

    def create_user(self, password, email, username=None):
        """
        Create base user
        :param email:
        :param username:
        :param password:
        :return: Account or False
        """
        email_validator = EmailValidator()
        try:
            email_validator(email)
            email = self.normalize_email(email)
        except ValidationError as e:
            raise ValidationError(e)

        reset_key = ''.join(random.choice(string.ascii_lowercase) for i in range(64))

        user = self.model(
            username=username,
            email=email,
            meta={
                "triggers": {
                    "fresh": True
                },
                "reset_key": reset_key
            }
        )

        user.set_password(password)

        UserGroup = apps.get_model('accounts.UserGroup')
        GroupMembership = apps.get_model('accounts.GroupMembership')

        try:
            customer_group = UserGroup.objects.get(slug='customers')
        except UserGroup.DoesNotExist:
            customer_group = UserGroup.objects.create(
                slug='customers',
                name='Customers',
            )

        user.save(using=self._db)
        try:
            GroupMembership.objects.create(
                account=user,
                group=customer_group,
                is_owner=False
            )
        except IntegrityError:
            pass
        return user

    def create_superuser(self, username, password, email):
        user = self.create_user(
            username=username,
            password=password,
            email=email,
        )
        user.is_admin = True

        UserGroup = apps.get_model('accounts.UserGroup')
        GroupMembership = apps.get_model('accounts.GroupMembership')

        try:
            su_group = UserGroup.objects.get(slug='superusers')
        except UserGroup.DoesNotExist:
            su_group = UserGroup.objects.create(
                slug='superusers',
                name='Super Users',
            )

        user.save(using=self._db)

        try:

            is_owner = GroupMembership.objects.filter(is_owner=True).count() == 0

            GroupMembership.objects.create(
                account=user,
                group=su_group,
                is_owner=is_owner
            )
        except IntegrityError:
            pass

        return user
