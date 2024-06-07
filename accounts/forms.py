from django import forms
from .models import Asignacion, Docente, Grado, Seccion

class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['docente_nombre', 'grado_nombre', 'seccion_nombre']