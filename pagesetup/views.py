from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
from django.db.models import Q
from django.contrib.auth import get_user_model
# User = get_user_model()


@login_required(login_url ='/login')
def index(request):

    first_name = request.user.first_name
    profile = Profile.objects.get(user = request.user)
    posts = Posts.objects.all()
    total_posts = len(Posts.objects.filter(user = request.user.username))
    followers = len(FollowUser.objects.filter(following = request.user.username))

    user_object = FollowUser.objects.filter(follower=request.user.username)
    # feed = [Posts.objects.filter(user = i.following) for i in user_object]
    # feed.append(Posts.objects.filter(user = request.user.username))
    # feed = list(chain(*feed))
    # feed = sorted(feed, key=lambda i: i.date)
    # posts = feed

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_object:
        user_list = User.objects.get(username=user.following)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile_list = []

    for users in final_suggestions_list:
        profile_lists = Profile.objects.filter(user = users)
        username_profile_list.append(profile_lists)

    recommend = list(chain(*username_profile_list))

    # user suggestion ends

    context = {
        'first_name':first_name.capitalize(),
        'profile':profile,
        'posts':posts,
        'total_post':total_posts,
        'followers':followers,
        'recommend':recommend,
    }

    return render (request , 'index.html' , context)

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
            posts = Posts.objects.filter(user=request.user)
            for post in posts:
                post.icon = image
                post.save()
        
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
def profile(request , pk):
    
    # main profile
    main_profile = Profile.objects.get(user = request.user)

    # profile being opened
    current_cred = User.objects.get(username = pk)
    current_profile = Profile.objects.get(user = current_cred)
    current_posts = Posts.objects.filter(user = pk)

    follow_str = ''
    if FollowUser.objects.filter(follower = request.user.username , following = pk):
        follow_str = "Unfollow"
    else:
        follow_str = "Follow"

    context = {
        'first_name':request.user.first_name.capitalize(),
        'profile':current_profile,
        'posts':current_posts,
        'main_profile':main_profile,
        'current_cred':current_cred,
        'follow_str':follow_str,
    }

    return render(request,'profile.html' , context)

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

@login_required(login_url='/login')
def follow(request):

    if request.method =="POST":
        follower = request.POST.get('follower')
        following = request.POST.get('following')

        filters = FollowUser.objects.filter(follower = follower , following = following).first()
        if filters is not None:
            filters = FollowUser.objects.get(follower = follower , following = following)
            filters.delete()
        else:
            new_follow = FollowUser.objects.create(follower=follower,following=following)
            new_follow.save()
        
        return redirect('/profile/'+following)


    return redirect('/')

@login_required(login_url='/login')
def delete(request , id):
    post = Posts.objects.get(id = id)
    post.delete()
    username = request.user.username
    return redirect('/profile/'+username)

@login_required(login_url='/login')
def update(request , id):
    username = request.user.username
    return redirect('/profile/'+username)

@login_required(login_url='/login')
def search(request):
    
    if request.method == "POST":

        field = request.POST.get('field')
        users = User.objects.filter(
            Q(username__icontains=field)|
            Q(first_name__icontains=field)|
            Q(last_name__icontains=field)
        )
      
        profiles = []
        for user in users:
            profiles.append(Profile.objects.filter(user=user))

        profiles = list(chain(*profiles))

        context = {
            'first_name':request.user.first_name.capitalize(),
            'profiles':profiles,
            'profile':Profile.objects.get(user = request.user),
        }    

    return render(request,'search.html',context)
    

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

def register_page(request):  # sourcery skip: last-if-guard

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

        messages.info(request, "Account created successfully")
        return redirect('/register')

    return render(request , 'register_page.html')