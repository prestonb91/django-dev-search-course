# Render import renders templates. 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib import messages
from django.db.models import Q
# Checks to see if someone is logged in before action.
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProjects

# Create your views here.

# Projects function called on access to root url.
def projects(request): 
    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 6)

    context = { 'projects': projects, 'search_query': search_query, 'custom_range': custom_range }
    return render(request, 'projects/projects.html', context)

# id value being called as parameter from project url.
def project(request, pk): 
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    # Process the review
    if request.method == "POST":
        # Gives the vote and comment
        form = ReviewForm(request.POST)
        # Get instance of request before save so can edit instance before saving. 
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        # Update project votecount.
        projectObj.getVoteCount

        # Pass up to frontend success message. 
        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=projectObj.id)

    context = { 'project': projectObj, 'form': form }
    return render(request, 'projects/single-project.html', context)

# Takes in POST request from 'project_form.html'
# If they are not logged in, redirects them to login page. 
@login_required(login_url="login")
def createProject(request):
    # Grab the logged in profile to specify which profile for project CRUD operations.
    profile = request.user.profile

    projectForm = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(','," ").split()
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

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

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
        # Splits each individual word typed in newtags textarea. 
        newtags = request.POST.get('newtags').replace(','," ").split()

        # request.POST data is going to be sent into instance=project data. 
        projectForm = ProjectForm(request.POST, request.FILES, instance=project)
        if projectForm.is_valid():
            project = projectForm.save()
            # Loop through tags and add newly created tags. 
            for tag in newtags:
                # newtags is a list. This will get a tag if exists, if doesn't exist then will create. 
                tag, created = Tag.objects.get_or_create(name=tag)
                # Access project many to many relationship with tags. 
                project.tags.add(tag)
            return redirect('account')

    context = {'projectForm': projectForm, 'project': project}
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
