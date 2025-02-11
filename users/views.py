from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill, Message
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles

# Create your views here.

def loginUser(request):
    # Page variable to register conditionally. 
    page = 'login'

    # Prevents accessing the login page if user is logged in and redirects to profiles page. 
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":

        # Extract form fields. 
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            # Checking if user exists in the database. 
            user = User.objects.get(username=username)
        except:
            # If user does not exist, print out flash message. 
            messages.error(request, 'Username does not exist')

        # If checks pass, authenticate function. Authenticate will take user and password to see if matches, then return user instance or none. 
        user = authenticate(request, username=username, password=password)

        # If user does exist, then log user in.
        if user is not None:
            # Login function creates a session for that user in the database. Adds cookie. 
            login(request, user)
            # Send user to next route, what was passed in into the url. 
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    # Logs user out and deletes their session.
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')

def registerUser(request):
    # Page variable to register conditionally. 
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        # Passes in request.POST data, the username and double password as confirmation.
        form = CustomUserCreationForm(request.POST)
        # is_valid method to check if all inputs are valid and no data has been manipulated.
        if form.is_valid():
            # Instead of just saving immediately, this holds a temporary instance a user object before processing, if we want to modify.
            user = form.save(commit=False)
            # Checks for case sensitivity. 
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            # Create session based token and add to cookies
            login(request, user)
            return redirect('edit-account')
        else:
            messages.success(request, 'An error has occured during registration')
    

    context = { 'page': page, 'form': form }
    return render(request, 'users/login_register.html', context)

def profiles(request):
    # searchProfiles located in utils. 
    # Trigger searchProfiles function and returns profile and query set
    profiles, search_query = searchProfiles(request)
    search_query = ''

    custom_range, profiles = paginateProfiles(request, profiles, 6)

    context = { 'profiles':profiles, 'search_query':search_query, 'custom_range': custom_range }
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = { 'profile': profile,'topSkills': topSkills, 'otherSkills': otherSkills }
    return render(request, 'users/user-profile.html', context)

# Decorator where if not logged in, will redirect to login page.
@login_required(login_url='login')
def userAccount(request):
    # Instead of calling a pk to identify account, can get the logged in user with request.user.profile
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    # Passing in ProfileForm created in user forms.py to access it in profile-form.html
    # Putting in instance=profile prefills the information with existing profile information.
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    # Get logged in user's profile information.
    profile = request.user.profile
    form = SkillForm()

    # If post request, process this.
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            # Gives us instance of object of skills and now we can update the owner. 
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            messages.success(request, 'Skill was added!')

            return redirect('account')
        else:
            messages.error(request, 'An error has occured adding the skill.')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    # Ensures will get the skill only for that owner. 
    skill = profile.skill_set.get(id=pk)
    # Prefills the instance of skill that is received to edit. 
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            # Don't need to set the owner because skill has already been created and connected with an owner. 
            form.save()

            messages.success(request, 'Skill was updated!')

            return redirect('account')
        else:
            messages.error(request, 'An error has occured updating the skill.')


    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()

        messages.success(request, 'Skill was successfully deleted!')

        return redirect('account')

    context = {'object':skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def inbox(request):
    # First get currently logged in user. 
    profile = request.user.profile
    # Don't need to set get all due to related_name set in message model. 
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()

    context = {'messageRequests':messageRequests, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    # When user opens message, change is_read to True. 
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message':message}
    return render(request, 'users/message.html', context)

def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    context = {'recipient':recipient, 'form':form}
    return render(request, 'users/message_form.html', context)