# Render import renders templates. 
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Projects function called on access to projects/
def projects(request): 
    msg = 'Hello, you are on the projects page.'
    return render(request, 'projects/projects.html', {'msg': msg})

# pk value being called as parameter from project url
def project(request, id): 
    return render(request, 'projects/single-project.html')
