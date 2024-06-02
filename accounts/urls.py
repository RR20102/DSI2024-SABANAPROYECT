from django.urls import path
from . import views

urlpatterns = [
    #Codigo Menu administrador - Agregado por Daniel 
    path('menuadministrador/', views.menuadministrador, name='menuadministrador'),
    path('registroestudiante/', views.registroestudiante, name='registroestudiante'),
    path('registrodocente/', views.registrodocente, name='registrodocente'),
    path('visualizardatosregistros/', views.visualizarregistro, name='visualizarregistro'),
    path('administrarasignaciondocente/', views.administrarasignaciondocente, name='administrarasignaciondocente'),
    path('visualizarasignaciondocente/', views.visualizarasignaciondocente, name='visualizarasignaciondocente',)
]