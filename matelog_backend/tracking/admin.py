# tracking/admin.py
# Sistema de tracking mejorado


from django.contrib import admin
from .models import (
    SesionEstudio,
    ProgresoLeccion,
    ProgresoTema,
    RespuestaEjercicio,
    # ActividadPantalla,  # ELIMINADO - Ya no se usa en admin
    IntentoTema,
    TiempoPantalla,  # NUEVO
    ClicBoton,       # NUEVO
)


@admin.register(SesionEstudio)
class SesionEstudioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_inicio', 'fecha_fin', 'duracion_display', 'tipo_cierre')
    list_filter = ('fecha_inicio', 'tipo_cierre', 'usuario')
    search_fields = ('usuario__username',)
    readonly_fields = ('fecha_inicio', 'fecha_fin')
    ordering = ('-fecha_inicio',)

    fieldsets = (
        ('Información General', {
            'fields': ('usuario', 'fecha_inicio', 'fecha_fin')
        }),
        ('Duración', {
            'fields': ('duracion_segundos', 'duracion_minutos')
        }),
        ('Cierre de Sesión', {
            'fields': ('tipo_cierre', 'ultima_actividad')
        }),
    )

    def duracion_display(self, obj):
        """Muestra la duración en formato legible"""
        if obj.duracion_segundos:
            mins = obj.duracion_segundos // 60
            secs = obj.duracion_segundos % 60
            return f"{mins}m {secs}s"
        elif obj.duracion_minutos:
            return f"{obj.duracion_minutos}m"
        return "0m"
    duracion_display.short_description = 'Duración'

    # Acciones personalizadas
    actions = ['exportar_sesiones_csv']

    def exportar_sesiones_csv(self, request, queryset):
        """
        Exporta las sesiones de estudio seleccionadas a CSV.
        Formato ACUMULATIVO: Una fila por sesión completa.
        """
        import csv
        from django.http import HttpResponse
        from datetime import datetime

        # Advertencia si hay muchos registros
        total_registros = queryset.count()
        if total_registros > 10000:
            self.message_user(
                request,
                f"⚠️ Tienes {total_registros} sesiones seleccionadas. "
                f"La exportación puede tardar 15-30 segundos. "
                f"Considera usar filtros para reducir la cantidad.",
                level='warning'
            )

        # Configurar respuesta HTTP
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="sesiones_estudio_{timestamp}.csv"'

        # UTF-8 BOM para que Excel reconozca correctamente los caracteres especiales
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow([
            'Usuario',
            'Fecha Inicio',
            'Fecha Fin',
            'Duración (segundos)',
            'Duración (minutos)',
            'Tipo Cierre',
            'Última Actividad'
        ])

        # Optimización: select_related para reducir consultas a la BD
        queryset_optimizado = queryset.select_related('usuario')

        # Exportar datos
        for sesion in queryset_optimizado:
            writer.writerow([
                sesion.usuario.username,
                sesion.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S') if sesion.fecha_inicio else '',
                sesion.fecha_fin.strftime('%Y-%m-%d %H:%M:%S') if sesion.fecha_fin else '',
                sesion.duracion_segundos,
                sesion.duracion_minutos,
                sesion.get_tipo_cierre_display() if sesion.tipo_cierre else '',
                sesion.ultima_actividad.strftime('%Y-%m-%d %H:%M:%S') if sesion.ultima_actividad else ''
            ])

        self.message_user(request, f'✅ Se exportaron {total_registros} sesiones correctamente.')
        return response

    exportar_sesiones_csv.short_description = "📊 Exportar sesiones seleccionadas a CSV"








@admin.register(ProgresoLeccion)
class ProgresoLeccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'leccion', 'estado', 'porcentaje_completado', 'fecha_inicio', 'fecha_completado')
    list_filter = ('estado', 'leccion', 'fecha_inicio')
    search_fields = ('usuario__username', 'leccion__titulo')
    readonly_fields = ('fecha_inicio', 'fecha_completado')
    ordering = ('leccion__orden', 'usuario')








@admin.register(ProgresoTema)
class ProgresoTemaAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'tema',
        'estado',
        'desbloqueado',
        'porcentaje_acierto',
        'intentos_realizados',  # Modificación 7
        'fecha_completado'
    )
    list_filter = ('estado', 'desbloqueado', 'tema__leccion', 'fecha_inicio')
    search_fields = ('usuario__username', 'tema__titulo')
    readonly_fields = ('fecha_inicio', 'fecha_completado')
    ordering = ('tema__leccion__orden', 'tema__orden', 'usuario')

    fieldsets = (
        ('Información General', {
            'fields': ('usuario', 'tema', 'estado', 'desbloqueado')
        }),
        ('Progreso', {
            'fields': ('porcentaje_acierto', 'intentos_realizados')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_completado')
        }),
    )

    # Acciones personalizadas
    actions = ['exportar_progreso_tema_csv']

    def exportar_progreso_tema_csv(self, request, queryset):
        """
        Exporta el progreso de temas seleccionado a CSV.
        Formato ACUMULATIVO: Una fila por usuario/tema con contadores totales.
        Incluye tiempos acumulados y contadores de clics.
        """
        import csv
        from django.http import HttpResponse
        from datetime import datetime

        # Advertencia si hay muchos registros
        total_registros = queryset.count()
        if total_registros > 10000:
            self.message_user(
                request,
                f"⚠️ Tienes {total_registros} registros de progreso seleccionados. "
                f"La exportación puede tardar 15-30 segundos. "
                f"Considera usar filtros para reducir la cantidad.",
                level='warning'
            )

        # Configurar respuesta HTTP
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="progreso_tema_{timestamp}.csv"'

        # UTF-8 BOM para Excel
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow([
            'Usuario',
            'Tema',
            'Lección',
            'Estado',
            'Desbloqueado',
            '% Acierto',
            'Intentos Realizados',
            'Tiempo Total Teoría (seg)',
            'Tiempo Total Ejemplos (seg)',
            'Clics Ver Otro Ejemplo',
            'Clics Regresar',
            'Clics Volver Tema',
            'Clics Ir Ejercicios',
            'Clics Ayuda',
            'Fecha Inicio',
            'Fecha Completado'
        ])

        # Optimización: select_related para reducir consultas
        queryset_optimizado = queryset.select_related('usuario', 'tema', 'tema__leccion')

        # Exportar datos
        for progreso in queryset_optimizado:
            writer.writerow([
                progreso.usuario.username,
                progreso.tema.titulo,
                progreso.tema.leccion.titulo if progreso.tema.leccion else '',
                progreso.get_estado_display(),
                'Sí' if progreso.desbloqueado else 'No',
                float(progreso.porcentaje_acierto),
                progreso.intentos_realizados,
                progreso.tiempo_total_teoria_segundos,
                progreso.tiempo_total_ejemplos_segundos,
                progreso.clics_ver_otro_ejemplo,
                progreso.clics_regresar,
                progreso.clics_volver_tema,
                progreso.clics_ir_ejercicios,
                progreso.clics_ayuda,
                progreso.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S') if progreso.fecha_inicio else '',
                progreso.fecha_completado.strftime('%Y-%m-%d %H:%M:%S') if progreso.fecha_completado else ''
            ])

        self.message_user(request, f'✅ Se exportaron {total_registros} registros de progreso correctamente.')
        return response

    exportar_progreso_tema_csv.short_description = "📊 Exportar progreso seleccionado a CSV (ACUMULATIVO)"








@admin.register(RespuestaEjercicio)
class RespuestaEjercicioAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'ejercicio_breve',
        'es_correcta',
        'uso_ayuda',
        'tiempo_respuesta_segundos',
        'fecha_respuesta'
    )
    list_filter = ('es_correcta', 'uso_ayuda', 'fecha_respuesta', 'ejercicio__tema')
    search_fields = ('usuario__username', 'ejercicio__enunciado')
    readonly_fields = ('fecha_respuesta',)
    ordering = ('-fecha_respuesta',)

    def ejercicio_breve(self, obj):
        return obj.ejercicio.enunciado[:50] + '...' if len(obj.ejercicio.enunciado) > 50 else obj.ejercicio.enunciado
    ejercicio_breve.short_description = 'Ejercicio'

    # Acciones personalizadas
    actions = ['exportar_respuestas_csv']

    def exportar_respuestas_csv(self, request, queryset):
        """
        Exporta las respuestas de ejercicios seleccionadas a CSV.
        Formato INDIVIDUAL: Una fila por cada respuesta registrada.
        """
        import csv
        from django.http import HttpResponse
        from datetime import datetime

        # Advertencia si hay muchos registros
        total_registros = queryset.count()
        if total_registros > 10000:
            self.message_user(
                request,
                f"⚠️ Tienes {total_registros} respuestas seleccionadas. "
                f"La exportación puede tardar 15-30 segundos. "
                f"Considera usar filtros para reducir la cantidad.",
                level='warning'
            )

        # Configurar respuesta HTTP
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="respuestas_ejercicios_{timestamp}.csv"'

        # UTF-8 BOM para Excel
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow([
            'Usuario',
            'Ejercicio',
            'Tema',
            'Lección',
            'Respuesta Usuario',
            'Es Correcta',
            'Usó Ayuda',
            'Tiempo Respuesta (seg)',
            'Fecha/Hora Respuesta'
        ])

        # Optimización: select_related para reducir consultas
        queryset_optimizado = queryset.select_related(
            'usuario',
            'ejercicio',
            'ejercicio__tema',
            'ejercicio__tema__leccion'
        )

        # Exportar datos
        for respuesta in queryset_optimizado:
            writer.writerow([
                respuesta.usuario.username,
                respuesta.ejercicio.enunciado,
                respuesta.ejercicio.tema.titulo if respuesta.ejercicio.tema else '',
                respuesta.ejercicio.tema.leccion.titulo if respuesta.ejercicio.tema and respuesta.ejercicio.tema.leccion else '',
                respuesta.respuesta_usuario,
                'Sí' if respuesta.es_correcta else 'No',
                'Sí' if respuesta.uso_ayuda else 'No',
                respuesta.tiempo_respuesta_segundos,
                respuesta.fecha_respuesta.strftime('%Y-%m-%d %H:%M:%S')
            ])

        self.message_user(request, f'✅ Se exportaron {total_registros} respuestas correctamente.')
        return response

    exportar_respuestas_csv.short_description = "📊 Exportar respuestas seleccionadas a CSV (INDIVIDUAL)"


# ActividadPantalla ELIMINADO - Reemplazado por TiempoPantalla y ClicBoton
# Se mantiene el modelo en models.py como histórico pero NO se muestra en admin
# @admin.register(ActividadPantalla)
# class ActividadPantallaAdmin(admin.ModelAdmin):
#     list_display = (
#         'usuario_display',
#         'tipo_pantalla',
#         'tiempo_segundos',
#         'veces_volver_contenido',
#         'veces_ver_ejemplo_extra',
#         'veces_ir_a_ejercicios',
#         'tiempo_inicio',
#         'tiempo_fin'
#     )
#     list_filter = ('tipo_pantalla', 'tiempo_inicio', 'usuario')
#     search_fields = ('usuario__username',)
#     readonly_fields = ('tiempo_inicio', 'tiempo_fin')
#     ordering = ('-tiempo_inicio',)
#
#     fieldsets = (
#         ('Información General', {
#             'fields': ('usuario', 'tipo_pantalla', 'tiempo_inicio', 'tiempo_fin', 'tiempo_segundos')
#         }),
#         ('Metadatos', {
#             'fields': ('leccion_id', 'tema_id')
#         }),
#         ('Tracking de Navegación', {
#             'fields': (
#                 'veces_volver_contenido',
#                 'veces_ver_ejemplo_extra',
#                 'veces_ir_a_ejercicios'
#             ),
#             'description': 'Registro de acciones de navegación del usuario durante el contenido del tema'
#         }),
#     )
#
#     def usuario_display(self, obj):
#         return obj.usuario.username if obj.usuario else 'Anónimo'
#     usuario_display.short_description = 'Usuario'


# Modificación 7: Admin para IntentoTema
@admin.register(IntentoTema)
class IntentoTemaAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'tema',
        'numero_intento',
        'porcentaje_acierto',
        'aprobado',
        'ejercicios_correctos_display',
        'ejercicios_con_ayuda',
        'tiempo_total_minutos',
        'mejora_porcentaje',
        'fecha_finalizacion'
    )
   
    list_filter = (
        'aprobado',
        'tema__leccion',
        'tema',
        'numero_intento',
        'fecha_finalizacion'
    )
   
    search_fields = (
        'usuario__username',
        'tema__titulo'
    )
   
    readonly_fields = (
        'fecha_inicio',
        'fecha_finalizacion',
        'mejora_porcentaje'
    )
   
    ordering = ('-fecha_finalizacion',)
   
    fieldsets = (
        ('Información General', {
            'fields': ('usuario', 'tema', 'progreso_tema', 'numero_intento')
        }),
        ('Resultados del Intento', {
            'fields': (
                'ejercicios_correctos',
                'ejercicios_incorrectos',
                'ejercicios_totales',
                'porcentaje_acierto',
                'aprobado'
            )
        }),
        ('Uso de Ayuda', {
            'fields': ('ejercicios_con_ayuda',)
        }),
        ('Tiempos', {
            'fields': (
                'tiempo_total_segundos',
                'tiempo_promedio_por_ejercicio'
            )
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_finalizacion')
        }),
        ('Mejora', {
            'fields': ('mejora_porcentaje',),
            'description': 'Mejora en porcentaje respecto al intento anterior'
        }),
    )
   
    def ejercicios_correctos_display(self, obj):
        return f"{obj.ejercicios_correctos}/{obj.ejercicios_totales}"
    ejercicios_correctos_display.short_description = 'Correctos/Total'
   
    def tiempo_total_minutos(self, obj):
        return f"{obj.tiempo_total_segundos // 60} min"
    tiempo_total_minutos.short_description = 'Tiempo Total'
   
    # Acciones personalizadas
    actions = ['exportar_intentos_csv']
   
    def exportar_intentos_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
       
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="intentos_temas.csv"'
       
        writer = csv.writer(response)
        writer.writerow([
            'Usuario',
            'Tema',
            'Número Intento',
            'Porcentaje Acierto',
            'Aprobado',
            'Correctos',
            'Incorrectos',
            'Con Ayuda',
            'Tiempo Total (seg)',
            'Tiempo Promedio (seg)',
            'Mejora %',
            'Fecha Finalización'
        ])
       
        for intento in queryset:
            writer.writerow([
                intento.usuario.username,
                intento.tema.titulo,
                intento.numero_intento,
                intento.porcentaje_acierto,
                'Sí' if intento.aprobado else 'No',
                intento.ejercicios_correctos,
                intento.ejercicios_incorrectos,
                intento.ejercicios_con_ayuda,
                intento.tiempo_total_segundos,
                intento.tiempo_promedio_por_ejercicio,
                intento.mejora_porcentaje or 0,
                intento.fecha_finalizacion.strftime('%Y-%m-%d %H:%M:%S')
            ])
       
        return response
   
    exportar_intentos_csv.short_description = "Exportar intentos seleccionados a CSV"


# ==================== NUEVOS MODELOS DE TRACKING ====================

@admin.register(TiempoPantalla)
class TiempoPantallaAdmin(admin.ModelAdmin):
    """
    Admin para TiempoPantalla - Eventos individuales de tiempo en pantalla.
    Muestra registros individuales, pero las vistas matriciales se implementarán como vistas personalizadas.
    """
    list_display = (
        'usuario',
        'tema',
        'tipo_contenido',
        'numero',
        'nombre_completo_display',
        'tiempo_segundos',
        'cambio_pestana_display',
        'timestamp'
    )
    list_filter = ('tipo_contenido', 'tema', 'cambio_pestana', 'timestamp')
    search_fields = ('usuario__username', 'tema__titulo')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

    fieldsets = (
        ('Información General', {
            'fields': ('usuario', 'tema', 'timestamp')
        }),
        ('Contenido', {
            'fields': ('tipo_contenido', 'numero', 'contenido', 'ejercicio')
        }),
        ('Tiempo', {
            'fields': ('tiempo_segundos', 'cambio_pestana')
        }),
    )

    def nombre_completo_display(self, obj):
        """Muestra el nombre completo del contenido: 'Teoría 1', 'Ejemplo 2', etc."""
        return obj.nombre_completo
    nombre_completo_display.short_description = 'Contenido'

    def cambio_pestana_display(self, obj):
        """Muestra Sí/No en lugar de True/False"""
        return 'Sí' if obj.cambio_pestana else 'No'
    cambio_pestana_display.short_description = 'Cambió Pestaña'

    # Acciones personalizadas
    actions = ['exportar_tiempo_pantalla_csv']

    def exportar_tiempo_pantalla_csv(self, request, queryset):
        """
        Exporta los registros de tiempo en pantalla seleccionados a CSV.
        Formato INDIVIDUAL: Una fila por cada evento de tiempo registrado.
        """
        import csv
        from django.http import HttpResponse
        from datetime import datetime

        # Advertencia si hay muchos registros
        total_registros = queryset.count()
        if total_registros > 10000:
            self.message_user(
                request,
                f"⚠️ Tienes {total_registros} eventos de tiempo seleccionados. "
                f"La exportación puede tardar 15-30 segundos. "
                f"Considera usar filtros para reducir la cantidad.",
                level='warning'
            )

        # Configurar respuesta HTTP
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="tiempo_pantalla_{timestamp}.csv"'

        # UTF-8 BOM para Excel
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow([
            'Usuario',
            'Tema',
            'Lección',
            'Tipo Contenido',
            'Número',
            'Nombre Completo',
            'Tiempo (seg)',
            'Cambió Pestaña',
            'Fecha/Hora'
        ])

        # Optimización: select_related para reducir consultas
        queryset_optimizado = queryset.select_related(
            'usuario',
            'tema',
            'tema__leccion',
            'contenido',
            'ejercicio'
        )

        # Exportar datos
        for tiempo in queryset_optimizado:
            writer.writerow([
                tiempo.usuario.username,
                tiempo.tema.titulo,
                tiempo.tema.leccion.titulo if tiempo.tema.leccion else '',
                tiempo.get_tipo_contenido_display(),
                tiempo.numero,
                tiempo.nombre_completo,
                tiempo.tiempo_segundos,
                'Sí' if tiempo.cambio_pestana else 'No',
                tiempo.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])

        self.message_user(request, f'✅ Se exportaron {total_registros} eventos de tiempo correctamente.')
        return response

    exportar_tiempo_pantalla_csv.short_description = "📊 Exportar tiempos seleccionados a CSV (INDIVIDUAL)"


@admin.register(ClicBoton)
class ClicBotonAdmin(admin.ModelAdmin):
    """
    Admin para ClicBoton - Eventos individuales de clics en botones.
    Muestra registros individuales, pero las vistas matriciales se implementarán como vistas personalizadas.
    """
    list_display = (
        'usuario',
        'tema',
        'tipo_boton',
        'tipo_boton_display',
        'timestamp'
    )
    list_filter = ('tipo_boton', 'tema', 'timestamp')
    search_fields = ('usuario__username', 'tema__titulo')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

    fieldsets = (
        ('Información General', {
            'fields': ('usuario', 'tema', 'timestamp')
        }),
        ('Botón', {
            'fields': ('tipo_boton',)
        }),
    )

    def tipo_boton_display(self, obj):
        """Muestra el nombre legible del tipo de botón"""
        return obj.get_tipo_boton_display()
    tipo_boton_display.short_description = 'Botón'

    # Acciones personalizadas
    actions = ['exportar_clics_csv']

    def exportar_clics_csv(self, request, queryset):
        """
        Exporta los clics en botones seleccionados a CSV.
        Formato INDIVIDUAL: Una fila por cada clic registrado.
        """
        import csv
        from django.http import HttpResponse
        from datetime import datetime

        # Advertencia si hay muchos registros
        total_registros = queryset.count()
        if total_registros > 10000:
            self.message_user(
                request,
                f"⚠️ Tienes {total_registros} clics seleccionados. "
                f"La exportación puede tardar 15-30 segundos. "
                f"Considera usar filtros para reducir la cantidad.",
                level='warning'
            )

        # Configurar respuesta HTTP
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="clics_botones_{timestamp}.csv"'

        # UTF-8 BOM para Excel
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow([
            'Usuario',
            'Tema',
            'Lección',
            'Tipo de Botón',
            'Fecha/Hora'
        ])

        # Optimización: select_related para reducir consultas
        queryset_optimizado = queryset.select_related(
            'usuario',
            'tema',
            'tema__leccion'
        )

        # Exportar datos
        for clic in queryset_optimizado:
            writer.writerow([
                clic.usuario.username,
                clic.tema.titulo if clic.tema else '',
                clic.tema.leccion.titulo if clic.tema and clic.tema.leccion else '',
                clic.get_tipo_boton_display(),
                clic.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])

        self.message_user(request, f'✅ Se exportaron {total_registros} clics correctamente.')
        return response

    exportar_clics_csv.short_description = "📊 Exportar clics seleccionados a CSV (INDIVIDUAL)"



