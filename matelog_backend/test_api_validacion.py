"""
Script para probar el endpoint de validación del API.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matelog_backend.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from lessons.views import ValidarRespuestaView
from lessons.models import Ejercicio
import json

User = get_user_model()

print("=" * 80)
print("PRUEBA DEL ENDPOINT API - /api/ejercicios/validar/")
print("=" * 80)
print()

# Crear usuario de prueba
user, created = User.objects.get_or_create(
    username='test_user',
    defaults={'email': 'test@test.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print("Usuario de prueba creado")
else:
    print("Usuario de prueba existente")

print()

# Crear factory para simular requests
factory = RequestFactory()

# Probar ejercicio 1
ejercicio = Ejercicio.objects.get(id=1)
print(f"Ejercicio ID: {ejercicio.id}")
print(f"Tipo: {ejercicio.tipo}")
print(f"Respuesta correcta en BD: '{ejercicio.respuesta_correcta}'")
print()

# Simular diferentes requests
casos_prueba = [
    {"ejercicio_id": 1, "respuesta": "B"},
    {"ejercicio_id": 1, "respuesta": "b"},
    {"ejercicio_id": 1, "respuesta": " B "},
    {"ejercicio_id": 1, "respuesta": "A"},  # Incorrecta
]

view = ValidarRespuestaView.as_view()

print("PRUEBAS DEL ENDPOINT:")
print("-" * 80)

for i, data in enumerate(casos_prueba, 1):
    print(f"\nPrueba {i}:")
    print(f"  Datos enviados: {data}")

    # Crear request POST
    request = factory.post(
        '/api/ejercicios/validar/',
        data=json.dumps(data),
        content_type='application/json'
    )
    request.user = user

    # Ejecutar vista
    try:
        response = view(request)
        print(f"  Status code: {response.status_code}")

        if hasattr(response, 'data'):
            print(f"  Respuesta: {response.data}")
            if 'es_correcta' in response.data:
                resultado = response.data['es_correcta']
                simbolo = "OK" if resultado else "FAIL"
                print(f"  es_correcta: {resultado} {simbolo}")
        else:
            # DRF Response
            content = json.loads(response.content.decode('utf-8'))
            print(f"  Respuesta: {content}")
            if 'es_correcta' in content:
                resultado = content['es_correcta']
                simbolo = "OK" if resultado else "FAIL"
                print(f"  es_correcta: {resultado} {simbolo}")

    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()

print()
print("=" * 80)
print("FIN DE PRUEBAS")
print("=" * 80)
