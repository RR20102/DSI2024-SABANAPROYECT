from django.urls import path
#from django.contrib import admin
from . import views
from .views import registrar_estudiante, listar_estudiantes, editar_estudiante, agregar_horario, lista_horarios, ver_horarios

urlpatterns = [
    #Codio Login - Codigo Chritian
    path('accounts/login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('accounts/logout/',views.exit,name='exit'),
    path('accounts/profile/',views.profile,name='profile'),
    path('listar-estudiantes/',views.listar_estudiantes,name='listar_estudiantes'),
    path('registrar-estudiantes/',views.registrar_estudiante,name='registrar_estudiante'),
    path('editar-estudiantes/<int:id>/',views.editar_estudiante,name='editar_estudiante'),
    path('eliminar_estudiante/<int:id>/', views.eliminar_estudiante, name='eliminar_estudiante'),



    path('listar-docentes/',views.listar_docentes,name='listardocentes'),
    #Codigo Menu administrador - Agregado por Daniel


    path('registrodocente/', views.registrodocente, name='registrodocente'),
    #path('visualizardatosregistros/', views.visualizarregistro, name='visualizarregistro'),
    #Codigo Asignacion Docente - Daniel
    path('administrarasignaciondocente/', views.administrarasignaciondocente, name='administrarasignaciondocente'),
    path('eliminarasignacion/<int:id>/', views.eliminarasignacion, name='eliminarasignacion'),
    path('editarasignacion/<int:id>/', views.editarasignacion, name='editarasignacion'),
    path('visualizarasignaciondocente/', views.visualizarasignaciondocente, name='visualizarasignaciondocente'),


    # #Codigo Segundo Sprint - Daniel
    path('agregar-horario/', agregar_horario, name='agregar_horario'),
    path('lista-horarios/', lista_horarios, name='lista_horarios'),
    path('ver-horarios/<int:docente_materia_id>/', ver_horarios, name='ver_horarios'),

]