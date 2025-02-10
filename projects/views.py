# Render import renders templates. 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm
from django.db.models import Q
# Checks to see if someone is logged in before action.
from django.contrib.auth.decorators import login_required
from .utils import searchProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

# Projects function called on access to root url.
def projects(request): 
    projects, search_query = searchProjects(request)

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(projects, results)

    # On page load, if page is an integer, then load first page. 
    # Except if not an integer in the url, defaults to the first page. 
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    # If user tries to access page that does not exist, default to last page. 
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    # Getting 3 projects and first page of those 3 projects. 
    projects = paginator.page(page)

    context = { 'projects': projects, 'search_query': search_query, 'paginator': paginator }
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
    # Grab the logged in profile to specify which profile for project CRUD operations.
    profile = request.user.profile

    projectForm = ProjectForm()

    if request.method == 'POST':
        # request.FILES enables backend to take in files sent by form. 
        projectForm = ProjectForm(request.POST, request.FILES)
        # Django model forms checks if form is valid, if all fields are required. 
        if projectForm.is_valid():
            # form.save() creates and saves the content of the form to the database. 
            # Commit=False gives us instance of current project to update the owner attribute. 
            project = projectForm.save(commit=False)
            project.owner = profile
            # Took the logged in user, the project itself, and resaved it in the profile. 
            project.save()
            # After form is saved, redirects the user to the main projects page. 
            return redirect('account')

    context = { 'projectForm': projectForm }
    return render(request, 'projects/project_form.html', context)

# Form request to update a project.
@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    # Gets project that has same id as pk. 
    # project_set querying all the projects of that user. 
    project = profile.project_set.get(id=pk)
    # Takes that project instance and prefills in projectForm variable. 
    projectForm = ProjectForm(instance=project)

    if request.method == 'POST':
        # request.POST data is going to be sent into instance=project data. 
        projectForm = ProjectForm(request.POST, request.FILES, instance=project)
        if projectForm.is_valid():
            projectForm.save()
            return redirect('account')

    context = {'projectForm': projectForm}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.profile_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = { 'object': project }
    return render(request, 'delete_template.html', context)
