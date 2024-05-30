from django.db import models

# Create your models here.
class Docente(models.Model):
    dui= models.CharField(primary_key=True, max_length=9, null = False, unique= True)
    nombreDocente = models.TextField(max_length=100, null= False)
    apellidoDocente = models.TextField(max_length=100, null= False)
    generoDocente = models.CharField(max_length=1, null= False)
    direccionDocente = models.TextField(max_length=100, null = False)
    correoDocente = models.EmailField(unique= True, null = False )
    fechaRegistroDocente = models.DateField(auto_now_add=True, null=False)