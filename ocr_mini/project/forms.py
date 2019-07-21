from .models import Project, Image
from django.forms import ModelForm
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = (
            'title',
            'description'
        )