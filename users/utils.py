from django.db.models import Q
from .models import Profile, Skill

# Used in profiles in users/views.py for cleaner code. 
def searchProfiles(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    # icontains makes it case insensitive
    # If search_query is empty, returns all. 
    # Wrapping filter parameters in Q allows it to enable an OR search.
    # Distinct ensures only get one instance of each user. 
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        # Does profile have a skill that is lsited in the query set. 
        Q(skill__in=skills)
        )

    # Function will perform all searches and return back query set and actual value. 
    return profiles, search_query