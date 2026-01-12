"""
Script para debuggear problemas de validación con ejercicios reales.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matelog_backend.settings')
django.setup()

from lessons.models import Ejercicio


def probar_ejercicios():
    """Prueba todos los ejercicios con diferentes respuestas."""
    print("=" * 80)
    print("PRUEBA DE VALIDACION CON EJERCICIOS REALES")
    print("=" * 80)
    print()

    ejercicios = Ejercicio.objects.all()
    print(f"Total de ejercicios en BD: {ejercicios.count()}")
    print()

    for ej in ejercicios:
        print("-" * 80)
        print(f"Ejercicio ID: {ej.id}")
        print(f"Tema: {ej.tema.titulo}")
        print(f"Tipo: {ej.tipo}")
        print(f"Enunciado: {ej.enunciado[:100]}...")
        print(f"Respuesta correcta almacenada: [{ej.respuesta_correcta}]")

        if ej.tipo == 'MULTIPLE':
            # Probar con la respuesta correcta en diferentes formatos
            opciones = ej.opciones.all()
            print(f"Opciones disponibles: {[f'{o.letra}: {o.texto[:30]}' for o in opciones]}")

            pruebas = [
                ej.respuesta_correcta,  # Tal cual está
                ej.respuesta_correcta.lower(),  # Minúscula
                ej.respuesta_correcta.upper(),  # Mayúscula
                f" {ej.respuesta_correcta} ",  # Con espacios
            ]

            print("\nPruebas de validacion:")
            for prueba in pruebas:
                resultado = ej.validar_respuesta(prueba)
                simbolo = "OK" if resultado else "FAIL"
                print(f"  Respuesta: [{prueba}] -> {resultado} {simbolo}")

        else:  # ABIERTO
            # Probar con la respuesta correcta en diferentes formatos
            pruebas = [
                ej.respuesta_correcta,  # Tal cual está
                ej.respuesta_correcta.lower(),  # Minúscula
                ej.respuesta_correcta.upper(),  # Mayúscula
                ej.respuesta_correcta.capitalize(),  # Primera letra mayúscula
                f" {ej.respuesta_correcta} ",  # Con espacios
                ej.respuesta_correcta + ".",  # Con punto
            ]

            print("\nPruebas de validacion:")
            for prueba in pruebas:
                resultado = ej.validar_respuesta(prueba)
                simbolo = "OK" if resultado else "FAIL"
                print(f"  Respuesta: [{prueba}] -> {resultado} {simbolo}")

        print()


def verificar_normalizacion():
    """Verifica que la normalización funcione correctamente."""
    print("=" * 80)
    print("VERIFICACION DE NORMALIZACION")
    print("=" * 80)
    print()

    # Importar la función de normalización del modelo
    import unicodedata
    import string

    def normalizar(texto):
        texto = ' '.join(texto.split())
        texto = texto.lower()
        texto = ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
        texto = texto.translate(str.maketrans('', '', string.punctuation))
        return texto.strip()

    casos_prueba = [
        ("La Derivada", "la derivada"),
        ("la derivada.", "la derivada"),
        ("  la   derivada  ", "la derivada"),
        ("derivación", "derivacion"),
        ("DERIVADA!", "derivada"),
    ]

    print("Casos de prueba de normalización:")
    for original, esperado in casos_prueba:
        normalizado = normalizar(original)
        coincide = normalizado == esperado
        simbolo = "OK" if coincide else "ERROR"
        print(f"  '{original}' -> '{normalizado}' (esperado: '{esperado}') {simbolo}")

    print()


def casos_especificos():
    """Permite probar casos específicos que el usuario reporte."""
    print("=" * 80)
    print("PRUEBA DE CASOS ESPECIFICOS")
    print("=" * 80)
    print()

    print("Ingresa el ID del ejercicio y la respuesta que dio el usuario")
    print("Esto ayudará a identificar exactamente qué está fallando")
    print()
    print("Ejercicios disponibles:")

    for ej in Ejercicio.objects.all():
        print(f"  ID {ej.id}: {ej.enunciado[:60]}... (Tipo: {ej.tipo})")

    print()
    print("Para probar un caso específico, edita este script y agrega:")
    print("  ejercicio_id = X")
    print("  respuesta_usuario = 'tu respuesta'")
    print()

    # AQUÍ EL USUARIO PUEDE AGREGAR CASOS ESPECÍFICOS
    # Ejemplo:
    # ejercicio_id = 1
    # respuesta_usuario = "verdadero"
    # ejercicio = Ejercicio.objects.get(id=ejercicio_id)
    # resultado = ejercicio.validar_respuesta(respuesta_usuario)
    # print(f"Ejercicio {ejercicio_id}: '{respuesta_usuario}' -> {resultado}")


if __name__ == "__main__":
    print("\n")
    verificar_normalizacion()
    print("\n")
    probar_ejercicios()
    print("\n")
    casos_especificos()
