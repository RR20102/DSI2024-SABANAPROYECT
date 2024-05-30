from django.shortcuts import render

#Añadido#
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Login successful')
        else:
            messages.error(request, 'Credenciales Invalidas.')
    return render(request, 'accounts/login.html')
  