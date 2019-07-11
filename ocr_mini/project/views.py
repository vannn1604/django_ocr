from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Image
from django.contrib import messages
import datetime
from PIL import Image as Image2
import pytesseract
# Create your views here.

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def ocr(filename):
    return pytesseract.image_to_string(Image2.open(filename))


def updateImage(request, project_id, image_id):
    if request.method == "POST":
        img = Image.objects.get(pk=image_id)
        img.title = request.POST['title']
        img.auto_OCR = False
        img.save()
        project = Project.objects.get(pk=project_id)
        project.updated_at = datetime.datetime.now()
        project.save()
    return redirect('detailimage', project_id=project_id, image_id=image_id)


def deleteImage(request, project_id, image_id):
    Image.objects.get(pk=image_id).delete()
    project = Project.objects.get(pk=project_id)
    project.updated_at = datetime.datetime.now()
    project.save()
    return redirect('image', project_id)


def editImage(request, project_id, image_id):
    img = Image.objects.get(pk=image_id)
    image = {
        'title': img.title,
        'created_at': img.created_at,
        'updated_at': img.updated_at,
        'auto_OCR': img.auto_OCR,
        'source': img.source,
        'project': Project.objects.get(pk=project_id),
        'image_id': image_id,
        'username': request.user.username,
    }
    return render(request, 'project/editimage.html', image)


def detailImage(request, project_id, image_id):
    img = Image.objects.get(pk=image_id)
    image = {
        'title': img.title,
        'created_at': img.created_at,
        'updated_at': img.updated_at,
        'auto_OCR': img.auto_OCR,
        'source': img.source,
        'project': Project.objects.get(pk=project_id),
        'image_id': image_id,
        'username': request.user.username,
    }
    return render(request, 'project/detailimage.html', image)


def uploadingimage(request, project_id):
    if request.method == 'POST' and request.FILES['source']:
        source = request.FILES['source']
        title = ocr(source)
        image = Image(source=source, title=title, project_id=project_id)
        image.save()
        project = Project.objects.get(pk=project_id)
        project.updated_at = datetime.datetime.now()
        project.save()
    return redirect('image', project_id=project_id)
        

def creatingproject(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        request.user.project_set.create(title=title, description=description, user_id=request.user.id)  

    project_id = Project.objects.filter(user_id=request.user.id).last().id
    return redirect('detailproject', project_id=project_id)


def createproject(request):
    return render(request, 'project/createproject.html', {'username': request.user.username})


def project(request):
    # current_user = request.user
    if request.session.has_key('username'):    
        list_project = Project.objects.filter(user_id=request.user.id).order_by('-created_at')
        return render(request, 'project/project.html', {'list_project': list_project, 'username': request.user.username})
    return redirect('login')


def detailProject(request, project_id):
    if request.session.has_key('username'):    
        p = Project.objects.get(pk=project_id)
        project = {
            'title': p.title,
            'created_at': p.created_at,
            'updated_at': p.updated_at,
            'description': p.description,
            # 'list_img': p.image_set.all(),
            'project_id': project_id,
            'username': request.user.username,
        }
        return render(request, 'project/detailproject.html', project)
    return redirect('login')


def editProject(request, project_id):
    project = Project.objects.get(pk=project_id)
    return render(request, 'project/editproject.html', {'project': project, 'username': request.user.username})


def updatingProject(request, project_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        project = Project.objects.get(pk=project_id)
        project.title = title
        project.description = description
        project.save()
    return redirect('detailproject', project_id)


def deleteProject(request, project_id):
    Project.objects.get(pk=project_id).delete()
    return redirect('project')


def image(request, project_id):
    if request.session.has_key('username'):
        image = Project.objects.get(pk=project_id).image_set.all()
        content = {
            'image': image,
            'username': request.user.username,
            'project': Project.objects.get(pk=project_id),
        }
        return render(request, 'project/image.html', content)
    return redirect('login')