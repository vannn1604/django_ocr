from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.project, name='project'),
    path('<int:project_id>/', views.detailProject, name='detailproject'),
    path('createproject/', views.createproject, name='createproject'),
    path('creatingproject/', views.creatingproject, name='creatingproject'),
    path('<int:project_id>/editproject/', views.editProject, name='editproject'),
    path('<int:project_id>/updatingproject/', views.updatingProject, name='updatingproject'),
    path('<int:project_id>/deleteproject/', views.deleteProject, name='deleteproject'),
    path('<int:project_id>/image/', views.image, name='image'),
    path('uploadingimage/<int:project_id>/', views.uploadingimage, name='uploadingimage'),
    path('<int:project_id>/image/<int:image_id>/', views.detailImage, name='detailimage'),
    path('<int:project_id>/editimage/<int:image_id>/', views.editImage, name='editimage'),
    path('<int:project_id>/updateimage/<int:image_id>/', views.updateImage, name='updateimage'),
    path('<int:project_id>/deleteimage/<int:image_id>/', views.deleteImage, name='deleteimage')
]