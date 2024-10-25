from django.contrib import admin
from .models import Grado, Seccion, GradoSeccion, Docente, Estudiante, Materia, MateriaGradoSeccion,DocenteMateriaGrado,TipoActividad
# Register your models here.

admin.site.register(Grado)
admin.site.register(Seccion)
admin.site.register(GradoSeccion)
admin.site.register(Docente)
admin.site.register(Estudiante)
admin.site.register(Materia)
admin.site.register(MateriaGradoSeccion)
admin.site.register(DocenteMateriaGrado)
admin.site.register(TipoActividad)
