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


class EstudianteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Contraseña')

    class Meta:
        model = Estudiante
        fields = [
            'nombreAlumno', 'apellidoAlumno', 'edadAlumno', 'numeroTelefonoAlumno',
            'nombreResponsable', 'apellidoResposable', 'numeroTelefonoResposable',
            'duiResponsable', 'direccionResponsable', 'edadResponsable'
        ]

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        nombreAlumno = cleaned_data.get('nombreAlumno')
        apellidoAlumno = cleaned_data.get('apellidoAlumno')
        password = cleaned_data.get('password')
        
        # Generar el username combinando el nombre y apellido del estudiante
        username = f"{nombreAlumno.lower()}.{apellidoAlumno.lower()}"

        # Asegurarse de que el username es único
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            password=password,
        )

        estudiante = super().save(commit=False)
        estudiante.user = user
        if commit:
            estudiante.save()
        return estudiante

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