# 🎨 Ejemplos de HTML Avanzado para Contenido MateLog

Esta guía contiene ejemplos prácticos de HTML que puedes copiar y pegar directamente en tus contenidos, ejercicios y retroalimentación.

---

## 📊 Tablas de Verdad Estilizadas

### Tabla Simple con Colores

```html
<h3>Tabla de Verdad: Conjunción (p ∧ q)</h3>

<table style="width: 70%; margin: 20px auto; border-collapse: collapse; font-family: Arial;">
    <thead>
        <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <th style="border: 2px solid #ddd; padding: 12px; font-size: 1.1em;">p</th>
            <th style="border: 2px solid #ddd; padding: 12px; font-size: 1.1em;">q</th>
            <th style="border: 2px solid #ddd; padding: 12px; font-size: 1.1em;">p ∧ q</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">V</td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">V</td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; background: #d4edda; font-weight: bold;">V</td>
        </tr>
        <tr style="background: #f9f9f9;">
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">V</td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">F</td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; background: #f8d7da; font-weight: bold;">F</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">F</td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">V</td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; background: #f8d7da; font-weight: bold;">F</td>
        </tr>
        <tr style="background: #f9f9f9;">
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">F</td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">F</td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; background: #f8d7da; font-weight: bold;">F</td>
        </tr>
    </tbody>
</table>

<p style="text-align: center; margin-top: 15px; color: #666;">
    <em>La conjunción solo es verdadera cuando ambas proposiciones son verdaderas</em>
</p>
```

### Tabla Comparativa de Conectivos

```html
<h3>Comparación de Conectivos Lógicos</h3>

<table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
    <thead>
        <tr style="background: #667eea; color: white;">
            <th style="border: 1px solid #ddd; padding: 12px; width: 20%;">Conectivo</th>
            <th style="border: 1px solid #ddd; padding: 12px; width: 15%;">Símbolo</th>
            <th style="border: 1px solid #ddd; padding: 12px; width: 30%;">Ejemplo</th>
            <th style="border: 1px solid #ddd; padding: 12px; width: 35%;">Verdadero cuando...</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Conjunción</strong></td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.3em;">∧</td>
            <td style="border: 1px solid #ddd; padding: 10px;">p ∧ q</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Ambas son verdaderas</td>
        </tr>
        <tr style="background: #f9f9f9;">
            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Disyunción</strong></td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.3em;">∨</td>
            <td style="border: 1px solid #ddd; padding: 10px;">p ∨ q</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Al menos una es verdadera</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Negación</strong></td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.3em;">¬</td>
            <td style="border: 1px solid #ddd; padding: 10px;">¬p</td>
            <td style="border: 1px solid #ddd; padding: 10px;">p es falsa</td>
        </tr>
        <tr style="background: #f9f9f9;">
            <td style="border: 1px solid #ddd; padding: 10px;"><strong>Implicación</strong></td>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.3em;">→</td>
            <td style="border: 1px solid #ddd; padding: 10px;">p → q</td>
            <td style="border: 1px solid #ddd; padding: 10px;">p es falsa o q es verdadera</td>
        </tr>
    </tbody>
</table>
```

---

## 🎓 Cajas de Información Destacada

### Caja de Definición

```html
<div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 5px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;">
    <h4 style="margin-top: 0; color: #667eea;">
        📚 Definición: Proposición
    </h4>
    <p style="margin-bottom: 0; line-height: 1.6;">
        Una <strong>proposición</strong> es una oración declarativa que puede ser
        verdadera o falsa, pero no ambas al mismo tiempo.
    </p>
</div>
```

### Caja de Advertencia

```html
<div style="background: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;">
    <h4 style="margin-top: 0; color: #856404;">
        ⚠️ Advertencia
    </h4>
    <p style="margin-bottom: 0; color: #856404; line-height: 1.6;">
        No confundas la disyunción inclusiva (∨) con la disyunción exclusiva (⊕).
        En lógica proposicional, "o" es inclusivo por defecto.
    </p>
</div>
```

### Caja de Ejemplo

```html
<div style="background: #d4edda;
            border-left: 5px solid #28a745;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;">
    <h4 style="margin-top: 0; color: #155724;">
        💡 Ejemplo Práctico
    </h4>
    <p style="margin-bottom: 10px; color: #155724;">
        Sean las proposiciones:
    </p>
    <ul style="color: #155724; line-height: 1.8;">
        <li><strong>p:</strong> "Está lloviendo"</li>
        <li><strong>q:</strong> "Llevo paraguas"</li>
    </ul>
    <p style="margin-bottom: 0; color: #155724;">
        Entonces <strong>p → q</strong> significa: "Si está lloviendo, entonces llevo paraguas"
    </p>
</div>
```

### Caja de Nota Importante

```html
<div style="background: #e7f3ff;
            border-left: 5px solid #2196f3;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;">
    <h4 style="margin-top: 0; color: #1976d2;">
        📌 Nota Importante
    </h4>
    <p style="margin-bottom: 0; color: #1565c0; line-height: 1.6;">
        Recuerda que en lógica clásica solo existen dos valores de verdad:
        <strong>Verdadero (V)</strong> y <strong>Falso (F)</strong>.
    </p>
</div>
```

---

## 🔢 Símbolos Matemáticos y Lógicos

### Lista de Símbolos Comunes

```html
<h3>Símbolos Lógicos Fundamentales</h3>

<table style="width: 90%; margin: 20px auto; border-collapse: collapse;">
    <thead>
        <tr style="background: #f0f0f0;">
            <th style="border: 1px solid #ddd; padding: 12px; width: 15%;">Símbolo</th>
            <th style="border: 1px solid #ddd; padding: 12px; width: 25%;">Nombre</th>
            <th style="border: 1px solid #ddd; padding: 12px; width: 30%;">Se lee como...</th>
            <th style="border: 1px solid #ddd; padding: 12px; width: 30%;">Código HTML</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.5em;">∧</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Conjunción</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Y, y</td>
            <td style="border: 1px solid #ddd; padding: 10px; font-family: monospace;">&amp;and;</td>
        </tr>
        <tr style="background: #f9f9f9;">
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.5em;">∨</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Disyunción</td>
            <td style="border: 1px solid #ddd; padding: 10px;">O, o</td>
            <td style="border: 1px solid #ddd; padding: 10px; font-family: monospace;">&amp;or;</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.5em;">¬</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Negación</td>
            <td style="border: 1px solid #ddd; padding: 10px;">No, negación de</td>
            <td style="border: 1px solid #ddd; padding: 10px; font-family: monospace;">&amp;not;</td>
        </tr>
        <tr style="background: #f9f9f9;">
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.5em;">→</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Implicación</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Si... entonces</td>
            <td style="border: 1px solid #ddd; padding: 10px; font-family: monospace;">&amp;rarr;</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.5em;">↔</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Bicondicional</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Si y solo si</td>
            <td style="border: 1px solid #ddd; padding: 10px; font-family: monospace;">&amp;harr;</td>
        </tr>
        <tr style="background: #f9f9f9;">
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.5em;">∀</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Cuantificador universal</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Para todo</td>
            <td style="border: 1px solid #ddd; padding: 10px; font-family: monospace;">&amp;forall;</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.5em;">∃</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Cuantificador existencial</td>
            <td style="border: 1px solid #ddd; padding: 10px;">Existe</td>
            <td style="border: 1px solid #ddd; padding: 10px; font-family: monospace;">&amp;exist;</td>
        </tr>
    </tbody>
</table>
```

### Fórmulas con Símbolos

```html
<h3>Leyes de De Morgan</h3>

<div style="background: #f5f5f5; padding: 25px; margin: 20px 0; border-radius: 10px; text-align: center;">
    <p style="font-size: 1.3em; margin: 10px 0; font-family: 'Times New Roman', serif;">
        ¬(p ∧ q) ≡ (¬p ∨ ¬q)
    </p>
    <p style="font-size: 1.3em; margin: 10px 0; font-family: 'Times New Roman', serif;">
        ¬(p ∨ q) ≡ (¬p ∧ ¬q)
    </p>
</div>

<p style="text-align: center; color: #666; font-style: italic;">
    La negación de una conjunción es la disyunción de las negaciones
</p>
```

---

## 📋 Listas Avanzadas

### Lista con Iconos

```html
<h3>Pasos para Construir una Tabla de Verdad</h3>

<ol style="line-height: 2; font-size: 1.05em;">
    <li>
        <strong>🔍 Identificar proposiciones:</strong>
        Encuentra todas las variables proposicionales (p, q, r, ...)
    </li>
    <li>
        <strong>📊 Calcular filas:</strong>
        Usa la fórmula 2<sup>n</sup> donde n es el número de proposiciones
    </li>
    <li>
        <strong>📝 Listar combinaciones:</strong>
        Escribe todas las combinaciones posibles de V y F
    </li>
    <li>
        <strong>⚡ Evaluar expresión:</strong>
        Calcula el valor de verdad para cada combinación
    </li>
    <li>
        <strong>✅ Verificar resultados:</strong>
        Revisa que todas las filas estén completas
    </li>
</ol>
```

### Lista con Colores

```html
<h3>Tipos de Proposiciones</h3>

<ul style="list-style: none; padding-left: 0;">
    <li style="background: #d4edda; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 5px solid #28a745;">
        <strong>✅ Tautología:</strong> Siempre verdadera (ej: p ∨ ¬p)
    </li>
    <li style="background: #f8d7da; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 5px solid #dc3545;">
        <strong>❌ Contradicción:</strong> Siempre falsa (ej: p ∧ ¬p)
    </li>
    <li style="background: #fff3cd; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 5px solid #ffc107;">
        <strong>⚖️ Contingencia:</strong> Puede ser V o F dependiendo de los valores
    </li>
</ul>
```

---

## 🎯 Ejercicios Interactivos (Visualmente Atractivos)

### Ejercicio con Paso a Paso

```html
<h3>Ejercicio Resuelto: Evaluación de Expresión</h3>

<div style="background: #e7f3ff; padding: 20px; border-radius: 10px; margin: 20px 0;">
    <p><strong>Evalúa:</strong> (p ∧ q) ∨ ¬r cuando p=V, q=F, r=V</p>

    <div style="background: white; padding: 15px; margin: 15px 0; border-radius: 8px; border: 2px solid #2196f3;">
        <p style="margin: 5px 0;"><strong>Paso 1:</strong> Sustituir valores</p>
        <p style="margin: 5px 0; font-family: monospace; font-size: 1.1em; color: #1976d2;">
            (V ∧ F) ∨ ¬V
        </p>
    </div>

    <div style="background: white; padding: 15px; margin: 15px 0; border-radius: 8px; border: 2px solid #2196f3;">
        <p style="margin: 5px 0;"><strong>Paso 2:</strong> Evaluar paréntesis (p ∧ q)</p>
        <p style="margin: 5px 0; font-family: monospace; font-size: 1.1em; color: #1976d2;">
            F ∨ ¬V
        </p>
    </div>

    <div style="background: white; padding: 15px; margin: 15px 0; border-radius: 8px; border: 2px solid #2196f3;">
        <p style="margin: 5px 0;"><strong>Paso 3:</strong> Evaluar negación (¬r)</p>
        <p style="margin: 5px 0; font-family: monospace; font-size: 1.1em; color: #1976d2;">
            F ∨ F
        </p>
    </div>

    <div style="background: #d4edda; padding: 15px; margin: 15px 0; border-radius: 8px; border: 3px solid #28a745;">
        <p style="margin: 5px 0;"><strong>✅ Resultado Final:</strong></p>
        <p style="margin: 5px 0; font-family: monospace; font-size: 1.3em; color: #155724; font-weight: bold;">
            F (Falso)
        </p>
    </div>
</div>
```

### Ejercicio con Opciones Visuales

```html
<p><strong>¿Cuál de las siguientes tablas representa correctamente la conjunción (p ∧ q)?</strong></p>

<div style="display: flex; gap: 20px; flex-wrap: wrap; margin: 20px 0;">
    <!-- Opción A -->
    <div style="flex: 1; min-width: 200px; border: 3px solid #28a745; border-radius: 10px; padding: 15px; background: #d4edda;">
        <p style="text-align: center; font-weight: bold; color: #155724; margin-top: 0;">Opción A ✓</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
            <tr style="background: #28a745; color: white;">
                <th style="border: 1px solid #ddd; padding: 8px;">p</th>
                <th style="border: 1px solid #ddd; padding: 8px;">q</th>
                <th style="border: 1px solid #ddd; padding: 8px;">p∧q</th>
            </tr>
            <tr><td style="border: 1px solid #ddd; padding: 8px; text-align: center;">V</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">V</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">V</td></tr>
            <tr><td style="border: 1px solid #ddd; padding: 8px; text-align: center;">V</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">F</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">F</td></tr>
        </table>
    </div>

    <!-- Opción B -->
    <div style="flex: 1; min-width: 200px; border: 2px solid #ddd; border-radius: 10px; padding: 15px; background: #f9f9f9;">
        <p style="text-align: center; font-weight: bold; margin-top: 0;">Opción B</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
            <tr style="background: #999; color: white;">
                <th style="border: 1px solid #ddd; padding: 8px;">p</th>
                <th style="border: 1px solid #ddd; padding: 8px;">q</th>
                <th style="border: 1px solid #ddd; padding: 8px;">p∧q</th>
            </tr>
            <tr><td style="border: 1px solid #ddd; padding: 8px; text-align: center;">V</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">V</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">F</td></tr>
            <tr><td style="border: 1px solid #ddd; padding: 8px; text-align: center;">V</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">F</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">V</td></tr>
        </table>
    </div>
</div>
```

---

## 🔗 Texto con Enlaces y Formato Especial

### Texto con Destacados de Color

```html
<p>
    En lógica proposicional, trabajamos con dos valores de verdad:
    <span style="background: #d4edda; padding: 3px 8px; border-radius: 5px; font-weight: bold; color: #155724;">
        Verdadero (V)
    </span>
    y
    <span style="background: #f8d7da; padding: 3px 8px; border-radius: 5px; font-weight: bold; color: #721c24;">
        Falso (F)
    </span>
</p>
```

### Código Inline

```html
<p>
    La proposición se denota como
    <code style="background: #f5f5f5; padding: 3px 6px; border-radius: 4px; font-family: monospace; color: #d63384;">
        p: "Llueve"
    </code>
    y tiene un valor de verdad bien definido.
</p>
```

---

## 💯 Retroalimentación Avanzada

### Retroalimentación Correcta Motivadora

```html
<div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            padding: 25px;
            border-radius: 15px;
            border: 3px solid #28a745;
            text-align: center;">
    <h3 style="color: #155724; margin-top: 0; font-size: 1.5em;">
        🎉 ¡Excelente trabajo!
    </h3>
    <p style="color: #155724; font-size: 1.1em; line-height: 1.6;">
        Has comprendido correctamente el concepto de conjunción lógica.
        La conjunción (∧) solo es verdadera cuando <strong>ambas</strong>
        proposiciones son verdaderas.
    </p>
    <p style="color: #155724; margin-bottom: 0; font-style: italic;">
        ¡Continúa así! 💪
    </p>
</div>
```

### Retroalimentación Incorrecta Educativa

```html
<div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            padding: 25px;
            border-radius: 15px;
            border: 3px solid #dc3545;">
    <h3 style="color: #721c24; margin-top: 0; font-size: 1.4em;">
        ❌ No es correcto, pero no te preocupes
    </h3>
    <p style="color: #721c24; line-height: 1.6;">
        <strong>Revisemos el concepto:</strong>
    </p>
    <ul style="color: #721c24; line-height: 1.8; text-align: left;">
        <li>Una proposición debe ser una oración <strong>declarativa</strong></li>
        <li>Las preguntas NO son proposiciones porque no afirman ni niegan nada</li>
        <li>Las órdenes tampoco son proposiciones</li>
    </ul>
    <div style="background: #fff3cd; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 5px solid #ffc107;">
        <p style="color: #856404; margin: 0;">
            <strong>💡 Tip:</strong> Pregúntate: "¿Puedo decir si esto es verdadero o falso?"
            Si no puedes, probablemente no sea una proposición.
        </p>
    </div>
    <p style="color: #721c24; margin-bottom: 0; text-align: center; font-style: italic;">
        Revisa la teoría y vuelve a intentarlo 📚
    </p>
</div>
```

---

**¡Usa estos ejemplos para crear contenido visualmente atractivo y educativo en MateLog!** 🎨✨
