from django.db.models import QuerySet

from common_core.managers.thread_aware import ThreadAwareBaseManager


class ProfilePhotoQuerySet(QuerySet):
    def actives(self):
        return self.filter(is_active=True)

    def by_ref(self, ref: str, pk: str):
        filter = {
            f"{ref}__pk": pk
        }
        return self.filter(**filter)


class ProfilePhotoManager(ThreadAwareBaseManager):

    def actives(self):
        return ProfilePhotoQuerySet().actives()
    
    def by_ref(self, ref: str, pk: str):
        return ProfilePhotoQuerySet().by_ref(ref, pk)
    
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)
