"""
Script para verificar que los nuevos modelos de tracking funcionan correctamente.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matelog_backend.settings')
django.setup()

from tracking.models import SesionEstudio, TiempoPantalla, ClicBoton
from lessons.models import Tema, ContenidoTema, Ejercicio
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 80)
print("VERIFICACIÓN DE NUEVOS MODELOS DE TRACKING")
print("=" * 80)
print()

# ==================== 1. Verificar SesionEstudio ====================
print("1. Verificando modelo SesionEstudio (modificado)...")
print("-" * 80)

# Verificar campos nuevos
sesion_fields = [f.name for f in SesionEstudio._meta.get_fields()]
campos_requeridos = ['duracion_segundos', 'tipo_cierre', 'ultima_actividad']

for campo in campos_requeridos:
    if campo in sesion_fields:
        print(f"  [OK] Campo '{campo}' existe")
    else:
        print(f"  [ERROR] Campo '{campo}' NO existe")

# Verificar choices de tipo_cierre
tipo_cierre_field = SesionEstudio._meta.get_field('tipo_cierre')
print(f"\n  Opciones de tipo_cierre:")
for choice in SesionEstudio.TIPO_CIERRE_CHOICES:
    print(f"    - {choice[0]}: {choice[1]}")

print()

# ==================== 2. Verificar TiempoPantalla ====================
print("2. Verificando modelo TiempoPantalla (nuevo)...")
print("-" * 80)

tiempo_fields = [f.name for f in TiempoPantalla._meta.get_fields()]
campos_requeridos_tiempo = ['usuario', 'tema', 'contenido', 'ejercicio', 'tipo_contenido',
                             'numero', 'tiempo_segundos', 'cambio_pestana', 'timestamp']

for campo in campos_requeridos_tiempo:
    if campo in tiempo_fields:
        print(f"  [OK] Campo '{campo}' existe")
    else:
        print(f"  [ERROR] Campo '{campo}' NO existe")

# Verificar choices de tipo_contenido
print(f"\n  Opciones de tipo_contenido:")
for choice in TiempoPantalla.TIPO_CONTENIDO_CHOICES:
    print(f"    - {choice[0]}: {choice[1]}")

# Verificar propiedad nombre_completo
print(f"\n  Verificando propiedad 'nombre_completo':")
print(f"    - Método existe: {hasattr(TiempoPantalla, 'nombre_completo')}")

print()

# ==================== 3. Verificar ClicBoton ====================
print("3. Verificando modelo ClicBoton (nuevo)...")
print("-" * 80)

clic_fields = [f.name for f in ClicBoton._meta.get_fields()]
campos_requeridos_clic = ['usuario', 'tema', 'tipo_boton', 'timestamp']

for campo in campos_requeridos_clic:
    if campo in clic_fields:
        print(f"  [OK] Campo '{campo}' existe")
    else:
        print(f"  [ERROR] Campo '{campo}' NO existe")

# Verificar choices de tipo_boton
print(f"\n  Opciones de tipo_boton:")
for choice in ClicBoton.TIPO_BOTON_CHOICES:
    print(f"    - {choice[0]}: {choice[1]}")

print()

# ==================== 4. Prueba de Creación (Opcional) ====================
print("4. Prueba de creación de registros...")
print("-" * 80)

try:
    # Buscar un usuario de prueba
    usuario = User.objects.first()

    if not usuario:
        print("  ⚠ No hay usuarios en la BD. Saltando prueba de creación.")
    else:
        print(f"  Usuario de prueba: {usuario.username}")

        # Buscar un tema de prueba
        tema = Tema.objects.first()

        if not tema:
            print("  ⚠ No hay temas en la BD. Saltando prueba de creación.")
        else:
            print(f"  Tema de prueba: {tema.titulo}")

            # Crear sesión de prueba
            print("\n  Creando SesionEstudio de prueba...")
            sesion = SesionEstudio.objects.create(
                usuario=usuario,
                duracion_segundos=3600,
                tipo_cierre='LOGOUT'
            )
            print(f"    [OK] Sesion creada: {sesion}")

            # Crear TiempoPantalla de prueba
            print("\n  Creando TiempoPantalla de prueba...")
            tiempo = TiempoPantalla.objects.create(
                usuario=usuario,
                tema=tema,
                tipo_contenido='TEORIA',
                numero=1,
                tiempo_segundos=120,
                cambio_pestana=False
            )
            print(f"    [OK] TiempoPantalla creado: {tiempo}")
            print(f"    [OK] Nombre completo: {tiempo.nombre_completo}")

            # Crear ClicBoton de prueba
            print("\n  Creando ClicBoton de prueba...")
            clic = ClicBoton.objects.create(
                usuario=usuario,
                tema=tema,
                tipo_boton='VER_AYUDA'
            )
            print(f"    [OK] ClicBoton creado: {clic}")

            # Limpiar registros de prueba
            print("\n  Limpiando registros de prueba...")
            sesion.delete()
            tiempo.delete()
            clic.delete()
            print("    [OK] Registros de prueba eliminados")

except Exception as e:
    print(f"  [ERROR] Error en prueba de creacion: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
print("VERIFICACIÓN COMPLETADA")
print("=" * 80)
