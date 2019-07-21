from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.project, name="project"),
    path("<int:project_id>/", views.project_detail, name="detailproject"),
    path("createproject/", views.project_create, name="createproject"),
    # path('creatingproject/', views.creatingproject, name='creatingproject'),
    path("<int:project_id>/editproject/", views.project_edit, name="editproject"),
    # path(
    #     "<int:project_id>/updatingproject/",
    #     views.project_update,
    #     name="updatingproject",
    # ),
    path("<int:project_id>/deleteproject/", views.project_delete, name="deleteproject"),
    path("<int:project_id>/image/", views.image, name="image"),
    path(
        "uploadingimage/<int:project_id>/", views.image_uploading, name="uploadingimage"
    ),
    path(
        "<int:project_id>/image/<int:image_id>/", views.image_detail, name="detailimage"
    ),
    path(
        "<int:project_id>/editimage/<int:image_id>/", views.image_edit, name="editimage"
    ),
    # path(
    #     "<int:project_id>/updateimage/<int:image_id>/",
    #     views.image_update,
    #     name="updateimage",
    # ),
    path(
        "<int:project_id>/deleteimage/<int:image_id>/",
        views.image_delete,
        name="deleteimage",
    ),
]
