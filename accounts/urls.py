from django.urls import path, include

urlpatterns = [
    path('', include("accounts.controllers.account.urls")),
]
