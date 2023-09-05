from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True , default='lorem ipsum')
    profile_pic = models.ImageField(upload_to= "profile_pic" , default='defpic.jpeg')
    location = models.CharField(max_length=100 , blank=True , default='india')

    def __str__(self):
        return self.user.username
    
class Posts(models.Model):
    user = models.CharField(max_length=30)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts')
    likes = models.IntegerField(default=1)
    date = models.DateField(default=datetime.now)
    icon = models.ImageField(default='icon.png')

    def __str__(self):
        return f'{self.user}|{self.date}'
    
class likePost(models.Model):
    post_id = models.IntegerField()
    username = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.username}|{self.post_id}'

class FollowUser(models.Model):
    follower = models.CharField(max_length=100)
    following = models.CharField(max_length=10)