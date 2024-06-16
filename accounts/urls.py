from django.urls import path
#from django.contrib import admin
from . import views

urlpatterns = [
    #Codio Login - Codigo Chritian
    path('accounts/login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('accounts/logout/',views.exit,name='exit'),
    path('accounts/profile/',views.profile,name='profile'),
   
    #Codigo Menu administrador - Agregado por Daniel 
    
    
    path('registrodocente/', views.registrodocente, name='registrodocente'),
    
    path('visualizarasignaciondocente/', views.visualizarasignaciondocente, name='visualizarasignaciondocente'),
    
]