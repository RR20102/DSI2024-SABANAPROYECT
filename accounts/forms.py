from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Docente

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
        fields = ['dui', 'nombreDocente', 'apellidoDocente', 'generoDocente', 'direccionDocente', 'correoDocente']
        widgets = {
            'dui': forms.TextInput(attrs={'placeholder': '00000000-0'}),
            'nombreDocente': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre'}),
            'apellidoDocente': forms.TextInput(attrs={'placeholder': 'Ingrese el apellido'}),
            'generoDocente': forms.Select(choices=[('M', 'Masculino'), ('F', 'Femenino')]),
            'direccionDocente': forms.TextInput(attrs={'placeholder': 'Ingrese la dirección'}),
            'correoDocente': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
        }

    def clean_dui(self):
        """
        Validación personalizada para el DUI:
        - Verificar que el DUI tenga el formato correcto (xxxxxxxx-x).
        - Verificar que el DUI no esté duplicado (ignorando el usuario actual si está editando).
        """
        dui = self.cleaned_data['dui']

        # Verificar el formato del DUI
        if len(dui) != 10 or dui[8] != '-':
            raise forms.ValidationError("El DUI debe tener el formato: xxxxxxxx-x")

        # Verificar si el DUI ya existe (excluyendo al usuario actual si está editando)
        if Docente.objects.filter(dui=dui).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un docente con este DUI.")

        return dui

    def clean_generoDocente(self):
        """
        Validación personalizada para el género:
        - Asegurar que solo se permitan valores válidos ('M' o 'F').
        """
        genero = self.cleaned_data['generoDocente']
        if genero not in ['M', 'F']:
            raise forms.ValidationError("Seleccione un género válido (M/F).")
        return genero

    def clean(self):
        """ Validaciones adicionales a nivel de formulario """
        cleaned_data = super().clean()
        # ... agregar validaciones adicionales si es necesario ...
        return cleaned_data