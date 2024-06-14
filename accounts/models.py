from django.db import models
from django.contrib.auth.models import User
from django import template

# Create your models here.
register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name):
    user.groups.filter(name=group_name).exists()
    return  

#Codigo Agreado Christian 
class Docente(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE )
    dui= models.CharField(primary_key=True, max_length=9, null = False, unique= True)
    numeroTelefono = models.TextField(max_length=8, null = False)
    nombreDocente = models.CharField(max_length=100, null= False)
    apellidoDocente = models.TextField(max_length=100, null= False)
    generoDocente = models.CharField(max_length=1, null= False)
    direccionDocente = models.TextField(max_length=100, null = False)
    correoDocente = models.EmailField(unique= True, null = False )
    edadDocente = models.IntegerField()

    GRADOS_CHOICES = [
        ('Primer Grado', 'Primer Grado'),
        ('Segundo Grado', 'Segundo Grado'),
        ('Tercer Grado', 'Tercer Grado'),
        ('Cuarto Grado', 'Cuarto Grado'),
        ('Quinto Grado', 'Quinto Grado'),
        ('Sexto Grado', 'Sexto Grado'),
        ('Septimo Grado', 'Septimo Grado'),
        ('Octavo Grado', 'Octavo Grado'),
        ('Noveno Grado', 'Noveno Grado'),
    ]

    gradoAsignado = models.CharField(max_length=25, choices=GRADOS_CHOICES)
    fechaRegistroDocente = models.DateField(auto_now_add=True, null=False)

    def __str__(self):
        return f"{self.nombreDocente}   {self.apellidoDocente}"

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

    def __str__(self):
        return self.nombreAlumno      


#Codigo Agregado  Daniel
class Grado(models.Model):
    idGrado = models.AutoField(primary_key=True, unique=True, null=False)
    nombreGrado = models.CharField(max_length=25)

    def __str__(self):
        return self.nombreGrado


class Seccion(models.Model):
    idSeccion = models.AutoField(primary_key=True)
    nombreSeccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombreSeccion

class GradoSeccion(models.Model):
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='grado_secciones')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='grado_secciones')

    class Meta:
        unique_together = ('grado', 'seccion')

    def __str__(self):
        return f"{self.grado.nombreGrado} - {self.seccion.nombreSeccion}"


class Asignacion(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, related_name='asignaciones')
    grado_seccion = models.ForeignKey(GradoSeccion, on_delete=models.CASCADE, related_name='asignaciones')

    def __str__(self):
        return f"{self.docente.nombreDocente} - {self.grado_seccion.grado.nombreGrado} - {self.grado_seccion.seccion.nombreSeccion}"
