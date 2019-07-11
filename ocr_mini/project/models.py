from django.db import models
from django.conf import settings
from datetime import datetime
# Create your models here.


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default='New Project')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    description = models.TextField(default='')


class Image(models.Model):
    auto_OCR = models.BooleanField(default=True)
    title = models.CharField(max_length=255, default='')
    source = models.ImageField(upload_to='%Y/%m/%d', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)