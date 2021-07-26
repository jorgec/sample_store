from django.urls import path

from profiles.controllers.views import profile_views
from profiles.controllers.restapi.profile import api as profile_api
from profiles.controllers.restapi.profile_photo import api as profile_photo_api

urlpatterns = [
    path('', profile_views.ProfileHomeView.as_view(), name='profile_home_view'),
    path('update/', profile_views.ProfileUpdateView.as_view(), name='profile_update_view'),
    path('account/update/', profile_views.AccountUpdateView.as_view(), name='account_update_view'),
    path('account/password/', profile_views.AccountPasswordUpdateView.as_view(), name='account_password_view'),
]

urlpatterns += [
    path(
        "api/v1/<profile>",
        profile_api.ProfileAPIViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
            'post': 'create'
        }),
        name='profile_api'
    ),
    path(
        "api/v1/<profile>/photos",
        profile_photo_api.ProfilePhotoAPI.as_view({
            'get': 'list',
            'patch': 'partial_update',
            'delete': 'destroy',
            'post': 'create'
        }),
        name='profile_photo_api'
    )

]
