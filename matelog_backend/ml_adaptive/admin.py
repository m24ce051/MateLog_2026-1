# ml_adaptive/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import CodigoAcceso, PerfilUsuario, RespuestaEscala, MetricasML, ClasificacionML, RespuestaExamenAbierta


@admin.register(CodigoAcceso)
class CodigoAccesoAdmin(admin.ModelAdmin):
    list_display = ['codigo_display', 'grupo_display', 'activo_display', 'fecha_creacion']
    list_filter = ['grupo', 'activo']
    search_fields = ['codigo', 'descripcion']
    ordering = ['grupo', 'codigo']

    fieldsets = [
        ('Información del Código', {
            'fields': ['codigo', 'grupo', 'activo']
        }),
        ('Descripción', {
            'fields': ['descripcion']
        }),
        ('Metadatos', {
            'fields': ['fecha_creacion', 'fecha_modificacion'],
            'classes': ['collapse']
        })
    ]

    readonly_fields = ['fecha_creacion', 'fecha_modificacion']

    def codigo_display(self, obj):
        """Muestra el código con ícono de estado."""
        status = "✓" if obj.activo else "✗"
        color = "#28a745" if obj.activo else "#dc3545"
        return format_html(
            '<span style="color: {};">{}</span> <strong>{}</strong>',
            color, status, obj.codigo
        )
    codigo_display.short_description = 'Código'

    def grupo_display(self, obj):
        """Muestra el grupo con color."""
        color = "#007bff" if obj.grupo == 'CONTROL' else "#ff6b6b"
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_grupo_display()
        )
    grupo_display.short_description = 'Grupo'

    def activo_display(self, obj):
        """Muestra el estado activo con ícono."""
        if obj.activo:
            return format_html('<span style="color: #28a745;">● Activo</span>')
        return format_html('<span style="color: #dc3545;">● Inactivo</span>')
    activo_display.short_description = 'Estado'


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'username_display',
        'grupo_display',
        'clasificacion_autoeficacia_display',
        'codigo_usado',
        'completitud_display',
        'fecha_registro'
    ]
    list_filter = ['grupo', 'clasificacion_autoeficacia', 'completo_autoeficacia_pre', 'completo_diagnostico']
    search_fields = ['user__username', 'user__email', 'codigo_usado']
    ordering = ['grupo', 'user__username']

    fieldsets = [
        ('Usuario', {
            'fields': ['user']
        }),
        ('Información de Grupo', {
            'fields': ['grupo', 'codigo_usado', 'clasificacion_autoeficacia']
        }),
        ('Estado de Evaluaciones', {
            'fields': [
                'completo_autoeficacia_pre',
                'completo_diagnostico',
                'completo_autoeficacia_post',
                'completo_final'
            ]
        }),
        ('Metadatos', {
            'fields': ['fecha_registro', 'fecha_modificacion'],
            'classes': ['collapse']
        })
    ]

    readonly_fields = ['fecha_registro', 'fecha_modificacion']

    def username_display(self, obj):
        """Muestra el nombre de usuario."""
        return obj.user.username
    username_display.short_description = 'Usuario'
    username_display.admin_order_field = 'user__username'

    def grupo_display(self, obj):
        """Muestra el grupo con color."""
        color = "#007bff" if obj.grupo == 'CONTROL' else "#ff6b6b"
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_grupo_display()
        )
    grupo_display.short_description = 'Grupo'
    grupo_display.admin_order_field = 'grupo'

    def clasificacion_autoeficacia_display(self, obj):
        """Muestra la clasificación de autoeficacia con colores."""
        if not obj.clasificacion_autoeficacia:
            return format_html('<span style="color: #6c757d;">Sin clasificar</span>')

        colors = {
            'ALTO': '#28a745',
            'MEDIO': '#ffc107',
            'BAJO': '#dc3545'
        }
        color = colors.get(obj.clasificacion_autoeficacia, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_clasificacion_autoeficacia_display()
        )
    clasificacion_autoeficacia_display.short_description = 'Autoeficacia'
    clasificacion_autoeficacia_display.admin_order_field = 'clasificacion_autoeficacia'

    def completitud_display(self, obj):
        """Muestra el estado de completitud de evaluaciones."""
        checks = [
            obj.completo_autoeficacia_pre,
            obj.completo_diagnostico,
            obj.completo_autoeficacia_post,
            obj.completo_final
        ]
        total = sum(checks)
        color = '#28a745' if total == 4 else '#ffc107' if total > 0 else '#dc3545'
        return format_html(
            '<span style="color: {};">{}/4 evaluaciones</span>',
            color, total
        )
    completitud_display.short_description = 'Completitud'


@admin.register(RespuestaEscala)
class RespuestaEscalaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo_escala', 'pregunta_numero', 'respuesta', 'fecha_respuesta']
    list_filter = ['tipo_escala', 'usuario']
    search_fields = ['usuario__username']
    ordering = ['usuario', 'tipo_escala', 'pregunta_numero']

    readonly_fields = ['fecha_respuesta']

    def has_add_permission(self, request):
        """Las respuestas se crean desde el frontend, no desde admin."""
        return False


@admin.register(MetricasML)
class MetricasMLAdmin(admin.ModelAdmin):
    list_display = [
        'usuario',
        'leccion',
        'tasa_exito_display',
        'tasa_primer_intento_display',
        'total_ejercicios',
        'tiempo_total_display',
        'fecha_finalizacion'
    ]
    list_filter = ['leccion', 'usuario__perfil__grupo']
    search_fields = ['usuario__username', 'leccion__titulo']
    ordering = ['usuario', 'leccion__orden']

    fieldsets = [
        ('Identificación', {
            'fields': ['usuario', 'leccion']
        }),
        ('Métricas de Ejercicios', {
            'fields': [
                'total_ejercicios',
                'ejercicios_correctos_primer_intento',
                'ejercicios_correctos_varios_intentos',
                'ejercicios_con_ayuda'
            ]
        }),
        ('Métricas de Tiempo', {
            'fields': [
                'tiempo_total_segundos',
                'tiempo_promedio_por_ejercicio'
            ]
        }),
        ('Métricas de Interacción', {
            'fields': [
                'total_intentos',
                'veces_retrocedio'
            ]
        }),
        ('Fechas', {
            'fields': [
                'fecha_inicio',
                'fecha_finalizacion',
                'fecha_creacion',
                'fecha_modificacion'
            ],
            'classes': ['collapse']
        })
    ]

    readonly_fields = ['fecha_creacion', 'fecha_modificacion']

    def tasa_exito_display(self, obj):
        """Muestra la tasa de éxito con color."""
        tasa = obj.calcular_tasa_exito()
        if tasa >= 80:
            color = '#28a745'
        elif tasa >= 60:
            color = '#ffc107'
        else:
            color = '#dc3545'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, tasa
        )
    tasa_exito_display.short_description = 'Tasa de Éxito'

    def tasa_primer_intento_display(self, obj):
        """Muestra la tasa de éxito al primer intento."""
        tasa = obj.calcular_tasa_primer_intento()
        if tasa >= 70:
            color = '#28a745'
        elif tasa >= 50:
            color = '#ffc107'
        else:
            color = '#dc3545'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, tasa
        )
    tasa_primer_intento_display.short_description = '1er Intento'

    def tiempo_total_display(self, obj):
        """Muestra el tiempo total en formato legible."""
        minutos = obj.tiempo_total_segundos // 60
        segundos = obj.tiempo_total_segundos % 60
        return f"{minutos}m {segundos}s"
    tiempo_total_display.short_description = 'Tiempo Total'

    def has_add_permission(self, request):
        """Las métricas se crean automáticamente desde el frontend."""
        return False


@admin.register(ClasificacionML)
class ClasificacionMLAdmin(admin.ModelAdmin):
    list_display = [
        'usuario',
        'leccion',
        'nivel_rendimiento_display',
        'confianza_display',
        'fecha_clasificacion'
    ]
    list_filter = ['nivel_rendimiento', 'leccion']
    search_fields = ['usuario__username', 'leccion__titulo']
    ordering = ['usuario', 'leccion__orden', '-fecha_clasificacion']

    fieldsets = [
        ('Identificación', {
            'fields': ['usuario', 'leccion']
        }),
        ('Clasificación', {
            'fields': ['nivel_rendimiento', 'confianza']
        }),
        ('Detalles Técnicos', {
            'fields': ['caracteristicas_json'],
            'classes': ['collapse']
        }),
        ('Metadatos', {
            'fields': ['fecha_clasificacion'],
            'classes': ['collapse']
        })
    ]

    readonly_fields = ['fecha_clasificacion']

    def nivel_rendimiento_display(self, obj):
        """Muestra el nivel de rendimiento con colores."""
        colors = {
            'ALTO': '#28a745',
            'MEDIO': '#ffc107',
            'BAJO': '#dc3545'
        }
        color = colors.get(obj.nivel_rendimiento, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_nivel_rendimiento_display()
        )
    nivel_rendimiento_display.short_description = 'Nivel de Rendimiento'
    nivel_rendimiento_display.admin_order_field = 'nivel_rendimiento'

    def confianza_display(self, obj):
        """Muestra la confianza con barra de progreso visual."""
        color = '#28a745' if obj.confianza >= 80 else '#ffc107' if obj.confianza >= 60 else '#dc3545'
        return format_html(
            '<div style="width: 100px; background: #e9ecef; border-radius: 3px;">'
            '<div style="width: {}%; background: {}; color: white; text-align: center; '
            'padding: 2px 0; border-radius: 3px; font-size: 11px;">{:.1f}%</div></div>',
            obj.confianza, color, obj.confianza
        )
    confianza_display.short_description = 'Confianza'
    confianza_display.admin_order_field = 'confianza'

    def has_add_permission(self, request):
        """Las clasificaciones se generan automáticamente por el modelo ML."""
        return False


@admin.register(RespuestaExamenAbierta)
class RespuestaExamenAbiertaAdmin(admin.ModelAdmin):
    list_display = [
        'status_display',
        'usuario',
        'tipo_examen',
        'pregunta_numero',
        'similitud_display',
        'estado_revision_display',
        'fecha_respuesta'
    ]
    list_filter = ['tipo_examen', 'estado_revision', 'aprobada_automatica', 'aprobada_manual']
    search_fields = ['usuario__username', 'pregunta_texto', 'respuesta_estudiante']
    ordering = ['estado_revision', 'tipo_examen', 'usuario', 'pregunta_numero']

    fieldsets = [
        ('Identificación', {
            'fields': ['usuario', 'tipo_examen', 'pregunta_numero']
        }),
        ('Pregunta y Respuestas', {
            'fields': [
                'pregunta_texto',
                'respuesta_esperada',
                'respuesta_estudiante'
            ]
        }),
        ('Evaluación Automática', {
            'fields': [
                'similitud_automatica',
                'aprobada_automatica'
            ],
            'classes': ['collapse']
        }),
        ('Revisión Manual', {
            'fields': [
                'estado_revision',
                'aprobada_manual',
                'feedback_admin',
                'revisado_por',
                'fecha_revision'
            ]
        }),
        ('Metadatos', {
            'fields': [
                'fecha_respuesta',
                'fecha_modificacion'
            ],
            'classes': ['collapse']
        })
    ]

    readonly_fields = [
        'usuario',
        'tipo_examen',
        'pregunta_numero',
        'pregunta_texto',
        'respuesta_esperada',
        'respuesta_estudiante',
        'similitud_automatica',
        'aprobada_automatica',
        'fecha_respuesta',
        'fecha_modificacion'
    ]

    actions = ['aprobar_respuestas', 'rechazar_respuestas', 'marcar_pendiente']

    def status_display(self, obj):
        """Muestra el estado general con ícono."""
        if obj.aprobada_manual is True:
            return format_html('<span style="color: #28a745; font-size: 16px;">✓</span>')
        elif obj.aprobada_manual is False:
            return format_html('<span style="color: #dc3545; font-size: 16px;">✗</span>')
        elif obj.aprobada_automatica is True:
            return format_html('<span style="color: #ffc107; font-size: 16px;">◐</span>')
        elif obj.aprobada_automatica is False:
            return format_html('<span style="color: #fd7e14; font-size: 16px;">◑</span>')
        return format_html('<span style="color: #6c757d; font-size: 16px;">?</span>')
    status_display.short_description = '●'

    def similitud_display(self, obj):
        """Muestra la similitud automática con barra de progreso."""
        if obj.similitud_automatica is None:
            return format_html('<span style="color: #6c757d;">Sin evaluar</span>')

        if obj.similitud_automatica >= 70:
            color = '#28a745'
        elif obj.similitud_automatica >= 50:
            color = '#ffc107'
        else:
            color = '#dc3545'

        return format_html(
            '<div style="width: 100px; background: #e9ecef; border-radius: 3px;">'
            '<div style="width: {}%; background: {}; color: white; text-align: center; '
            'padding: 2px 0; border-radius: 3px; font-size: 11px;">{:.0f}%</div></div>',
            obj.similitud_automatica, color, obj.similitud_automatica
        )
    similitud_display.short_description = 'Similitud Auto'

    def estado_revision_display(self, obj):
        """Muestra el estado de revisión con colores."""
        colors = {
            'PENDIENTE': '#ffc107',
            'APROBADA': '#28a745',
            'RECHAZADA': '#dc3545'
        }
        color = colors.get(obj.estado_revision, '#6c757d')

        # Indicar si hay revisión manual
        if obj.aprobada_manual is not None:
            icon = '👤'  # Revisión manual
        elif obj.aprobada_automatica is not None:
            icon = '🤖'  # Solo automática
        else:
            icon = '⏳'  # Sin evaluar

        return format_html(
            '{} <span style="color: {}; font-weight: bold;">{}</span>',
            icon, color, obj.get_estado_revision_display()
        )
    estado_revision_display.short_description = 'Estado'

    def aprobar_respuestas(self, request, queryset):
        """Aprueba manualmente las respuestas seleccionadas."""
        updated = 0
        for respuesta in queryset:
            respuesta.aprobada_manual = True
            respuesta.estado_revision = 'APROBADA'
            respuesta.revisado_por = request.user
            respuesta.fecha_revision = timezone.now()
            respuesta.save()
            updated += 1

        self.message_user(request, f'{updated} respuesta(s) aprobada(s) exitosamente.')
    aprobar_respuestas.short_description = '✓ Aprobar respuestas seleccionadas'

    def rechazar_respuestas(self, request, queryset):
        """Rechaza manualmente las respuestas seleccionadas."""
        updated = 0
        for respuesta in queryset:
            respuesta.aprobada_manual = False
            respuesta.estado_revision = 'RECHAZADA'
            respuesta.revisado_por = request.user
            respuesta.fecha_revision = timezone.now()
            respuesta.save()
            updated += 1

        self.message_user(request, f'{updated} respuesta(s) rechazada(s).')
    rechazar_respuestas.short_description = '✗ Rechazar respuestas seleccionadas'

    def marcar_pendiente(self, request, queryset):
        """Marca las respuestas como pendientes de revisión."""
        updated = queryset.update(
            estado_revision='PENDIENTE',
            aprobada_manual=None,
            revisado_por=None,
            fecha_revision=None
        )
        self.message_user(request, f'{updated} respuesta(s) marcada(s) como pendiente.')
    marcar_pendiente.short_description = '⏳ Marcar como pendiente'

    def save_model(self, request, obj, form, change):
        """Al guardar una respuesta revisada manualmente, actualizar campos."""
        if change and obj.aprobada_manual is not None:
            obj.revisado_por = request.user
            if obj.fecha_revision is None:
                obj.fecha_revision = timezone.now()

            if obj.aprobada_manual:
                obj.estado_revision = 'APROBADA'
            else:
                obj.estado_revision = 'RECHAZADA'

        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        """Las respuestas se crean desde el frontend."""
        return False
