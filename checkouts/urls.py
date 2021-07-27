from django.urls import path

from checkouts.controllers.payment.views import main as payment_views
from checkouts.controllers.checkout.views import main as checkout_views

urlpatterns = [
    path("payments/card", payment_views.CardEntryView.as_view(), name="card_payments"),

    path("success", checkout_views.CheckoutSuccessView.as_view(), name="checkout_success"),
    path("list", checkout_views.CheckoutListAllView.as_view(), name="checkout_list_all_view"),
]