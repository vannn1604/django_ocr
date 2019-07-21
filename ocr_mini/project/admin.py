from django.contrib import admin

from .models import Image, Project

# Register your models here.
admin.site.register(Project)
admin.site.register(Image)
