from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from accounts.models import Account, UserGroup, GroupMembership
from .models.account.admin import UserAdmin

# Now register the new SubscriptionAdmin...
admin.site.register(Account, UserAdmin)
admin.site.register(UserGroup)
admin.site.register(GroupMembership)
admin.site.register(Permission)
# ... and, since we're not using Django's built-in permissions,
# unregister the UserGroup model from admin.
admin.site.unregister(Group)
