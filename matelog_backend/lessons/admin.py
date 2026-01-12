from django.contrib import admin
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from django.db import models
from .models import Leccion, Tema, ContenidoTema, Ejercicio, OpcionMultiple




@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ('orden', 'titulo', 'is_active', 'fecha_creacion')
    list_filter = ('is_active', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    ordering = ('orden',)
   
    # Modificación 8: TinyMCE para descripción
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }




class ContenidoTemaInline(admin.TabularInline):
    model = ContenidoTema
    extra = 1
    fields = ('tipo', 'orden', 'contenido_texto')
    ordering = ('orden',)
   
    # Modificación 8: TinyMCE para contenido_texto
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 20})},
    }




class EjercicioInline(admin.TabularInline):
    model = Ejercicio
    extra = 0
    fields = ('orden', 'tipo', 'enunciado', 'dificultad', 'obligatorio')
    show_change_link = True
    ordering = ('orden',)




@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('orden', 'leccion', 'titulo', 'is_active')
    list_filter = ('leccion', 'is_active', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    ordering = ('leccion__orden', 'orden')
    inlines = [ContenidoTemaInline, EjercicioInline]
   
    # Modificación 8: TinyMCE para descripción
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }




@admin.register(ContenidoTema)
class ContenidoTemaAdmin(admin.ModelAdmin):
    list_display = ('tema', 'tipo', 'orden', 'fecha_creacion')
    list_filter = ('tipo', 'tema__leccion', 'fecha_creacion')
    search_fields = ('tema__titulo', 'contenido_texto')
    ordering = ('tema__leccion__orden', 'tema__orden', 'orden')
   
    # Modificación 8: TinyMCE para contenido_texto
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }




class OpcionMultipleInline(admin.TabularInline):
    model = OpcionMultiple
    extra = 4
    fields = ('letra', 'texto')
    ordering = ('letra',)




@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('tema', 'orden', 'tipo', 'dificultad_display', 'obligatorio_display')
    list_filter = ('tipo', 'dificultad', 'obligatorio', 'tema__leccion')
    search_fields = ('tema__titulo', 'enunciado', 'instruccion')
    ordering = ('tema__leccion__orden', 'tema__orden', 'orden')
    inlines = [OpcionMultipleInline]

    # Modificación 8: TinyMCE para campos de texto largo
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 15})},
    }

    def dificultad_display(self, obj):
        """Muestra la dificultad con color."""
        colors = {
            'FACIL': '#28a745',
            'INTERMEDIO': '#ffc107',
            'DIFICIL': '#dc3545'
        }
        color = colors.get(obj.dificultad, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_dificultad_display()
        )
    dificultad_display.short_description = 'Dificultad'
    dificultad_display.admin_order_field = 'dificultad'

    def obligatorio_display(self, obj):
        """Muestra si es obligatorio para el grupo Control."""
        if obj.obligatorio:
            return format_html('<span style="color: #007bff; font-weight: bold;">✓ Control</span>')
        return format_html('<span style="color: #6c757d;">Experimental</span>')
    obligatorio_display.short_description = 'Grupo'
    obligatorio_display.admin_order_field = 'obligatorio'

    def save_model(self, request, obj, form, change):
        """
        Validar antes de guardar desde el admin.
        Las validaciones se ejecutan automáticamente en el método save() del modelo.
        """
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            # Mostrar errores de validación en el admin
            from django.contrib import messages
            messages.error(request, f'Error al guardar: {str(e)}')
            raise




@admin.register(OpcionMultiple)
class OpcionMultipleAdmin(admin.ModelAdmin):
    list_display = ('ejercicio', 'letra', 'texto_preview')
    list_filter = ('ejercicio__tema__leccion',)
    search_fields = ('ejercicio__enunciado', 'texto')
    ordering = ('ejercicio__tema__leccion__orden', 'ejercicio__tema__orden', 'ejercicio__orden', 'letra')
   
    def texto_preview(self, obj):
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_preview.short_description = 'Texto'


