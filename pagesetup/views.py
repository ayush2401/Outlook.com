from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

@login_required(login_url ='/login')
def index(request):

    first_name = request.user.first_name
    profile = Profile.objects.get(user = request.user)
    
    context = {
        'first_name':first_name.upper(),
        'profile':profile,
    }

    return render (request , 'index.html' , context)

def login_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request , 'Invalid username')
            return redirect('/login')
        
        user = authenticate(username = username , password = password)

        if user is None:
            messages.error(request , 'Invalid password')
            return redirect('/login')
        else:

            login(request,user)
            return redirect('/')


    return render(request , 'login_page.html')

def logout_page(request):
    logout(request)
    return redirect('/login')

def register_page(request):

    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, "Username already taken")
            return redirect('/register')


        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )

        user.set_password(password)
        user.save()

        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model)
        new_profile.save()

        return redirect('/register')

    return render(request , 'register_page.html')

@login_required(login_url='/login')
def settings(request):

    if request.method == "POST":
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        image = request.FILES.get('image')

        profile = Profile.objects.get(user=request.user)
        profile.bio = bio
        profile.location = location

        if image:
            profile.profile_pic = image
        
        profile.save()
        messages.success(request,"Profile updated successfully")
        return redirect('/settings')
    
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile':profile,
    }

    return render(request , 'settings.html' , context)