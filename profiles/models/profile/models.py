from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields

from common_core.models import AuditBase, IdentityBase
from common_core.models.meta import MetaBase
from profiles.models.profile.managers import GenderManager, ProfileManager


class Gender(IdentityBase, AuditBase, MetaBase):
    name = models.CharField(max_length=32, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)

    objects = GenderManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Profile(IdentityBase, AuditBase, MetaBase):
    # Fields
    first_name = models.CharField(max_length=32, blank=False, null=True, default='')
    middle_name = models.CharField(max_length=32, blank=True, null=True, default='')
    last_name = models.CharField(max_length=32, blank=False, null=True, default='')
    date_of_birth = models.DateField(default=None, blank=True, null=True)

    # Relationship Fields
    gender = models.ForeignKey(Gender, related_name='gender_profiles', on_delete=models.SET_NULL, null=True, blank=True)
    account = models.OneToOneField(
        'accounts.Account',
        on_delete=models.CASCADE,
    )

    objects = ProfileManager()

    class Meta:
        ordering = ('last_name', 'first_name')

    def __str__(self):
        return self.get_full_name()

    def get_casual_name(self):
        if self.first_name != '':
            return self.first_name
        return 'Unnamed'

    def get_name(self):
        if self.first_name != '' and self.last_name != '':
            return '{} {}'.format(
                self.first_name, self.last_name
            )
        else:
            if self.account.username is not None:
                return self.account.username
            return self.account.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return '{}, {}'.format(
                self.last_name, self.first_name
            )
        else:
            try:
                if self.account.username is not None:
                    return self.account.username
            except AttributeError:
                return 'Unnamed'
            return 'Unnamed'

    def get_username(self):
        try:
            return self.account.username
        except AttributeError:
            return self.account.id

    def get_photo(self):
        ProfilePhoto = apps.get_model('profiles.ProfilePhoto')
        try:
            return ProfilePhoto.objects.get(profile=self, is_primary=True)
        except ProfilePhoto.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return ProfilePhoto.objects.filter(profile=self, is_primary=True).first()


################################################################################
# === Signals ===
################################################################################
@receiver(post_save, sender=Profile)
def scaffold_post_save(sender, instance=None, created=False, **kwargs):
    pass


@receiver(pre_save, sender=Profile)
def scaffold_pre_save(sender, instance=None, created=False, **kwargs):
    pass
