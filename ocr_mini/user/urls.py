from django.contrib.auth import views as views_auth
from django.urls import include, path, reverse_lazy

from . import views

urlpatterns = [
    path("", views.session_check, name="session_check"),
    path(
        "login/",
        views_auth.LoginView.as_view(template_name="user/login.html"),
        name="login",
    ),
    path("register/", views.register, name="register"),
    path("accounts/profile/", views.profile, name="home"),
    path(
        "logout/",
        views_auth.LogoutView.as_view(template_name="user/logout.html"),
        name="logout",
    ),
    path(
        "password/",
        views_auth.PasswordChangeView.as_view(success_url=reverse_lazy("home")),
        name="password_change",
    ),
    path("change-user/", views.user_change, name="user_change"),
]
