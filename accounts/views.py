from django.shortcuts import render, get_object_or_404, redirect
#Importacion de modelos de la base de datos - Codigo Daniel 
from .models import Docente, Grado, Seccion, Asignacion
#from .forms import AsignacionForm
from django.contrib import messages  # Importa messages
from django.http import JsonResponse

#Codigo Christian 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

#Login Codigo Christian 
def login_view(request):
    
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciales Invalidas.')
            
    return render(request, 'accounts/login.html', {'form': form})

@login_required 
def home(request):

    return render(request, 'accounts/home.html')

def exit(request):
    logout(request)
    return redirect('home')


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