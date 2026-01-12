"""
Limpiar respuestas antiguas del ejercicio 1.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matelog_backend.settings')
django.setup()

from tracking.models import RespuestaEjercicio
from lessons.models import Ejercicio

print("=" * 80)
print("LIMPIANDO RESPUESTAS ANTIGUAS DEL EJERCICIO 1")
print("=" * 80)
print()

ejercicio = Ejercicio.objects.get(id=1)

# Buscar respuestas del ejercicio 1
respuestas = RespuestaEjercicio.objects.filter(ejercicio=ejercicio)

print(f"Respuestas encontradas para el ejercicio 1: {respuestas.count()}")
print()

if respuestas.count() > 0:
    print("DETALLES DE LAS RESPUESTAS:")
    print("-" * 80)
    for resp in respuestas:
        print(f"  Usuario: {resp.usuario.username}")
        print(f"  Respuesta: '{resp.respuesta_usuario}'")
        print(f"  Es correcta: {resp.es_correcta}")
        print(f"  Fecha: {resp.fecha_respuesta}")
        print()

    # Eliminar todas
    confirmacion = input("¿Eliminar todas estas respuestas? (si/no): ")
    if confirmacion.lower() == 'si':
        count = respuestas.count()
        respuestas.delete()
        print(f"\n✓ {count} respuestas eliminadas correctamente")
        print("\nAhora puedes volver a responder el ejercicio 1")
    else:
        print("\nNo se eliminó nada")
else:
    print("No hay respuestas registradas para el ejercicio 1")

print()
print("=" * 80)
