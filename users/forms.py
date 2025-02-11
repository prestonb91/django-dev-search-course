from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill

class CustomUserCreationForm(UserCreationForm):
    # Specifies metadata about the form, like the model it is based on and what fields should be included
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        # Identifying fields to customize.
        labels = {
            'first_name': 'Name'
        }

    # Loop through and apply a class styling to every field of user creation form
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for name, field, in self.fields.items():
            field.widget.attrs.update({'class':'input'})

# ModelForm is a generic model form wheras UserCreationForm is specific for user registration
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'bio', 'short_intro', 'profile_image', 'social_github', 'social_youtube', 'social_x', 'social_linkedin', 'social_website']

    # Loop through and apply a class styling to every field of user creation form
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field, in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        # Want the skill form to be able to access all except modifying the owner
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field, in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field, in self.fields.items():
            field.widget.attrs.update({'class':'input'})


