from django.urls import path
#from django.contrib import admin
from . import views
from .views import registrar_estudiante, listar_estudiantes, editar_estudiante

urlpatterns = [
    #Codio Login - Codigo Chritian
    path('accounts/login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('accounts/logout/',views.exit,name='exit'),
    path('accounts/profile/',views.profile,name='profile'),
    path('correo/', views.envio_correo, name='correo'),
    #Codigo Menu administrador - Agregado por Daniel 
    path('menuadministrador/', views.menuadministrador, name='menuadministrador'),
    path('registroestudiante/', views.registroestudiante, name='registroestudiante'),
    path('registrodocente/', views.registrodocente, name='registrodocente'),
    path('visualizardatosregistros/', views.visualizarregistro, name='visualizarregistro'),
    #path('administrarasignaciondocente/', views.administrarasignaciondocente, name='administrarasignaciondocente'),
    #path('visualizarasignaciondocente/', views.visualizarasignaciondocente, name='visualizarasignaciondocente'),
    #path('editarasignacion/<int:id>/', views.editarasignacion, name='editarasignacion'),
    #path('eliminarasignacion/<int:id>/', views.eliminarasignacion, name='eliminarasignacion'),  # Nueva ruta para eliminar asignación
    #path('pruebasdjango/', views.pruebasdjango, name='pruebasdjango'),
    path('administrarasignaciondocente/', views.administrarasignaciondocente, name='administrarasignaciondocente'),
    path('visualizarasignaciondocente/', views.visualizarasignaciondocente, name='visualizarasignaciondocente'),
    path('editarasignacion/<int:id>/', views.editarasignacion, name='editarasignacion'),
    path('eliminarasignacion/<int:id>/', views.eliminarasignacion, name='eliminarasignacion'),
    path('registrar_estudiante/', registrar_estudiante, name='registrar_estudiante'),
    path('listar_estudiantes/', listar_estudiantes, name='listar_estudiantes'),
    path('editar_estudiante/<int:id_alumno>/', views.editar_estudiante, name='editar_estudiante'),
]