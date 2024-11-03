from django import forms
from django.forms.models import modelformset_factory
import calendar


#Codigo Daniel 
from .models import Asignacion, Docente, GradoSeccion, Estudiante, Asistencia, MateriaGradoSeccion, DocenteMateriaGrado, TipoActividad, ActividadAcademica, NotaActividad, Conducta
from django.contrib.auth.models import User

#Codigo Christian 
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django_select2.forms import Select2MultipleWidget
from django.forms import modelformset_factory
#Codigo Daniel 

class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['docente', 'grado_seccion']
        widgets = {
            'docente': forms.Select(attrs={'class': 'select-form'}),
            'grado_seccion': forms.Select(attrs={'class': 'select-form'}),
        }

    def __init__(self, *args, **kwargs):
        super(AsignacionForm, self).__init__(*args, **kwargs)
        
        # Cambiar las opciones para el campo 'grado_seccion' para usar 'id_gradoseccion'
        self.fields['grado_seccion'].queryset = GradoSeccion.objects.all()
        self.fields['grado_seccion'].label_from_instance = lambda obj: f"{obj.grado.nombreGrado} - {obj.seccion.nombreSeccion}"


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

class AsistenciaForm(forms.ModelForm):
    asistio = forms.ChoiceField(choices=ASISTENCIA_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Asistencia
        fields = ['id_alumno', 'asistio']

    def clean_id_alumno(self):
        id_alumno = self.cleaned_data.get('id_alumno')
        if not id_alumno:
            raise forms.ValidationError("El campo 'id_alumno' es obligatorio.")
        return id_alumno


AsistenciaFormSet = modelformset_factory(Asistencia, form=AsistenciaForm, extra=0)


class GradoSeccionForm(forms.Form):
    grado_seccion = forms.ModelChoiceField(
        queryset=GradoSeccion.objects.none(),  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de asistencia"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GradoSeccionForm, self).__init__(*args, **kwargs)
        
        if user and hasattr(user, 'docente'):
            docente = user.docente
            grados_secciones_asignados = Asignacion.objects.filter(docente=docente).values_list('grado_seccion__id_gradoseccion', flat=True)
            self.fields['grado_seccion'].queryset = GradoSeccion.objects.filter(id_gradoseccion__in=grados_secciones_asignados)

MESES = [
    ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), 
    ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'), 
    ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
]

YEARS = [(str(year), str(year)) for year in range(2020, 2031)]

class ReporteAsistenciaForm(forms.Form):
    grado_seccion = forms.ModelChoiceField(queryset=GradoSeccion.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    mes = forms.ChoiceField(
        choices=MESES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Mes"
    )
    año = forms.ChoiceField(
        choices=YEARS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Año"
    )





#Codigo Daniel SP2 Asignacion de Horarios de Clases 
from .models import HorarioClase, DocenteMateriaGrado

class HorarioClaseForm(forms.ModelForm):
    class Meta:
        model = HorarioClase
        fields = ['docente_materia_grado', 'dia_semana', 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(HorarioClaseForm, self).__init__(*args, **kwargs)
        self.fields['docente_materia_grado'].queryset = DocenteMateriaGrado.objects.all()
        self.fields['docente_materia_grado'].label_from_instance = lambda obj: f"{obj.dui} - {obj.id_matrgrasec.id_materia.nombre_materia} - {obj.id_matrgrasec.id_gradoseccion.grado.nombreGrado} - {obj.id_matrgrasec.id_gradoseccion.seccion.nombreSeccion}"

    # Validación para evitar conflictos de horarios
    def clean(self):
        cleaned_data = super().clean()
        docente_materia_grado = cleaned_data.get("docente_materia_grado")
        dia_semana = cleaned_data.get("dia_semana")
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")
        

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
             raise forms.ValidationError("La hora de fin debe ser mayor que la hora de inicio.")

         # Verificar si el horario se está editando
        if self.instance and self.instance.id:  # Verifica si es una instancia existente
            # Excluir el horario actual de la verificación
            horarios_conflictivos = HorarioClase.objects.filter(
                docente_materia_grado=docente_materia_grado,
                dia_semana=dia_semana,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            ).exclude(id=self.instance.id)  # Excluir el horario que se está editando
            
            if horarios_conflictivos.exists():
                raise forms.ValidationError("Ya existe un horario conflictivo para este docente y materia.")
        else:
            # Si no es una instancia existente, solo verificar si hay conflictos
            if HorarioClase.objects.filter(
                docente_materia_grado=docente_materia_grado,
                dia_semana=dia_semana,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            ).exists():
                raise forms.ValidationError("Ya existe un horario conflictivo para este docente y materia.")

        return cleaned_data


class DocenteMateriaGradoForm(forms.ModelForm):
    # Reemplazamos el campo id_matrgrasec por un multiselect
    id_matrgrasec = forms.ModelMultipleChoiceField(
        queryset=MateriaGradoSeccion.objects.all(),
        widget=Select2MultipleWidget,  # Usamos Select2MultipleWidget
        required=True
    )

    class Meta:
        model = DocenteMateriaGrado
        fields = ['dui', 'id_matrgrasec']


class ActividadAcademicaForm(forms.ModelForm):
    class Meta:
        model = ActividadAcademica
        fields = ['id_tipoactividad', 'id_matrgrasec', 'nombre_actividad', 'descripcion_actividad', 'fecha_actividad']
        widgets = {
            'fecha_actividad': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Aseguramos que el widget sea tipo "date"
        }
        labels = {
            'id_tipoactividad': 'Tipo de Actividad', 
            'id_matrgrasec' : 'Materia Asignada',
            'nombre_actividad' : 'Nombre de la Actividad',
            'descripcion_actividad' : 'Descripción de la Actividad',
            'fecha_actividad' : 'Fecha de la Actividad'
        }
    def __init__(self, *args, **kwargs):
        # Obtenemos el docente (docente actual) del contexto que pasaremos en la vista
        docente = kwargs.pop('docente', None)
        super(ActividadAcademicaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_actividad'].input_formats = ['%Y-%m-%d']
        # Filtrar el campo id_matrgrasec para mostrar solo las materias asignadas al docente
        if docente:
            # Obtener los MateriaGradoSeccion asignados al docente
            materias_asignadas = DocenteMateriaGrado.objects.filter(dui=docente).values_list('id_matrgrasec', flat=True)
            
            # Filtrar el queryset de id_matrgrasec en base a las materias del docente
            self.fields['id_matrgrasec'].queryset = self.fields['id_matrgrasec'].queryset.filter(id_matrgrasec__in=materias_asignadas)

        # Añadir clases de Bootstrap 5 a los campos del formulario
        self.fields['id_tipoactividad'].widget.attrs.update({'class': 'form-control'})
        self.fields['id_matrgrasec'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre_actividad'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion_actividad'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_actividad'].widget.attrs.update({'class': 'form-control', 'type': 'date'})

    
"""class NotaActividadForm(forms.ModelForm):

   class Meta:
        model = NotaActividad
        fields = ['nota', 'id_actividad']  # Solo queremos editar la nota
        # Personalizar el widget para que sea un campo de entrada numérico
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 10, 'class': 'form-control'} ),
        'id_actividad': forms.HiddenInput()
        }
         
        
    def __init__(self, *args, **kwargs):
        actividad_id = kwargs.pop('actividad_id', None)  # Extraemos actividad_id si se pasa
        super().__init__(*args, **kwargs)
        
        # Aseguramos que se define un nombre específico si `actividad_id` está presente
        if actividad_id:
            self.fields['nota'].widget.attrs.update({
                'id': f'nota_{actividad_id}',  # Nombre único por ID de actividad
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'step': '0.1'
            })

            if actividad_id:
                self.fields['actividad_id'] = forms.IntegerField(initial=actividad_id, widget=forms.HiddenInput())
"""


class NotaActividadForm(forms.ModelForm):
    class Meta:
        model = NotaActividad
        fields = ['id_nota','nota']  # Solo incluimos el campo 'nota'
        widgets = {
            'id_nota': forms.HiddenInput(),
            'id_actividad': forms.HiddenInput(),  # Lo configuramos como campo oculto
            'nota': forms.NumberInput(attrs={'step': '0.01', 'min': 0, 'max': 10, 'required': 'true','class': 'form-control'})  # Suponiendo que las notas son de 0 a 10
        }

    def clean_nota(self):
        nota = self.cleaned_data.get('nota')
        if nota is not None and (nota < 0 or nota > 10):
            raise forms.ValidationError("La nota debe estar entre 0 y 10.")
        return nota



#Registro de Conducta 
class ConductaForm(forms.ModelForm):
    class Meta:
        model = Conducta
        fields = ['fecha_conducta', 'obsevacion_conducta', 'nota_conducta']
        widgets = {
            'fecha_conducta': forms.DateInput(attrs={'type': 'date'}),
            'obsevacion_conducta': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observación de la conducta...'}),
            'nota_conducta': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'Ingrese la nota'}),
        }

    def __init__(self, *args, **kwargs):
        super(ConductaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_conducta'].label = "Fecha de Conducta"
        self.fields['obsevacion_conducta'].label = "Observación"
        self.fields['nota_conducta'].label = "Nota"
# class ConductaForm(forms.ModelForm):
#     class Meta:
#         model = Conducta
#         fields = ['descripcion', 'fecha', 'observacion']
#         labels = {
#             'descripcion': 'Descripción de la Conducta',
#             'fecha': 'Fecha',
#             'observacion': 'Observación Adicional'
#         }
#         widgets = {
#             'fecha': forms.DateInput(attrs={'type': 'date'})
#         }

# class ConductaForm(forms.ModelForm):
#     class Meta:
#         model = Conducta
#         fields = ['id_alumno', 'fecha_conducta', 'obsevacion_conducta', 'nota_conducta']
#         labels = {
#             'id_alumno': 'Estudiante',
#             'fecha_conducta': 'Fecha',
#             'obsevacion_conducta': 'Observación',
#             'nota_conducta': 'Nota de Conducta',
#         }
         
#         widgets = {
#             'fecha_conducta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#         }