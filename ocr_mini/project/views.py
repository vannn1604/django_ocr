import datetime
from .models import Project, Image
from .forms import ProjectForm

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from utils.ocr_utils import ocr


# import default libs
# import time, os

# import third party libs
# import django

# import self module
# from .models import *




# def upload_image()
# class ImageModel
def updateImage(request, project_id, image_id):
    if request.method == "POST":
        img = Image.objects.get(pk=image_id)
        img.title = request.POST["title"]
        img.auto_OCR = False
        img.save()
        project = Project.objects.get(pk=project_id)
        project.updated_at = datetime.datetime.now()
        project.save()
    return redirect("detailimage", project_id=project_id, image_id=image_id)


def deleteImage(request, project_id, image_id):
    Image.objects.get(pk=image_id).delete()
    project = Project.objects.get(pk=project_id)
    project.updated_at = datetime.datetime.now()
    project.save()
    return redirect("image", project_id)


def editImage(request, project_id, image_id):
    img = Image.objects.get(pk=image_id)
    image = {
        "title": img.title,
        "created_at": img.created_at,
        "updated_at": img.updated_at,
        "auto_OCR": img.auto_OCR,
        "source": img.source,
        "project": Project.objects.get(pk=project_id),
        "image_id": image_id,
        "username": request.user.username,
    }
    return render(request, "project/editimage.html", image)


def detailImage(request, project_id, image_id):
    img = Image.objects.get(pk=image_id)
    image = {
        "title": img.title,
        "created_at": img.created_at,
        "updated_at": img.updated_at,
        "auto_OCR": img.auto_OCR,
        "source": img.source,
        "project": Project.objects.get(pk=project_id),
        "image_id": image_id,
        "username": request.user.username,
    }
    return render(request, "project/detailimage.html", image)


def uploadingImage(request, project_id):
    if request.method == "POST" and "source" in request.FILES:
        for item in request.FILES.getlist('source'):
            title = ocr(item)
            image = Image(source=item, title=title, project_id=project_id)
            image.save()
        project = Project.objects.get(pk=project_id)
        project.updated_at = datetime.datetime.now()
        project.save()
    else:
        messages.warning(request, "You have not selected a file")
    return redirect("image", project_id=project_id)
# def uploadingImage(request, project_id):
#     if request.method == "POST" and "source" in request.FILES:
#         source = request.FILES["source"]
#         title = ocr(source)
#         image = Image(source=source, title=title, project_id=project_id)
#         image.save()
#         project = Project.objects.get(pk=project_id)
#         project.updated_at = datetime.datetime.now()
#         project.save()
#     else:
#         messages.warning(request, "You have not selected a file")
#     return redirect("image", project_id=project_id)


# def creatingproject(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         description = request.POST['description']
#         request.user.project_set.create(title=title, description=description, user_id=request.user.id)

#     project_id = Project.objects.filter(user_id=request.user.id).last().id
#     return redirect('detailproject', project_id=project_id)


def createProject(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            if Project.objects.filter(title=request.POST["title"]):
                messages.warning(request, "Project Name Exists")
                return redirect("createproject")
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            project_id = (
                Project.objects.filter(user_id=request.user.id).last().id
            )
            return redirect("detailproject", project_id=project_id)
    form = ProjectForm(request.POST)
    return render(
        request,
        "project/createproject.html",
        {"username": request.user.username, "form": form},
    )


# def createproject(request):
#     return render(request, 'project/createproject.html', {'username': request.user.username})


def project(request):
    # current_user = request.user
    if request.session.has_key("username"):
        list_project = Project.objects.filter(user_id=request.user.id).order_by(
            "-created_at"
        )
        return render(
            request,
            "project/project.html",
            {"list_project": list_project, "username": request.user.username},
        )
    return redirect("login")


def detailProject(request, project_id):
    if request.session.has_key("username"):
        p = Project.objects.get(pk=project_id)
        project = {
            "title": p.title,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
            "description": p.description,
            # 'list_img': p.image_set.all(),
            "project_id": project_id,
            "username": request.user.username,
        }
        return render(request, "project/detailproject.html", project)
    return redirect("login")


def editProject(request, project_id):
    project = Project.objects.get(pk=project_id)
    return render(
        request,
        "project/editproject.html",
        {"project": project, "username": request.user.username},
    )


def updatingProject(request, project_id):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        project = Project.objects.get(pk=project_id)
        project.title = title
        project.description = description
        project.save()
    return redirect("detailproject", project_id)


def deleteProject(request, project_id):
    Project.objects.get(pk=project_id).delete()
    return redirect("project")


def image(request, project_id):
    if request.session.has_key("username"):
        image = Project.objects.get(pk=project_id).image_set.all()
        content = {
            "image": image,
            "username": request.user.username,
            "project": Project.objects.get(pk=project_id),
        }
        return render(request, "project/image.html", content)
    return redirect("login")
