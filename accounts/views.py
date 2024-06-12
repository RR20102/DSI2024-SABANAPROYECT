from django.shortcuts import render, get_object_or_404, redirect
#Importacion de modelos de la base de datos - Codigo Daniel 
from .models import Docente, Grado, Seccion, GradoSeccion, Asignacion
from .forms import AsignacionForm
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
@login_required 
def menuadministrador(request):
    return render(request, 'accounts/menuadministrador.html')
@login_required 
def registroestudiante(request):
    return render(request, 'accounts/registroestudiante.html')
@login_required 
def registrodocente(request):
    return render(request, 'accounts/registrodocente.html')
@login_required 
def visualizarregistro(request):
    return render(request, 'accounts/visualizardatosregistro.html')

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


def visualizarasignaciondocente(request):
    asignaciones = Asignacion.objects.all()
    return render(request, 'accounts/visualizarasignaciondocente.html', {'asignaciones': asignaciones})

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
    
# def editarasignacion(request, id):
#     asignacion = get_object_or_404(Asignacion, id=id)
#     if request.method == 'POST':
#         form = AsignacionForm(request.POST, instance=asignacion)
#         if form.is_valid():
#             # Realizar la validación adicional antes de guardar
#             cleaned_data = form.cleaned_data
#             docente = cleaned_data['docente']
#             grado_seccion = cleaned_data['grado_seccion']
#             if Asignacion.objects.filter(docente=docente, grado_seccion__seccion=grado_seccion.seccion).exclude(id=asignacion.id).exists():
#                 # Si el docente ya está asignado a una sección igual, mostrar un mensaje de error
#                 messages.error(request, 'El docente ya está asignado a una sección igual.')
#                 return redirect('editarasignacion', id=id)
#             else:
#                 # Si la validación pasa, guardar la asignación
#                 form.save()
#                 messages.success(request, 'Asignación actualizada con éxito.')
#                 return redirect('visualizarasignaciondocente')
#         else:
#             # Si el formulario no es válido, mostrar errores
#             messages.error(request, 'Por favor corrige los errores en el formulario.')
#     else:
#         form = AsignacionForm(instance=asignacion)

#     return render(request, 'accounts/editarasignacion.html', {'form': form, 'asignacion': asignacion})

# def editarasignacion(request, id):
#     asignacion = get_object_or_404(Asignacion, id=id)
#     if request.method == 'POST':
#         form = AsignacionForm(request.POST, instance=asignacion)
#         if form.is_valid():
#             form.save()
#             if request.is_ajax():
#                 return JsonResponse({'success': True})
#             messages.success(request, 'Asignación actualizada con éxito.')
#             return redirect('visualizarasignaciondocente')
#         else:
#             if request.is_ajax():
#                 return JsonResponse({'success': False, 'errors': form.errors})
#     else:
#         form = AsignacionForm(instance=asignacion)

#     return render(request, 'accounts/editarasignacion.html', {'form': form, 'asignacion': asignacion})


def eliminarasignacion(request, id):
    asignacion = get_object_or_404(Asignacion, id=id)
    if request.method == 'POST':
        asignacion.delete()
        messages.success(request, 'Asignación eliminada con éxito.')
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
