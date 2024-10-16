from django.db import models
from django.contrib.auth.models import User
from django import template
from django.core.validators import RegexValidator

# Create your models here.
register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name):
    user.groups.filter(name=group_name).exists()
    return  

#Codigo Agreado Christian 
class Docente(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    user = models.OneToOneField(User, on_delete= models.CASCADE )
    dui= models.CharField(primary_key=True, max_length=9, null = False, unique= True)
    nombreDocente = models.CharField(max_length=100, null= False)
    apellidoDocente = models.CharField(max_length=100, null= False)
    generoDocente = models.CharField(max_length=1, null= False, choices=GENERO_CHOICES)
    direccionDocente = models.CharField(max_length=100, null = False)
    correoDocente = models.EmailField(unique= True, null = False )
    fechaRegistroDocente = models.DateField(auto_now_add=True, null=False)
    edadDocente = models.IntegerField(null=False)
    telefonoDocente = models.CharField(max_length = 8, validators=[RegexValidator(r'^\d{8}$', 'Ingrese un número de teléfono válido de 8 dígitos.')] ,null = False)


    def __str__(self):
        return f"{self.nombreDocente}   {self.apellidoDocente}"


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
    id_gradoseccion = models.AutoField(primary_key=True, unique=True, null=False)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='grado_secciones')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='grado_secciones')

    class Meta:
        unique_together = ('grado', 'seccion')

    def __str__(self):
        return f"{self.grado.nombreGrado} - {self.seccion.nombreSeccion}"




class Estudiante(models.Model):
    
  
    user = models.OneToOneField(User, on_delete= models.CASCADE )
    id_alumno = models.AutoField(primary_key= True, unique= True, null= False)
    nombreAlumno = models.CharField(max_length = 100, null= False)
    apellidoAlumno = models.CharField(max_length = 100, null= False)
    edadAlumno = models.IntegerField(null=False)
    id_gradoseccion = models.ForeignKey(GradoSeccion, on_delete=models.RESTRICT)
    numeroTelefonoAlumno = models.CharField(max_length = 8, null = False)
    fechaRegistroAlumno = models.DateField(auto_now_add=True, null=False)
    nombreResponsable = models.CharField(max_length = 100, null= False)
    apellidoResposable = models.CharField(max_length = 100, null= False)
    numeroTelefonoResposable = models.CharField(max_length = 8, null = False)
    duiResponsable= models.CharField( max_length=9, null = False, unique= True)
    direccionResponsable = models.CharField(max_length=100, null = False)
    edadResponsable = models.IntegerField(null=False) 


    def __str__(self):
        return f"{self.nombreAlumno} d{self.apellidoAlumno}"      


class Asignacion(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, related_name='asignaciones')
    grado_seccion = models.ForeignKey(GradoSeccion, on_delete=models.CASCADE, related_name='asignaciones')

    def __str__(self):
        return f"{self.docente.nombreDocente} - {self.grado_seccion.grado.nombreGrado} - {self.grado_seccion.seccion.nombreSeccion}"

#segundo sprint
class TipoActividad(models.Model):
    id_tipoactividad = models.AutoField(primary_key=True, unique=True, null=False)
    nombretipoactividad = models.CharField(max_length=100)

class Materia(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nombre_materia = models.CharField(max_length=25)
    anio_materia = models.IntegerField()

class MateriaGradoSeccion(models.Model):
    id_matrgrasec = models.AutoField(primary_key=True, unique=True, null=False)
    id_materia = models.ForeignKey(Materia, on_delete=models.RESTRICT, null=True)
    id_gradoseccion = models.ForeignKey(GradoSeccion, on_delete=models.RESTRICT, null=True)


class DocenteMateriaGrado(models.Model):
    id_doc_mat_grado = models.AutoField(primary_key=True, unique=True, null=False)
    dui = models.ForeignKey(Docente, on_delete=models.RESTRICT, null=True)
    id_matrgrasec = models.ForeignKey(MateriaGradoSeccion, on_delete=models.RESTRICT)


class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True, unique=True, null=False)
    id_alumno = models.ForeignKey(Estudiante, on_delete=models.RESTRICT)
    idgradoseccion = models.ForeignKey(GradoSeccion, on_delete=models.RESTRICT)
    fechaasistencia = models.DateField()
    asistio = models.CharField(max_length=1)

class Conducta(models.Model):
    id_conducta = models.AutoField(primary_key=True, unique=True, null=False)
    id_alumno = models.ForeignKey(Estudiante, on_delete=models.RESTRICT)
    fecha_conducta = models.CharField(max_length=15)
    obsevacion_conducta = models.CharField(max_length=250)
    nota_conducta = models.FloatField()

class ActividadAcademica(models.Model):
    id_actividad = models.AutoField(primary_key=True, unique=True, null=False)
    id_tipoactividad = models.ForeignKey(TipoActividad, on_delete=models.RESTRICT, unique=True, null=False)
    id_alumno = models.ForeignKey(Estudiante, on_delete=models.RESTRICT)
    id_matrgrasec = models.ForeignKey(MateriaGradoSeccion, on_delete=models.RESTRICT)
    nombre_actividad = models.CharField(max_length=25)
    descripcion_actividad = models.CharField(max_length=50)
    fecha_actividad = models.DateField()
    nota = models.FloatField()

#Codigo para Horarios de Clases 
class HorarioClase(models.Model):
    docente_materia_grado = models.ForeignKey(DocenteMateriaGrado, on_delete=models.CASCADE, null=True)  # Ahora permite valores nulos
    dia_semana = models.CharField(max_length=9, choices=[
        ('Lunes', 'Lunes'), 
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'), 
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('docente_materia_grado', 'dia_semana', 'hora_inicio', 'hora_fin')

    def __str__(self):
        return f"{self.docente_materia_grado} ({self.dia_semana}, {self.hora_inicio} - {self.hora_fin})"