from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Posts)
admin.site.register(likePost)
admin.site.register(FollowUser)