"""
Debug en vivo del problema.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matelog_backend.settings')
django.setup()

from lessons.models import Ejercicio
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 80)
print("DEBUG EN VIVO - EJERCICIO 1")
print("=" * 80)
print()

# Cargar ejercicio 1
ejercicio = Ejercicio.objects.get(id=1)

print("DATOS DEL EJERCICIO:")
print("-" * 80)
print(f"ID: {ejercicio.id}")
print(f"Tipo: {ejercicio.tipo}")
print(f"Respuesta correcta: '{ejercicio.respuesta_correcta}'")
print(f"Tipo de dato: {type(ejercicio.respuesta_correcta)}")
print(f"Longitud: {len(ejercicio.respuesta_correcta)}")
print(f"Bytes: {ejercicio.respuesta_correcta.encode('utf-8')}")
print(f"Repr: {repr(ejercicio.respuesta_correcta)}")
print()

# Caracteres individuales
print("CARACTERES INDIVIDUALES:")
print("-" * 80)
for i, char in enumerate(ejercicio.respuesta_correcta):
    print(f"  Pos {i}: '{char}' (ASCII={ord(char)}, hex={hex(ord(char))})")
print()

# Opciones del ejercicio
print("OPCIONES DISPONIBLES:")
print("-" * 80)
opciones = ejercicio.opciones.all().order_by('letra')
for op in opciones:
    print(f"  Letra: '{op.letra}' -> {op.texto[:50]}")
print()

# PROBAR VALIDACIÓN DIRECTA
print("PRUEBA DE VALIDACION DIRECTA:")
print("-" * 80)

pruebas = ["B", "b", " B ", "A", "C"]
for prueba in pruebas:
    resultado = ejercicio.validar_respuesta(prueba)
    print(f"  validar_respuesta('{prueba}') = {resultado}")
print()

# SIMULAR EXACTAMENTE LO QUE HACE LA VISTA
print("SIMULACION DE LA VISTA ValidarRespuestaView:")
print("-" * 80)

respuesta_usuario = "B"

print(f"1. Respuesta del usuario: '{respuesta_usuario}'")
print(f"2. Tipo de ejercicio: {ejercicio.tipo}")
print(f"3. ¿Es MULTIPLE?: {ejercicio.tipo == 'MULTIPLE'}")
print()

# Ejecutar validación
es_correcta = ejercicio.validar_respuesta(respuesta_usuario)
print(f"4. Resultado de validar_respuesta(): {es_correcta}")
print()

# Desglosar el proceso
if ejercicio.tipo == 'MULTIPLE':
    print("DESGLOSE DEL PROCESO DE VALIDACION:")
    print("-" * 80)

    # Paso por paso
    paso1 = respuesta_usuario.strip()
    print(f"  Paso 1 - strip(): '{respuesta_usuario}' -> '{paso1}'")

    paso2 = paso1.upper()
    print(f"  Paso 2 - upper(): '{paso1}' -> '{paso2}'")

    paso3 = ejercicio.respuesta_correcta.upper()
    print(f"  Paso 3 - respuesta_correcta.upper(): '{ejercicio.respuesta_correcta}' -> '{paso3}'")

    resultado_comparacion = paso2 == paso3
    print(f"  Paso 4 - Comparacion: '{paso2}' == '{paso3}' = {resultado_comparacion}")
    print()

    # Comparación byte por byte
    print("  COMPARACION BYTE POR BYTE:")
    max_len = max(len(paso2), len(paso3))
    for i in range(max_len):
        c1 = paso2[i] if i < len(paso2) else '(fin)'
        c2 = paso3[i] if i < len(paso3) else '(fin)'

        if isinstance(c1, str) and isinstance(c2, str):
            match = c1 == c2
            ord1 = ord(c1)
            ord2 = ord(c2)
            print(f"    [{i}] '{c1}' (ord={ord1}) vs '{c2}' (ord={ord2}) = {match}")
        else:
            print(f"    [{i}] {c1} vs {c2}")

print()
print("=" * 80)
print("FIN DEL DEBUG")
print("=" * 80)
