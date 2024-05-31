from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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

