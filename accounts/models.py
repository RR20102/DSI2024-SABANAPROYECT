from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#Codigo Agreado Christian 
class Docente(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE )
    dui= models.CharField(primary_key=True, max_length=9, null = False, unique= True)
    nombreDocente = models.TextField(max_length=100, null= False)
    apellidoDocente = models.TextField(max_length=100, null= False)
    generoDocente = models.CharField(max_length=1, null= False)
    direccionDocente = models.TextField(max_length=100, null = False)
    correoDocente = models.EmailField(unique= True, null = False )
    fechaRegistroDocente = models.DateField(auto_now_add=True, null=False)

class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE )
    id_alumno = models.AutoField(primary_key= True, unique= True, null= False)
    nombreAlumno = models.TextField(max_length = 100, null= False)
    apellidoAlumno = models.TextField(max_length = 100, null= False)
    edadAlumno = models.IntegerField(null=False)
    numeroTelefonoAlumno = models.CharField(max_length = 8, null = False)
    fechaRegistroAlumno = models.DateField(auto_now_add=True, null=False)
    nombreResponsable = models.TextField(max_length = 100, null= False)
    apellidoResposable = models.TextField(max_length = 100, null= False)
    numeroTelefonoResposable = models.CharField(max_length = 8, null = False)
    duiResponsable= models.CharField( max_length=9, null = False, unique= True)
    direccionResponsable = models.TextField(max_length=100, null = False)
    edadResponsable = models.IntegerField(null=False)       


#Codigo Agregado  Daniel 
class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    # Otros campos relevantes para el docente, como edad, asignatura, etc.

    def __str__(self):
        return self.nombre

class Grado(models.Model):
    #id_grado = models.AutoField(primary_key= True, unique= True, null= False)
    nombre = models.CharField(max_length=100)
    # Otros campos relevantes para el grado, como nivel, año, etc.
    #Agregar autoincrementable que sea la llave primaria 

    def __str__(self):
        return self.nombre

class Seccion(models.Model):
    #id_seccion = models.AutoField(primary_key= True, unique= True, null= False)
    nombre = models.CharField(max_length=100)
    # Otros campos relevantes para la sección, como horario, número de estudiantes, etc.

    def __str__(self):
        return self.nombre

class Asignacion(models.Model):
    #id_asignacion = models.AutoField(primary_key= True, unique= True, null= False)
    docente_nombre = models.CharField(max_length=100)  # Cambiar a CharField
    grado_nombre = models.CharField(max_length=100)    # Cambiar a CharField
    seccion_nombre = models.CharField(max_length=100)  # Cambiar a CharField

    def __str__(self):
        return f"{self.docente} - {self.grado} - {self.seccion}"