# 🚀 Referencia Rápida - Gestión de Contenido MateLog

## Ejecución del Script

```bash
# Windows
.\venv\Scripts\activate
cd matelog_backend
python manage.py shell < contenido.db

# Linux/Mac
source venv/bin/activate
cd matelog_backend
python manage.py shell < contenido.db
```

---

## 📚 Plantillas de Código

### Nueva Lección

```python
leccionX = Leccion.objects.create(
    orden=X,
    titulo="Título de la Lección",
    descripcion="<p>Descripción HTML</p>",
    is_active=True
)
```

### Nuevo Tema

```python
temaX_Y = Tema.objects.create(
    leccion=leccionX,
    orden=Y,
    titulo="Título del Tema",
    descripcion="<p>Descripción HTML</p>",
    is_active=True
)
```

### Nuevo Contenido (Teoría/Ejemplo)

```python
ContenidoTema.objects.create(
    tema=temaX_Y,
    orden=Z,
    tipo='TEORIA',  # TEORIA, EJEMPLO, EJEMPLO_EXTRA, RESUMEN
    contenido_texto="""
        <h3>Título</h3>
        <p>Contenido en HTML</p>
    """
)
```

### Ejercicio de Respuesta Abierta

```python
Ejercicio.objects.create(
    tema=temaX_Y,
    orden=N,
    tipo='ABIERTO',
    dificultad='FACIL',  # FACIL, INTERMEDIO, DIFICIL
    mostrar_dificultad=False,
    instruccion='<p>Instrucciones</p>',
    enunciado='<p>Pregunta</p>',
    respuesta_correcta='respuesta',
    texto_ayuda='<p>Ayuda opcional</p>',
    retroalimentacion_correcta='<p>¡Correcto!</p>',
    retroalimentacion_incorrecta='<p>Incorrecto</p>'
)
```

### Ejercicio de Opción Múltiple

```python
# 1. Crear ejercicio
ejercicio = Ejercicio.objects.create(
    tema=temaX_Y,
    orden=N,
    tipo='MULTIPLE',
    dificultad='INTERMEDIO',
    mostrar_dificultad=True,
    instruccion='<p>Selecciona la correcta:</p>',
    enunciado='<p>Pregunta</p>',
    respuesta_correcta='A',  # A, B, C o D
    texto_ayuda='<p>Pista</p>',
    retroalimentacion_correcta='<p>¡Bien!</p>',
    retroalimentacion_incorrecta='<p>Mal</p>'
)

# 2. Crear opciones
OpcionMultiple.objects.create(ejercicio=ejercicio, letra='A', texto='Opción A')
OpcionMultiple.objects.create(ejercicio=ejercicio, letra='B', texto='Opción B')
OpcionMultiple.objects.create(ejercicio=ejercicio, letra='C', texto='Opción C')
OpcionMultiple.objects.create(ejercicio=ejercicio, letra='D', texto='Opción D')
```

---

## 🎨 Etiquetas HTML Útiles

### Estructura Básica
```html
<h3>Título de Sección</h3>
<h4>Subtítulo</h4>
<p>Párrafo de texto normal.</p>
<p><strong>Texto en negrita</strong></p>
<p><em>Texto en cursiva</em></p>
```

### Listas
```html
<!-- Lista sin orden -->
<ul>
    <li>Elemento 1</li>
    <li>Elemento 2</li>
    <li>Elemento 3</li>
</ul>

<!-- Lista ordenada -->
<ol>
    <li>Primer paso</li>
    <li>Segundo paso</li>
    <li>Tercer paso</li>
</ol>
```

### Tablas
```html
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background: #f0f0f0;">
        <th style="border: 1px solid #ddd; padding: 10px;">Columna 1</th>
        <th style="border: 1px solid #ddd; padding: 10px;">Columna 2</th>
    </tr>
    <tr>
        <td style="border: 1px solid #ddd; padding: 10px;">Dato 1</td>
        <td style="border: 1px solid #ddd; padding: 10px;">Dato 2</td>
    </tr>
</table>
```

### Símbolos Matemáticos (HTML Entities)
```html
<!-- Lógica -->
∧  (conjunción: Y)       → &and;
∨  (disyunción: O)       → &or;
¬  (negación: NO)        → &not;
→  (implicación)         → &rarr;
↔  (bicondicional)       → &harr;

<!-- Matemáticas -->
≤  (menor o igual)       → &le;
≥  (mayor o igual)       → &ge;
≠  (diferente)           → &ne;
∞  (infinito)            → &infin;
∑  (sumatoria)           → &sum;
∏  (productoria)         → &prod;

<!-- Griegos -->
α  (alfa)                → &alpha;
β  (beta)                → &beta;
∈  (pertenece)           → &isin;
∉  (no pertenece)        → &notin;
```

### Estilos de Texto
```html
<!-- Centrado -->
<p style="text-align: center;">Texto centrado</p>

<!-- Color -->
<p style="color: #667eea;">Texto morado</p>

<!-- Tamaño de fuente -->
<p style="font-size: 1.2em;">Texto más grande</p>

<!-- Fondo coloreado -->
<p style="background: #d4edda; padding: 10px;">Texto con fondo verde</p>

<!-- Combinado -->
<p style="text-align: center; font-size: 1.3em; color: #667eea;">
    <strong>Texto destacado</strong>
</p>
```

---

## 🔢 Valores y Opciones

### Tipos de Contenido
- `TEORIA` → Conceptos teóricos
- `EJEMPLO` → Ejemplos prácticos
- `EJEMPLO_EXTRA` → Ejemplos adicionales (opcional)
- `RESUMEN` → Resumen del tema

### Tipos de Ejercicio
- `ABIERTO` → Respuesta de texto libre
- `MULTIPLE` → Opción múltiple (A, B, C, D)

### Dificultad
- `FACIL` → Nivel básico
- `INTERMEDIO` → Nivel medio
- `DIFICIL` → Nivel avanzado

### Opciones Múltiples (letras)
- `A`, `B`, `C`, `D`

---

## ⚙️ Configuración de Orden

### Números de Orden Recomendados

```python
# LECCIONES (globales)
Lección 1: orden=1
Lección 2: orden=2
Lección 3: orden=3

# TEMAS (dentro de cada lección)
Tema 1 de Lección 1: orden=1
Tema 2 de Lección 1: orden=2

# CONTENIDOS (dentro de cada tema)
Teoría 1: orden=1
Ejemplo 1: orden=2
Ejemplo Extra: orden=3
Teoría 2: orden=4

# EJERCICIOS (dentro de cada tema)
Ejercicio 1: orden=1
Ejercicio 2: orden=2
...
Ejercicio 15: orden=15
```

---

## 🎯 Buenas Prácticas

### 1. Distribución de Dificultad
```python
# En 15 ejercicios:
Ejercicios 1-5:   dificultad='FACIL'
Ejercicios 6-10:  dificultad='INTERMEDIO'
Ejercicios 11-15: dificultad='DIFICIL'
```

### 2. Mostrar Dificultad
```python
# Ocultar en ejercicios fáciles
mostrar_dificultad=False  # Para FACIL

# Mostrar en ejercicios difíciles
mostrar_dificultad=True   # Para INTERMEDIO y DIFICIL
```

### 3. Retroalimentación Útil
```python
# ✅ BIEN - Retroalimentación educativa
retroalimentacion_incorrecta="""
    <p>Incorrecto. Recuerda que una proposición debe tener un valor
    de verdad definido. Las preguntas no son proposiciones.</p>
"""

# ❌ MAL - Retroalimentación vacía
retroalimentacion_incorrecta="<p>Incorrecto</p>"
```

### 4. Ayuda Efectiva
```python
# ✅ BIEN - Ayuda que orienta
texto_ayuda="""
    <p>Recuerda la tabla de verdad de la conjunción (∧):
    solo es verdadera cuando AMBAS proposiciones son verdaderas.</p>
"""

# ❌ MAL - Ayuda que da la respuesta
texto_ayuda="<p>La respuesta es A</p>"
```

---

## 🛠️ Comandos Útiles

### Ver contenido actual
```bash
python manage.py shell
```
```python
from lessons.models import *

# Contar elementos
print(f"Lecciones: {Leccion.objects.count()}")
print(f"Temas: {Tema.objects.count()}")
print(f"Ejercicios: {Ejercicio.objects.count()}")

# Listar lecciones
for leccion in Leccion.objects.all():
    print(f"{leccion.orden}. {leccion.titulo}")
```

### Backup de la base de datos
```bash
# Windows
copy db.sqlite3 db.sqlite3.backup

# Linux/Mac
cp db.sqlite3 db.sqlite3.backup
```

### Restaurar backup
```bash
# Windows
copy db.sqlite3.backup db.sqlite3

# Linux/Mac
cp db.sqlite3.backup db.sqlite3
```

---

## 🚨 Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `UNIQUE constraint failed` | Orden duplicado | Verifica números de orden |
| `Ejercicio matching query does not exist` | Referencia incorrecta | Verifica nombres de variables |
| `OpcionMultiple does not exist` | Opción faltante | Crea opciones A, B, C, D |
| `respuesta_correcta must be A, B, C or D` | Letra inválida | Usa solo A, B, C o D en MULTIPLE |

---

## 📋 Checklist Antes de Ejecutar

- [ ] Backup de la base de datos realizado
- [ ] Entorno virtual activado
- [ ] Estás en el directorio correcto (`matelog_backend`)
- [ ] Números de orden son únicos y secuenciales
- [ ] Ejercicios MULTIPLE tienen sus opciones creadas
- [ ] `respuesta_correcta` coincide con una opción válida
- [ ] HTML está bien formado (sin etiquetas sin cerrar)

---

**¡Listo para crear contenido educativo increíble!** 📚✨
