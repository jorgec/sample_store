from django.urls import path
from .views import public

urlpatterns = [
    path("", public.ProductPublicListView.as_view(), name="products_public_list"),
]