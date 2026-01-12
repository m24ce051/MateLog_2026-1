# ml_adaptive/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class CodigoAcceso(models.Model):
    """
    Códigos de acceso para asignación de grupos (Control vs Experimental).
    LMB = Control, MLZ = Experimental
    """
    GRUPO_CHOICES = [
        ('CONTROL', 'Control'),
        ('EXPERIMENTAL', 'Experimental')
    ]

    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código de Acceso",
        help_text="Código que los estudiantes ingresarán (LMB o MLZ)"
    )
    grupo = models.CharField(
        max_length=15,
        choices=GRUPO_CHOICES,
        verbose_name="Grupo Asignado"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si está inactivo, el código no será válido para nuevos registros"
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Notas internas sobre este código"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Código de Acceso'
        verbose_name_plural = 'Códigos de Acceso'
        ordering = ['grupo', 'codigo']

    def __str__(self):
        status = "✓" if self.activo else "✗"
        return f"{status} {self.codigo} → {self.get_grupo_display()}"


class PerfilUsuario(models.Model):
    """
    Perfil extendido de usuario con información de grupo y clasificación.
    Cada usuario tiene un perfil que determina su grupo y nivel de autoeficacia.
    """
    GRUPO_CHOICES = [
        ('CONTROL', 'Control'),
        ('EXPERIMENTAL', 'Experimental')
    ]

    CLASIFICACION_AUTOEFICACIA_CHOICES = [
        ('ALTO', 'Alto'),
        ('MEDIO', 'Medio'),
        ('BAJO', 'Bajo')
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name="Usuario"
    )
    grupo = models.CharField(
        max_length=15,
        choices=GRUPO_CHOICES,
        verbose_name="Grupo Experimental"
    )
    codigo_usado = models.CharField(
        max_length=10,
        verbose_name="Código Utilizado",
        help_text="Código de acceso que usó para registrarse"
    )
    clasificacion_autoeficacia = models.CharField(
        max_length=20,
        choices=CLASIFICACION_AUTOEFICACIA_CHOICES,
        null=True,
        blank=True,
        verbose_name="Clasificación de Autoeficacia",
        help_text="Clasificación calculada a partir de la escala de autoeficacia pre-test"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    # Flags de completitud de evaluaciones
    completo_autoeficacia_pre = models.BooleanField(
        default=False,
        verbose_name="Completó Autoeficacia Pre-test"
    )
    completo_diagnostico = models.BooleanField(
        default=False,
        verbose_name="Completó Examen Diagnóstico"
    )
    completo_autoeficacia_post = models.BooleanField(
        default=False,
        verbose_name="Completó Autoeficacia Post-test"
    )
    completo_final = models.BooleanField(
        default=False,
        verbose_name="Completó Examen Final"
    )

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
        ordering = ['grupo', 'user__username']

    def __str__(self):
        clasificacion = f" [{self.clasificacion_autoeficacia}]" if self.clasificacion_autoeficacia else ""
        return f"{self.user.username} - {self.get_grupo_display()}{clasificacion}"


class RespuestaEscala(models.Model):
    """
    Almacena respuestas a escalas de autoeficacia y exámenes diagnóstico/final.
    Ambos grupos (Control y Experimental) completan todas las escalas.
    """
    TIPO_ESCALA_CHOICES = [
        ('AUTOEFICACIA_PRE', 'Autoeficacia Pre-test'),
        ('AUTOEFICACIA_POST', 'Autoeficacia Post-test'),
        ('DIAGNOSTICO', 'Examen Diagnóstico'),
        ('FINAL', 'Examen Final'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='respuestas_escalas',
        verbose_name="Usuario"
    )
    tipo_escala = models.CharField(
        max_length=30,
        choices=TIPO_ESCALA_CHOICES,
        verbose_name="Tipo de Escala"
    )
    pregunta_numero = models.IntegerField(
        verbose_name="Número de Pregunta",
        help_text="Número de la pregunta dentro de la escala/examen"
    )
    respuesta = models.IntegerField(
        verbose_name="Respuesta",
        help_text="Para autoeficacia: 1-4 (Likert). Para exámenes: 0 (incorrecta) o 1 (correcta)"
    )
    fecha_respuesta = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Respuesta"
    )

    class Meta:
        verbose_name = 'Respuesta de Escala'
        verbose_name_plural = 'Respuestas de Escalas'
        ordering = ['usuario', 'tipo_escala', 'pregunta_numero']
        unique_together = ['usuario', 'tipo_escala', 'pregunta_numero']

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_escala_display()} - Pregunta {self.pregunta_numero}"


class MetricasML(models.Model):
    """
    Métricas de comportamiento del usuario durante las lecciones.
    Se recolectan para AMBOS grupos (Control y Experimental).
    Para Control: solo almacenamiento. Para Experimental: se usan en clasificación ML.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='metricas_ml',
        verbose_name="Usuario"
    )
    leccion = models.ForeignKey(
        'lessons.Leccion',
        on_delete=models.CASCADE,
        related_name='metricas_ml',
        verbose_name="Lección"
    )

    # Métricas de ejercicios
    total_ejercicios = models.IntegerField(
        default=0,
        verbose_name="Total de Ejercicios Vistos"
    )
    ejercicios_correctos_primer_intento = models.IntegerField(
        default=0,
        verbose_name="Ejercicios Correctos al Primer Intento"
    )
    ejercicios_correctos_varios_intentos = models.IntegerField(
        default=0,
        verbose_name="Ejercicios Correctos en Varios Intentos"
    )
    ejercicios_con_ayuda = models.IntegerField(
        default=0,
        verbose_name="Ejercicios con Ayuda Solicitada"
    )

    # Métricas de tiempo
    tiempo_total_segundos = models.IntegerField(
        default=0,
        verbose_name="Tiempo Total (segundos)"
    )
    tiempo_promedio_por_ejercicio = models.FloatField(
        default=0.0,
        verbose_name="Tiempo Promedio por Ejercicio (segundos)"
    )

    # Métricas de interacción
    total_intentos = models.IntegerField(
        default=0,
        verbose_name="Total de Intentos en Todos los Ejercicios"
    )
    veces_retrocedio = models.IntegerField(
        default=0,
        verbose_name="Veces que Retrocedió a Contenido Anterior"
    )

    fecha_inicio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Inicio de Lección"
    )
    fecha_finalizacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Finalización de Lección"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Métrica ML'
        verbose_name_plural = 'Métricas ML'
        ordering = ['usuario', 'leccion__orden']
        unique_together = ['usuario', 'leccion']

    def __str__(self):
        return f"{self.usuario.username} - {self.leccion.titulo}"

    def calcular_tasa_exito(self):
        """Calcula la tasa de éxito en los ejercicios."""
        if self.total_ejercicios == 0:
            return 0.0
        correctos_total = self.ejercicios_correctos_primer_intento + self.ejercicios_correctos_varios_intentos
        return (correctos_total / self.total_ejercicios) * 100

    def calcular_tasa_primer_intento(self):
        """Calcula la tasa de éxito al primer intento."""
        if self.total_ejercicios == 0:
            return 0.0
        return (self.ejercicios_correctos_primer_intento / self.total_ejercicios) * 100


class ClasificacionML(models.Model):
    """
    Almacena las clasificaciones de Machine Learning para el grupo Experimental.
    Se calculan para ambos grupos pero solo se APLICAN al Experimental.
    """
    NIVEL_RENDIMIENTO_CHOICES = [
        ('ALTO', 'Alto Rendimiento'),
        ('MEDIO', 'Rendimiento Medio'),
        ('BAJO', 'Bajo Rendimiento')
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clasificaciones_ml',
        verbose_name="Usuario"
    )
    leccion = models.ForeignKey(
        'lessons.Leccion',
        on_delete=models.CASCADE,
        related_name='clasificaciones_ml',
        verbose_name="Lección Evaluada"
    )
    nivel_rendimiento = models.CharField(
        max_length=20,
        choices=NIVEL_RENDIMIENTO_CHOICES,
        verbose_name="Nivel de Rendimiento Calculado"
    )
    confianza = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        verbose_name="Confianza del Modelo (%)",
        help_text="Porcentaje de confianza de la clasificación"
    )
    caracteristicas_json = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Características Utilizadas",
        help_text="JSON con las características que se usaron para la clasificación"
    )
    fecha_clasificacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Clasificación"
    )

    class Meta:
        verbose_name = 'Clasificación ML'
        verbose_name_plural = 'Clasificaciones ML'
        ordering = ['usuario', 'leccion__orden', '-fecha_clasificacion']

    def __str__(self):
        return f"{self.usuario.username} - {self.leccion.titulo} → {self.get_nivel_rendimiento_display()} ({self.confianza:.1f}%)"


class RespuestaExamenAbierta(models.Model):
    """
    Almacena respuestas abiertas del examen final.
    Permite evaluación automática (similitud de texto) y manual (revisión por admin).
    """
    TIPO_EXAMEN_CHOICES = [
        ('DIAGNOSTICO', 'Examen Diagnóstico'),
        ('FINAL', 'Examen Final'),
    ]

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente de Revisión'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='respuestas_abiertas',
        verbose_name="Usuario"
    )
    tipo_examen = models.CharField(
        max_length=20,
        choices=TIPO_EXAMEN_CHOICES,
        default='FINAL',
        verbose_name="Tipo de Examen"
    )
    pregunta_numero = models.IntegerField(
        verbose_name="Número de Pregunta"
    )
    pregunta_texto = models.TextField(
        verbose_name="Texto de la Pregunta",
        help_text="Se guarda para referencia"
    )
    respuesta_esperada = models.TextField(
        verbose_name="Respuesta Esperada",
        help_text="Respuesta correcta o esperada para comparación"
    )
    respuesta_estudiante = models.TextField(
        verbose_name="Respuesta del Estudiante"
    )

    # Evaluación automática
    similitud_automatica = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        verbose_name="Similitud Automática (%)",
        help_text="Porcentaje de similitud calculado automáticamente"
    )
    aprobada_automatica = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Aprobada Automáticamente",
        help_text="True si similitud >= 70%"
    )

    # Evaluación manual
    estado_revision = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE',
        verbose_name="Estado de Revisión"
    )
    aprobada_manual = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Aprobada Manualmente",
        help_text="Decisión final del administrador"
    )
    feedback_admin = models.TextField(
        blank=True,
        verbose_name="Feedback del Administrador",
        help_text="Comentarios del revisor"
    )
    revisado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='revisiones_realizadas',
        verbose_name="Revisado Por"
    )
    fecha_revision = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Revisión"
    )

    fecha_respuesta = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Respuesta"
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Modificación"
    )

    class Meta:
        verbose_name = 'Respuesta Abierta de Examen'
        verbose_name_plural = 'Respuestas Abiertas de Exámenes'
        ordering = ['usuario', 'tipo_examen', 'pregunta_numero']
        unique_together = ['usuario', 'tipo_examen', 'pregunta_numero']

    def __str__(self):
        estado = "✓" if self.aprobada_final() else "✗" if self.aprobada_final() is False else "?"
        return f"{estado} {self.usuario.username} - {self.get_tipo_examen_display()} - P{self.pregunta_numero}"

    def aprobada_final(self):
        """
        Determina si la respuesta está aprobada (manual tiene prioridad sobre automática).
        """
        if self.aprobada_manual is not None:
            return self.aprobada_manual
        return self.aprobada_automatica

    def requiere_revision_manual(self):
        """
        Verifica si la respuesta requiere revisión manual.
        """
        return self.estado_revision == 'PENDIENTE' and self.aprobada_manual is None
