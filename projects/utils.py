from django.db.models import Q
from .models import Project, Tag

def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        # __name goes into owner model to get inner value
        Q(owner__name__icontains=search_query) |
        # Project model has a tags attribute so will search this. 
        Q(tags__in=tags)
        )
    
    return projects, search_query