from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from accounts.models.account.constants import ADMIN_URL
from accounts.models.account.forms import LoginForm, RegistrationForm


class AccountPostLoginView(View):
    """
    Post-login actions performed after authentication by allauth
    Place all user-type specific actions here (e.g. redirections, logging)
    """

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_admin:
                return HttpResponseRedirect(ADMIN_URL)
            else:
                return HttpResponseRedirect(reverse("event_list"))
        except AttributeError:
            return HttpResponseRedirect(reverse("login"))


class AccountRegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()

        context = {
            "form": form
        }

        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('home'))
        else:
            context = {
                "form": form
            }

        return render(request, 'accounts/register.html', context)


class AccountLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("home"))


class AccountLoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()

        context = {
            "form": form
        }

        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if not user.is_active:
                    messages.error(
                        request, "User account is not active", extra_tags="warning"
                    )
                else:
                    login(request, user)
                    messages.success(request, f"Welcome, {user}!", extra_tags="success")

                    next = request.GET.get('next', None)
                    url = reverse('postlogin')
                    if next:
                        url += "?next=" + next
                    return HttpResponseRedirect(url)
            else:
                messages.error(request, "Invalid credentials", extra_tags="warning")
        else:
            messages.error(request, form.errors, extra_tags="warning")

        context = {
            "form": form,
        }
        return render(request, "accounts/login.html", context)
