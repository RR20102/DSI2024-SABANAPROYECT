# Importamos los modelos necesarios
from accounts.models import Materia, GradoSeccion, MateriaGradoSeccion

# Obtenemos todas las materias
todas_las_materias = Materia.objects.all()

# Obtenemos todas las combinaciones de grados y secciones
todos_los_grados_secciones = GradoSeccion.objects.all()

# Lista para almacenar las instancias de MateriaGradoSeccion a insertar
materia_grado_seccion_combinaciones = []

# Iteramos sobre todas las materias
for materia in todas_las_materias:
    # Iteramos sobre todos los grados y secciones
    for gradoseccion in todos_los_grados_secciones:
        # Creamos una instancia de MateriaGradoSeccion
        combinacion = MateriaGradoSeccion(
            id_materia=materia,
            id_gradoseccion=gradoseccion
        )
        # Añadimos la instancia a la lista
        materia_grado_seccion_combinaciones.append(combinacion)

# Insertamos todas las combinaciones en la base de datos de una vez
MateriaGradoSeccion.objects.bulk_create(materia_grado_seccion_combinaciones)

print(f"Se han insertado {len(materia_grado_seccion_combinaciones)} combinaciones de Materia y GradoSeccion.")