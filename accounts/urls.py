from django.urls import path
#from django.contrib import admin
from . import views 
from .views import registrar_conducta, registrar_conducta_detalle, listar_conductas
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
    path('notas/',views.notas_estudiantes, name = 'notas_estudiantes'),
    path('editar_nota/<int:estudiante_id>/<int:materia_id>/', views.editar_nota, name='editar_nota'),
    path('ver_notas/<int:estudiante_id>/<int:materia_id>/', views.editar_nota, name='ver_nota'),
    path('reporte_notas/', views.reporte_notas, name='reporte_notas'),
    path('resumen-academico/', views.resumen_academico, name='resumen_academico'),
    path('boleta_pdf/', views.boleta_pdf, name='boleta_pdf'),
    path('listar-docentes/',views.listar_docentes,name='listardocentes'),
    path('calendar-est/', views.calendar_est, name='calendar_est'),
    path('calendar/load/', views.load_activities, name='load_activities'),
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

    #Codigo Registro de Asistencia - Ricardo
    path('asistencia/gestionar_asistencia/', gestionar_asistencia, name='gestionar_asistencia'),
    path('asistencia/registrar_asistencia/<int:grado_seccion_id>/<str:fecha>/', registrar_asistencia, name='registrar_asistencia'),
    path('asistencia/ver_asistencias/', views.ver_asistencias, name='ver_asistencias'),
    path('asistencia/editar/<int:id_asistencia>/', views.editar_asistencia, name='editar_asistencia'),
    path('asistencia/eliminar/<int:id_asistencia>/', views.eliminar_asistencia, name='eliminar_asistencia'),
    path('asistencia/generar_reporte_asistencia/', views.generar_reporte_asistencia, name='generar_reporte_asistencia'),
    path('asistencia/reporte_asistencia/', views.reporte_asistencia, name='reporte_asistencia'),
    
    
    #Registro de Conducta 
    path('registrar_conducta/', registrar_conducta, name='registrar_conducta'),
    path('registrar_conducta/<int:estudiante_id>/', registrar_conducta_detalle, name='registrar_conducta_detalle'),
    path('listar-conductas/', listar_conductas, name='listar_conductas'),
]