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
    
    #Codigo Registro de Asistencia - Ricardo
    path('asistencia/listar-registros/', views.registro_asistencia, name='registroasistencia'),
    path('asistencia/seleccionar_grado/', views.seleccionar_grado, name='seleccionar_grado'),
    path('asistencia/registrar_asistencia/<int:id_gradoseccion>/<str:fecha>/', views.registrar_asistencia, name='registrar_asistencia'),
]