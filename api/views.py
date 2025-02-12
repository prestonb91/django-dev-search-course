from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review

# See all available API routes. 
@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'api/projects'},
        {'GET':'api/projects/id'},
        {'POST':'api/projects/id/vote'},

        {'POST':'api/users/token'},
        {'POST':'api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    # Grab all projects. 
    projects = Project.objects.all()
    # Takes the projects queryset and serialzies into JSON. 
    # many=True lets it know it is serializing many objects.
    serializer = ProjectSerializer(projects, many=True)

    # .data takes out the data.  
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):

    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):

    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    # Returns return value of review get from database if exists.
    # Created returns as true or false.
    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )

    review.value = data['value']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)

