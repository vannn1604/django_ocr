from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from . import views

urlpatterns = [
    path('', views.checkSession, name='checksession'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='home'),
    path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('password/', PasswordChangeView.as_view(success_url=reverse_lazy('home')), name='changepassword'),
    path('changeuser/', views.changeUser, name='changeuser'),
]