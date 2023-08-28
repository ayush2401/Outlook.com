from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name = 'index'),
    path('login' , views.login_page , name='login'),
    path('register' , views.register_page , name='register'),
    path('logout' , views.logout_page , name='logout'),
    path('settings',views.settings,name='settings')
]
