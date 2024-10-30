from django.urls import path
#from django.contrib import admin
from . import views
from .views import registrar_estudiante, listar_estudiantes, editar_estudiante, registrar_asistencia, gestionar_asistencia,generar_reporte_asistencia, reporte_asistencia, asignarMaterias, agregar_horario, lista_horarios, ver_horarios, eliminar_horario, editar_horario, lista_docentes, ver_horarios_docente, horario_docente, horario_estudiante
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
    
    #Codigo Registro de Asistencia - Ricardo
    path('asistencia/gestionar_asistencia/', gestionar_asistencia, name='gestionar_asistencia'),
    path('asistencia/registrar_asistencia/<int:grado_seccion_id>/<str:fecha>/', registrar_asistencia, name='registrar_asistencia'),
    path('asistencia/ver_asistencias/', views.ver_asistencias, name='ver_asistencias'),
    path('asistencia/editar/<int:id_asistencia>/', views.editar_asistencia, name='editar_asistencia'),
    path('asistencia/eliminar/<int:id_asistencia>/', views.eliminar_asistencia, name='eliminar_asistencia'),
    path('asistencia/generar_reporte_asistencia/', views.generar_reporte_asistencia, name='generar_reporte_asistencia'),
    path('asistencia/reporte_asistencia/', views.reporte_asistencia, name='reporte_asistencia'),


]