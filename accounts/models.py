from django.db import models

# Create your models here.

class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    # Otros campos relevantes para el docente, como edad, asignatura, etc.

    def __str__(self):
        return self.nombre

class Grado(models.Model):
    nombre = models.CharField(max_length=100)
    # Otros campos relevantes para el grado, como nivel, año, etc.

    def __str__(self):
        return self.nombre

class Seccion(models.Model):
    nombre = models.CharField(max_length=100)
    # Otros campos relevantes para la sección, como horario, número de estudiantes, etc.

    def __str__(self):
        return self.nombre

class Asignacion(models.Model):

    docente_nombre = models.CharField(max_length=100)  # Cambiar a CharField
    grado_nombre = models.CharField(max_length=100)    # Cambiar a CharField
    seccion_nombre = models.CharField(max_length=100)  # Cambiar a CharField

    def __str__(self):
        return f"{self.docente} - {self.grado} - {self.seccion}"