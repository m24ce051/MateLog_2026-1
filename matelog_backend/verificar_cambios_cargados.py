"""
Verificar si el servidor tiene los cambios cargados.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matelog_backend.settings')
django.setup()

from lessons.models import Ejercicio
import inspect

print("=" * 80)
print("VERIFICACION: ¿EL SERVIDOR TIENE LOS CAMBIOS CARGADOS?")
print("=" * 80)
print()

# Obtener el código fuente del método validar_respuesta
codigo = inspect.getsource(Ejercicio.validar_respuesta)

print("Codigo del metodo validar_respuesta:")
print("-" * 80)
print(codigo)
print("-" * 80)
print()

# Verificar si tiene los cambios nuevos
if 'string.punctuation' in codigo:
    print("RESULTADO: SI TIENE LOS CAMBIOS NUEVOS")
    print("El codigo incluye la eliminacion de puntuacion")
else:
    print("RESULTADO: NO TIENE LOS CAMBIOS - CODIGO ANTIGUO")
    print("El codigo NO incluye string.punctuation")

print()

# Probar directamente
print("=" * 80)
print("PRUEBA DIRECTA CON EJERCICIO 1:")
print("=" * 80)

ejercicio = Ejercicio.objects.get(id=1)
print(f"Respuesta correcta en BD: '{ejercicio.respuesta_correcta}'")
print()

pruebas = ["B", "b", " B "]
for prueba in pruebas:
    resultado = ejercicio.validar_respuesta(prueba)
    print(f"  validar_respuesta('{prueba}') = {resultado}")

print()
print("=" * 80)
