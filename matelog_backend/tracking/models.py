# tracking/models.py
# ACTUALIZACIÓN: Agregar estos campos al modelo ActividadPantalla existente


from django.db import models
from django.conf import settings
from lessons.models import Leccion, Tema, Ejercicio, ContenidoTema


class SesionEstudio(models.Model):
    """
    Modelo para registrar las sesiones de estudio de los usuarios.
    Una sesión abarca desde que el usuario inicia sesión hasta que cierra.
    Detecta cierre por: logout explícito, cierre de ventana, o 5 min de inactividad.
    """
    TIPO_CIERRE_CHOICES = [
        ('LOGOUT', 'Logout Explícito'),
        ('INACTIVIDAD', 'Inactividad (5 min)'),
        ('CIERRE_VENTANA', 'Cierre de Ventana/Pestaña'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sesiones'
    )
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    duracion_minutos = models.IntegerField(
        default=0,
        help_text="Duración total de la sesión en minutos (DEPRECATED, usar duracion_segundos)"
    )
    duracion_segundos = models.PositiveIntegerField(
        default=0,
        help_text="Duración total de la sesión en segundos"
    )
    tipo_cierre = models.CharField(
        max_length=20,
        choices=TIPO_CIERRE_CHOICES,
        null=True,
        blank=True,
        help_text="Tipo de cierre de la sesión"
    )
    ultima_actividad = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Última actividad registrada en la sesión"
    )

    class Meta:
        verbose_name = 'Sesión de Estudio'
        verbose_name_plural = 'Sesiones de Estudio'
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['usuario', 'fecha_inicio']),
            models.Index(fields=['usuario', 'tipo_cierre']),
            models.Index(fields=['fecha_inicio']),
        ]

    def __str__(self):
        duracion_str = f"{self.duracion_segundos}s" if self.duracion_segundos else f"{self.duracion_minutos}min"
        return f"{self.usuario.username} - {self.fecha_inicio.strftime('%Y-%m-%d %H:%M')} - {duracion_str}"








class ProgresoLeccion(models.Model):
    """
    Modelo para registrar el progreso del usuario en cada lección.
    """
    ESTADO_CHOICES = [
        ('SIN_INICIAR', 'Sin Iniciar'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADA', 'Completada'),
    ]




    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progreso_lecciones'
    )
    leccion = models.ForeignKey(
        Leccion,
        on_delete=models.CASCADE,
        related_name='progreso_usuarios'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='SIN_INICIAR'
    )
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    porcentaje_completado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Porcentaje de temas completados en la lección"
    )




    class Meta:
        verbose_name = 'Progreso de Lección'
        verbose_name_plural = 'Progreso de Lecciones'
        unique_together = ['usuario', 'leccion']
        ordering = ['leccion__orden']




    def __str__(self):
        return f"{self.usuario.username} - {self.leccion.titulo} ({self.estado})"








class ProgresoTema(models.Model):
    """
    Modelo para registrar el progreso del usuario en cada tema.
    """
    ESTADO_CHOICES = [
        ('SIN_INICIAR', 'Sin Iniciar'),
        ('INICIADO', 'Iniciado'),
        ('COMPLETADO', 'Completado'),
    ]




    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progreso_temas'
    )
    tema = models.ForeignKey(
        Tema,
        on_delete=models.CASCADE,
        related_name='progreso_usuarios'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='SIN_INICIAR'
    )
    desbloqueado = models.BooleanField(
        default=False,
        help_text="Indica si el tema está desbloqueado para el usuario"
    )
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    porcentaje_acierto = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Porcentaje de aciertos en los ejercicios del tema"
    )
    intentos_realizados = models.PositiveIntegerField(
        default=0,
        help_text="Número de veces que el usuario ha intentado completar este tema"
    )

    contenidos_vistos = models.ManyToManyField(
        'lessons.ContenidoTema',
        blank=True,
        related_name='visto_por',
        help_text='Contenidos que el usuario ha visto (excluyendo EJEMPLO_EXTRA)'
    )

    
    # NUEVOS CAMPOS: Tracking agregado
    tiempo_total_teoria_segundos = models.IntegerField(
        default=0,
        help_text="Tiempo total en segundos viendo contenido de teoría"
    )
    tiempo_total_ejemplos_segundos = models.IntegerField(
        default=0,
        help_text="Tiempo total en segundos viendo contenido de ejemplos"
    )
    clics_ver_otro_ejemplo = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad de veces que hizo clic en 'Ver otro ejemplo'"
    )
    clics_regresar = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad de veces que hizo clic en 'Regresar' en el contenido"
    )
    clics_volver_tema = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad de veces que hizo clic en 'Volver al tema' desde ejercicios"
    )
    clics_ir_ejercicios = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad de veces que hizo clic en 'Ir a ejercicios'"
    )
    clics_ayuda = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad de veces que hizo clic en 'Ver Ayuda'"
    )


    class Meta:
        verbose_name = 'Progreso de Tema'
        verbose_name_plural = 'Progreso de Temas'
        unique_together = ['usuario', 'tema']
        ordering = ['tema__orden']




    def __str__(self):
        return f"{self.usuario.username} - {self.tema.titulo} ({self.estado})"


    def calcular_progreso_contenido(self):
        """
        Calcula el porcentaje de contenido completado.
        NO cuenta EJEMPLO_EXTRA.
        """
        # Total de contenidos (sin EJEMPLO_EXTRA)
        contenidos_totales = self.tema.contenidos.exclude(
            tipo='EJEMPLO_EXTRA'
        ).count()
       
        if contenidos_totales == 0:
            return 0
       
        # Contenidos vistos (sin EJEMPLO_EXTRA)
        contenidos_vistos_count = self.contenidos_vistos.exclude(
            tipo='EJEMPLO_EXTRA'
        ).count()
       
        return (contenidos_vistos_count / contenidos_totales) * 100
   
    @property
    def contenido_completado(self):
        """Número de contenidos vistos (sin EJEMPLO_EXTRA)"""
        return self.contenidos_vistos.exclude(tipo='EJEMPLO_EXTRA').count()
   
    @property
    def contenidos_count(self):
        """Total de contenidos (sin EJEMPLO_EXTRA)"""
        return self.tema.contenidos.exclude(tipo='EJEMPLO_EXTRA').count()




class RespuestaEjercicio(models.Model):
    """
    Modelo para registrar las respuestas de los usuarios a los ejercicios.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )
    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.CASCADE,
        related_name='respuestas_usuarios'
    )
    progreso_tema = models.ForeignKey(
        ProgresoTema,
        on_delete=models.CASCADE,
        related_name='respuestas',
        null=True,
        blank=True
    )
    respuesta_usuario = models.TextField(help_text="Respuesta proporcionada por el usuario")
    es_correcta = models.BooleanField(help_text="Indica si la respuesta fue correcta")
    uso_ayuda = models.BooleanField(
        default=False,
        help_text="Indica si el usuario vio la ayuda antes de responder"
    )
    tiempo_respuesta_segundos = models.IntegerField(
        default=0,
        help_text="Tiempo que tardó el usuario en responder (en segundos)"
    )
    fecha_respuesta = models.DateTimeField(auto_now_add=True)




    class Meta:
        verbose_name = 'Respuesta de Ejercicio'
        verbose_name_plural = 'Respuestas de Ejercicios'
        ordering = ['-fecha_respuesta']
        indexes = [
            models.Index(fields=['usuario', 'ejercicio']),
            models.Index(fields=['progreso_tema', 'es_correcta']),
            models.Index(fields=['fecha_respuesta']),
        ]




    def __str__(self):
        return f"{self.usuario.username} - {self.ejercicio.enunciado[:50]} - {'Correcta' if self.es_correcta else 'Incorrecta'}"




class ActividadPantalla(models.Model):
    """
    Modelo para registrar el tiempo que el usuario pasa en cada pantalla.
    """
    TIPO_PANTALLA_CHOICES = [
        ('LOGIN', 'Login'),
        ('REGISTRO', 'Registro'),
        ('LISTA_LECCIONES', 'Lista de Lecciones'),
        ('DETALLE_LECCION', 'Detalle de Lección'),
        ('CONTENIDO_TEMA', 'Contenido del Tema'),
        ('EJERCICIOS', 'Ejercicios'),
        ('OTRA', 'Otra'),
    ]


    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actividades_pantalla',
        null=True,
        blank=True
    )
    tipo_pantalla = models.CharField(
        max_length=30,
        choices=TIPO_PANTALLA_CHOICES
    )
    tiempo_inicio = models.DateTimeField(auto_now_add=True)
    tiempo_fin = models.DateTimeField(null=True, blank=True)
    tiempo_segundos = models.IntegerField(
        default=0,
        help_text="Tiempo total en la pantalla en segundos"
    )
   
    # Metadatos adicionales
    leccion_id = models.IntegerField(null=True, blank=True)
    tema_id = models.IntegerField(null=True, blank=True)
   
    # Tracking de navegación
    veces_volver_contenido = models.PositiveIntegerField(
        default=0,
        help_text="Número de veces que presionó el botón 'Volver' en el contenido del tema"
    )
   
    # NUEVOS CAMPOS: Tracking de acciones adicionales
    veces_ver_ejemplo_extra = models.PositiveIntegerField(
        default=0,
        help_text="Número de veces que presionó 'Ver Otro Ejemplo'"
    )
   
    veces_ir_a_ejercicios = models.PositiveIntegerField(
        default=0,
        help_text="Número de veces que fue directo a ejercicios desde el contenido"
    )


    class Meta:
        verbose_name = 'Actividad de Pantalla'
        verbose_name_plural = 'Actividades de Pantalla'
        ordering = ['-tiempo_inicio']
        indexes = [
            models.Index(fields=['usuario', 'tipo_pantalla']),
            models.Index(fields=['tiempo_inicio']),
            models.Index(fields=['leccion_id', 'tema_id']),
        ]


    def __str__(self):
        usuario_str = self.usuario.username if self.usuario else "Anónimo"
        return f"{usuario_str} - {self.tipo_pantalla} - {self.tiempo_segundos}s"


   
# Modificación 7: Nuevo modelo para tracking de reintentos
class IntentoTema(models.Model):
    """
    Modelo para registrar cada intento que hace un usuario en un tema.
    Permite analizar el progreso y mejora del estudiante en reintentos.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='intentos_temas'
    )
    tema = models.ForeignKey(
        Tema,
        on_delete=models.CASCADE,
        related_name='intentos'
    )
    progreso_tema = models.ForeignKey(
        ProgresoTema,
        on_delete=models.CASCADE,
        related_name='intentos',
        help_text="Relación con el progreso general del tema"
    )
    numero_intento = models.PositiveIntegerField(
        help_text="Número de intento (1, 2, 3, ...)"
    )
   
    # Resultados del intento
    ejercicios_correctos = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad de ejercicios respondidos correctamente"
    )
    ejercicios_incorrectos = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad de ejercicios respondidos incorrectamente"
    )
    ejercicios_totales = models.PositiveIntegerField(
        help_text="Total de ejercicios del tema"
    )
    porcentaje_acierto = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Porcentaje de aciertos en este intento"
    )
   
    # Uso de ayuda
    ejercicios_con_ayuda = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad de ejercicios donde usó la ayuda"
    )
   
    # Tiempos
    tiempo_total_segundos = models.IntegerField(
        default=0,
        help_text="Tiempo total invertido en este intento"
    )
    tiempo_promedio_por_ejercicio = models.IntegerField(
        default=0,
        help_text="Tiempo promedio por ejercicio en segundos"
    )
   
    # Resultado final
    aprobado = models.BooleanField(
        default=False,
        help_text="Indica si alcanzó el 80% requerido para aprobar"
    )
   
    # Fechas
    fecha_inicio = models.DateTimeField(
        help_text="Fecha y hora en que comenzó el intento"
    )
    fecha_finalizacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que finalizó el intento"
    )
   
    # Mejora respecto al intento anterior
    mejora_porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Mejora en porcentaje respecto al intento anterior"
    )




    class Meta:
        verbose_name = 'Intento de Tema'
        verbose_name_plural = 'Intentos de Temas'
        ordering = ['-fecha_finalizacion']
        unique_together = ['usuario', 'tema', 'numero_intento']
        indexes = [
            models.Index(fields=['usuario', 'tema', 'aprobado']),
            models.Index(fields=['fecha_finalizacion']),
            models.Index(fields=['tema', 'aprobado']),
        ]




    def __str__(self):
        return f"{self.usuario.username} - {self.tema.titulo} - Intento {self.numero_intento} ({self.porcentaje_acierto}%)"
   
    def calcular_mejora(self):
        """
        Calcula la mejora respecto al intento anterior.
        """
        if self.numero_intento > 1:
            intento_anterior = IntentoTema.objects.filter(
                usuario=self.usuario,
                tema=self.tema,
                numero_intento=self.numero_intento - 1
            ).first()
           
            if intento_anterior:
                self.mejora_porcentaje = self.porcentaje_acierto - intento_anterior.porcentaje_acierto
            else:
                self.mejora_porcentaje = 0
        else:
            self.mejora_porcentaje = 0

class EventoTracking(models.Model):
    """
    Modelo para registrar eventos individuales de tracking.
    Permite análisis detallado de la actividad del usuario.
    """
    TIPO_EVENTO_CHOICES = [
        ('TEORIA_VISTA', 'Teoría Vista'),
        ('EJEMPLO_VISTO', 'Ejemplo Visto'),
        ('EJERCICIO_VISTO', 'Ejercicio Visto'),
        ('CLIC_VER_OTRO_EJEMPLO', 'Clic Ver Otro Ejemplo'),
        ('CLIC_REGRESAR', 'Clic Regresar'),
        ('CLIC_VOLVER_TEMA', 'Clic Volver al Tema'),
        ('CLIC_IR_EJERCICIOS', 'Clic Ir a Ejercicios'),
        ('CLIC_AYUDA', 'Clic Ver Ayuda'),
        ('CAMBIO_PESTANA', 'Cambio de Pestaña'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eventos_tracking'
    )
    tema = models.ForeignKey(
        Tema,
        on_delete=models.CASCADE,
        related_name='eventos_tracking'
    )
    tipo_evento = models.CharField(
        max_length=30,
        choices=TIPO_EVENTO_CHOICES,
        help_text="Tipo de evento registrado"
    )
    
    # Campos opcionales según el tipo de evento
    contenido_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ID del ContenidoTema si aplica"
    )
    ejercicio_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ID del Ejercicio si aplica"
    )
    numero_intento = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Número de intento para ejercicios"
    )
    
    # Tiempo y cambio de pestaña
    tiempo_segundos = models.IntegerField(
        null=True,
        blank=True,
        help_text="Tiempo en segundos (null si hubo cambio de pestaña)"
    )
    cambio_pestana = models.BooleanField(
        default=False,
        help_text="Indica si el usuario cambió de pestaña durante este evento"
    )
    
    # Timestamp
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora del evento"
    )
    
    class Meta:
        verbose_name = 'Evento de Tracking'
        verbose_name_plural = 'Eventos de Tracking'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['usuario', 'tema']),
            models.Index(fields=['tipo_evento']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.usuario.username} - {self.tema.titulo} - {self.get_tipo_evento_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


# ==================== NUEVOS MODELOS DE TRACKING ====================

class TiempoPantalla(models.Model):
    """
    Modelo para registrar eventos individuales de tiempo en pantallas específicas.
    Cada registro representa UNA VISITA a un contenido específico.
    Reemplaza a ActividadPantalla para tracking específico de Teoría/Ejemplo/Ejercicio.
    """
    TIPO_CONTENIDO_CHOICES = [
        ('TEORIA', 'Teoría'),
        ('EJEMPLO', 'Ejemplo'),
        ('EJERCICIO', 'Ejercicio'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tiempos_pantalla'
    )
    tema = models.ForeignKey(
        Tema,
        on_delete=models.CASCADE,
        related_name='tiempos_pantalla'
    )
    contenido = models.ForeignKey(
        ContenidoTema,
        on_delete=models.CASCADE,
        related_name='tiempos_registrados',
        null=True,
        blank=True,
        help_text="Referencia al contenido específico (Teoría o Ejemplo)"
    )
    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.CASCADE,
        related_name='tiempos_registrados',
        null=True,
        blank=True,
        help_text="Referencia al ejercicio específico"
    )
    tipo_contenido = models.CharField(
        max_length=20,
        choices=TIPO_CONTENIDO_CHOICES,
        help_text="Tipo de contenido (Teoría, Ejemplo, Ejercicio)"
    )
    numero = models.PositiveIntegerField(
        help_text="Número del contenido dentro del tema (1, 2, 3...)"
    )
    tiempo_segundos = models.PositiveIntegerField(
        help_text="Tiempo en segundos que pasó en esta pantalla"
    )
    cambio_pestana = models.BooleanField(
        default=False,
        help_text="Indica si el usuario cambió de pestaña durante esta visita"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora del registro"
    )

    class Meta:
        verbose_name = 'Tiempo en Pantalla'
        verbose_name_plural = 'Tiempos en Pantalla'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['usuario', 'tema']),
            models.Index(fields=['tipo_contenido']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        nombre_contenido = self.nombre_completo
        return f"{self.usuario.username} - {self.tema.titulo} - {nombre_contenido} - {self.tiempo_segundos}s"

    @property
    def nombre_completo(self):
        """Retorna el nombre completo del contenido: 'Teoría 1', 'Ejemplo 2', etc."""
        tipo_display = self.get_tipo_contenido_display()
        return f"{tipo_display} {self.numero}"


class ClicBoton(models.Model):
    """
    Modelo para registrar clics en botones específicos.
    Cada registro representa UN CLIC en un botón.
    Solo registra los 5 botones específicos requeridos.
    """
    TIPO_BOTON_CHOICES = [
        ('REGRESAR', 'Regresar'),
        ('IR_EJERCICIOS', 'Ir a ejercicios'),
        ('VOLVER', 'Volver'),
        ('OTRO_EJEMPLO', 'Otro ejemplo'),
        ('VER_AYUDA', 'Ver Ayuda'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clics_botones'
    )
    tema = models.ForeignKey(
        Tema,
        on_delete=models.CASCADE,
        related_name='clics_botones',
        null=True,
        blank=True,
        help_text="Tema relacionado (null si es navegación global)"
    )
    tipo_boton = models.CharField(
        max_length=20,
        choices=TIPO_BOTON_CHOICES,
        help_text="Tipo de botón clickeado"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora del clic"
    )

    class Meta:
        verbose_name = 'Clic en Botón'
        verbose_name_plural = 'Clics en Botones'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['usuario', 'tema']),
            models.Index(fields=['tipo_boton']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        tema_str = self.tema.titulo if self.tema else "Global"
        return f"{self.usuario.username} - {tema_str} - {self.get_tipo_boton_display()}"

