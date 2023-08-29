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
    posts = Posts.objects.all()
  
    context = {
        'first_name':first_name.capitalize(),
        'profile':profile,
        'posts':posts,
        
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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = User.objects.get(username=request.user.username)
        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
            
        user.save()
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

@login_required(login_url='/login')
def post(request):

    profile = Profile.objects.get(user = request.user)
    if request.method == "POST":
        image = request.FILES.get('image')
        caption = request.POST.get('caption')

        if image:
            new_post = Posts.objects.create(
                user = request.user.username,
                caption = caption,
                image = image,
                icon = profile.profile_pic,
            )

        new_post.save()
        return redirect('/')
    
    return redirect('/')

@login_required(login_url='/login')
def profile(request):
    
    prof = Profile.objects.get(user = request.user)
    posts = Posts.objects.filter(user = request.user.username)
    context = {
        'first_name':request.user.first_name.capitalize(),
        'profile':prof,
        'posts':posts,
        'name':f'{request.user.first_name} {request.user.last_name}',
        'navicon':prof.profile_pic,
    }

    return render(request,'profile.html' , context)

@login_required(login_url='/login')
def oprofile(request , id):

    posts = Posts.objects.get(id = id)
    username = posts.user
    user_model = User.objects.get(username=username)
    profile = Profile.objects.get(user = user_model)
    current_user = Profile.objects.get(user = request.user)
    navicon = current_user.profile_pic
  
    context = {
        'profile':profile,
        'posts': Posts.objects.filter(user = username),
        'name':f'{user_model.first_name} {user_model.last_name}',
        'navicon':navicon,
        'first_name':request.user.first_name.capitalize(),
    }

    return render(request , 'profile.html' , context)

@login_required(login_url='/login')
def like_post(request , id):
    username = request.user.username
    post = Posts.objects.get(id = id)
    like_filter = likePost.objects.filter(post_id = id , username = username).first()
    if like_filter is None:
        new_like = likePost.objects.create(post_id = id , username = username)
        new_like.save()
        post.likes = post.likes + 1
    else:
        like_filter.delete()
        post.likes = post.likes - 1
    post.save()
    return redirect('/')
