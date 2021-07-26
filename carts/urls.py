from django.urls import path, include


urlpatterns = [
    path("api/", include("carts.controllers.cart.urls")),
]