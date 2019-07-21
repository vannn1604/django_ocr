from django.contrib.auth import forms
from django.contrib.auth.models import User


class UserChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
