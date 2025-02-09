from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
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