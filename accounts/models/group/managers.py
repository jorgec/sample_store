from common_core.managers.thread_aware import ThreadAwareBaseManager


class GroupManager(ThreadAwareBaseManager):
    """
    The manager for the auth's UserGroup model.
    """
    use_in_migrations = True
