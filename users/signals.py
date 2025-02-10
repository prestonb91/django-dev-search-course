# Importing signal that will trigger after save. 
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile

## Anytime the save method is called on Profile, this method is triggered. 
# @receiver(post_save, sender=Profile)
# Sender is the model that sends this, instance is the instance of the object that triggers, created lets us know true or false if a new record was added or not. 
# This now creates a profile once a user is created. 
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        # Create a profile.
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = 'Welcome to DevSearch'
        message = 'Start your DevSearch journey with us today.'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

# Without this, when profile gets deleted, user stays. 
def deleteUser(sender, instance, **kwargs):
    # Instance here is the profile and get the user (as they are connected in a 1to1 relationship)
    user = instance.user
    user.delete()

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    # Able to get the user from profile as it is a 1to1 relationship
    user = profile.user
    # If first instance of user being created, do not fire this signal since it will go into recursive loop.
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

# Anytime the save method is called on Profile, this method is triggered. 
post_save.connect(createProfile, sender=User)
# Anytime the user is updated, triggers the profile to save the user fields.
post_save.connect(updateUser, sender=Profile)
# Anytime a user is deleted, this method is triggered
post_delete.connect(deleteUser, sender=Profile) 