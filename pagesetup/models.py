from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True , default='lorem ipsum')
    profile_pic = models.ImageField(upload_to= "profile_pic" , default='defpic.jpeg')
    location = models.CharField(max_length=100 , blank=True , default='india')

    def __str__(self):
        return self.user.username