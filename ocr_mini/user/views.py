from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from project.models import Project

from .forms import UserChangeForm

# Create your views here.


def session_check(request):
    if request.session.has_key("username"):
        return redirect("home")
    return redirect("login")


def user_change(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Profile Successfully!")
            return redirect("home")
    form = UserChangeForm()
    return render(request, "user/user-change.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    form = UserCreationForm()
    return render(request, "user/register.html", {"form": form})


@login_required
def profile(request):
    request.session["username"] = request.user.username
    profile = {
        "email": request.user.email,
        "username": request.user.username,
        "firstname": request.user.first_name,
        "lastname": request.user.last_name,
    }
    return render(request, "user/home.html", profile)
