# 📚 Guía de Gestión de Contenido - MateLog

## 📋 Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Estructura de Archivos](#estructura-de-archivos)
- [Cómo Usar el Archivo de Contenido](#cómo-usar-el-archivo-de-contenido)
- [Cómo Agregar Contenido Nuevo](#cómo-agregar-contenido-nuevo)
- [Cómo Modificar Contenido Existente](#cómo-modificar-contenido-existente)
- [Cómo Eliminar Contenido](#cómo-eliminar-contenido)
- [Estructura de los Modelos](#estructura-de-los-modelos)
- [Ejemplos Prácticos](#ejemplos-prácticos)
- [Solución de Problemas](#solución-de-problemas)

---

## 📖 Descripción General

El archivo `contenido.db` contiene todo el contenido educativo de MateLog, organizado en lecciones, temas, contenidos y ejercicios. Este archivo permite:

- ✅ Cargar contenido inicial en la base de datos
- ✅ Actualizar contenido existente
- ✅ Agregar nuevo material educativo
- ✅ Reemplazar completamente el contenido

---

## 📁 Estructura de Archivos

```
matelog_backend/
├── contenido.db          # Archivo con el contenido educativo actual
├── populate_db.py        # Archivo de población simple (legacy)
├── README_CONTENIDO.md   # Esta guía
└── lessons/
    └── models.py         # Definición de los modelos de datos
```

---

## Cómo Usar el Archivo de Contenido

### Opción 1: Cargar el contenido (Recomendado)

```bash
# 1. Activar el entorno virtual
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Ir al directorio del backend
cd matelog_backend

# 3. Ejecutar el script de contenido
python manage.py shell < contenido.db
```

### Opción 2: Ejecutar desde el shell de Django

```bash
python manage.py shell
```

Luego, dentro del shell:

```python
exec(open('contenido.db').read())
```

---

## ➕ Cómo Agregar Contenido Nuevo

### 1. Agregar una Nueva Lección

Copia y modifica el siguiente bloque al final del archivo, **antes del resumen final**:

```python
# ================================================================================================
# LECCIÓN 3: TÍTULO DE TU NUEVA LECCIÓN
# ================================================================================================
print("📚 Creando Lección 3: Título de tu nueva lección...")

leccion3 = Leccion.objects.create(
    orden=3,  # Incrementa el número secuencialmente
    titulo="Título de tu nueva lección",
    descripcion="""
        <p>Descripción detallada de la lección en HTML.</p>
        <p>Puedes usar múltiples párrafos y etiquetas HTML.</p>
    """,
    is_active=True  # True para que sea visible, False para ocultarla
)
```

### 2. Agregar un Nuevo Tema a una Lección

```python
tema3_1 = Tema.objects.create(
    leccion=leccion3,  # Referencia a la lección creada arriba
    orden=1,  # Orden dentro de la lección
    titulo="Título del Tema",
    descripcion="""
        <p>Descripción del tema en HTML.</p>
    """,
    is_active=True
)
```

### 3. Agregar Contenido Teórico o Ejemplos

```python
# TEORÍA
ContenidoTema.objects.create(
    tema=tema3_1,
    orden=1,
    tipo='TEORIA',  # Opciones: TEORIA, EJEMPLO, EJEMPLO_EXTRA, RESUMEN
    contenido_texto="""
        <h3>Título del Contenido</h3>
        <p>Texto del contenido con <strong>formato HTML</strong>.</p>
        <ul>
            <li>Viñeta 1</li>
            <li>Viñeta 2</li>
        </ul>
    """
)

# EJEMPLO
ContenidoTema.objects.create(
    tema=tema3_1,
    orden=2,
    tipo='EJEMPLO',
    contenido_texto="""
        <h3>Ejemplo Práctico</h3>
        <p>Desarrollo del ejemplo paso a paso.</p>
    """
)
```

### 4. Agregar Ejercicios

#### Ejercicio de Respuesta Abierta

```python
ejercicio1 = Ejercicio.objects.create(
    tema=tema3_1,
    orden=1,
    tipo='ABIERTO',
    dificultad='FACIL',  # FACIL, INTERMEDIO, DIFICIL
    mostrar_dificultad=False,  # True para mostrar la dificultad al estudiante
    instruccion='<p>Instrucciones para el estudiante</p>',
    enunciado='<p>Pregunta del ejercicio</p>',
    respuesta_correcta='respuesta esperada',  # Texto exacto (se normalizan espacios y tildes)
    texto_ayuda='<p>Pista opcional para ayudar al estudiante</p>',
    retroalimentacion_correcta='<p>Mensaje cuando acierta</p>',
    retroalimentacion_incorrecta='<p>Mensaje cuando falla</p>'
)
```

#### Ejercicio de Opción Múltiple

```python
# 1. Crear el ejercicio
ejercicio2 = Ejercicio.objects.create(
    tema=tema3_1,
    orden=2,
    tipo='MULTIPLE',
    dificultad='INTERMEDIO',
    mostrar_dificultad=True,
    instruccion='<p>Selecciona la opción correcta:</p>',
    enunciado='<p>¿Cuál es la respuesta correcta?</p>',
    respuesta_correcta='A',  # Letra de la opción correcta: A, B, C o D
    texto_ayuda='<p>Pista para resolver el ejercicio</p>',
    retroalimentacion_correcta='<p>¡Correcto! Explicación adicional.</p>',
    retroalimentacion_incorrecta='<p>Incorrecto. Revisa el concepto.</p>'
)

# 2. Crear las opciones
OpcionMultiple.objects.create(ejercicio=ejercicio2, letra='A', texto='Opción A (correcta)')
OpcionMultiple.objects.create(ejercicio=ejercicio2, letra='B', texto='Opción B')
OpcionMultiple.objects.create(ejercicio=ejercicio2, letra='C', texto='Opción C')
OpcionMultiple.objects.create(ejercicio=ejercicio2, letra='D', texto='Opción D')
```

---

## ✏️ Cómo Modificar Contenido Existente

### Método 1: Editar directamente el archivo contenido.db

1. Abre `contenido.db` en un editor de texto
2. Busca el contenido que deseas modificar (usa Ctrl+F)
3. Modifica el texto HTML en `contenido_texto`, `enunciado`, etc.
4. Guarda el archivo
5. Ejecuta el script nuevamente: `python manage.py shell < contenido.db`

**⚠️ IMPORTANTE:** Esto eliminará TODO el contenido actual y cargará el nuevo.

### Método 2: Modificar desde el Panel de Administración

1. Accede a `http://localhost:8000/admin/`
2. Inicia sesión con tu cuenta de superusuario
3. Navega a Lecciones → Temas → Contenidos o Ejercicios
4. Edita directamente desde la interfaz web

**✅ Ventaja:** No requiere recargar la base de datos completa.

---

## 🗑️ Cómo Eliminar Contenido

### Opción 1: Desactivar (Recomendado)

En lugar de eliminar, cambia `is_active=False`:

```python
leccion1 = Leccion.objects.create(
    orden=1,
    titulo="Lección Desactivada",
    descripcion="...",
    is_active=False  # ← Oculta la lección sin eliminarla
)
```

### Opción 2: Comentar en el archivo

Agrega `#` al inicio de cada línea para comentar el bloque:

```python
# leccion_eliminada = Leccion.objects.create(
#     orden=99,
#     titulo="Esta lección no se creará",
#     ...
# )
```

### Opción 3: Eliminar completamente

1. Elimina el bloque de código del archivo
2. **IMPORTANTE:** Ajusta los números de `orden` para mantener la secuencia
3. Ejecuta el script de nuevo

---

## 🏗️ Estructura de los Modelos

### Jerarquía de Datos

```
Leccion (Nivel 1)
└── Tema (Nivel 2)
    ├── ContenidoTema (Teoría, Ejemplos, Resumen)
    └── Ejercicio (Nivel 3)
        └── OpcionMultiple (solo para ejercicios MULTIPLE)
```

### Campos Importantes

#### Leccion
- `orden` (int): Orden de aparición (1, 2, 3...)
- `titulo` (str): Título de la lección
- `descripcion` (HTML): Descripción detallada
- `is_active` (bool): Si es visible o no

#### Tema
- `leccion` (FK): Lección a la que pertenece
- `orden` (int): Orden dentro de la lección
- `titulo` (str): Título del tema
- `descripcion` (HTML): Descripción del tema
- `is_active` (bool): Si es visible o no

#### ContenidoTema
- `tema` (FK): Tema al que pertenece
- `orden` (int): Orden dentro del tema
- `tipo` (choice): TEORIA, EJEMPLO, EJEMPLO_EXTRA, RESUMEN
- `contenido_texto` (HTML): Contenido completo en HTML

#### Ejercicio
- `tema` (FK): Tema al que pertenece
- `orden` (int): Número de ejercicio
- `tipo` (choice): ABIERTO o MULTIPLE
- `dificultad` (choice): FACIL, INTERMEDIO, DIFICIL
- `mostrar_dificultad` (bool): Si se muestra al estudiante
- `instruccion` (HTML): Instrucciones para el estudiante
- `enunciado` (HTML): Pregunta del ejercicio
- `respuesta_correcta` (str): Respuesta esperada
- `texto_ayuda` (HTML): Pista opcional
- `retroalimentacion_correcta` (HTML): Mensaje de éxito
- `retroalimentacion_incorrecta` (HTML): Mensaje de error

#### OpcionMultiple
- `ejercicio` (FK): Ejercicio al que pertenece
- `letra` (choice): A, B, C, D
- `texto` (str): Texto de la opción

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Agregar una Lección Completa

```python
# Nueva lección
leccion_logica_avanzada = Leccion.objects.create(
    orden=3,
    titulo="Lógica Avanzada",
    descripcion="<p>Estudiaremos implicaciones, equivalencias y cuantificadores.</p>",
    is_active=True
)

# Tema de la lección
tema_implicacion = Tema.objects.create(
    leccion=leccion_logica_avanzada,
    orden=1,
    titulo="Implicación Lógica",
    descripcion="<p>La implicación es un conectivo fundamental.</p>",
    is_active=True
)

# Contenido teórico
ContenidoTema.objects.create(
    tema=tema_implicacion,
    orden=1,
    tipo='TEORIA',
    contenido_texto="""
        <h3>Implicación (p → q)</h3>
        <p>Si p entonces q</p>
        <p>Solo es falsa cuando p es verdadero y q es falso.</p>
    """
)

# Ejercicio
ej = Ejercicio.objects.create(
    tema=tema_implicacion,
    orden=1,
    tipo='MULTIPLE',
    dificultad='INTERMEDIO',
    mostrar_dificultad=True,
    instruccion='<p>Selecciona el valor correcto:</p>',
    enunciado='<p>Si p es V y q es F, ¿cuál es el valor de p → q?</p>',
    respuesta_correcta='B',
    texto_ayuda='<p>Recuerda la tabla de verdad de la implicación.</p>',
    retroalimentacion_correcta='<p>¡Correcto! La implicación es falsa.</p>',
    retroalimentacion_incorrecta='<p>Revisa la tabla de verdad.</p>'
)

OpcionMultiple.objects.create(ejercicio=ej, letra='A', texto='Verdadero')
OpcionMultiple.objects.create(ejercicio=ej, letra='B', texto='Falso')
OpcionMultiple.objects.create(ejercicio=ej, letra='C', texto='Indeterminado')

print("✓ Lección de Lógica Avanzada creada")
```

### Ejemplo 2: Cambiar la Descripción de una Lección

**Antes:**
```python
leccion1 = Leccion.objects.create(
    orden=1,
    titulo="Introducción a la Lógica",
    descripcion="<p>Descripción antigua</p>",
    is_active=True
)
```

**Después:**
```python
leccion1 = Leccion.objects.create(
    orden=1,
    titulo="Introducción a la Lógica",
    descripcion="""
        <p>Descripción nueva y mejorada con más detalles.</p>
        <p>Ahora incluye ejemplos y objetivos de aprendizaje.</p>
    """,
    is_active=True
)
```

---

## 🔧 Solución de Problemas

### Problema: "django.db.utils.IntegrityError: UNIQUE constraint failed"

**Causa:** Intentas crear dos elementos con el mismo número de `orden`.

**Solución:** Verifica que los números de `orden` sean únicos dentro de cada nivel:
- Lecciones: orden debe ser único globalmente
- Temas: orden debe ser único dentro de cada lección
- Contenidos: orden debe ser único dentro de cada tema
- Ejercicios: orden debe ser único dentro de cada tema

### Problema: "OpcionMultiple matching query does not exist"

**Causa:** En un ejercicio MULTIPLE, la `respuesta_correcta` no coincide con ninguna opción.

**Solución:** Asegúrate de que `respuesta_correcta='A'` coincida con una OpcionMultiple con `letra='A'`.

### Problema: El contenido no aparece en el frontend

**Posibles causas:**
1. `is_active=False` → Cambia a `True`
2. Error en la carga → Revisa la consola al ejecutar el script
3. Cache del navegador → Recarga con Ctrl+F5

### Problema: "No module named 'lessons'"

**Causa:** No estás en el directorio correcto o el entorno virtual no está activado.

**Solución:**
```bash
cd matelog_backend
.\venv\Scripts\activate
python manage.py shell < contenido.db
```

---

## 📝 Notas Finales

1. **Backup:** Antes de ejecutar el script, considera hacer backup de la base de datos:
   ```bash
   cp db.sqlite3 db.sqlite3.backup
   ```

2. **HTML Permitido:** Puedes usar cualquier etiqueta HTML válida en los campos de texto:
   - `<h3>`, `<h4>`: Títulos
   - `<p>`: Párrafos
   - `<strong>`, `<b>`: Negritas
   - `<em>`, `<i>`: Cursivas
   - `<ul>`, `<ol>`, `<li>`: Listas
   - `<table>`, `<tr>`, `<td>`: Tablas
   - Estilos inline: `style="color: red;"`

3. **Orden Recomendado de Dificultad:**
   - Ejercicios 1-5: FACIL
   - Ejercicios 6-10: INTERMEDIO
   - Ejercicios 11-15: DIFICIL

4. **Testing:** Después de cargar contenido nuevo, prueba en el frontend:
   - http://localhost:5173/lecciones
   - Verifica que todo se visualice correctamente
   - Prueba los ejercicios para validar respuestas

---

## 📞 Soporte

Si encuentras problemas o necesitas ayuda:
1. Revisa esta guía completa
2. Consulta la documentación de Django: https://docs.djangoproject.com/
3. Verifica los logs en la consola al ejecutar el script

---

**¡Éxito con tu contenido educativo!** 🎓
