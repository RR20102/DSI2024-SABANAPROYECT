from django.forms import modelformset_factory, BaseModelFormSet
from .models import NotaActividad
from .forms import NotaActividadForm
from django.forms import ValidationError # Asegúrate de importar el formulario

class CustomNotaActividadFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()  # Llama a la validación estándar

        # Validación personalizada: ignora el campo `id_nota`
        for form in self.forms:
            if form.cleaned_data.get('nota') is None:
                raise forms.ValidationError("La nota es un campo obligatorio.")

# Crear el FormSet usando la clase personalizada
NotaActividadFormSet = modelformset_factory(
    NotaActividad,
    form=NotaActividadForm,
    formset=CustomNotaActividadFormSet,
    extra=0  # Ajusta esto según sea necesario
)