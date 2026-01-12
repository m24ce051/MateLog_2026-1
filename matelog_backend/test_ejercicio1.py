"""
Script para investigar específicamente el ejercicio 1.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matelog_backend.settings')
django.setup()

from lessons.models import Ejercicio, OpcionMultiple


print("=" * 80)
print("INVESTIGACION DETALLADA - EJERCICIO 1")
print("=" * 80)
print()

# Obtener ejercicio 1
ejercicio = Ejercicio.objects.get(id=1)

print(f"ID: {ejercicio.id}")
print(f"Tema: {ejercicio.tema.titulo}")
print(f"Tipo: {ejercicio.tipo}")
print(f"Orden: {ejercicio.orden}")
print()

print(f"Enunciado completo:")
print(f"{ejercicio.enunciado}")
print()

print(f"Respuesta correcta almacenada en BD:")
print(f"  Valor: '{ejercicio.respuesta_correcta}'")
print(f"  Tipo: {type(ejercicio.respuesta_correcta)}")
print(f"  Longitud: {len(ejercicio.respuesta_correcta)}")
print(f"  Repr: {repr(ejercicio.respuesta_correcta)}")
print(f"  Bytes: {ejercicio.respuesta_correcta.encode('utf-8')}")
print()

# Mostrar opciones
print("Opciones múltiples:")
opciones = ejercicio.opciones.all().order_by('letra')
for opcion in opciones:
    print(f"  [{opcion.letra}] {opcion.texto}")
print()

# Probar validación con diferentes variantes de "B"
print("PRUEBAS DE VALIDACION:")
print("-" * 80)

pruebas = [
    "B",
    "b",
    " B ",
    "B ",
    " B",
    "\tB\t",
]

for i, prueba in enumerate(pruebas, 1):
    resultado = ejercicio.validar_respuesta(prueba)
    print(f"Prueba {i}:")
    print(f"  Entrada: '{prueba}'")
    print(f"  Repr: {repr(prueba)}")
    print(f"  Bytes: {prueba.encode('utf-8')}")
    print(f"  Resultado: {resultado}")

    # Mostrar el proceso de validación paso a paso
    prueba_stripped = prueba.strip()
    prueba_upper = prueba_stripped.upper()
    correcta_upper = ejercicio.respuesta_correcta.upper()

    print(f"  Proceso:")
    print(f"    1. strip(): '{prueba}' -> '{prueba_stripped}'")
    print(f"    2. upper(): '{prueba_stripped}' -> '{prueba_upper}'")
    print(f"    3. Correcta upper(): '{correcta_upper}'")
    print(f"    4. Comparacion: '{prueba_upper}' == '{correcta_upper}' = {prueba_upper == correcta_upper}")
    print()

# Verificar si hay caracteres ocultos
print("VERIFICACION DE CARACTERES OCULTOS:")
print("-" * 80)
for i, char in enumerate(ejercicio.respuesta_correcta):
    print(f"  Posicion {i}: '{char}' (ord={ord(char)}, hex={hex(ord(char))})")
print()

# Simular exactamente lo que hace el método validar_respuesta
print("SIMULACION EXACTA DEL METODO validar_respuesta:")
print("-" * 80)
respuesta_usuario = "B"
print(f"Tipo de ejercicio: {ejercicio.tipo}")
print(f"Es MULTIPLE: {ejercicio.tipo == 'MULTIPLE'}")
print()

if ejercicio.tipo == 'MULTIPLE':
    izq = respuesta_usuario.strip().upper()
    der = ejercicio.respuesta_correcta.upper()
    resultado = izq == der

    print(f"Lado izquierdo: '{izq}' (len={len(izq)}, repr={repr(izq)})")
    print(f"Lado derecho: '{der}' (len={len(der)}, repr={repr(der)})")
    print(f"Comparacion: {resultado}")
    print()

    # Comparación byte por byte
    print("Comparacion byte por byte:")
    for i in range(max(len(izq), len(der))):
        c1 = izq[i] if i < len(izq) else '(fin)'
        c2 = der[i] if i < len(der) else '(fin)'
        match = c1 == c2 if isinstance(c1, str) and isinstance(c2, str) else False
        print(f"  Pos {i}: '{c1}' vs '{c2}' = {match}")

print()
print("=" * 80)
print("FIN DE INVESTIGACION")
print("=" * 80)
