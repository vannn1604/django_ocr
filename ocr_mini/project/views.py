import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from utils.ocr_utils import ocr

from .forms import ProjectForm
from .models import Image, Project


def image_delete(request, project_id, image_id):
    Image.objects.get(pk=image_id).delete()
    project = Project.objects.get(pk=project_id)
    project.updated_at = datetime.datetime.now()
    project.save()
    return redirect("image", project_id)


def image_edit(request, project_id, image_id):
    if request.method == "POST":
        
        img = Image.objects.get(pk=image_id)
        if request.POST["title"]:
            if request.POST["title"] != img.title:
                img.title = request.POST["title"]
                img.auto_OCR = False
                img.save()
                project = Project.objects.get(pk=project_id)
                project.updated_at = datetime.datetime.now()
                project.save()
                return redirect("detailimage", project_id=project_id, image_id=image_id)
            else:
                messages.warning(request, "The label has not changed.")
        else:
            messages.warning(request, "The label has not None.")
        return redirect("editimage", project_id, image_id)
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


def image_detail(request, project_id, image_id):
    img = Image.objects.get(pk=image_id)
    image = {
        "title": img.title,
        "created_at": img.created_at,
        "updated_at": img.updated_at,
        "auto_OCR": img.auto_OCR,
        "timing": img.timing,
        "source": img.source,
        "project": Project.objects.get(pk=project_id),
        "image_id": image_id,
        "username": request.user.username,
    }
    return render(request, "project/detailimage.html", image)


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


def image_uploading(request, project_id):
    if request.method == "POST" and "source" in request.FILES:
        for item in request.FILES.getlist("source"):
            first_time = datetime.datetime.now().timestamp()
            title = ocr(item)
            last_time = datetime.datetime.now().timestamp()
            image = Image(
                source=item,
                title=title,
                project_id=project_id,
                timing=last_time - first_time,
            )
            image.save()
        project = Project.objects.get(pk=project_id)
        project.updated_at = datetime.datetime.now()
        project.save()
    else:
        messages.warning(request, "You have not selected a file")
    return redirect("image", project_id=project_id)


def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            if Project.objects.filter(title=request.POST["title"]):
                messages.warning(request, "Project Name Exists")
                return redirect("createproject")
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            project_id = Project.objects.filter(user_id=request.user.id).last().id
            return redirect("detailproject", project_id=project_id)
    form = ProjectForm(request.POST)
    return render(
        request,
        "project/createproject.html",
        {"username": request.user.username, "form": form},
    )


def project(request):
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


def project_detail(request, project_id):
    if request.session.has_key("username"):
        p = Project.objects.get(pk=project_id)
        project = {
            "title": p.title,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
            "description": p.description,
            "project_id": project_id,
            "username": request.user.username,
        }
        return render(request, "project/detailproject.html", project)
    return redirect("login")


def project_edit(request, project_id):
    if request.method == "POST":
        if request.POST["title"] and request.POST["description"]:
            title = request.POST["title"]
            description = request.POST["description"]
            project = Project.objects.get(pk=project_id)
            if title != project.title or description != project.description:
                project.title = request.POST["title"]
                project.description = request.POST["description"]
                project.save()
                return redirect("detailproject", project_id)
            else:
                messages.warning(request, "Nothing changed.")
        else:
            messages.warning(request, "Project'name or Description cannot be blank.")
    project = Project.objects.get(pk=project_id)
    return render(
        request,
        "project/editproject.html",
        {"project": project, "username": request.user.username},
    )


# def project_update(request, project_id):
#     if request.method == "POST":
#         title = request.POST["title"]
#         description = request.POST["description"]
#         project = Project.objects.get(pk=project_id)
#         project.title = title
#         project.description = description
#         project.save()
#     return redirect("detailproject", project_id)


def project_delete(request, project_id):
    Project.objects.get(pk=project_id).delete()
    return redirect("project")
