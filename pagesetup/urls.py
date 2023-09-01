from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name = 'index'),
    path('login' , views.login_page , name='login'),
    path('register' , views.register_page , name='register'),
    path('logout' , views.logout_page , name='logout'),
    path('settings',views.settings,name='settings'),
    path('post',views.post,name='post'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('like-post/<id>',views.like_post,name='like-post'),
    path('follow',views.follow,name='follow'),
    path('profile/delete/<id>',views.delete,name='delete'),
    path('profile/update/<id>',views.update,name='update'),
    path('search',views.search,name='search'),
]
