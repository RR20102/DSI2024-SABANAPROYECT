from django import forms

#Codigo Daniel 
from .models import Asignacion, Docente, Grado, Seccion

#Codigo Christian 
from django.contrib.auth.forms import AuthenticationForm

#Codigo Daniel 
"""class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['docente_nombre', 'grado_nombre', 'seccion_nombre'] """


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