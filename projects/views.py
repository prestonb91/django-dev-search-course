# Render import renders templates. 
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

projectsList = [
    {
        'id': '1', 
        'title': 'Ecommerce Website', 
        'description': 'Fully functional ecommerce website' 
    },
    { 
        'id': '2', 
        'title': 'Portfolio Website',
        'description': 'A personal website to write articles and display work' 
    },
    {
        'id': '3', 
        'title': 'Social Network', 
        'description': 'An open source project built by the community' 
    }
]

# Projects function called on access to projects/
def projects(request): 
    msg = 'projects'
    number = 10
    return render(request, 'projects/projects.html', {'msg': msg, 'number': number, 'projectsList': projectsList})

# id value being called as parameter from project url
def project(request, pk): 
    projectObj = None
    for i in projectsList:
        if i['id'] == pk:
            projectObj = i
    return render(request, 'projects/single-project.html', {'project': projectObj})
