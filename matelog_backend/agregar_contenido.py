"""
================================================================================================
SCRIPT PARA AGREGAR CONTENIDO SIN ELIMINAR EL EXISTENTE
================================================================================================

Este script permite AGREGAR contenido nuevo a MateLog SIN eliminar lo que ya existe.
Ejecutar con: python manage.py shell < agregar_contenido.py

DIFERENCIAS con contenido.db:
- contenido.db: ELIMINA todo y carga de cero (reset completo)
- agregar_contenido.py: AÑADE contenido sin tocar lo existente (expansión)

USO TÍPICO:
1. Ya tienes contenido cargado en MateLog
2. Quieres agregar una nueva lección o tema
3. Ejecutas este script para expandir sin perder nada

INSTRUCCIONES:
1. Copia las plantillas de abajo
2. Modifica con tu contenido nuevo
3. Asegúrate de usar números de 'orden' que NO existan
4. Ejecuta: python manage.py shell < agregar_contenido.py

================================================================================================
"""

from lessons.models import Leccion, Tema, ContenidoTema, Ejercicio, OpcionMultiple

print("🚀 Agregando contenido nuevo a MateLog...")
print("=" * 80)
print("⚠️  MODO: AGREGAR (no elimina contenido existente)")
print("=" * 80)
print()

# ================================================================================================
# VERIFICAR CONTENIDO EXISTENTE
# ================================================================================================
print("📊 Estado actual de la base de datos:")
print(f"  - Lecciones: {Leccion.objects.count()}")
print(f"  - Temas: {Tema.objects.count()}")
print(f"  - Contenidos: {ContenidoTema.objects.count()}")
print(f"  - Ejercicios: {Ejercicio.objects.count()}")
print()

# Listar lecciones existentes
print("📚 Lecciones existentes:")
for leccion in Leccion.objects.all().order_by('orden'):
    temas_count = leccion.temas.count()
    print(f"  {leccion.orden}. {leccion.titulo} ({temas_count} temas)")
print()

# ================================================================================================
# EJEMPLO: AGREGAR UNA NUEVA LECCIÓN
# ================================================================================================
# DESCOMENTA Y MODIFICA ESTE BLOQUE PARA AGREGAR TU CONTENIDO

"""
print("➕ Agregando nueva lección...")

# Verificar que el orden no exista
orden_nueva_leccion = 99  # CAMBIA ESTO por un número que no exista
if Leccion.objects.filter(orden=orden_nueva_leccion).exists():
    print(f"  ⚠️  Ya existe una lección con orden {orden_nueva_leccion}")
    print("  💡 Cambia el número de orden o elimina la lección existente desde el admin")
else:
    leccion_nueva = Leccion.objects.create(
        orden=orden_nueva_leccion,
        titulo="Título de tu Nueva Lección",
        descripcion='''
            <p>Descripción detallada de la nueva lección.</p>
            <p>Puedes usar HTML para dar formato.</p>
        ''',
        is_active=True
    )
    print(f"  ✓ Lección '{leccion_nueva.titulo}' creada")

    # Agregar un tema a la nueva lección
    tema_nuevo = Tema.objects.create(
        leccion=leccion_nueva,
        orden=1,
        titulo="Primer Tema de la Nueva Lección",
        descripcion='<p>Descripción del tema.</p>',
        is_active=True
    )
    print(f"    ✓ Tema '{tema_nuevo.titulo}' creado")

    # Agregar contenido al tema
    ContenidoTema.objects.create(
        tema=tema_nuevo,
        orden=1,
        tipo='TEORIA',
        contenido_texto='''
            <h3>Conceptos Fundamentales</h3>
            <p>Aquí va el contenido teórico...</p>
        '''
    )
    print(f"      ✓ Contenido teórico agregado")

    # Agregar un ejercicio
    ejercicio = Ejercicio.objects.create(
        tema=tema_nuevo,
        orden=1,
        tipo='MULTIPLE',
        dificultad='FACIL',
        mostrar_dificultad=False,
        instruccion='<p>Selecciona la opción correcta:</p>',
        enunciado='<p>Pregunta de ejemplo</p>',
        respuesta_correcta='A',
        texto_ayuda='<p>Pista para el estudiante</p>',
        retroalimentacion_correcta='<p>¡Correcto! ✓</p>',
        retroalimentacion_incorrecta='<p>Incorrecto. Intenta de nuevo.</p>'
    )

    OpcionMultiple.objects.create(ejercicio=ejercicio, letra='A', texto='Respuesta correcta')
    OpcionMultiple.objects.create(ejercicio=ejercicio, letra='B', texto='Respuesta incorrecta 1')
    OpcionMultiple.objects.create(ejercicio=ejercicio, letra='C', texto='Respuesta incorrecta 2')
    OpcionMultiple.objects.create(ejercicio=ejercicio, letra='D', texto='Respuesta incorrecta 3')

    print(f"      ✓ Ejercicio agregado con opciones")

print()
"""

# ================================================================================================
# EJEMPLO: AGREGAR UN TEMA A UNA LECCIÓN EXISTENTE
# ================================================================================================
# DESCOMENTA Y MODIFICA ESTE BLOQUE PARA AGREGAR UN TEMA A UNA LECCIÓN EXISTENTE

"""
print("➕ Agregando tema a lección existente...")

# Obtener la lección existente (por ejemplo, la lección 1)
try:
    leccion_existente = Leccion.objects.get(orden=1)
    print(f"  📖 Lección encontrada: {leccion_existente.titulo}")

    # Verificar cuántos temas tiene
    ultimo_orden = leccion_existente.temas.count()
    nuevo_orden = ultimo_orden + 1

    # Crear el nuevo tema
    tema_adicional = Tema.objects.create(
        leccion=leccion_existente,
        orden=nuevo_orden,
        titulo="Tema Adicional",
        descripcion='<p>Este es un tema nuevo agregado a una lección existente.</p>',
        is_active=True
    )
    print(f"  ✓ Tema '{tema_adicional.titulo}' agregado como tema #{nuevo_orden}")

    # Agregar contenido al tema
    ContenidoTema.objects.create(
        tema=tema_adicional,
        orden=1,
        tipo='TEORIA',
        contenido_texto='<h3>Nuevo Contenido</h3><p>Contenido del tema adicional...</p>'
    )

    # Agregar ejercicios (ejemplo rápido)
    for i in range(1, 6):  # 5 ejercicios de ejemplo
        Ejercicio.objects.create(
            tema=tema_adicional,
            orden=i,
            tipo='ABIERTO',
            dificultad='FACIL',
            mostrar_dificultad=False,
            instruccion='<p>Responde la pregunta:</p>',
            enunciado=f'<p>Pregunta {i} del tema adicional</p>',
            respuesta_correcta='respuesta',
            texto_ayuda='<p>Ayuda para resolver</p>'
        )

    print(f"    ✓ {tema_adicional.ejercicios.count()} ejercicios agregados")

except Leccion.DoesNotExist:
    print("  ⚠️  No se encontró la lección con orden 1")
    print("  💡 Verifica que la lección existe o cambia el número de orden")

print()
"""

# ================================================================================================
# PLANTILLA: AGREGAR EJERCICIOS A UN TEMA EXISTENTE
# ================================================================================================
# DESCOMENTA Y MODIFICA ESTE BLOQUE PARA AGREGAR EJERCICIOS A UN TEMA EXISTENTE

"""
print("➕ Agregando ejercicios a tema existente...")

try:
    # Obtener el tema existente (por ejemplo, Lección 1, Tema 1)
    tema_existente = Tema.objects.get(leccion__orden=1, orden=1)
    print(f"  📖 Tema encontrado: {tema_existente.titulo}")

    # Verificar cuántos ejercicios tiene
    ultimo_ejercicio = tema_existente.ejercicios.count()
    print(f"  📝 El tema tiene actualmente {ultimo_ejercicio} ejercicios")

    # Agregar nuevos ejercicios empezando desde el siguiente número
    for i in range(1, 4):  # Agregar 3 ejercicios nuevos
        nuevo_orden = ultimo_ejercicio + i

        ejercicio_nuevo = Ejercicio.objects.create(
            tema=tema_existente,
            orden=nuevo_orden,
            tipo='MULTIPLE',
            dificultad='INTERMEDIO',
            mostrar_dificultad=True,
            instruccion='<p>Selecciona la opción correcta:</p>',
            enunciado=f'<p>Nuevo ejercicio adicional #{nuevo_orden}</p>',
            respuesta_correcta='A',
            texto_ayuda='<p>Pista útil</p>',
            retroalimentacion_correcta='<p>¡Excelente!</p>',
            retroalimentacion_incorrecta='<p>Revisa el concepto.</p>'
        )

        # Crear opciones
        OpcionMultiple.objects.create(ejercicio=ejercicio_nuevo, letra='A', texto='Correcta')
        OpcionMultiple.objects.create(ejercicio=ejercicio_nuevo, letra='B', texto='Incorrecta 1')
        OpcionMultiple.objects.create(ejercicio=ejercicio_nuevo, letra='C', texto='Incorrecta 2')
        OpcionMultiple.objects.create(ejercicio=ejercicio_nuevo, letra='D', texto='Incorrecta 3')

    print(f"  ✓ {tema_existente.ejercicios.count()} ejercicios en total ahora")

except Tema.DoesNotExist:
    print("  ⚠️  No se encontró el tema especificado")
    print("  💡 Verifica los números de orden de lección y tema")

print()
"""

# ================================================================================================
# RESUMEN FINAL
# ================================================================================================
print("=" * 80)
print("📊 Estado final de la base de datos:")
print(f"  - Lecciones: {Leccion.objects.count()}")
print(f"  - Temas: {Tema.objects.count()}")
print(f"  - Contenidos: {ContenidoTema.objects.count()}")
print(f"  - Ejercicios: {Ejercicio.objects.count()}")
print(f"  - Opciones múltiples: {OpcionMultiple.objects.count()}")
print()

print("📚 Lecciones actuales:")
for leccion in Leccion.objects.all().order_by('orden'):
    print(f"  {leccion.orden}. {leccion.titulo}")
    for tema in leccion.temas.all().order_by('orden'):
        ejercicios = tema.ejercicios.count()
        print(f"      → Tema {tema.orden}: {tema.titulo} ({ejercicios} ejercicios)")
print()

print("=" * 80)
print("✅ Proceso completado")
print()
print("💡 PRÓXIMOS PASOS:")
print("   1. Si no agregaste contenido, descomenta los bloques de ejemplo")
print("   2. Modifica los bloques con tu contenido")
print("   3. Vuelve a ejecutar: python manage.py shell < agregar_contenido.py")
print("   4. Verifica en el admin: http://localhost:8000/admin/")
print("=" * 80)
