from datetime import datetime

from django.conf import settings
from django.db import models

# Create your models here.


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="New Project")
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)


class Image(models.Model):
    title = models.CharField(max_length=255, default="")
    source = models.ImageField(upload_to="%Y/%m/%d", null=True, blank=True)
    auto_OCR = models.BooleanField(default=True)
    timing = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
