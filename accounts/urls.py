from django.urls import path
#from django.contrib import admin
from . import views
from .views import registrar_estudiante, listar_estudiantes, editar_estudiante, asignarMaterias, agregar_horario, lista_horarios, ver_horarios, eliminar_horario, editar_horario, lista_docentes, ver_horarios_docente, horario_docente, horario_estudiante
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



    path('materias/', views.listar_materias, name='materias'),
    path('asinar-materias/', views.asignarMaterias, name='asignar_materias'),
    path('calendario/', views.calendario, name= 'calendario'),
    path('api/actividades/', views.obtener_actividades, name='obtener_actividades'),
     path('editar/actividad/<int:id>/', views.editar_actividad, name='editar_actividad'),
   
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


    path('eliminar_horario/<int:horario_id>/', views.eliminar_horario, name='eliminar_horario'),
    path('editar_horario/<int:horario_id>/', editar_horario, name='editar_horario'),
    
    path('docentes/', lista_docentes, name='lista_docentes'),
    path('horarios-docente/<str:docente_dui>/', ver_horarios_docente, name='ver_horarios_docente'),
    
    path('mi-horario/', horario_docente, name='mi_horario'),
    path('mi-horario-estudiante/', horario_estudiante, name='horario_estudiante'),


]