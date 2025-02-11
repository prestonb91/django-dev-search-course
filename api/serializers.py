from rest_framework import serializers
from projects.models import Project

# Takes in Project model and serializes it into a JSON object. 
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'