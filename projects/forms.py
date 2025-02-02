from django.forms import ModelForm
from .models import Project

# Django looks at Project model and creates a form based on the model its attributes
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # __all__ generates a field for every attribute
        # Determines which fields to show in the form. 
        fields = ['title', 'description', 'demo_link', 'source_link', 'tags']