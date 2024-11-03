from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.forms import modelformset_factory
#Importacion de modelos de la base de datos - Codigo Daniel 
from .models import Docente, Grado, Seccion, Asignacion, Estudiante, GradoSeccion, Asistencia, MateriaGradoSeccion, DocenteMateriaGrado, ActividadAcademica, NotaActividad, HorarioClase, Conducta
from .forms import AsignacionForm, EstudianteForm, AsistenciaForm, GradoSeccionForm, ReporteAsistenciaForm, MESES, DocenteMateriaGradoForm, ActividadAcademicaForm, NotaActividadForm, HorarioClaseForm, ConductaForm
from django.contrib import messages  # Importa messages
from django.http import JsonResponse
import json
from django.utils import timezone
from calendar import monthrange
from calendar import month_name
from datetime import datetime

#Codigo Christian 
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from .forms import LoginForm, DocenteForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Avg , F
from smtplib import SMTPException
import random
import string
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils import timezone
import calendar
from datetime import datetime

from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

from .formsets import NotaActividadFormSet




#Login Codigo Christian 
def login_view(request):
    
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not request.session.session_key: 
                request.session = SessionStore()
                request.session.create() 

                request.session['user_id'] = User.objects.filter(username=username).values_list('id', flat=True).first()
            return redirect('home')
        else:
            messages.error(request, 'Credenciales Invalidas.')
            
    return render(request, 'accounts/login.html', {'form': form})

@login_required 
def home(request):
    contexto = {}
    user = request.user
    groups = user.groups.all()  # Obtiene todos los grupos a los que pertenece el usuario
    group_names = [group.name for group in groups]
    

    if 'Administrador' in group_names:
        contexto['es_admin'] =True
    else:
        contexto['es_admin']=False
    
    if 'Docente' in group_names:
        contexto['es_docente'] =True
        docente = request.user.docente  

        materias_asignadas = DocenteMateriaGrado.objects.filter(dui=docente).select_related('id_matrgrasec')
        asignaciones = Asignacion.objects.filter(docente=docente)
        # Obtener grados y secciones asignados
        grados_seccion_asignados = [asignacion.grado_seccion for asignacion in asignaciones]
        
        contexto['materias_asignadas']=materias_asignadas
        contexto['grados_seccion_asignados']=grados_seccion_asignados
    else:
        contexto['es_docente']=False

    if 'Estudiante' in group_names:
        contexto['es_est'] =True
    else:
        contexto['es_est']=False
    return render(request, 'accounts/home.html', contexto)

def exit(request):
    logout(request)
    return redirect('home')

def get_grupos(request):
    roles = {}
    user = request.user
    groups = user.groups.all()  # Obtiene todos los grupos a los que pertenece el usuario
    group_names = [group.name for group in groups]
    
    if 'Administrador' in group_names:
        roles['es_admin'] =True
    else:
        roles['es_admin']=False
    
    if 'Docente' in group_names:
        roles['es_docente'] =True
    else:
        roles['es_docente']=False

    if 'Estudiante' in group_names:
        roles['es_est'] =True
    else:
        roles['es_est']=False
    return roles
@login_required
def profile(request):
    usuario = request.user
    contexto = get_grupos(request)
    persona = None
    if contexto['es_docente']:
        persona = usuario.docente
        usuario = User.objects.get(username=usuario)
        persona = get_object_or_404(Docente, user=usuario)
    elif contexto['es_est']:
        persona = usuario.estudiante
        usuario = User.objects.get(username=usuario)
        persona = get_object_or_404(Estudiante, user=usuario)
   
    contexto['persona']=persona
   
    
    
    return render(request, 'accounts/profile.html',contexto)

def generate_random_password(length=8):
    """Genera una contraseña aleatoria"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))
     
def generate_unique_username(nombre, apellidos):
    """Genera un nombre de usuario único basado en el nombre y apellido"""
    base_username = f"{nombre.split()[0]}.{apellidos.split()[0]}".lower()
    username = base_username
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{''.join(random.choices(string.digits, k=2))}"
    return username

def generate_unique_username_alumno(nombre, apellidos):
    """Genera un nombre de usuario único basado en la primera letra del nombre
     y la primera letra del primer apellido, más 7 números aleatorios."""
    base_username = f"{nombre[0]}{apellidos[0]}".lower()
    random_digits = ''.join(random.choices(string.digits, k=5))
    username = f"{base_username}{random_digits}"
    
    # Verificar si el nombre de usuario ya existe (opcional pero recomendado)
    while User.objects.filter(username=username).exists():
        random_digits = ''.join(random.choices(string.digits, k=7))
        username = f"{base_username}{random_digits}"
    return username

def registrar_docente(nombre, apellidos, correo_electronico, dui, genero, direccion, edad, telefono):
    """
    Registra un docente y crea un usuario asociado.

    Args:
        nombre (str): Nombre del docente.
        apellidos (str): Apellidos del docente.
        correo_electronico (str): Correo electrónico del docente.
        dui (str): DUI del docente.
        genero (str): Género del docente.
        direccion (str): Dirección del docente.
        edad (int): Edad del docente.
        telefono (str): Teléfono del docente.

    Returns:
        dict: Información sobre el registro, incluyendo el mensaje si es exitoso.
    """
    try:
        # Validar que el correo electrónico sea único
        if User.objects.filter(email=correo_electronico).exists():
            return {'success': False, 'message': 'El correo electrónico ya está registrado.'}
        
        # Generar un nombre de usuario único
        username = generate_unique_username(nombre, apellidos)
        print(username)
        if username is None:
            print('nombre de usuario nulo.')
        # Generar una contraseña aleatoria
        password = generate_random_password()
        
        # Crear el usuario
        user = User.objects.create_user(username=username, password=password, email=correo_electronico)
        
        user.first_name = nombre
        user.last_name = apellidos
        
        
        # Crear el docente asociado
        docente = Docente(
            user=user, 
            dui=dui, 
            nombreDocente=nombre, 
            apellidoDocente=apellidos, 
            generoDocente=genero, 
            direccionDocente=direccion, 
            correoDocente=correo_electronico,
            edadDocente=edad, 
            telefonoDocente=telefono
        )
        docente.save()

         # Agregar el usuario al grupo "Docentes"
        try:
            grupo_docentes = Group.objects.get(name='Docente')
        except Group.DoesNotExist:
            return {'success': False, 'message': 'El grupo "Docente" no existe.'}
        
        user.groups.add(grupo_docentes)
        
        # Enviar el correo electrónico con el username y la contraseña
        try:
            # Enviar el correo electrónico con el username y la contraseña
            to_email = correo_electronico
            subject = 'No responsa a Este correo - Registro exitoso'
            message = f'Escuela La Sabana \n {docente.__str__()} Su usuario ha sido creado exitosamente.\n\nUsername: {username}\nContraseña: {password}'
            send_mail(subject, message, None, [to_email], fail_silently=False)
        except SMTPException as e:
            return {'success': False, 'message': 'El usuario fue creado, pero ocurrió un error al enviar el correo electrónico.'}
        
        return {'success': True, 'message': 'El Docente fue Registrado con exito.'}
    
    except IntegrityError as e:
        return {'success': False, 'message': str(e)}
    except ValidationError as e:
        return {'success': False, 'message': str(e)}

def registrar_alumno(nombreAlumno, apellidoAlumno, gradoAlumno, edadAlumno, telefonoAlumno, nombreTutor, apellidoTutor, telTutor, duiTutor, dirTutor, edadTutor):
    
    try:
        # Validar que el correo electrónico sea único
        
        
        # Generar un nombre de usuario único
        username = generate_unique_username_alumno(nombreAlumno, apellidoAlumno)
        
        # Generar una contraseña aleatoria
        password = generate_random_password()
        
        # Crear el usuario
        user = User.objects.create_user(username=username, password=password)
        user.first_name = nombreAlumno
        user.last_name = apellidoAlumno
        user.save()
        
        # Crear el estudiante asociado
        alumno = Estudiante(
            user=user, 
            nombreAlumno=nombreAlumno, 
            apellidoAlumno=apellidoAlumno,  
            edadAlumno=edadAlumno,
            id_gradoseccion = gradoAlumno,
            numeroTelefonoAlumno=telefonoAlumno, 
            nombreResponsable=nombreTutor,
            apellidoResposable=apellidoTutor,
            numeroTelefonoResposable=telTutor, 
            duiResponsable=duiTutor,
            direccionResponsable=dirTutor,
            edadResponsable=edadTutor
        )
        alumno.save()

         # Agregar el usuario al grupo "Docentes"
        try:
            grupo_est = Group.objects.get(name='Estudiante')
        except Group.DoesNotExist:
            return {'success': False, 'message': 'El grupo "Estudiante" no existe.'}
        
        user.groups.add(grupo_est)
        
        # Enviar el correo electrónico con el username y la contraseña
        #try:
            # Enviar el correo electrónico con el username y la contraseña
        """ send_mail(
                'No responsa a Este correo - Registro exitoso',
                f'Escuela La Sabana \n {Estudiante.__str__()} Su usuario ha sido creado exitosamente.\n\nUsername: {username}\nContraseña: {password}',
                'admin@example.com',  # Debería ser el correo del sistema
                [correo_electronico],
                fail_silently=False,
            )
        except SMTPException as e:
            return {'success': False, 'message': 'El usuario fue creado, pero ocurrió un error al enviar el correo electrónico.'} """
        
        return {'success': True, 'message': 'El usuario fue creado correctamente.', 'username': username, 'password': password}
    
    except IntegrityError as e:
        return {'success': False, 'message': str(e)}
    except ValidationError as e:
        return {'success': False, 'message': str(e)}
    


#Codigo Menu administrador - Agregado por Daniel 
@login_required
def registrodocente(request):
    resultado = None
    
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        
        if form.is_valid():
            resultado = registrar_docente(
                nombre= form.cleaned_data['nombreDocente'],
                apellidos= form.cleaned_data['apellidoDocente'],
                correo_electronico=form.cleaned_data['correoDocente'],
                dui=form.cleaned_data['dui'],
                genero=form.cleaned_data['generoDocente'],
                direccion=form.cleaned_data['direccionDocente'],
                edad=form.cleaned_data['edadDocente'],
                telefono= form.cleaned_data['telefonoDocente']                         
                )
            if resultado['success']:
                messages.success(request, resultado['message'])
                form = DocenteForm()
                return render(request,'accounts/registrodocente.html', {'form': form})
            else:
                messages.error(request, resultado['message'])
                form = DocenteForm()
                return render(request,'accounts/registrodocente.html', {'form': form})
    else:
        form = DocenteForm()

    return render(request, 'accounts/registrodocente.html',{'form': form})


@login_required
def visualizarasignaciondocente(request):
    asignaciones = Asignacion.objects.all()
    return render(request, 'accounts/visualizarasignaciondocente.html', {
        'asignaciones': asignaciones
    })





@login_required 
def administrarasignaciondocente(request):
    if request.method == 'POST':
        # Obtener el DUI del docente y el id de grado_seccion desde el formulario
        docente_dui = request.POST.get('docente')
        grado_seccion_id = request.POST.get('grado_seccion')
        
        if not docente_dui or not grado_seccion_id:
            messages.error(request, 'Por favor selecciona un docente y un grado y sección antes de guardar.')
            return redirect('administrarasignaciondocente')
        
        # Verifica si el docente ya está asignado a una sección del grado seleccionado
        docente_asignaciones = Asignacion.objects.filter(docente__dui=docente_dui)
        try:
            grado_seccion = GradoSeccion.objects.get(id_gradoseccion=grado_seccion_id)
        except GradoSeccion.DoesNotExist:
            messages.error(request, 'Grado y sección no encontrados.')
            return redirect('administrarasignaciondocente')

        seccion_actual = grado_seccion.seccion
        
        # Acumula mensajes de error
        errores = []

        # Verificar si el docente ya tiene 2 asignaciones en total
        if docente_asignaciones.count() >= 2:
            errores.append('El docente ya tiene el máximo de asignaciones permitidas.')
        
        # Verificar si el docente ya está asignado a la misma sección del grado
        for asignacion in docente_asignaciones:
            if asignacion.grado_seccion.seccion == seccion_actual:
                errores.append('El docente ya está asignado a un Grado con la misma sección.')

        # Si hay errores, mostrar un único mensaje de error concatenado
        if errores:
            mensaje_final = " ".join(errores)  # Concatenar todos los errores en un solo mensaje
            messages.error(request, mensaje_final)
            return redirect('administrarasignaciondocente')
        
        # Crear la asignación
        try:
            docente = Docente.objects.get(dui=docente_dui)
        except Docente.DoesNotExist:
            messages.error(request, 'Docente no encontrado.')
            return redirect('administrarasignaciondocente')
        
        # Crear la asignación
        Asignacion.objects.create(docente=docente, grado_seccion=grado_seccion)
        messages.success(request, 'Asignación guardada con éxito')
        return redirect('administrarasignaciondocente')

    # Obtener todos los docentes y grados_secciones para el formulario
    formd = DocenteMateriaGradoForm()
    docentes = Docente.objects.all()
    grados_secciones = GradoSeccion.objects.all()
    

    return render(request, 'accounts/administrarasignaciondocente.html', {
        'docentes': docentes,
        'grados_secciones': grados_secciones,
        'formd': formd
    })


@login_required 
def visualizarasignaciondocente(request):
    asignaciones = Asignacion.objects.all()
    return render(request, 'accounts/visualizarasignaciondocente.html', {'asignaciones': asignaciones})

 
@login_required
def editarasignacion(request, id):
    asignacion = get_object_or_404(Asignacion, id=id)
    
    if request.method == 'POST':
        form = AsignacionForm(request.POST, instance=asignacion)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            docente = cleaned_data['docente']
            grado_seccion = cleaned_data['grado_seccion']  # Esto utilizará id_gradoseccion en el modelo

            # Verificar si el docente ya está asignado a la misma sección
            if Asignacion.objects.filter(docente=docente, grado_seccion__seccion=grado_seccion.seccion).exclude(id=asignacion.id).exists():
                return JsonResponse({'success': False, 'message': 'El docente ya está asignado a una sección igual.'})
            else:
                form.save()
                return JsonResponse({'success': True, 'message': 'Asignación actualizada con éxito.'})
        else:
            # Devolver los errores del formulario
            errors = dict([(field, [error for error in errors]) for field, errors in form.errors.items()])
            return JsonResponse({'success': False, 'errors': errors})

    else:
        form = AsignacionForm(instance=asignacion)

    return render(request, 'accounts/editarasignacion.html', {'form': form, 'asignacion': asignacion})

@login_required
def eliminarasignacion(request, id):
    asignacion = get_object_or_404(Asignacion, id=id)
    if request.method == 'POST':
        asignacion.delete()
        messages.success(request, 'Asignación eliminada con éxito.')
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def registrar_estudiante(request):
    resultado =None
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            resultado= registrar_alumno(
                nombreAlumno=form.cleaned_data['nombreAlumno'],
                apellidoAlumno=form.cleaned_data['apellidoAlumno'],
                edadAlumno=form.cleaned_data['edadAlumno'],
                gradoAlumno = form.cleaned_data['id_gradoseccion'],
                telefonoAlumno=form.cleaned_data['numeroTelefonoAlumno'],
                nombreTutor=form.cleaned_data['nombreResponsable'],
                apellidoTutor=form.cleaned_data['apellidoResposable'],
                telTutor=form.cleaned_data['numeroTelefonoResposable'],
                duiTutor=form.cleaned_data['duiResponsable'],
                dirTutor=form.cleaned_data['direccionResponsable'],
                edadTutor=form.cleaned_data['edadResponsable']
            )
            if resultado['success']:
                messages.success(request, resultado['message'])
                form = EstudianteForm()
                return render(request,'accounts/registrar_estudiante.html', {'form': form, 'usuario':resultado['username'], 'contra':resultado['password']})
            else:
                messages.error(request, resultado['message'])
                form = EstudianteForm()
                return render(request,'accounts/registrar_estudiante.html', {'form': form})
    else:
        form = EstudianteForm()
    
    return render(request, 'accounts/registrar_estudiante.html', {'form': form})


@login_required
def listar_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'accounts/listar_estudiantes.html', {'estudiantes': estudiantes})

@login_required
def listar_docentes(request):
    docentes = Docente.objects.all()
    return render(request, 'accounts/listar_docentes.html', {'docentes': docentes})


@login_required
def editar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id_alumno=id)
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Datos del estudiante actualizados con éxito.'})
        else:
            return JsonResponse({'success': False, 'message': 'Error al actualizar los datos del estudiante.'})
    else:
        form = EstudianteForm(instance=estudiante)

    return render(request, 'accounts/editar_estudiante.html', {'form': form, 'estudiante': estudiante})

@login_required
def eliminar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id_alumno=id)
    
    if request.method == 'POST':
        # Confirmar eliminación
        estudiante.delete()
        messages.success(request, 'Estudiante eliminado con éxito.')
        return JsonResponse({'success': True, 'message': 'Estudiante eliminado con éxito.'})
    
    # Si no es método POST, retornar un error
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})



# Codigo Registro de asistencia
@login_required
def gestionar_asistencia(request):
    if request.method == "POST":
        form = GradoSeccionForm(request.POST, user=request.user)
        if form.is_valid():
            grado_seccion_id = form.cleaned_data['grado_seccion'].id_gradoseccion
            fecha = form.cleaned_data['fecha']
            return redirect('registrar_asistencia', grado_seccion_id=grado_seccion_id, fecha=fecha)
    else:
        form = GradoSeccionForm(user=request.user)
    return render(request, 'accounts/gestionar_asistencia.html', {'form': form})

@login_required
def registrar_asistencia(request, grado_seccion_id, fecha):
    grado_seccion = GradoSeccion.objects.get(id_gradoseccion=grado_seccion_id)
    estudiantes = Estudiante.objects.filter(id_gradoseccion=grado_seccion_id)
    asistencias = {
        asistencia.id_alumno.id_alumno: asistencia.asistio
        for asistencia in Asistencia.objects.filter(idgradoseccion=grado_seccion_id, fechaasistencia=fecha)
    }

    if request.method == "POST":
        for estudiante in estudiantes:
            asistio = request.POST.get(f'asistio_{estudiante.id_alumno}')
            if not asistio:
                messages.error(request, 'Todos los campos deben ser llenados')
                return redirect('registrar_asistencia', grado_seccion_id=grado_seccion_id, fecha=fecha)

            Asistencia.objects.update_or_create(
                id_alumno=estudiante,
                idgradoseccion_id=grado_seccion_id,
                fechaasistencia=fecha,
                defaults={'asistio': asistio}
            )

        messages.success(request, 'Asistencia registrada exitosamente')
        return redirect('gestionar_asistencia')

    return render(request, 'accounts/registrar_asistencia.html', {
        'estudiantes': estudiantes,
        'fecha': fecha,
        'grado_seccion': grado_seccion,
        'asistencias': asistencias
    })


@login_required
def ver_asistencias(request):
    docente = request.user.docente
    grados_secciones_asignados = Asignacion.objects.filter(docente=docente).values_list('grado_seccion', flat=True)
    asistencias = Asistencia.objects.filter(idgradoseccion__in=grados_secciones_asignados).order_by('-fechaasistencia')
    return render(request, 'accounts/ver_asistencias.html', {'asistencias': asistencias})


@login_required
def editar_asistencia(request, id_asistencia):
    asistencia = get_object_or_404(Asistencia, id_asistencia=id_asistencia)

    print(f"Editando asistencia para ID: {asistencia.id_asistencia}")  

    if request.method == 'POST':
        print("Formulario enviado.") 
        print("Datos recibidos:", request.POST)  

        form = AsistenciaForm(request.POST, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, "Asistencia actualizada exitosamente.")
            return redirect('ver_asistencias')
        else:
            print(f"Errores en el formulario: {form.errors}") 
    else:
        form = AsistenciaForm(instance=asistencia)

    return render(request, 'accounts/editar_asistencia.html', {'form': form, 'asistencia': asistencia})


@login_required
def eliminar_asistencia(request, id_asistencia):
    asistencia = get_object_or_404(Asistencia, id_asistencia=id_asistencia)
    asistencia.delete()
    messages.success(request, "Asistencia eliminada exitosamente.")
    return redirect('ver_asistencias')  


@login_required
def generar_reporte_asistencia(request):
    form = ReporteAsistenciaForm()
    return render(request, 'accounts/generar_reporte_asistencia.html', {'form': form})


@login_required
def reporte_asistencia(request):
    if request.method == "POST":
        form = ReporteAsistenciaForm(request.POST)
        if form.is_valid():
            grado_seccion_id = form.cleaned_data['grado_seccion'].id_gradoseccion
            mes = int(form.cleaned_data['mes'])
            año = int(form.cleaned_data['año'])
            nombre_mes = [nombre for numero, nombre in MESES if numero == str(mes)][0]
            grado_seccion = GradoSeccion.objects.get(id_gradoseccion=grado_seccion_id)
            estudiantes = Estudiante.objects.filter(id_gradoseccion=grado_seccion_id)
            
            # Obtener días del mes seleccionado
            num_dias = monthrange(año, mes)[1]
            dias_mes = range(1, num_dias + 1)
            
            # Generar la estructura de asistencia
            asistencias = []
            for estudiante in estudiantes:
                asistencia_dias = []
                for dia in dias_mes:
                    fecha = datetime(año, mes, dia).date()
                    asistencia = Asistencia.objects.filter(id_alumno=estudiante, fechaasistencia=fecha).first()
                    asistencia_dias.append(asistencia.asistio if asistencia else "")
                asistencias.append({
                    'estudiante': estudiante,
                    'asistencia_dias': asistencia_dias
                })
            
            return render(request, 'accounts/reporte_asistencia.html', {
                'grado_seccion': grado_seccion,
                'nombre_mes': nombre_mes,
                'año': año,
                'dias_mes': dias_mes,
                'asistencias': asistencias
            })
        else:
            messages.error(request, 'Formulario inválido')
            return redirect('generar_reporte_asistencia')
    else:
        form = ReporteAsistenciaForm()
    return render(request, 'accounts/generar_reporte_asistencia.html', {'form': form})







# Vista para asignar Horarios de Clases Docentes y Estudiantes - Daniel SP2

#from django.db.models import Q  # Para hacer búsquedas con múltiples campos
@login_required
def agregar_horario(request):
    if request.method == 'POST':
        form = HorarioClaseForm(request.POST)
        if form.is_valid():
            docente_materia_grado = form.cleaned_data.get("docente_materia_grado")
            dia_semana = form.cleaned_data.get("dia_semana")
            hora_inicio = form.cleaned_data.get("hora_inicio")
            hora_fin = form.cleaned_data.get("hora_fin")

            # Validación de que la hora de fin sea mayor que la hora de inicio
            if hora_inicio >= hora_fin:
                messages.error(request, "La hora de fin debe ser mayor que la hora de inicio.")
                return render(request, 'accounts/agregar_horario.html', {'form': form})

            # Validación para evitar conflictos de horarios
            if HorarioClase.objects.filter(
                docente_materia_grado=docente_materia_grado,
                dia_semana=dia_semana,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            ).exists():
                messages.error(request, "Ya existe un horario conflictivo para este docente y materia.")
                return render(request, 'accounts/agregar_horario.html', {'form': form})

             # Validación adicional: verificar si el docente tiene otra materia asignada en el mismo día y hora
            if HorarioClase.objects.filter(
                docente_materia_grado__dui=docente_materia_grado.dui,  # Verificar por el mismo docente
                dia_semana=dia_semana,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            ).exists():
                messages.error(request, "El docente ya tiene otra materia asignada en este día y hora.")
                return render(request, 'accounts/agregar_horario.html', {'form': form})

            # Si todo es válido, guardar el formulario
            form.save()
            messages.success(request, "Horario agregado con éxito.")
            return redirect('lista_horarios')
    else:
        form = HorarioClaseForm()
    
    return render(request, 'accounts/agregar_horario.html', {'form': form})
 
@login_required
def lista_horarios(request):
    # Obtener todos los DocenteMateriaGrado ordenados por grado
    docente_materias = DocenteMateriaGrado.objects.all().order_by('id_matrgrasec__id_gradoseccion__grado__nombreGrado')

    # Obtener el valor del parámetro 'search' de la URL
    search_query = request.GET.get('search', '')

    if search_query:
        # Filtrar los resultados según el campo de búsqueda
        docente_materias = DocenteMateriaGrado.objects.filter(
            id_matrgrasec__id_materia__nombre_materia__icontains=search_query
        ).distinct() | DocenteMateriaGrado.objects.filter(
            dui__nombreDocente__icontains=search_query
        ).distinct() | DocenteMateriaGrado.objects.filter(
            id_matrgrasec__id_gradoseccion__grado__nombreGrado__icontains=search_query
        ).distinct()

    return render(request, 'accounts/lista_horarios.html', {
        'docente_materias': docente_materias,
        'search_query': search_query  # Pasar el término de búsqueda para mantenerlo en el campo de texto
    })

     
@login_required
def ver_horarios(request, docente_materia_id):
    # Obtener el objeto DocenteMateriaGrado
    docente_materia = get_object_or_404(DocenteMateriaGrado, id_doc_mat_grado=docente_materia_id)

    # Obtener todos los horarios de este docente
    horarios = HorarioClase.objects.filter(docente_materia_grado=docente_materia)

    # Ordenar los horarios por día de la semana y hora de inicio
    dias_orden = {
        'Lunes': 1,
        'Martes': 2,
        'Miércoles': 3,
        'Jueves': 4,
        'Viernes': 5,
        'Sábado': 6,
        'Domingo': 7
    }

    horarios = sorted(horarios, key=lambda h: (dias_orden[h.dia_semana], h.hora_inicio))

    return render(request, 'accounts/ver_horarios.html', {
        'docente_materia': docente_materia,
        'horarios': horarios
    })
 
@login_required
def eliminar_horario(request, horario_id):
    horario = get_object_or_404(HorarioClase, id=horario_id)
    horario.delete()
    messages.success(request, "Horario eliminado con éxito.")
    return redirect('ver_horarios', docente_materia_id=horario.docente_materia_grado.id_doc_mat_grado)
@login_required
def editar_horario(request, horario_id):
    horario = get_object_or_404(HorarioClase, id=horario_id)

    if request.method == 'POST':
        form = HorarioClaseForm(request.POST, instance=horario)  # Pasar la instancia del horario actual
        if form.is_valid():
            form.save()  # Guardar el formulario, ya tiene la validación incorporada
            messages.success(request, "Horario actualizado con éxito.")
            return redirect('ver_horarios', docente_materia_id=horario.docente_materia_grado.id_doc_mat_grado)
        else:
            # Mostrar errores específicos de los campos
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    else:
        form = HorarioClaseForm(instance=horario)

    return render(request, 'accounts/editar_horario.html', {'form': form})
@login_required
def lista_docentes(request):
    # Obtener todos los docentes de la base de datos
    docentes = Docente.objects.all()

    return render(request, 'accounts/lista_horarios_completos.html', {
        'docentes': docentes
    })


@login_required
def ver_horarios_docente(request, docente_dui):
    # Obtener el docente a través de su DUI
    docente = get_object_or_404(Docente, dui=docente_dui)

    # Obtener todas las asignaciones del docente y sus horarios
    horarios = HorarioClase.objects.filter(docente_materia_grado__dui=docente).order_by('dia_semana', 'hora_inicio')
    
      
    # Ordenar los horarios por día de la semana y hora de inicio
    dias_orden = {
        'Lunes': 1,
        'Martes': 2,
        'Miércoles': 3,
        'Jueves': 4,
        'Viernes': 5,
        'Sábado': 6,
        'Domingo': 7
    }

    horarios = sorted(horarios, key=lambda h: (dias_orden[h.dia_semana], h.hora_inicio))


    return render(request, 'accounts/ver_horario_completo.html', {
        'docente': docente,
        'horarios': horarios
    })
    
    
#Vista para docente especficamnente 
@login_required
def horario_docente(request):
    # Obtener el docente asociado al usuario autenticado
    docente = get_object_or_404(Docente, user=request.user)
    
    # Obtener todos los horarios del docente
    horarios = HorarioClase.objects.filter(docente_materia_grado__dui=docente).order_by('dia_semana', 'hora_inicio')
    
    # Ordenar los horarios por día de la semana y hora de inicio
    dias_orden = {
        'Lunes': 1,
        'Martes': 2,
        'Miércoles': 3,
        'Jueves': 4,
        'Viernes': 5,
        'Sábado': 6,
        'Domingo': 7
    }

    horarios = sorted(horarios, key=lambda h: (dias_orden[h.dia_semana], h.hora_inicio))

    return render(request, 'accounts/horario_docente.html', {
        'docente': docente,
        'horarios': horarios,
    })
    
#Vista para estudiantes especificamente 
@login_required
def horario_estudiante(request):
    # Obtener el estudiante que está autenticado
    estudiante = get_object_or_404(Estudiante, user=request.user)

    # Obtener el grado y sección asignados al estudiante
    grado_seccion = estudiante.id_gradoseccion

    # Obtener los horarios correspondientes al grado y sección del estudiante
    horarios = HorarioClase.objects.filter(docente_materia_grado__id_matrgrasec__id_gradoseccion=grado_seccion).order_by('dia_semana', 'hora_inicio')

    return render(request, 'accounts/horario_estudiante.html', {
        'estudiante': estudiante,
        'horarios': horarios
    })

@login_required
def listar_materias(request):
    grado_id = request.GET.get('grado', 'todos')
    page_number = request.GET.get('page', 1)  # Manejo de paginación
    materias = MateriaGradoSeccion.objects.all()  # Obtener todas las materias

    if grado_id != 'todos':
        materias = materias.filter(id_gradoseccion=grado_id)  # Filtrar por grado

    paginator = Paginator(materias, 10)  # Suponiendo que quieres 10 materias por página
    page_materia = paginator.get_page(page_number)

    # Obtener todos los grados para llenar el select
    grados = GradoSeccion.objects.all().order_by('grado')  # Asegúrate de tener tu modelo correcto

    return render(request, 'accounts/listar_materias.html', {'page_materia' : page_materia, 'grados': grados, 'selected_grado': grado_id})
@login_required
def asignarMaterias(request):
    formd = DocenteMateriaGradoForm()
    if request.method == 'POST':
        docente = Docente.objects.get(dui=request.POST.get('dui'))
        materias_grados = request.POST.getlist('id_matrgrasec') 
        mat_asig = " "
        mat_no_asig = " "
        for materia_grado in materias_grados:
            mat_grad = MateriaGradoSeccion.objects.get(id_matrgrasec = materia_grado)
            if DocenteMateriaGrado.objects.filter(dui = docente, id_matrgrasec = mat_grad).exists() or DocenteMateriaGrado.objects.filter(id_matrgrasec = mat_grad).exists():
                mat_no_asig += mat_grad.__str__() + ', '
            else:
                DocenteMateriaGrado.objects.create(
                    dui=docente,
                    id_matrgrasec=mat_grad
                )
                mat_asig += mat_grad.__str__() + ', ' 
        if mat_asig != " ":
            messages.success(request, f"Asignación de las Materias: {mat_asig} realizada con éxito")
        
        if mat_no_asig != " ":
            messages.error(request, f"La Asignación de las Materias: {mat_no_asig} ya exite")
         
    return render(request, 'accounts/asignar_materias.html', {'formd' : formd})
@login_required
def calendario(request):
     # Suponiendo que el docente se obtiene del usuario autenticado
    docente = Docente.objects.get(user=request.user)

    if request.method == 'POST':
        form = ActividadAcademicaForm(request.POST, docente=docente)
        if form.is_valid():
            form.save()
            print('formulario saved')
            return redirect('calendario')  # Redirigir a la lista de actividades
    else:
        form = ActividadAcademicaForm(docente=docente)
    return render(request, 'accounts/calendario.html', {'form': form})

def obtener_actividades(request):
    actividades = ActividadAcademica.objects.all()
    eventos = []
    
    # Convertir las actividades en el formato requerido por FullCalendar
    for actividad in actividades:
        eventos.append({
            'id': actividad.id_actividad,
            'title': actividad.nombre_actividad,
            'start': actividad.fecha_actividad.isoformat(),
            'description': actividad.descripcion_actividad,
        })
    
    return JsonResponse(eventos, safe=False)
@login_required
def editar_actividad(request, id):
    actividad = get_object_or_404(ActividadAcademica, id_actividad=id)
    docente = Docente.objects.get(user=request.user)
    if request.method == 'POST':
        form = ActividadAcademicaForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # Respuesta exitosa para el AJAX
        else:
            # Extraer etiquetas de los campos con errores
            field_errors = form.errors # Ahora usaremos 'field_errors'
            field_labels = {field: form.fields[field].label for field in form.fields}
            # Responder con JSON que incluye errores y etiquetas
            return JsonResponse({
                'success': False,
                'errors': field_errors,  # Usamos field_errors aquí
                'labels': field_labels
            }, status=400)
    else:
        form = ActividadAcademicaForm(instance=actividad, docente=docente)

    return render(request, 'accounts/editar_actividad_form.html', {'form': form, 'actividad': actividad})
@login_required
def notas_estudiantes(request):
    # Obtener las materias asignadas al docente autenticado
    asignaciones = DocenteMateriaGrado.objects.filter(dui=request.user.docente.dui).select_related(
        'id_matrgrasec__id_materia', 'id_matrgrasec__id_gradoseccion'
    )

    # Construir una lista de asignaciones con el ID de `id_matrgrasec` incluido
    asignaciones_con_id = [
        {
            'id': asignacion.id_matrgrasec.id_matrgrasec,
            'nombre_materia': f"{asignacion.id_matrgrasec.id_materia.nombre_materia} - "
                              f"{asignacion.id_matrgrasec.id_gradoseccion.grado.nombreGrado} - "
                              f"{asignacion.id_matrgrasec.id_gradoseccion.seccion.nombreSeccion}"
        }
        for asignacion in asignaciones
    ]

    # Obtener estudiantes y preparar el contexto
    materia_seleccionada_id = request.GET.get('materia_id')
    if materia_seleccionada_id:
        materia_seleccionada_id = int(materia_seleccionada_id)
    estudiantes = []
    meses_con_actividades = []
    if materia_seleccionada_id:
        materia_grado_seccion = get_object_or_404(MateriaGradoSeccion, id_matrgrasec=materia_seleccionada_id)
        gradoseccion = materia_grado_seccion.id_gradoseccion
        estudiantes = Estudiante.objects.filter(id_gradoseccion=gradoseccion)

        actividades = ActividadAcademica.objects.filter(id_matrgrasec=materia_grado_seccion) \
               .annotate(
                   month=ExtractMonth('fecha_actividad'),
                   year=ExtractYear('fecha_actividad')
               ) \
               .values('month', 'year') \
               .distinct()
        meses_con_actividades = []
        for actividad in actividades:
            month = actividad['month']
            year = actividad['year']
            # Comprobar si el mes ya está en la lista de meses_con_actividades
            if month and month not in [m['numero'] for m in meses_con_actividades]:
                meses_con_actividades.append({
                    'numero': month,
                    'nombre': calendar.month_name[month].capitalize(),
                    'year': year
                })

        # Resultado de meses_con_actividades
       
    # Obtener el año actual
    año_actual = timezone.now().year

    # Convertir los meses en una lista ordenada

    return render(request, 'accounts/estudiantes_notas.html', {
        'asignaciones': asignaciones_con_id,
        'estudiantes': estudiantes,
        'materia_seleccionada_id': materia_seleccionada_id,
        'meses_con_actividades': meses_con_actividades,
        'año_actual': año_actual,
    })
    
@login_required
def editar_nota(request, estudiante_id, materia_id):
    # Cargar estudiante y materia_grado_seccion
    estudiante = get_object_or_404(Estudiante, id_alumno=estudiante_id)
    materia_grado_seccion = get_object_or_404(MateriaGradoSeccion, id_matrgrasec=materia_id)

    mes = request.GET.get('mes')
    year = request.GET.get('year')

    actividades = ActividadAcademica.objects.filter(
        id_matrgrasec=materia_grado_seccion,
    ).annotate(
        month=ExtractMonth('fecha_actividad'),
        year=ExtractYear('fecha_actividad')
    ).filter(
        month=mes,
        year=year
    )

    for actividad in actividades:
        NotaActividad.objects.get_or_create(id_alumno=estudiante, id_actividad=actividad, defaults={'nota': 0})

    # Asegúrate de que esto devuelva un QuerySet
    notas = NotaActividad.objects.filter(id_alumno=estudiante, id_actividad__in=actividades)

    # Crear el FormSet con el queryset de notas
    formset = NotaActividadFormSet(queryset=notas)

    # Si es un POST, procesamos los datos enviados
    if request.method == 'POST':
        formset = NotaActividadFormSet(request.POST, queryset=notas)

        if formset.is_valid():
            formset.save()
            messages.success(request, 'Notas guardadas con éxito.')
            return redirect('notas_estudiantes')
        else:
            print(formset.errors)  # Para depuración, muestra los errores de validación en consola

    # Enviar el FormSet completo a la plantilla
    return render(request, 'accounts/editar_notas.html', {
        'estudiante': estudiante,
        'materia': materia_grado_seccion,
        'formset': formset,
        'mes': calendar.month_name[int(mes)],
        'year': year
    })
@login_required
def reporte_notas(request):
    estudiante = request.user.estudiante  # Obtiene el estudiante del usuario logueado

    # Obtener el mes y el año seleccionados en la consulta GET
    mes_seleccionado = request.GET.get('mes')
    año_seleccionado = request.GET.get('year')

    # Filtrar las actividades y notas del estudiante
    actividades_notas = NotaActividad.objects.filter(
        id_alumno=estudiante
    ).annotate(
        mes=ExtractMonth('id_actividad__fecha_actividad'),
        año=ExtractYear('id_actividad__fecha_actividad')
    )

    # Filtrar por el mes y el año seleccionados, si se especificó
    if mes_seleccionado and año_seleccionado:
        actividades_notas = actividades_notas.filter(mes=mes_seleccionado, año=año_seleccionado)

    # Obtener los meses y años disponibles
    meses_disponibles = actividades_notas.values_list('mes', flat=True).distinct()
    años_disponibles = actividades_notas.values_list('año', flat=True).distinct()

    # Calcular promedios por materia, mes y año
    actividades_por_año_mes_y_materia = {}

    # Filtrar las actividades de tipo "Tarea"
    actividades_tarea = actividades_notas.filter(id_actividad__id_tipoactividad_id=101)

    # Agrupar notas por materia
    for actividad in actividades_notas:
        materia = actividad.id_actividad.id_matrgrasec.id_materia
        mes = actividad.mes
        año = actividad.año

        if año not in actividades_por_año_mes_y_materia:
            actividades_por_año_mes_y_materia[año] = {}

        if mes not in actividades_por_año_mes_y_materia[año]:
            actividades_por_año_mes_y_materia[año][mes] = {}

        if materia not in actividades_por_año_mes_y_materia[año][mes]:
            actividades_por_año_mes_y_materia[año][mes][materia] = {
                'notas': [],
                'promedio_tarea': None,
                'nota_examen': None,
                'nota_tarea_integradora': None,
                'promedio_final': None,
            }

        actividades_por_año_mes_y_materia[año][mes][materia]['notas'].append(actividad)

    # Calcular promedios
    for año, meses in actividades_por_año_mes_y_materia.items():
        for mes, materias in meses.items():
            for materia, datos in materias.items():
                # Calcular promedio de actividades tipo Tarea
                tareas = actividades_tarea.filter(id_actividad__id_matrgrasec__id_materia=materia, mes=mes, año=año)
                if tareas.exists():
                    promedio_tarea = tareas.aggregate(promedio=Avg('nota'))['promedio']
                    datos['promedio_tarea'] = promedio_tarea

                # Obtener notas del examen y tarea integradora
                examen = actividades_notas.filter(id_actividad__id_tipoactividad_id=1, id_actividad__id_matrgrasec__id_materia=materia, mes=mes, año=año).first()
                tarea_integradora = actividades_notas.filter(id_actividad__id_tipoactividad_id=201, id_actividad__id_matrgrasec__id_materia=materia, mes=mes, año=año).first()

                if examen:
                    datos['nota_examen'] = examen.nota
                if tarea_integradora:
                    datos['nota_tarea_integradora'] = tarea_integradora.nota

                # Calcular promedio final
                notas = [datos['promedio_tarea'], datos['nota_examen'], datos['nota_tarea_integradora']]
                notas = [nota for nota in notas if nota is not None]
                if notas:
                    datos['promedio_final'] = round(sum(notas) / len(notas),2)

    return render(request, 'accounts/reporte_notas.html', {
        'actividades_por_año_mes_y_materia': actividades_por_año_mes_y_materia,
        'meses_disponibles': [(mes, calendar.month_name[mes]) for mes in sorted(meses_disponibles)],
        'años_disponibles': sorted(años_disponibles),
        'mes_seleccionado': int(mes_seleccionado) if mes_seleccionado else None,
        'year_seleccionado': int(año_seleccionado) if año_seleccionado else None,
    })

@login_required
def resumen_academico(request):
    estudiante = request.user.estudiante  # Suponiendo que tenemos el estudiante desde el usuario logueado
    año_actual = datetime.now().year
    asignaciones = Asignacion.objects.filter(grado_seccion=estudiante.id_gradoseccion)
    docente= asignaciones.first().docente if asignaciones.exists() else None

    resumen = {}  # Estructura: {materia_id: {'nombre': str, 'promedios': {1: float, 2: float, ...}, 'promedio_final': float}}
    
    for materia in MateriaGradoSeccion.objects.filter(id_gradoseccion=estudiante.id_gradoseccion):
        # Inicializa la estructura de la materia en el resumen
        resumen[materia.id_matrgrasec] = {
            'nombre': materia.id_materia.nombre_materia,  # Nombre de la materia
            'promedios': {mes: None for mes in range(1, 13)},  # Espacio para cada mes
            'promedio_final': None
        }
        
        # Calcular los promedios de cada mes
        for mes in range(1, 13):
            # Filtrar notas del estudiante, materia, año y mes actual
            notas_mes = NotaActividad.objects.filter(
                id_alumno=estudiante,
                id_actividad__id_matrgrasec=materia,
                id_actividad__fecha_actividad__year=año_actual,
                id_actividad__fecha_actividad__month=mes
            )
            
            # Calcular el promedio de las tareas
            promedio_tareas = notas_mes.filter(id_actividad__id_tipoactividad=101).aggregate(promedio=Avg('nota'))['promedio']
            
            # Obtener las notas de "Examen" y "Tarea Integradora" si existen
            nota_examen = notas_mes.filter(id_actividad__id_tipoactividad=1).first()
            nota_integradora = notas_mes.filter(id_actividad__id_tipoactividad=201).first()
            
            # Sumar el promedio de tareas y las notas de Examen e Integradora
            notas_sumadas = [promedio_tareas if promedio_tareas else 0]
            if nota_examen:
                notas_sumadas.append(nota_examen.nota)
            if nota_integradora:
                notas_sumadas.append(nota_integradora.nota)

            # Calcular el promedio mensual solo si hay notas disponibles
            if notas_sumadas:
                promedio_mes = sum(notas_sumadas) / len(notas_sumadas)
                resumen[materia.id_matrgrasec]['promedios'][mes] = promedio_mes
        
        # Calcular el promedio anual de la materia
        promedios_validos = [
            promedio for promedio in resumen[materia.id_matrgrasec]['promedios'].values() if promedio is not None
        ]
        resumen[materia.id_matrgrasec]['promedio_final'] = sum(promedios_validos) / len(promedios_validos) if promedios_validos else None

    # Pasar los nombres de los meses para el template
    meses_nombres = [calendar.month_name[i] for i in range(1, 13)]
    meses_numeros = list(range(1, 13))  # Generar lista de números de 1 a 12
    return render(request, 'accounts/resumen_academico.html', {
        'resumen': resumen,
        'meses_nombres': meses_nombres,
        'meses_numeros': meses_numeros,
        'estudiante': estudiante,
        'docente': docente
    })

@login_required
def boleta_pdf(request):
    # Obtener el estudiante y el docente desde el usuario logueado
    estudiante = request.user.estudiante
    año_actual = datetime.now().year
    asignaciones = Asignacion.objects.filter(grado_seccion=estudiante.id_gradoseccion)
    docente = asignaciones.first().docente if asignaciones.exists() else None

    # Calcular el resumen académico (reutilizamos la lógica de la función resumen_academico)
    resumen = {}
    for materia in MateriaGradoSeccion.objects.filter(id_gradoseccion=estudiante.id_gradoseccion):
        resumen[materia.id_matrgrasec] = {
            'nombre': materia.id_materia.nombre_materia,
            'promedios': {mes: None for mes in range(1, 13)},
            'promedio_final': None
        }
        
        for mes in range(1, 13):
            notas_mes = NotaActividad.objects.filter(
                id_alumno=estudiante,
                id_actividad__id_matrgrasec=materia,
                id_actividad__fecha_actividad__year=año_actual,
                id_actividad__fecha_actividad__month=mes
            )
            promedio_tareas = notas_mes.filter(id_actividad__id_tipoactividad=101).aggregate(promedio=Avg('nota'))['promedio']
            nota_examen = notas_mes.filter(id_actividad__id_tipoactividad=1).first()
            nota_integradora = notas_mes.filter(id_actividad__id_tipoactividad=201).first()
            
            notas_sumadas = [promedio_tareas if promedio_tareas else 0]
            if nota_examen:
                notas_sumadas.append(nota_examen.nota)
            if nota_integradora:
                notas_sumadas.append(nota_integradora.nota)

            if notas_sumadas:
                promedio_mes = sum(notas_sumadas) / len(notas_sumadas)
                resumen[materia.id_matrgrasec]['promedios'][mes] = promedio_mes
        
        promedios_validos = [
            promedio for promedio in resumen[materia.id_matrgrasec]['promedios'].values() if promedio is not None
        ]
        resumen[materia.id_matrgrasec]['promedio_final'] = sum(promedios_validos) / len(promedios_validos) if promedios_validos else None

    # Configuración del PDF
     # Configuración del PDF con orientación horizontal
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{estudiante.nombreAlumno}.pdf"'
    pdf = canvas.Canvas(response, pagesize=landscape(letter))
    pdf.setTitle("Boleta de Notas")

    # Encabezado
     # Obtener el ancho y alto de la página
    width, height = landscape(letter)

     # Encabezado centrado
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2, height - 50, "Centro Escolar Jardines de la Sabana")
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2, height - 80, f"Nombre del Estudiante: {estudiante.nombreAlumno} {estudiante.apellidoAlumno}")
    pdf.drawCentredString(width / 2, height - 100, f"Grado: {estudiante.id_gradoseccion}")
    if docente:
        pdf.drawCentredString(width / 2, height - 120, f"Docente: {docente.nombreDocente} {docente.apellidoDocente}")

    # Preparar datos para la tabla
    encabezado = ["Materia"] + [calendar.month_abbr[i] for i in range(1, 13)] + ["Promedio Final"]
    datos_tabla = [encabezado]

    for materia_id, datos in resumen.items():
        fila = [datos['nombre']]
        for mes_num in range(1, 13):
            promedio_mes = datos['promedios'].get(mes_num)
            fila.append(f"{promedio_mes:.2f}" if promedio_mes is not None else "N/A")
        promedio_final = datos['promedio_final']
        fila.append(f"{promedio_final:.2f}" if promedio_final is not None else "N/A")
        datos_tabla.append(fila)

    # Crear y configurar la tabla
    table = Table(datos_tabla, colWidths=[80] + [40]*12 + [80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    # Colocar la tabla en el PDF
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 40, height - 300)  # Ajusta la posición vertical de la tabla según sea necesario

    # Espacio para las firmas
    pdf.setFont("Helvetica", 12)

     # Línea para la firma del docente (izquierda)
    firma_docente_x1 = 120  # Mueve la línea aún más a la izquierda
    firma_docente_x2 = 260  # Mueve la línea aún más a la izquierda
    firma_docente_y = height - 402
    pdf.line(firma_docente_x1, firma_docente_y, firma_docente_x2, firma_docente_y)  # Línea para la firma del docente
    # Dibujar etiqueta centrada
    pdf.drawCentredString((firma_docente_x1 + firma_docente_x2) / 2, height - 415, "Firma del Docente:")

    # Línea para la firma del director (derecha)
    firma_director_x1 = width - 220  # Mueve la línea aún más a la izquierda
    firma_director_x2 = width - 60    # Mueve la línea aún más a la izquierda
    firma_director_y = height - 402
    pdf.line(firma_director_x1, firma_director_y, firma_director_x2, firma_director_y)  # Línea para la firma del director
    # Dibujar etiqueta centrada
    pdf.drawCentredString((firma_director_x1 + firma_director_x2) / 2, height - 415, "Firma del Director:")


    pdf.showPage()
    pdf.save()
    return response

@login_required
def calendar_est(request):
    return render(request, 'accounts/calendar_est.html')

@login_required
def load_activities(request):
    estudiante = request.user.estudiante
    actividades = ActividadAcademica.objects.filter(id_matrgrasec__id_gradoseccion=estudiante.id_gradoseccion)

    events = []
    for actividad in actividades:
        events.append({
            'id': actividad.id_actividad,
            'title': actividad.nombre_actividad,
            'start': actividad.fecha_actividad.isoformat(),  # Usar ISO format para FullCalendar
            'description': actividad.descripcion_actividad,
        })
    
    return JsonResponse(events, safe=False)



#Registro de Conducta
def registrar_conducta(request):
    docente = request.user.docente  # Obtener el docente autenticado
    asignaciones = Asignacion.objects.filter(docente=docente)

    if request.method == 'POST':
        grado_seccion_id = request.POST.get('grado_seccion')
        estudiantes = Estudiante.objects.filter(id_gradoseccion_id=grado_seccion_id)
    else:
        grado_seccion_id = None
        estudiantes = []

    return render(request, 'accounts/registrar_conducta.html', {
        'asignaciones': asignaciones,
        'grado_seccion_id': grado_seccion_id,
        'estudiantes': estudiantes,
    })


def registrar_conducta_detalle(request, estudiante_id):
    estudiante = Estudiante.objects.get(id_alumno=estudiante_id)

    if request.method == 'POST':
        # Aquí debes manejar el registro de conducta, por ejemplo:
        fecha_conducta = request.POST.get('fecha_conducta')
        observacion_conducta = request.POST.get('observacion_conducta')
        nota_conducta = request.POST.get('nota_conducta')

        # Crea un nuevo registro de conducta
        Conducta.objects.create(
            id_alumno=estudiante,
            fecha_conducta=fecha_conducta,
            obsevacion_conducta=observacion_conducta,
            nota_conducta=nota_conducta
        )
        return redirect('registrar_conducta')  # Redirige a la vista anterior

    return render(request, 'accounts/registrar_conducta_detalle.html', {
        'estudiante': estudiante,
    })
 
def listar_conductas(request):
    conductas = None
    grados = Grado.objects.all()  # Obtén todos los grados

    if request.method == 'POST':
        grado_id = request.POST.get('grado')  # Obtiene el grado seleccionado
        if grado_id:
            # Obtén las secciones asociadas al grado
            secciones = GradoSeccion.objects.filter(grado_id=grado_id)
            # Obtén los estudiantes asociados a las secciones del grado
            estudiantes = Estudiante.objects.filter(id_gradoseccion__grado=grado_id)
            # Obtén las conductas de los estudiantes
            conductas = Conducta.objects.filter(id_alumno__in=estudiantes)

    context = {
        'grados': grados,
        
        'conductas': conductas,
    }
    return render(request, 'accounts/listar_conductas.html', context)