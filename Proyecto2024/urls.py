"""Proyecto2024 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#Codigo Agregado Daniel 
from accounts import views
#Codigo Agregado Christian 
from django.urls import include

urlpatterns = [
    #Codigo Christian 
    path('admin/', admin.site.urls),
    #Añadido
    #path('accounts/', include('django.contrib.auth.urls')),
    path('', include('accounts.urls')),
    
    
    #path('admin/', admin.site.urls),
    #Codigo Menu administrador - Agregado por Daniel 
    path('menuadministrador/', views.menuadministrador, name='menuadministrador'),
    path('registroestudiante/', views.registroestudiante, name='registroestudiante'),
    path('registrodocente/', views.registrodocente, name='registrodocente'),
    #path('visualizardatosregistros/', views.visualizarregistro, name='visualizarregistro'),
    path('administrarasignaciondocente/', views.administrarasignaciondocente, name='administrarasignaciondocente'),
    path('visualizarasignaciondocente/', views.visualizarasignaciondocente, name='visualizarasignaciondocente'),
    path('editarasignacion/<int:id>/', views.editarasignacion, name='editarasignacion'),
    path('eliminarasignacion/<int:id>/', views.eliminarasignacion, name='eliminarasignacion'),

]   
