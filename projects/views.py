# Render import renders templates. 
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Projects function called on access to projects/
def projects(request): 
    return render(request, 'projects.html')

# pk value being called as parameter from project url
def project(request, pk): 
    return HttpResponse('SINGLE PROJECT' + ' ' + pk)