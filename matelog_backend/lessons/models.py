# lessons/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import unicodedata
import string




class Leccion(models.Model):
    """
    Modelo de Lección. Representa el nivel superior de contenido.
    Usa soft delete (is_active) para mantener IDs consistentes.
    """
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(
        help_text="Descripción de la lección (soporta HTML desde TinyMCE)"
    )
    orden = models.PositiveIntegerField(
        unique=True,
        help_text="Orden de aparición en el frontend"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Si está inactiva, no se mostrará en el frontend"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = 'Lección'
        verbose_name_plural = 'Lecciones'
        ordering = ['orden']
   
    def __str__(self):
        status = "✓" if self.is_active else "✗"
        return f"{status} Lección {self.orden}: {self.titulo}"




class Tema(models.Model):
    """
    Modelo de Tema. Pertenece a una Lección.
    Contiene la teoría/ejemplos y los ejercicios.
    """
    leccion = models.ForeignKey(
        Leccion,
        on_delete=models.CASCADE,
        related_name='temas'
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(
        help_text="Descripción del tema (soporta HTML desde TinyMCE)"
    )
    orden = models.PositiveIntegerField(
        help_text="Orden dentro de la lección"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si está inactivo, no se mostrará en el frontend"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'
        ordering = ['leccion__orden', 'orden']
        unique_together = ['leccion', 'orden']
   
    def __str__(self):
        status = "✓" if self.is_active else "✗"
        return f"{status} {self.leccion.titulo} - Tema {self.orden}: {self.titulo}"




class ContenidoTema(models.Model):
    """
    Modelo para los recuadros de Teoría, Ejemplo, Ejemplo Extra y Resumen.
    Se muestran secuencialmente antes de los ejercicios.
    Las imágenes se insertan mediante TinyMCE.
    """
    TIPO_CHOICES = [
        ('TEORIA', 'Teoría'),
        ('EJEMPLO', 'Ejemplo'),
        ('EJEMPLO_EXTRA', 'Ejemplo Extra'),
        ('RESUMEN', 'Resumen'),
    ]
   
    tema = models.ForeignKey(
        Tema,
        on_delete=models.CASCADE,
        related_name='contenidos'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    orden = models.PositiveIntegerField(
        help_text="Orden de aparición dentro del tema"
    )
   
    # Contenido con HTML desde TinyMCE (incluye imágenes incrustadas)
    contenido_texto = models.TextField(
        help_text="Contenido en HTML desde TinyMCE (incluye formato, imágenes, tablas, etc.)"
    )
   
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = 'Contenido de Tema'
        verbose_name_plural = 'Contenidos de Temas'
        ordering = ['tema', 'orden']
        unique_together = ['tema', 'orden']
   
    def __str__(self):
        return f"{self.tema.titulo} - {self.get_tipo_display()} #{self.orden}"




class Ejercicio(models.Model):
    """
    Modelo de Ejercicio. Pertenece a un Tema.
    Puede ser de respuesta abierta o de opción múltiple.
    Las imágenes se insertan mediante TinyMCE en el enunciado.
    """
    TIPO_CHOICES = [
        ('ABIERTO', 'Respuesta Abierta'),
        ('MULTIPLE', 'Opción Múltiple'),
    ]
   
    DIFICULTAD_CHOICES = [
        ('FACIL', 'Fácil'),
        ('INTERMEDIO', 'Intermedio'),
        ('DIFICIL', 'Difícil'),
    ]
   
    tema = models.ForeignKey(
        Tema,
        on_delete=models.CASCADE,
        related_name='ejercicios'
    )
    orden = models.PositiveIntegerField(
        help_text="Orden dentro del tema (número de ejercicio)"
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    dificultad = models.CharField(max_length=15, choices=DIFICULTAD_CHOICES)
   
    # Contenido del ejercicio
    instruccion = models.TextField(
        help_text="Instrucciones para el estudiante (soporta HTML desde TinyMCE)"
    )
    enunciado = models.TextField(
        verbose_name="Ejercicio",
        help_text="El ejercicio en sí (soporta HTML desde TinyMCE, incluye imágenes)"
    )
   
    # Respuesta correcta
    respuesta_correcta = models.CharField(
        max_length=500,
        blank=False,
        help_text="Para abiertos: respuesta exacta. Para múltiple: letra de opción correcta (A, B, C, D)"
    )
   
    # Texto de ayuda y retroalimentación
    texto_ayuda = models.TextField(
        blank=True,
        help_text="Texto que se muestra al presionar 'Ayuda' (soporta HTML desde TinyMCE)"
    )
    retroalimentacion_correcta = models.TextField(
        blank=True,
        verbose_name="Retroalimentación (correcta)",
        help_text="Mensaje cuando la respuesta es correcta (soporta HTML desde TinyMCE)"
    )
    retroalimentacion_incorrecta = models.TextField(
        blank=True,
        verbose_name="Retroalimentación (incorrecta)",
        help_text="Mensaje cuando la respuesta es incorrecta (soporta HTML desde TinyMCE)"
    )
   
    # Control de visualización
    mostrar_dificultad = models.BooleanField(
        default=False,
        verbose_name="Mostrar dificultad",
        help_text="Si se marca, la dificultad será visible para el estudiante"
    )

    # MateLog-AE: Control de grupos
    obligatorio = models.BooleanField(
        default=False,
        verbose_name="Obligatorio para Control",
        help_text="Si está marcado, este ejercicio aparece en el grupo de Control. El grupo Experimental ve ejercicios según su clasificación de autoeficacia."
    )
   
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = 'Ejercicio'
        verbose_name_plural = 'Ejercicios'
        ordering = ['tema', 'orden']
        unique_together = ['tema', 'orden']
   
    def __str__(self):
        return f"{self.tema.titulo} - Ejercicio {self.orden}"

    def clean(self):
        """
        Validaciones personalizadas del modelo.
        """
        super().clean()

        # Validar que respuesta_correcta no esté vacía
        if not self.respuesta_correcta or not self.respuesta_correcta.strip():
            raise ValidationError({
                'respuesta_correcta': 'La respuesta correcta no puede estar vacía'
            })

        # Validaciones específicas para ejercicios MÚLTIPLE
        if self.tipo == 'MULTIPLE':
            respuesta_normalizada = self.respuesta_correcta.strip().upper()

            # Validar que sea una letra válida (A, B, C, D)
            if respuesta_normalizada not in ['A', 'B', 'C', 'D']:
                raise ValidationError({
                    'respuesta_correcta': f'Para ejercicios de opción múltiple, la respuesta debe ser A, B, C o D. Valor actual: "{self.respuesta_correcta}"'
                })

            # Validar que exista la opción correspondiente (solo si el objeto ya existe en BD)
            if self.pk:  # Solo validar si el ejercicio ya fue guardado
                if not self.opciones.filter(letra=respuesta_normalizada).exists():
                    raise ValidationError({
                        'respuesta_correcta': f'No existe una opción múltiple con la letra "{respuesta_normalizada}". Debe crear primero la opción antes de seleccionarla como correcta.'
                    })

    def save(self, *args, **kwargs):
        """
        Normaliza respuesta_correcta antes de guardar.
        """
        if self.tipo == 'ABIERTO':
            # Para ejercicios abiertos: normalizar espacios
            self.respuesta_correcta = ' '.join(self.respuesta_correcta.split()).strip()
        elif self.tipo == 'MULTIPLE':
            # Para ejercicios múltiples: normalizar a mayúscula sin espacios
            self.respuesta_correcta = self.respuesta_correcta.strip().upper()

        # Ejecutar validaciones antes de guardar
        self.full_clean()

        super().save(*args, **kwargs)

    def validar_respuesta(self, respuesta_usuario):
        """
        Valida la respuesta del usuario.
        Para abiertos: ignora mayúsculas, espacios, tildes y puntuación.
        Para múltiple: compara directamente.
        """
        if self.tipo == 'MULTIPLE':
            return respuesta_usuario.strip().upper() == self.respuesta_correcta.upper()

        # Para respuestas abiertas: normalizar
        def normalizar(texto):
            # Quitar espacios extras
            texto = ' '.join(texto.split())
            # Convertir a minúsculas
            texto = texto.lower()
            # Quitar tildes
            texto = ''.join(
                c for c in unicodedata.normalize('NFD', texto)
                if unicodedata.category(c) != 'Mn'
            )
            # Quitar signos de puntuación
            texto = texto.translate(str.maketrans('', '', string.punctuation))
            return texto.strip()

        return normalizar(respuesta_usuario) == normalizar(self.respuesta_correcta)




class OpcionMultiple(models.Model):
    """
    Modelo para las opciones de un ejercicio de opción múltiple.
    """
    LETRA_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
   
    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.CASCADE,
        related_name='opciones'
    )
    letra = models.CharField(max_length=1, choices=LETRA_CHOICES)
    texto = models.TextField(help_text="Texto de la opción")
   
    class Meta:
        verbose_name = 'Opción Múltiple'
        verbose_name_plural = 'Opciones Múltiples'
        ordering = ['letra']
        unique_together = ['ejercicio', 'letra']
   
    def __str__(self):
        return f"{self.ejercicio} - Opción {self.letra}"




# NOTA: Los modelos ProgresoLeccion, ProgresoTema y RespuestaEjercicio
# están en la app 'tracking'. Se importan desde allí en views.py y serializers.py


