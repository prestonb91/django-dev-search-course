from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

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
            return redirect('profiles')
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
            return redirect('profiles')
        else:
            messages.success(request, 'An error has occured during registration')
    

    context = { 'page': page, 'form': form }
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles = Profile.objects.all()
    context = { 'profiles': profiles }
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = { 'profile': profile,'topSkills': topSkills, 'otherSkills': otherSkills }
    return render(request, 'users/user-profile.html', context)
