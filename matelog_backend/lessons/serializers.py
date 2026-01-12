# lessons/serializers.py
from rest_framework import serializers
from .models import (
    Leccion, Tema, ContenidoTema, Ejercicio, OpcionMultiple
)
from tracking.models import (
    ProgresoLeccion, ProgresoTema, RespuestaEjercicio
)




class OpcionMultipleSerializer(serializers.ModelSerializer):
    """
    Serializer para opciones múltiples.
    """
    class Meta:
        model = OpcionMultiple
        fields = ['letra', 'texto']




class ContenidoTemaSerializer(serializers.ModelSerializer):
    """
    Serializer para contenido de temas (teoría/ejemplos).
    Las imágenes están incrustadas en contenido_texto mediante TinyMCE.
    """
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
   
    class Meta:
        model = ContenidoTema
        fields = ['id', 'tipo', 'tipo_display', 'orden', 'contenido_texto']




class EjercicioSerializer(serializers.ModelSerializer):
    """
    Serializer para ejercicios (sin incluir la respuesta correcta).
    Las imágenes están incrustadas en enunciado mediante TinyMCE.
    """
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    dificultad_display = serializers.CharField(source='get_dificultad_display', read_only=True)
    opciones = OpcionMultipleSerializer(many=True, read_only=True)
    tiene_ayuda = serializers.SerializerMethodField()
   
    class Meta:
        model = Ejercicio
        fields = [
            'id', 'orden', 'tipo', 'tipo_display', 'dificultad',
            'dificultad_display', 'mostrar_dificultad', 'instruccion',
            'enunciado', 'opciones', 'texto_ayuda', 'tiene_ayuda'
        ]
   
    def get_tiene_ayuda(self, obj):
        return bool(obj.texto_ayuda)




class EjercicioValidacionSerializer(serializers.Serializer):
    """
    Serializer para validar respuestas de ejercicios.
    """
    ejercicio_id = serializers.IntegerField()
    respuesta = serializers.CharField(max_length=500)
    uso_ayuda = serializers.BooleanField(default=False)
    tiempo_respuesta_segundos = serializers.IntegerField(required=False, allow_null=True)




class TemaListSerializer(serializers.ModelSerializer):
    """
    Serializer para lista de temas con información de progreso.
    FIX: Calcula progreso excluyendo EJEMPLO_EXTRA.
    """
    cantidad_contenidos = serializers.SerializerMethodField()
    cantidad_ejercicios = serializers.SerializerMethodField()
    contenidos_count = serializers.SerializerMethodField()
    progreso = serializers.SerializerMethodField()
   
    class Meta:
        model = Tema
        fields = [
            'id', 'titulo', 'descripcion', 'orden', 'leccion',
            'cantidad_contenidos', 'cantidad_ejercicios',
            'progreso', 'contenidos_count'
        ]
   
    def get_contenidos_count(self, obj):
        """Total de contenidos (excluyendo EJEMPLO_EXTRA) - alias para compatibilidad"""
        return obj.contenidos.exclude(tipo='EJEMPLO_EXTRA').count()

    def get_cantidad_contenidos(self, obj):
        """Total de contenidos (excluyendo EJEMPLO_EXTRA)"""
        return obj.contenidos.exclude(tipo='EJEMPLO_EXTRA').count()
   
    def get_cantidad_ejercicios(self, obj):
        """Total de ejercicios"""
        return obj.ejercicios.count()
   
    def get_progreso(self, obj):
        """
        Información de progreso del tema para el usuario actual.
        Incluye progreso de contenido y calificación de ejercicios.
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            contenidos_totales = obj.contenidos.exclude(tipo='EJEMPLO_EXTRA').count()
            return {
                'estado': 'SIN_INICIAR',
                'desbloqueado': False,
                'porcentaje_acierto': 0,
                'intentos_realizados': 0,
                'contenido_completado': 0,
                'contenidos_count': contenidos_totales
            }
       
        try:
            progreso_tema = ProgresoTema.objects.get(
                usuario=request.user,
                tema=obj
            )
           
            # Calcular contenido completado (sin EJEMPLO_EXTRA)
            contenidos_totales = obj.contenidos.exclude(tipo='EJEMPLO_EXTRA').count()
            contenido_completado = progreso_tema.contenido_completado
           
            return {
                'estado': progreso_tema.estado,
                'desbloqueado': progreso_tema.desbloqueado,
                'porcentaje_acierto': float(progreso_tema.porcentaje_acierto or 0),
                'intentos_realizados': progreso_tema.intentos_realizados,
                'contenido_completado': contenido_completado,
                'contenidos_count': contenidos_totales
            }
        except ProgresoTema.DoesNotExist:
            # Usuario no ha iniciado este tema
            contenidos_totales = obj.contenidos.exclude(tipo='EJEMPLO_EXTRA').count()
            return {
                'estado': 'SIN_INICIAR',
                'desbloqueado': False,
                'porcentaje_acierto': 0,
                'intentos_realizados': 0,
                'contenido_completado': 0,
                'contenidos_count': contenidos_totales
            }




class TemaDetailSerializer(serializers.ModelSerializer):
    """
    Serializer detallado para un tema específico con su contenido.
    MateLog-AE: Filtra ejercicios según el grupo del usuario (Control vs Experimental).
    """
    contenidos = ContenidoTemaSerializer(many=True, read_only=True)
    ejercicios = serializers.SerializerMethodField()

    class Meta:
        model = Tema
        fields = ['id', 'titulo', 'descripcion', 'orden', 'leccion', 'contenidos', 'ejercicios']

    def get_ejercicios(self, obj):
        """
        Filtra ejercicios según el grupo experimental del usuario.

        - Control: Solo ejercicios con obligatorio=True
        - Experimental: Ejercicios obligatorios + ejercicios según clasificación de autoeficacia
          - ALTO: obligatorios + INTERMEDIO + DIFICIL
          - MEDIO: obligatorios + INTERMEDIO
          - BAJO: obligatorios + FACIL + INTERMEDIO
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            # Si no hay usuario autenticado, devolver todos (no debería pasar)
            ejercicios = obj.ejercicios.all().order_by('orden')
            return EjercicioSerializer(ejercicios, many=True).data

        try:
            perfil = request.user.perfil
            grupo = perfil.grupo

            if grupo == 'CONTROL':
                # Grupo Control: solo ejercicios obligatorios
                ejercicios = obj.ejercicios.filter(obligatorio=True).order_by('orden')

            elif grupo == 'EXPERIMENTAL':
                # Grupo Experimental: ejercicios basados en clasificación de autoeficacia
                clasificacion = perfil.clasificacion_autoeficacia

                # Siempre incluir los obligatorios
                ejercicios_query = obj.ejercicios.filter(obligatorio=True)

                # Agregar ejercicios adicionales según clasificación
                if clasificacion == 'ALTO':
                    # Alto: agregar INTERMEDIO y DIFICIL
                    ejercicios_adicionales = obj.ejercicios.filter(
                        obligatorio=False,
                        dificultad__in=['INTERMEDIO', 'DIFICIL']
                    )
                    ejercicios = (ejercicios_query | ejercicios_adicionales).distinct().order_by('orden')

                elif clasificacion == 'MEDIO':
                    # Medio: agregar INTERMEDIO
                    ejercicios_adicionales = obj.ejercicios.filter(
                        obligatorio=False,
                        dificultad='INTERMEDIO'
                    )
                    ejercicios = (ejercicios_query | ejercicios_adicionales).distinct().order_by('orden')

                elif clasificacion == 'BAJO':
                    # Bajo: agregar FACIL e INTERMEDIO
                    ejercicios_adicionales = obj.ejercicios.filter(
                        obligatorio=False,
                        dificultad__in=['FACIL', 'INTERMEDIO']
                    )
                    ejercicios = (ejercicios_query | ejercicios_adicionales).distinct().order_by('orden')

                else:
                    # Sin clasificación aún: solo obligatorios (hasta que complete escala de autoeficacia)
                    ejercicios = ejercicios_query.order_by('orden')

            else:
                # Si no tiene grupo definido, mostrar todos (caso excepcional)
                ejercicios = obj.ejercicios.all().order_by('orden')

        except AttributeError:
            # Usuario sin perfil (usuarios antiguos antes de MateLog-AE)
            # Mostrar todos los ejercicios
            ejercicios = obj.ejercicios.all().order_by('orden')

        return EjercicioSerializer(ejercicios, many=True).data




class LeccionListSerializer(serializers.ModelSerializer):
    """
    Serializer para lista de lecciones (solo activas).
    """
    cantidad_temas = serializers.SerializerMethodField()
   
    class Meta:
        model = Leccion
        fields = ['id', 'titulo', 'descripcion', 'orden', 'cantidad_temas']
   
    def get_cantidad_temas(self, obj):
        return obj.temas.filter(is_active=True).count()




class LeccionDetailSerializer(serializers.ModelSerializer):
    """
    Serializer detallado para una lección con sus temas.
    FIX: Usa TemaListSerializer para incluir progreso.
    """
    temas = serializers.SerializerMethodField()
   
    class Meta:
        model = Leccion
        fields = ['id', 'titulo', 'descripcion', 'orden', 'temas']
   
    def get_temas(self, obj):
        """Obtener temas activos con información de progreso"""
        temas = obj.temas.filter(is_active=True).order_by('orden')
        serializer = TemaListSerializer(
            temas,
            many=True,
            context=self.context  # Pasar contexto para acceder al request
        )
        return serializer.data


