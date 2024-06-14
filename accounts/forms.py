from django import forms

#Codigo Daniel 
from .models import Asignacion, Docente, GradoSeccion

#Codigo Christian 
from django.contrib.auth.forms import AuthenticationForm

#Codigo Daniel 
class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['docente', 'grado_seccion']
    
    

#Codigo Christian 
class LoginForm(AuthenticationForm):
   def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'id_for_label': 'username',
            'id': 'username',
            'name': 'username',
            'placeholder': 'Ingrese Usuario',
            
        })
        
        self.fields['password'].widget.attrs.update({
            'id_for_label': 'password',
            'id': 'password',
            'name': 'password',
            'placeholder': 'contraseña',
        })

#Codigo Gustavo
class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = [
            'nombreDocente', 
            'apellidoDocente', 
            'generoDocente', 
            'edadDocente', 
            'direccionDocente',
            'correoDocente',
            'dui',
            'numeroTelefono'
         ]