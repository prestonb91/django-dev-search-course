from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# Takes in Project model and serializes it into a JSON object. 
class ProjectSerializer(serializers.ModelSerializer):
    # Connects owner attribute to ProfileSerializer to display entire owner object in project, nesting the relationship. 
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    # Add in an attribute by using method field. 
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'

    # Any field here has to start with get (get this value).
    # Self refers to serializer class. 
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data



