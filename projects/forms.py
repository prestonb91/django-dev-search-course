from django.forms import ModelForm
from django import forms
from .models import Project

# Django looks at Project model and creates a form based on the model its attributes
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # __all__ generates a field for every attribute
        # Determines which fields to show in the form. 
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']

        # Widgets allow for modifying classes. 
        widgets = {
            # Modifies default tags showing as multi select to check boxes.
            'tags':forms.CheckboxSelectMultiple(),
        }
    
    # Overrides init method. 
    # kwargs == key word argument
    def __init__(self, *args, **kwargs):
            # super function takes in ProjectForm (which class to modify), then pass in self, then init.
            super(ProjectForm, self).__init__(*args, **kwargs)

            # Loops through and modifies each field. 
            # self.fields.items() is a dictionary.
            for name, field in self.fields.items():
                # Go into each field and customize.
                field.widget.attrs.update({'class':'input'})

            # # Select fields to modify and change its attributes. 
            # # update({'class':'input'}) = Passes in dictionary and says what attribute to update, update the class and make it input. 
            # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add title'})