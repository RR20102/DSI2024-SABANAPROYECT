from django.contrib import admin
from .models import Grado, Seccion, GradoSeccion, Docente, Estudiante
# Register your models here.

admin.site.register(Grado)
admin.site.register(Seccion)
admin.site.register(GradoSeccion)
admin.site.register(Docente)
admin.site.register(Estudiante)