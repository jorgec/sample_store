"""
ICONS Directory
Profile 0.1
Profile Photo models
Profile Photo

Author: Jorge Cosgayon
"""

import uuid as uuid

from django.db import models as models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from common_core.models import AuditBase, IdentityBase
from common_core.models.meta import MetaBase
from .managers import ProfilePhotoManager as manager


def photo_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4(), ext)
    return 'uploads/{}/profile_photos/{}'.format(
        instance.profile.get_username(),
        filename
    )


class ProfilePhoto(IdentityBase, AuditBase, MetaBase):
    """
    Profile - Defines models for Profile

    Inherited fields:
    - AuditBase
    --- created
    --- updated
    --- created_by
    --- last_updated_by
    - IdentityBase
    --- uuid

    State/meta fields:
    - is_active
    - meta

    Identifier fields:
    -

    Property fields:
    -

    Relationship fields:
    -

    Methods:
    - 

    Signals:
    - Pre Save
    ---
    
    - Post Save
    --- 
    """

    # === Identifiers ===

    # === Properties ===
    photo = models.ImageField(upload_to=photo_upload_path, max_length=2048, null=True, default=None, blank=False)
    caption = models.TextField(max_length=500, default='', null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    # === State ===
    is_active = models.BooleanField(default=True)

    # === Relationship Fields ===
    profile = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='profile_photos'
    )

    objects = manager()

    class Meta:
        ordering = ('-is_primary', '-created',)
        verbose_name = 'Profile Photo'
        verbose_name_plural = 'Profile Photos'

    ################################################################################
    # === Magic Methods ===
    ################################################################################
    def __str__(self):
        if self.caption:
            return self.caption
        return self.id

    ################################################################################
    # === Model overrides ===
    ################################################################################
    def clean(self, *args, **kwargs):
        # add custom validation here
        super().clean()

    def save(self, *args, **kwargs):
        # self.full_clean()
        super().save(*args, **kwargs)

    ################################################################################
    # === Model-specific methods ===
    ################################################################################


################################################################################
# === Signals ===
################################################################################
@receiver(post_save, sender=ProfilePhoto)
def scaffold_post_save(sender, instance=None, created=False, **kwargs):
    pass


@receiver(pre_save, sender=ProfilePhoto)
def scaffold_pre_save(sender, instance=None, created=False, **kwargs):
    if instance.is_primary:
        ProfilePhoto.objects.filter(profile=instance.profile).exclude(
            pk=instance.pk
        ).update(
            is_primary=False
        )

################################################################################
# === Audit ===
################################################################################
