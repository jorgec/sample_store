from django.urls import path
from .restapi import main as api_urls

urlpatterns = [
    path("", api_urls.CartAPI.as_view(), name="cart_api"),
]
