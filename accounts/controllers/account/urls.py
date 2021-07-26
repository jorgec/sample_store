from django.urls import path

from .views import main as view_urls


urlpatterns = [
    path("logout", view_urls.AccountLogoutView.as_view(), name="logout"),
    path("login", view_urls.AccountLoginView.as_view(), name="login"),
    path("login/", view_urls.AccountLoginView.as_view(), name="login_"),
    path("postlogin", view_urls.AccountPostLoginView.as_view(), name="postlogin"),
    path("register", view_urls.AccountRegisterView.as_view(), name="register"),
]