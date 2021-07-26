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

from common_core.queryset.filtered_queryset import filtered_queryset
from products.models import Product


class ProductPublicListView(View):
    def get(self, request, *args, **kwargs):
        querystring = {key: val for key, val in request.GET.items()}

        if "page" in querystring:
            del (querystring["page"])

        obj_list = filtered_queryset(Product, querystring)

        paginator = Paginator(obj_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        urlparams = urllib.parse.urlencode(querystring)

        context = {
            "page_obj": page_obj,
            "page_title": "Products",
            "urlparams": urlparams,
            "querystring": querystring,
        }

        return render(request, "products/public/list.html", context)
