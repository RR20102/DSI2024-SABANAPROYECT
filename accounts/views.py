from django.shortcuts import render, get_object_or_404, redirect
#Importacion de modelos de la base de datos - Codigo Daniel 
from .models import Docente, Grado, Seccion, Asignacion, Estudiante, GradoSeccion, Asistencia
from .forms import AsignacionForm, EstudianteForm, AsistenciaFormSet, SeleccionarGradoSeccionForm
from django.contrib import messages  # Importa messages
from django.http import JsonResponse
import json
from django.utils import timezone

#Codigo Christian 
from django.contrib.auth import authenticate, login, logout
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
from smtplib import SMTPException
import random
import string

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



def visualizarasignaciondocente(request):
    asignaciones = Asignacion.objects.all()
    return render(request, 'accounts/visualizarasignaciondocente.html', {
        'asignaciones': asignaciones
    })





@login_required 
def administrarasignaciondocente(request):
    if request.method == 'POST':
        docente_dui = request.POST.get('docente')
        grado_seccion_id = request.POST.get('grado_seccion')
        
        if not docente_dui or not grado_seccion_id:
            messages.error(request, 'Por favor selecciona un docente y un grado y sección antes de guardar.')
            return redirect('administrarasignaciondocente')
        
        # Verifica si el docente ya está asignado a una sección del grado seleccionado
        docente_asignaciones = Asignacion.objects.filter(docente__dui=docente_dui)
        grado_seccion = GradoSeccion.objects.get(id=grado_seccion_id)
        seccion_actual = grado_seccion.seccion

        for asignacion in docente_asignaciones:
            if asignacion.grado_seccion.seccion == seccion_actual:
                messages.error(request, 'El docente ya está asignado a una sección del mismo grado.')
                return redirect('administrarasignaciondocente')
        
        # Verificar si el docente ya tiene 2 asignaciones en total
        if docente_asignaciones.count() >= 2:
            messages.error(request, 'El docente ya tiene el máximo de asignaciones permitidas.')
            return redirect('administrarasignaciondocente')
        
        # Crear una nueva instancia de Asignacion con los objetos obtenidos
        docente = Docente.objects.get(dui=docente_dui)
        Asignacion.objects.create(docente=docente, grado_seccion=grado_seccion)
        messages.success(request, 'Asignación guardada con éxito')
        return redirect('administrarasignaciondocente')

    docentes = Docente.objects.all()
    grados_secciones = GradoSeccion.objects.all()

    return render(request, 'accounts/administrarasignaciondocente.html', {
        'docentes': docentes,
        'grados_secciones': grados_secciones
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
            # Realizar la validación adicional antes de guardar
            cleaned_data = form.cleaned_data
            docente = cleaned_data['docente']
            grado_seccion = cleaned_data['grado_seccion']
            if Asignacion.objects.filter(docente=docente, grado_seccion__seccion=grado_seccion.seccion).exclude(id=asignacion.id).exists():
                # Si el docente ya está asignado a una sección igual, mostrar un mensaje de error
                return JsonResponse({'success': False, 'message': 'El docente ya está asignado a una sección igual.'})
            else:
                # Si la validación pasa, guardar la asignación
                form.save()
                return JsonResponse({'success': True, 'message': 'Asignación actualizada con éxito.'})
        else:
            # Si el formulario no es válido, devolver errores
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
    if request.method == 'POST':
        form = SeleccionarGradoSeccionForm(request.POST)
        if form.is_valid():
            grado_seccion = form.cleaned_data['grado_seccion']
            fecha = form.cleaned_data['fecha']
            return redirect('registrar_asistencia', id_gradoseccion=grado_seccion.id, fecha=fecha)
    else:
        form = SeleccionarGradoSeccionForm()

    return render(request, 'asistencia/gestion_asistencia.html', {'form': form})


@login_required
def registrar_asistencia(request, id_gradoseccion, fecha=None):

    fecha = fecha or timezone.now().date() 
    estudiantes = Estudiante.objects.filter(id_gradoseccion=id_gradoseccion)
    asistencias = Asistencia.objects.filter(idgradoseccion=id_gradoseccion, fechaasistencia=fecha)
    
    if not asistencias.exists():

        for estudiante in estudiantes:
            Asistencia.objects.create(id_alumno=estudiante, idgradoseccion_id=id_gradoseccion, fechaasistencia=fecha)
        asistencias = Asistencia.objects.filter(idgradoseccion=id_gradoseccion, fechaasistencia=fecha)

    if request.method == 'POST':
        formset = AsistenciaFormSet(request.POST, queryset=asistencias)
        if formset.is_valid():
            formset.save()
            return redirect('asistencia_exitosa')
    else:
        formset = AsistenciaFormSet(queryset=asistencias)

    return render(request, 'asistencia/gestion_asistencia.html', {'formset': formset, 'fecha': fecha})