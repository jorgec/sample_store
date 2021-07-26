from django.db import models


class ThreadAwareBaseManager(models.Manager):
    """
    Abstract class with helper functions relating to request object
    """

    def all_by_current_user(self):
        from common_core.middleware.thread_local_middleware import get_current_user
        user = get_current_user()
        if not user:
            return []

        queryset = super().get_queryset()

        try:
            if user.is_admin:
                return queryset
            return queryset.filter(created_by=user.pk)
        except AttributeError:
            return []
