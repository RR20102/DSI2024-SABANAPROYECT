from django import forms

#Codigo Daniel 
from .models import Asignacion, Docente, Grado, Seccion

#Codigo Christian 
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
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

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ['dui', 
                  'nombreDocente', 
                  'apellidoDocente', 
                  'generoDocente', 
                  'direccionDocente', 
                  'correoDocente', 
                  'edadDocente', 
                  'telefonoDocente' ]
        widgets = {
            'telefonoDocente': forms.TextInput(attrs={'pattern': r'^\d{8}$'}),
            'dui': forms.TextInput(attrs={'pattern': r'^\d{9}$'}),
        }


    def __init__(self, *args, **kwargs):
        super(DocenteForm, self).__init__(*args, **kwargs)
        if self.errors:
            self.is_validated = True
        else:
            self.is_validated = False
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                field.widget.attrs.update({'class': 'form-control is-invalid'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_dui(self):
        dui = self.cleaned_data.get('dui')
        if len(dui) != 9 or not dui.isdigit():
            raise ValidationError('El DUI debe tener exactamente 9 dígitos.')
        return dui

    def clean_telefonoDocente(self):
        telefono = self.cleaned_data.get('telefonoDocente')
        if len(telefono) != 8 or not telefono.isdigit():
            raise ValidationError('El teléfono debe tener exactamente 8 dígitos.')
        return telefono

    def clean_correoDocente(self):
        correo = self.cleaned_data.get('correoDocente')
        if not correo:
            raise ValidationError('Por favor, ingrese un correo electrónico válido.')
        
        if User.objects.filter(email=correo).exists():
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, ingrese otro.')
        return correo
    
