from django.urls import include, path

urlpatterns = [
    path("", include("products.controllers.products.urls"))
]