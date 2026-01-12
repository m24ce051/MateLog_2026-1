# 📚 Índice de Archivos de Gestión de Contenido - MateLog

Este directorio contiene todos los archivos necesarios para gestionar el contenido educativo de MateLog.

---

## 📂 Archivos Disponibles

### 1. **contenido.db** 🗄️
**Propósito:** Archivo principal con el contenido educativo completo de MateLog.

**Uso:**
```bash
python manage.py shell < contenido.db
```

**Características:**
- ✅ Contiene todo el contenido actual (2 lecciones, 3 temas, ~45 ejercicios)
- ✅ ELIMINA el contenido existente antes de cargar (reset completo)
- ✅ Ideal para inicializar la base de datos o restaurar contenido
- ✅ Ampliamente documentado con comentarios explicativos

**Cuándo usar:**
- Primera vez que configuras MateLog
- Quieres restaurar el contenido a su estado original
- Hiciste muchos cambios y quieres empezar de cero

---

### 2. **agregar_contenido.py** ➕
**Propósito:** Script para AGREGAR contenido nuevo sin eliminar el existente.

**Uso:**
```bash
python manage.py shell < agregar_contenido.py
```

**Características:**
- ✅ NO elimina contenido existente
- ✅ Permite expandir lecciones, temas y ejercicios
- ✅ Verifica conflictos de orden antes de crear
- ✅ Muestra el estado actual antes y después

**Cuándo usar:**
- Ya tienes contenido y quieres agregar más
- Quieres crear una nueva lección sin tocar las existentes
- Necesitas agregar ejercicios a un tema que ya existe

---

### 3. **README_CONTENIDO.md** 📖
**Propósito:** Guía completa y detallada de gestión de contenido.

**Contenido:**
- 📋 Cómo usar los archivos de contenido
- ➕ Cómo agregar contenido nuevo (lecciones, temas, ejercicios)
- ✏️ Cómo modificar contenido existente
- 🗑️ Cómo eliminar contenido
- 🏗️ Estructura detallada de los modelos
- 💡 Ejemplos prácticos paso a paso
- 🔧 Solución de problemas comunes

**Cuándo consultar:**
- Necesitas una guía completa de gestión de contenido
- Tienes dudas sobre la estructura de los modelos
- Encuentras errores y necesitas soluciones
- Quieres ver ejemplos detallados

---

### 4. **REFERENCIA_RAPIDA_CONTENIDO.md** ⚡
**Propósito:** Referencia rápida con plantillas y snippets de código.

**Contenido:**
- 🚀 Comandos de ejecución rápida
- 📚 Plantillas de código listas para copiar/pegar
- 🎨 Etiquetas HTML útiles con ejemplos
- 🔢 Lista de valores y opciones válidas
- ⚙️ Configuración de números de orden
- 🎯 Buenas prácticas recomendadas
- 🛠️ Comandos útiles de Django
- 🚨 Tabla de errores comunes

**Cuándo consultar:**
- Necesitas crear contenido rápidamente
- Quieres copiar una plantilla de lección/tema/ejercicio
- Necesitas recordar los símbolos HTML de operadores lógicos
- Buscas buenas prácticas de distribución de dificultad

---

### 5. **EJEMPLOS_HTML_AVANZADO.md** 🎨
**Propósito:** Galería de ejemplos de HTML avanzado para contenido visualmente atractivo.

**Contenido:**
- 📊 Tablas de verdad estilizadas con colores
- 🎓 Cajas de información destacada (definiciones, advertencias, ejemplos)
- 🔢 Símbolos matemáticos y lógicos con códigos HTML
- 📋 Listas avanzadas con iconos y colores
- 🎯 Ejercicios interactivos visualmente atractivos
- 🔗 Texto con formato especial
- 💯 Retroalimentación avanzada motivadora

**Cuándo consultar:**
- Quieres hacer tu contenido más visual y atractivo
- Necesitas tablas de verdad con colores
- Buscas símbolos matemáticos (∧, ∨, ¬, →, etc.)
- Quieres crear cajas de advertencia o notas destacadas
- Necesitas plantillas de retroalimentación educativa

---

### 6. **populate_db.py** (Legacy) 🕰️
**Propósito:** Archivo original de población (más simple, menos documentado).

**Nota:** Se recomienda usar **contenido.db** en su lugar, ya que está más completo y mejor documentado.

---

## 🎯 Flujo de Trabajo Recomendado

### Escenario 1: Primera vez usando MateLog
```bash
# 1. Activar entorno virtual
.\venv\Scripts\activate

# 2. Ir al directorio backend
cd matelog_backend

# 3. Cargar contenido inicial
python manage.py shell < contenido.db

# 4. Verificar en admin
# Ir a http://localhost:8000/admin/
```

### Escenario 2: Agregar una nueva lección
```bash
# 1. Consultar la referencia rápida
# Abrir: REFERENCIA_RAPIDA_CONTENIDO.md

# 2. Editar agregar_contenido.py
# Descomenta y modifica el bloque de nueva lección

# 3. Ejecutar
python manage.py shell < agregar_contenido.py

# 4. Verificar en frontend
# Ir a http://localhost:5173/lecciones
```

### Escenario 3: Modificar contenido existente

**Opción A: Desde el admin (Recomendado para cambios pequeños)**
```
1. Ir a http://localhost:8000/admin/
2. Navegar a Lecciones > Temas > Contenidos
3. Editar directamente
4. Guardar
```

**Opción B: Editando contenido.db (Para cambios grandes)**
```bash
# 1. Hacer backup
copy db.sqlite3 db.sqlite3.backup

# 2. Editar contenido.db con tu editor favorito
# Buscar y modificar el contenido HTML

# 3. Recargar
python manage.py shell < contenido.db

# 4. Si algo sale mal, restaurar backup
copy db.sqlite3.backup db.sqlite3
```

### Escenario 4: Crear contenido visualmente atractivo
```bash
# 1. Consultar ejemplos HTML avanzado
# Abrir: EJEMPLOS_HTML_AVANZADO.md

# 2. Copiar el HTML de ejemplo que necesites
# Por ejemplo: tabla de verdad con colores

# 3. Pegar en tu contenido_texto
# En contenido.db o en el admin

# 4. Cargar/guardar y verificar visualmente
```

---

## 📊 Comparativa de Archivos

| Característica | contenido.db | agregar_contenido.py | populate_db.py |
|----------------|--------------|----------------------|----------------|
| Elimina contenido existente | ✅ Sí | ❌ No | ✅ Sí |
| Contenido completo | ✅ Sí | ⚠️ Plantillas | ⚠️ Básico |
| Bien documentado | ✅ Sí | ✅ Sí | ❌ No |
| Ejemplos HTML avanzado | ✅ Algunos | ❌ No | ❌ No |
| Verificación de conflictos | ❌ No | ✅ Sí | ❌ No |
| Recomendado para | Inicio/Reset | Expansión | Legacy |

---

## 🆘 Ayuda Rápida

### ¿Qué archivo usar?

```
┌─ ¿Es tu primera vez?
│  └─ Usa: contenido.db
│
┌─ ¿Ya tienes contenido y quieres agregar más?
│  └─ Usa: agregar_contenido.py
│
┌─ ¿Necesitas ver cómo crear algo?
│  └─ Consulta: README_CONTENIDO.md
│
┌─ ¿Quieres copiar una plantilla rápida?
│  └─ Consulta: REFERENCIA_RAPIDA_CONTENIDO.md
│
└─ ¿Quieres hacer contenido más bonito?
   └─ Consulta: EJEMPLOS_HTML_AVANZADO.md
```

### Comandos Esenciales

```bash
# Cargar contenido completo (reset)
python manage.py shell < contenido.db

# Agregar contenido sin eliminar
python manage.py shell < agregar_contenido.py

# Ver contenido actual
python manage.py shell
>>> from lessons.models import *
>>> print(f"Lecciones: {Leccion.objects.count()}")

# Hacer backup
copy db.sqlite3 db.sqlite3.backup  # Windows
cp db.sqlite3 db.sqlite3.backup    # Linux/Mac

# Restaurar backup
copy db.sqlite3.backup db.sqlite3  # Windows
cp db.sqlite3.backup db.sqlite3    # Linux/Mac
```

---

## 📞 Contacto y Soporte

Si tienes dudas sobre algún archivo:

1. **Lee primero:** [README_CONTENIDO.md](README_CONTENIDO.md)
2. **Consulta la referencia:** [REFERENCIA_RAPIDA_CONTENIDO.md](REFERENCIA_RAPIDA_CONTENIDO.md)
3. **Verifica ejemplos:** [EJEMPLOS_HTML_AVANZADO.md](EJEMPLOS_HTML_AVANZADO.md)

---

## 📝 Resumen de Rutas

```
matelog_backend/
├── contenido.db                      # ⭐ Contenido completo (reset)
├── agregar_contenido.py              # ➕ Agregar sin eliminar
├── populate_db.py                    # 🕰️ Legacy (no recomendado)
│
├── INDEX_CONTENIDO.md                # 📂 Este archivo (índice)
├── README_CONTENIDO.md               # 📖 Guía completa
├── REFERENCIA_RAPIDA_CONTENIDO.md    # ⚡ Referencia rápida
└── EJEMPLOS_HTML_AVANZADO.md         # 🎨 Ejemplos HTML
```

---

**¡Todo listo para gestionar el contenido educativo de MateLog!** 🎓✨

**Recomendación:** Empieza leyendo [README_CONTENIDO.md](README_CONTENIDO.md) y ten [REFERENCIA_RAPIDA_CONTENIDO.md](REFERENCIA_RAPIDA_CONTENIDO.md) a la mano para consultas rápidas.
