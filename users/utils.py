from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):

    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    # On page load, if page is an integer, then load first page. 
    # Except if not an integer in the url, defaults to the first page. 
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    # If user tries to access page that does not exist, default to last page. 
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles

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