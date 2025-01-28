from django.shortcuts import render
from django.urls import HttpResponse

# Create your views here.

# Projects function called on access to projects/
def projects(request): 
    return HttpResponse('Here are our products')

# pk value being called as parameter from project url
def project(request, pk): 
    return HttpResponse('SINGLE PROJECT' + ' ' + pk)