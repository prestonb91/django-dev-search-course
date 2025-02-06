# Render import renders templates. 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
# Checks to see if someone is logged in before action.
from django.contrib.auth.decorators import login_required

# Create your views here.

# Projects function called on access to root url.
def projects(request): 
    projects = Project.objects.all()
    context = { 'projects': projects }
    return render(request, 'projects/projects.html', context)

# id value being called as parameter from project url.
def project(request, pk): 
    projectObj = Project.objects.get(id=pk)
    context = { 'project': projectObj }
    return render(request, 'projects/single-project.html', context)

# Takes in POST request from 'project_form.html'
# If they are not logged in, redirects them to login page. 
@login_required(login_url="login")
def createProject(request):
    projectForm = ProjectForm()

    if request.method == 'POST':
        # request.FILES enables backend to take in files sent by form. 
        projectForm = ProjectForm(request.POST, request.FILES)
        # Django model forms checks if form is valid, if all fields are required. 
        if projectForm.is_valid():
            # form.save() creates and saves the content of the form to the database. 
            projectForm.save()
            # After form is saved, redirects the user to the main projects page. 
            return redirect('projects')

    context = { 'projectForm': projectForm }
    return render(request, 'projects/project_form.html', context)

# Form request to update a project.
@login_required(login_url="login")
def updateProject(request, pk):
    # Gets project that has same id as pk. 
    project = Project.objects.get(id=pk)
    # Takes that project instance and prefills in projectForm variable. 
    projectForm = ProjectForm(instance=project)

    if request.method == 'POST':
        # request.POST data is going to be sent into instance=project data. 
        projectForm = ProjectForm(request.POST, request.FILES, instance=project)
        if projectForm.is_valid():
            projectForm.save()
            return redirect('project', pk=project.id)

    context = {'projectForm': projectForm}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = { 'object': project }
    return render(request, 'projects/delete_template.html', context)
