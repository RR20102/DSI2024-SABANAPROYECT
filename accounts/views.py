from django.shortcuts import render, redirect


#Añadido#
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

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
            
    return render(request, 'registration/login.html', {'form': form})

@login_required 
def home(request):

    return render(request, 'home.html')

def exit(request):
    logout(request)
    return redirect('home')


