from django.db import models, IntegrityError
from django.db.models import QuerySet

from common_core.managers.thread_aware import ThreadAwareBaseManager


class ProfileQuerySet(QuerySet):
    def males(self):
        return self.filter(gender__name__iexact='male')

    def females(self):
        return self.filter(gender__name__iexact='female')


class ProfileManager(models.Manager):

    def males(self):
        return ProfileQuerySet().males()

    def females(self):
        return ProfileQuerySet().females()

    def create(self, *args, **kwargs):
        if 'account' in kwargs:
            try:
                profile = self.get(account=kwargs['account'])
                return profile
            except self.model.DoesNotExist:
                return super(ProfileManager, self).create(*args, **kwargs)
            except KeyError:
                return super(ProfileManager, self).create(*args, **kwargs)
        return super(ProfileManager, self).create(*args, **kwargs)


class GenderManager(ThreadAwareBaseManager):
    def create(self, *args, **kwargs):
        try:
            return super().create(*args, **kwargs)
        except IntegrityError:
            return self.get(name=kwargs.get('name'))
