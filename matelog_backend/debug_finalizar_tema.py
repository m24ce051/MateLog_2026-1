"""
Debug del flujo completo de finalización de tema.
Este script simula el proceso de finalizar un tema para identificar posibles errores.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matelog_backend.settings')
django.setup()

from lessons.models import Tema, Ejercicio
from tracking.models import ProgresoTema, RespuestaEjercicio
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

print("=" * 80)
print("DEBUG: FLUJO DE FINALIZACION DE TEMA")
print("=" * 80)
print()

# Pedir datos al usuario
username = input("Ingresa el nombre de usuario: ")
tema_id = int(input("Ingresa el ID del tema: "))

try:
    usuario = User.objects.get(username=username)
    tema = Tema.objects.get(id=tema_id, is_active=True)

    print(f"\n✓ Usuario encontrado: {usuario.username}")
    print(f"✓ Tema encontrado: {tema.titulo}")
    print()

    # Obtener progreso del tema
    progreso_tema, created = ProgresoTema.objects.get_or_create(
        usuario=usuario,
        tema=tema,
        defaults={
            'desbloqueado': True,
            'estado': 'INICIADO',
            'fecha_inicio': timezone.now()
        }
    )

    if created:
        print("⚠ Se creó un nuevo ProgresoTema (no existía)")
    else:
        print(f"✓ ProgresoTema existente:")
        print(f"  - Estado: {progreso_tema.estado}")
        print(f"  - Desbloqueado: {progreso_tema.desbloqueado}")
        print(f"  - Intentos: {progreso_tema.intentos_realizados}")
    print()

    # Obtener respuestas del usuario
    respuestas = RespuestaEjercicio.objects.filter(
        usuario=usuario,
        progreso_tema=progreso_tema
    )

    print(f"RESPUESTAS DEL USUARIO:")
    print("-" * 80)
    total_ejercicios = tema.ejercicios.count()
    ejercicios_correctos = respuestas.filter(es_correcta=True).count()
    ejercicios_incorrectos = respuestas.filter(es_correcta=False).count()

    print(f"  Total de ejercicios en el tema: {total_ejercicios}")
    print(f"  Respuestas registradas: {respuestas.count()}")
    print(f"  Correctas: {ejercicios_correctos}")
    print(f"  Incorrectas: {ejercicios_incorrectos}")
    print()

    if total_ejercicios > 0:
        porcentaje_acierto = (ejercicios_correctos / total_ejercicios) * 100
        aprobado = porcentaje_acierto >= 80

        print(f"  Porcentaje de acierto: {porcentaje_acierto:.1f}%")
        print(f"  ¿Aprobado? {'SÍ' if aprobado else 'NO'} (requiere >= 80%)")
        print()

        if aprobado:
            print("BUSCANDO SIGUIENTE TEMA:")
            print("-" * 80)

            # Buscar siguiente tema
            siguiente_tema = Tema.objects.filter(
                leccion=tema.leccion,
                orden=tema.orden + 1,
                is_active=True
            ).first()

            if siguiente_tema:
                print(f"✓ Siguiente tema encontrado:")
                print(f"  - ID: {siguiente_tema.id}")
                print(f"  - Título: {siguiente_tema.titulo}")
                print(f"  - Orden: {siguiente_tema.orden}")
                print()

                # Verificar si ya está desbloqueado
                progreso_siguiente, created = ProgresoTema.objects.get_or_create(
                    usuario=usuario,
                    tema=siguiente_tema,
                    defaults={'desbloqueado': True}
                )

                if created:
                    print("  ✓ Siguiente tema desbloqueado (nuevo)")
                else:
                    print(f"  ℹ Siguiente tema ya existía:")
                    print(f"    - Desbloqueado: {progreso_siguiente.desbloqueado}")
                    print(f"    - Estado: {progreso_siguiente.estado}")

                print()
                print("DATOS QUE SE ENVIARÍAN AL FRONTEND:")
                print("-" * 80)
                print(f"  aprobado: {aprobado}")
                print(f"  porcentaje_acierto: {porcentaje_acierto}")
                print(f"  siguiente_tema_id: {siguiente_tema.id}")
                print(f"  siguiente_tema: {{")
                print(f"    'id': {siguiente_tema.id},")
                print(f"    'titulo': '{siguiente_tema.titulo}',")
                print(f"    'orden': {siguiente_tema.orden}")
                print(f"  }}")

            else:
                print("ℹ No hay siguiente tema (es el último de la lección)")
                print()
                print("DATOS QUE SE ENVIARÍAN AL FRONTEND:")
                print("-" * 80)
                print(f"  aprobado: {aprobado}")
                print(f"  porcentaje_acierto: {porcentaje_acierto}")
                print(f"  siguiente_tema_id: None")
                print(f"  siguiente_tema: None")
        else:
            print("❌ No aprobó (< 80%). No se desbloquea siguiente tema.")
    else:
        print("⚠ El tema no tiene ejercicios")

except User.DoesNotExist:
    print(f"\n❌ ERROR: Usuario '{username}' no encontrado")
except Tema.DoesNotExist:
    print(f"\n❌ ERROR: Tema con ID {tema_id} no encontrado o no está activo")
except Exception as e:
    import traceback
    print(f"\n❌ ERROR INESPERADO:")
    print(traceback.format_exc())

print()
print("=" * 80)
