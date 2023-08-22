from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name = 'index'),
    path('delete/<id>' , views.delete , name='delete'),
    path('update/<id>' , views.update , name='update'),
    path('login' , views.login_page , name='login'),
    path('register' , views.register_page , name='register'),
    path('logout' , views.logout_page , name='logout'),
]
