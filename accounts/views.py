from django.shortcuts import render, get_object_or_404, redirect
#Importacion de modelos de la base de datos - Codigo Daniel 
from .models import Docente, Grado, Seccion, Asignacion, Estudiante
#from .forms import AsignacionForm
from django.contrib import messages  # Importa messages
from django.http import JsonResponse
import json

#Codigo Christian 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from .forms import LoginForm
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

def envio_correo(request):

    try:
        to_email = 'christianadonayriveralopez@gmail.com'
        subject = 'Mensaje de prueba'
        message = 'este es un mensaje de prueba'
        send_mail(subject, message, None, [to_email])
        return HttpResponse('Correo enviado con exito')
    except Exception as e:
        error_message = str(e)
    return HttpResponse(error_message)
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
        dict: Información sobre el registro, incluyendo el username y la contraseña si es exitoso.
    """
    try:
        # Validar que el correo electrónico sea único
        if User.objects.filter(email=correo_electronico).exists():
            return {'success': False, 'message': 'El correo electrónico ya está registrado.'}
        
        # Generar un nombre de usuario único
        username = generate_unique_username(nombre, apellidos)
        
        # Generar una contraseña aleatoria
        password = generate_random_password()
        
        # Crear el usuario
        user = User.objects.create_user(username=username, password=password, email=correo_electronico)
        user.first_name = nombre
        user.last_name = apellidos
        user.save()
        
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
        
        # Enviar el correo electrónico con el username y la contraseña
        try:
            # Enviar el correo electrónico con el username y la contraseña
            send_mail(
                'No responsa a Este correo - Registro exitoso',
                f'Escuela La Sabana \n {docente.__str__()} Su usuario ha sido creado exitosamente.\n\nUsername: {username}\nContraseña: {password}',
                'admin@example.com',  # Debería ser el correo del sistema
                [correo_electronico],
                fail_silently=False,
            )
        except SMTPException as e:
            return {'success': False, 'message': 'El usuario fue creado, pero ocurrió un error al enviar el correo electrónico.'}
        
        return {'success': True, 'username': username, 'password': password}
    
    except IntegrityError as e:
        return {'success': False, 'message': str(e)}
    except ValidationError as e:
        return {'success': False, 'message': str(e)}
    

#Codigo Menu administrador - Agregado por Daniel 
def menuadministrador(request):
    return render(request, 'accounts/menuadministrador.html')

def registroestudiante(request):
    return render(request, 'accounts/registroestudiante.html')

def registrodocente(request):
    return render(request, 'accounts/registrodocente.html')

def visualizarregistro(request):
    return render(request, 'accounts/visualizardatosregistro.html')

def visualizarasignaciondocente(request):
    asignaciones = Asignacion.objects.all()
    return render(request, 'accounts/visualizarasignaciondocente.html', {
        'asignaciones': asignaciones
    })


"""def administrarasignaciondocente(request):
    if request.method == 'POST':
        docente_nombre = request.POST.get('docente')
        grado_nombre = request.POST.get('grado')
        seccion_nombre = request.POST.get('seccion')

        if not (docente_nombre and grado_nombre and seccion_nombre):
            messages.error(request, 'Debes seleccionar un docente, un grado y una sección.')
        else:
            docente = Docente.objects.get(nombre=docente_nombre)
            grado = Grado.objects.get(nombre=grado_nombre)
            seccion = Seccion.objects.get(nombre=seccion_nombre)
        
            Asignacion.objects.create(docente_nombre=docente, grado_nombre=grado, seccion_nombre=seccion)
            messages.success(request, 'Datos guardados con éxito')

        return redirect('administrarasignaciondocente')  # Redirige a la misma página

    docentes = Docente.objects.all().order_by('id')
    grados = Grado.objects.all().order_by('id')
    secciones = Seccion.objects.all().order_by('id')

    return render(request, 'accounts/administrarasignaciondocente.html', {
        'docentes': docentes, 
        'grados': grados, 
        'secciones': secciones
    }) """


"""def editarasignacion(request, id):
    asignacion = get_object_or_404(Asignacion, id=id)
    if request.method == 'POST':
        form = AsignacionForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignación actualizada con éxito')
            return redirect('visualizarasignaciondocente')
    else:
        form = AsignacionForm(instance=asignacion)
    
    return render(request, 'accounts/editarasignacion.html', {
        'form': form,
        'asignacion': asignacion
    }) """


"""def eliminarasignacion(request, id):
    asignacion = get_object_or_404(Asignacion, id=id)
    if request.method == 'POST':
        asignacion.delete()
        messages.success(request, 'Asignación eliminada con éxito')
        # Enviar una respuesta JSON para mostrar el mensaje con SweetAlert2
        return JsonResponse({'success': True})

    return redirect('editarasignacion', id=id)  # Si no es una solicitud POST, redirecciona a la página de edición
    """