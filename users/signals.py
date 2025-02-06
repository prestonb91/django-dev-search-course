# Importing signal that will trigger after save. 
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 
from django.contrib.auth.models import User
from .models import Profile

## Anytime the save method is called on Profile, this method is triggered. 
# @receiver(post_save, sender=Profile)
# Sender is the model that sends this, instance is the instance of the object that triggers, created lets us know true or false if a new record was added or not. 
# This now creates a profile once a user is created. 
def createProfile(sender, instance, created, ** kwargs):
    if created:
        user = instance
        # Create a profile.
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
        )

# Without this, when profile gets deleted, user stays. 
def deleteUser(sender, instance, **kwargs):
    # Instance here is the profile and get the user (as they are connected in a 1to1 relationship)
    user = instance.user
    user.delete()

# # Anytime the save method is called on Profile, this method is triggered. 
post_save.connect(createProfile, User)
# # Anytime a user is deleted, this method is triggered
post_delete.connect(deleteUser, Profile) 