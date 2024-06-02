from django.shortcuts import render

#Codigo Menu administrador - Agregado por Daniel 
def menuadministrador(request):
    return render(request, 'accounts/menuadministrador.html')

def registroestudiante(request):
    return render(request, 'accounts/registroestudiante.html')

def registrodocente(request):
    return render(request, 'accounts/registrodocente.html')

def visualizarregistro(request):
    return render(request, 'accounts/visualizardatosregistro.html')

def administrarasignaciondocente(request):
    return render(request, 'accounts/administrarasignaciondocente.html')

def visualizarasignaciondocente(request):
    return render(request, 'accounts/visualizarasignaciondocente.html')