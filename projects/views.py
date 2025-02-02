# Render import renders templates. 
from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm

# Create your views here.

# Projects function called on access to projects/
def projects(request): 
    projects = Project.objects.all()
    context = { 'projects': projects }
    return render(request, 'projects/projects.html', context)

# id value being called as parameter from project url
def project(request, pk): 
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    context = { 'project': projectObj }
    return render(request, 'projects/single-project.html', context)

def createProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)