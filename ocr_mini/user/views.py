from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from project.models import Project
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ChangeUser
# Create your views here.


def checkSession(request):
    if request.session.has_key('username'):
        return redirect('home')
    return redirect('login')

def changeUser(request):
    if request.method == "POST":
        form = ChangeUser(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = ChangeUser()
    return render(request, 'user/changeuser.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})


@login_required
def profile(request):
    request.session['username'] = request.user.username
    profile = {
        'email': request.user.email,
        'username': request.user.username,
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
    }
    return render(request, 'user/home.html', profile)
    






