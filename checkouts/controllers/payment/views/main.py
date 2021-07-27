import urllib.parse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View

from carts.models import Cart
from carts.utils.cart.cart_manager import CartManager
from common_core.queryset.filtered_queryset import filtered_queryset


class CardEntryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "view_cart"

    def get(self, request, *args, **kwargs):
        cart_manager = CartManager()
        if not request.session.get(settings.CART_ID, None):
            cart_manager.create()

        cart_in_session = cart_manager.get_cart_in_session()

        try:
            cart_in_db = Cart.objects.get(id=cart_in_session['id'])
        except Cart.DoesNotExist:
            cart_manager.create()
            cart_in_db = cart_manager.get_cart_in_db()
        except TypeError:
            return HttpResponseRedirect(reverse('home'))

        if cart_in_db.cart_items.count() <= 0:
            return HttpResponseRedirect(reverse('home'))

        context = {
            "page_title": "Card Payment",
            "cart": cart_in_db
        }

        return render(request, "payments/card_entry.html", context)
