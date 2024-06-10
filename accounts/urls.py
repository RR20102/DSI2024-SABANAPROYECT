from django.urls import path
#from django.contrib import admin
from . import views

urlpatterns = [
    #Codio Login - Codigo Chritian
    path('accounts/login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('accounts/logout/',views.exit,name='exit'), 

    #Codigo Menu administrador - Agregado por Daniel 
    path('menuadministrador/', views.menuadministrador, name='menuadministrador'),
    path('registroestudiante/', views.registroestudiante, name='registroestudiante'),
    path('registrodocente/', views.registrodocente, name='registrodocente'),
    path('visualizardatosregistros/', views.visualizarregistro, name='visualizarregistro'),
    path('administrarasignaciondocente/', views.administrarasignaciondocente, name='administrarasignaciondocente'),
    path('visualizarasignaciondocente/', views.visualizarasignaciondocente, name='visualizarasignaciondocente'),
     path('editarasignacion/<int:id>/', views.editarasignacion, name='editarasignacion'),
   # path('pruebasdjango/', views.pruebasdjango, name='pruebasdjango'),
]