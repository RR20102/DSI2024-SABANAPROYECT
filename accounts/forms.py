from django import forms

#Codigo Daniel 
from .models import Asignacion, Docente, GradoSeccion, Estudiante
from django.contrib.auth.models import User

#Codigo Christian 
from django.contrib.auth.forms import AuthenticationForm

#Codigo Daniel 
class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['docente', 'grado_seccion']
        widgets = {
            'docente' : forms.Select(attrs={'class':'select-form'}),
            'grado_seccion' : forms.Select(attrs={'class':'select-form'}),
        }

class EstudianteForm(forms.ModelForm):

    class Meta:
        model = Estudiante
        fields = [
            'nombreAlumno', 'apellidoAlumno', 'edadAlumno', 'numeroTelefonoAlumno',
            'nombreResponsable', 'apellidoResposable', 'numeroTelefonoResposable',
            'duiResponsable', 'direccionResponsable', 'edadResponsable'
        ]
        widgets = {
            'nombreAlumno': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre'}),
            'apellidoAlumno': forms.TextInput(attrs={'placeholder': 'Ingrese el apellido'}),
            'edadAlumno': forms.NumberInput(attrs={'placeholder': 'Ingrese la edad'}),
            'numeroTelefonoAlumno': forms.TextInput(attrs={'placeholder': 'Ingrese el número de teléfono', 'pattern': r'^\d{8}$'}),
            'nombreResponsable': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre'}),
            'apellidoResposable': forms.TextInput(attrs={'placeholder': 'Ingrese el apellido'}),
            'numeroTelefonoResposable': forms.TextInput(attrs={'placeholder': 'Ingrese el número de teléfono', 'pattern': r'^\d{8}$'}),
            'duiResponsable': forms.TextInput(attrs={'placeholder': 'Ingrese el DUI', 'pattern': r'^\d{9}$'}),
            'direccionResponsable': forms.Textarea(attrs={'placeholder': 'Ingrese la dirección'}),
            'edadResponsable': forms.NumberInput(attrs={'placeholder': 'Ingrese la edad'}),
        }

    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        if self.errors:
            self.is_validated = True
        else:
            self.is_validated = False
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                field.widget.attrs.update({'class': 'form-control is-invalid'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_edadAlumno(self):
        edadAlumno = self.cleaned_data.get('edadAlumno')
        if edadAlumno <= 0:
            raise forms.ValidationError('La edad debe ser mayor que cero')
        return edadAlumno

    def clean_edadResponsable(self):
        edadResponsable = self.cleaned_data.get('edadResponsable')
        if edadResponsable <= 0:
            raise forms.ValidationError('La edad debe ser mayor que cero')
        return edadResponsable

    def clean_duiResponsable(self):
        duiResponsable = self.cleaned_data.get('duiResponsable')
        if len(duiResponsable) != 9 or not duiResponsable.isdigit():
            raise forms.ValidationError('El DUI debe tener exactamente 9 dígitos')
        return duiResponsable

    def clean_numeroTelefonoAlumno(self):
        numeroTelefonoAlumno = self.cleaned_data.get('numeroTelefonoAlumno')
        if len(numeroTelefonoAlumno) != 8 or not numeroTelefonoAlumno.isdigit():
            raise forms.ValidationError('El número de teléfono debe tener exactamente 8 dígitos')
        return numeroTelefonoAlumno

    def clean_numeroTelefonoResposable(self):
        numeroTelefonoResposable = self.cleaned_data.get('numeroTelefonoResposable')
        if len(numeroTelefonoResposable) != 8 or not numeroTelefonoResposable.isdigit():
            raise forms.ValidationError('El número de teléfono debe tener exactamente 8 dígitos')
        return numeroTelefonoResposable

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