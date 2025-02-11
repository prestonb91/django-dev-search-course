from django.http import JsonResponse

# See all available API routes. 
def getRoutes(request):

    routes = [
        {'GET':'api/projects'},
        {'GET':'api/projects/id'},
        {'POST':'api/projects/id/vote'},

        {'POST':'api/users/token'},
        {'POST':'api/users/token/refresh'},
    ]

    # safe=False means turn the data into JSON data. 
    return JsonResponse(routes, safe=False)