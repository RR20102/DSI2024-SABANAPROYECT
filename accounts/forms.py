from django import forms
from django.forms.models import modelformset_factory


#Codigo Daniel 
from .models import Asignacion, Docente, GradoSeccion, Estudiante, Asistencia
from django.contrib.auth.models import User

#Codigo Christian 
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
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
            'nombreAlumno', 'apellidoAlumno', 'id_gradoseccion', 'edadAlumno', 'numeroTelefonoAlumno',
            'nombreResponsable', 'apellidoResposable', 'numeroTelefonoResposable',
            'duiResponsable', 'direccionResponsable', 'edadResponsable'
        ]
        widgets = {
            'nombreAlumno': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre'}),
            'apellidoAlumno': forms.TextInput(attrs={'placeholder': 'Ingrese el apellido'}),
            'id_gradoseccion': forms.Select(),
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
    

#Registro de asistencia
ASISTENCIA_CHOICES = [
        ('P', 'Presente'),
        ('A', 'Ausente'),
    ]

class SeleccionarGradoSeccionForm(forms.Form):
    grado_seccion = forms.ModelChoiceField(queryset=GradoSeccion.objects.all(), label="Grado y Sección")
    fecha = forms.DateField(widget=forms.SelectDateWidget(), label="Fecha de asistencia")

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['id_alumno', 'asistio']
        widgets = {
            'asistio': forms.RadioSelect(choices=ASISTENCIA_CHOICES),  # Usamos radio buttons
        }

AsistenciaFormSet = modelformset_factory(Asistencia, form=AsistenciaForm, extra=0)