# tracking/views.py
# AGREGAR estas vistas al archivo views.py existente


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from .models import (
    SesionEstudio, ActividadPantalla, EventoTracking, ProgresoTema,
    TiempoPantalla, ClicBoton  # NUEVOS modelos
)
from lessons.models import Tema, ContenidoTema
from .serializers import RegistrarEventoSerializer, EventoTrackingSerializer


class IniciarSesionView(APIView):
    """
    Vista para iniciar una sesión de estudio.
    Endpoint: POST /api/tracking/sesion/iniciar/
    """
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        sesion = SesionEstudio.objects.create(usuario=request.user)
        return Response({
            'sesion_id': sesion.id,
            'fecha_inicio': sesion.fecha_inicio
        }, status=status.HTTP_201_CREATED)








class FinalizarSesionView(APIView):
    """
    Vista para finalizar una sesión de estudio.
    Endpoint: POST /api/tracking/sesion/finalizar/
    """
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        sesion_id = request.data.get('sesion_id')
       
        if not sesion_id:
            return Response(
                {'error': 'Se requiere sesion_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        sesion = get_object_or_404(SesionEstudio, id=sesion_id, usuario=request.user)
        sesion.fecha_fin = timezone.now()
       
        # Calcular duración en minutos
        duracion = (sesion.fecha_fin - sesion.fecha_inicio).total_seconds() / 60
        sesion.duracion_minutos = int(duracion)
        sesion.save()
       
        return Response({
            'mensaje': 'Sesión finalizada correctamente',
            'duracion_minutos': sesion.duracion_minutos
        }, status=status.HTTP_200_OK)








class IniciarActividadView(APIView):
    """
    Vista para registrar el inicio de una actividad en una pantalla.
    Endpoint: POST /api/tracking/iniciar/
    """
    permission_classes = [AllowAny]
   
    def post(self, request):
        tipo_pantalla = request.data.get('tipo_pantalla', 'OTRA')
       
        # Obtener metadatos opcionales
        metadata = request.data.get('metadata', {})
        leccion_id = metadata.get('leccion_id')
        tema_id = metadata.get('tema_id')
       
        # Crear actividad
        actividad = ActividadPantalla.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            tipo_pantalla=tipo_pantalla,
            leccion_id=leccion_id,
            tema_id=tema_id
        )
       
        return Response({
            'actividad_id': actividad.id,
            'tiempo_inicio': actividad.tiempo_inicio
        }, status=status.HTTP_201_CREATED)








class FinalizarActividadView(APIView):
    """
    Vista para finalizar una actividad de pantalla.
    Endpoint: POST /api/tracking/finalizar/
    """
    permission_classes = [AllowAny]
   
    def post(self, request):
        actividad_id = request.data.get('actividad_id')
       
        if not actividad_id:
            return Response(
                {'error': 'Se requiere actividad_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        try:
            actividad = ActividadPantalla.objects.get(id=actividad_id)
            actividad.tiempo_fin = timezone.now()
           
            # Calcular tiempo en segundos
            tiempo_total = (actividad.tiempo_fin - actividad.tiempo_inicio).total_seconds()
            actividad.tiempo_segundos = int(tiempo_total)
            actividad.save()
           
            return Response({
                'mensaje': 'Actividad finalizada correctamente',
                'tiempo_segundos': actividad.tiempo_segundos
            }, status=status.HTTP_200_OK)
           
        except ActividadPantalla.DoesNotExist:
            return Response(
                {'error': 'Actividad no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )




class RegistrarVolverContenidoView(APIView):
    """
    Vista para registrar cuando el usuario presiona el botón "Volver" en el contenido.
    Endpoint: POST /api/tracking/volver-contenido/
    """
    permission_classes = [AllowAny]
   
    def post(self, request):
        actividad_id = request.data.get('actividad_id')
       
        if not actividad_id:
            return Response(
                {'error': 'Se requiere actividad_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        try:
            actividad = ActividadPantalla.objects.get(id=actividad_id)
            actividad.veces_volver_contenido += 1
            actividad.save()
           
            return Response({
                'mensaje': 'Click en volver registrado',
                'veces_volver': actividad.veces_volver_contenido
            }, status=status.HTTP_200_OK)
           
        except ActividadPantalla.DoesNotExist:
            return Response(
                {'error': 'Actividad no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )




class RegistrarVerEjemploExtraView(APIView):
    """
    Vista para registrar cuando el usuario presiona "Ver Otro Ejemplo".
    Endpoint: POST /api/tracking/ver-ejemplo-extra/
    """
    permission_classes = [AllowAny]
   
    def post(self, request):
        actividad_id = request.data.get('actividad_id')
       
        if not actividad_id:
            return Response(
                {'error': 'Se requiere actividad_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        try:
            actividad = ActividadPantalla.objects.get(id=actividad_id)
            actividad.veces_ver_ejemplo_extra += 1
            actividad.save()
           
            return Response({
                'mensaje': 'Ver ejemplo extra registrado',
                'veces_ver_ejemplo_extra': actividad.veces_ver_ejemplo_extra
            }, status=status.HTTP_200_OK)
           
        except ActividadPantalla.DoesNotExist:
            return Response(
                {'error': 'Actividad no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )




class RegistrarIrAEjerciciosView(APIView):
    """
    Vista para registrar cuando el usuario va directo a ejercicios desde el contenido.
    Endpoint: POST /api/tracking/ir-a-ejercicios/
    """
    permission_classes = [AllowAny]
   
    def post(self, request):
        actividad_id = request.data.get('actividad_id')
       
        if not actividad_id:
            return Response(
                {'error': 'Se requiere actividad_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        try:
            actividad = ActividadPantalla.objects.get(id=actividad_id)
            actividad.veces_ir_a_ejercicios += 1
            actividad.save()
           
            return Response({
                'mensaje': 'Ir a ejercicios registrado',
                'veces_ir_a_ejercicios': actividad.veces_ir_a_ejercicios
            }, status=status.HTTP_200_OK)
           
        except ActividadPantalla.DoesNotExist:
            return Response(
                {'error': 'Actividad no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )




class RegistrarVerEjemploExtraView(APIView):
    """
    Vista para registrar cuando el usuario presiona "Ver Otro Ejemplo".
    Endpoint: POST /api/tracking/ver-ejemplo-extra/
    """
    permission_classes = [AllowAny]
   
    def post(self, request):
        actividad_id = request.data.get('actividad_id')
       
        if not actividad_id:
            return Response(
                {'error': 'Se requiere actividad_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        try:
            actividad = ActividadPantalla.objects.get(id=actividad_id)
            actividad.veces_ver_ejemplo_extra += 1
            actividad.save()
           
            return Response({
                'mensaje': 'Ver ejemplo extra registrado',
                'veces_ver_ejemplo_extra': actividad.veces_ver_ejemplo_extra
            }, status=status.HTTP_200_OK)
           
        except ActividadPantalla.DoesNotExist:
            return Response(
                {'error': 'Actividad no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )




class RegistrarIrAEjerciciosView(APIView):
    """
    Vista para registrar cuando el usuario va directo a ejercicios desde el contenido.
    Endpoint: POST /api/tracking/ir-a-ejercicios/
    """
    permission_classes = [AllowAny]
   
    def post(self, request):
        actividad_id = request.data.get('actividad_id')
       
        if not actividad_id:
            return Response(
                {'error': 'Se requiere actividad_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        try:
            actividad = ActividadPantalla.objects.get(id=actividad_id)
            actividad.veces_ir_a_ejercicios += 1
            actividad.save()
           
            return Response({
                'mensaje': 'Ir a ejercicios registrado',
                'veces_ir_a_ejercicios': actividad.veces_ir_a_ejercicios
            }, status=status.HTTP_200_OK)
           
        except ActividadPantalla.DoesNotExist:
            return Response(
                {'error': 'Actividad no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

class RegistrarEventoView(APIView):
    """
    Vista para registrar eventos de tracking.
    Endpoint: POST /api/tracking/evento/
    
    Crea un EventoTracking y actualiza los campos agregados en ProgresoTema.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = RegistrarEventoSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        tipo_evento = validated_data['tipo_evento']
        tema_id = validated_data['tema_id']
        
        try:
            tema = Tema.objects.get(id=tema_id)
        except Tema.DoesNotExist:
            return Response(
                {'error': 'Tema no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Obtener o crear ProgresoTema
        progreso_tema, _ = ProgresoTema.objects.get_or_create(
            usuario=request.user,
            tema=tema,
            defaults={
                'desbloqueado': True,
                'estado': 'INICIADO',
                'fecha_inicio': timezone.now()
            }
        )
        
        # Usar transacción para asegurar consistencia
        with transaction.atomic():
            # Crear evento de tracking
            evento = EventoTracking.objects.create(
                usuario=request.user,
                tema=tema,
                tipo_evento=tipo_evento,
                contenido_id=validated_data.get('contenido_id'),
                ejercicio_id=validated_data.get('ejercicio_id'),
                numero_intento=validated_data.get('numero_intento'),
                tiempo_segundos=validated_data.get('tiempo_segundos'),
                cambio_pestana=validated_data.get('cambio_pestana', False)
            )
            
            # Actualizar campos agregados en ProgresoTema según el tipo de evento
            if tipo_evento == 'TEORIA_VISTA' and validated_data.get('tiempo_segundos') is not None:
                progreso_tema.tiempo_total_teoria_segundos += validated_data['tiempo_segundos']
            
            elif tipo_evento == 'EJEMPLO_VISTO' and validated_data.get('tiempo_segundos') is not None:
                progreso_tema.tiempo_total_ejemplos_segundos += validated_data['tiempo_segundos']
            
            elif tipo_evento == 'CLIC_VER_OTRO_EJEMPLO':
                progreso_tema.clics_ver_otro_ejemplo += 1
            
            elif tipo_evento == 'CLIC_REGRESAR':
                progreso_tema.clics_regresar += 1
            
            elif tipo_evento == 'CLIC_VOLVER_TEMA':
                progreso_tema.clics_volver_tema += 1
            
            elif tipo_evento == 'CLIC_IR_EJERCICIOS':
                progreso_tema.clics_ir_ejercicios += 1
            
            elif tipo_evento == 'CLIC_AYUDA':
                progreso_tema.clics_ayuda += 1
            
            # Guardar cambios en ProgresoTema
            progreso_tema.save()
        
        # Serializar el evento creado
        evento_serializer = EventoTrackingSerializer(evento)
        
        return Response({
            'mensaje': 'Evento registrado correctamente',
            'evento': evento_serializer.data,
            'progreso_tema_id': progreso_tema.id
        }, status=status.HTTP_201_CREATED)


# ==================== NUEVAS VISTAS PARA SISTEMA DE TRACKING MEJORADO ====================

class ActualizarActividadSesionView(APIView):
    """
    Vista para actualizar la última actividad de una sesión (heartbeat).
    Endpoint: POST /api/tracking/sesion/actividad/

    El frontend debe llamar esto cada 2 minutos para mantener la sesión activa.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sesion_id = request.data.get('sesion_id')

        if not sesion_id:
            return Response(
                {'error': 'Se requiere sesion_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        sesion = get_object_or_404(SesionEstudio, id=sesion_id, usuario=request.user)
        sesion.ultima_actividad = timezone.now()
        sesion.save(update_fields=['ultima_actividad'])

        return Response({
            'mensaje': 'Actividad actualizada',
            'ultima_actividad': sesion.ultima_actividad
        }, status=status.HTTP_200_OK)


class FinalizarSesionMejoradaView(APIView):
    """
    Vista para finalizar una sesión con tipo de cierre.
    Endpoint: POST /api/tracking/sesion/finalizar-mejorada/

    Body:
    {
        "sesion_id": 123,
        "tipo_cierre": "LOGOUT" | "INACTIVIDAD" | "CIERRE_VENTANA"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sesion_id = request.data.get('sesion_id')
        tipo_cierre = request.data.get('tipo_cierre', 'LOGOUT')

        if not sesion_id:
            return Response(
                {'error': 'Se requiere sesion_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar tipo_cierre
        tipos_validos = ['LOGOUT', 'INACTIVIDAD', 'CIERRE_VENTANA']
        if tipo_cierre not in tipos_validos:
            return Response(
                {'error': f'tipo_cierre debe ser uno de: {", ".join(tipos_validos)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        sesion = get_object_or_404(SesionEstudio, id=sesion_id, usuario=request.user)
        sesion.fecha_fin = timezone.now()
        sesion.tipo_cierre = tipo_cierre

        # Calcular duración en segundos
        duracion = (sesion.fecha_fin - sesion.fecha_inicio).total_seconds()
        sesion.duracion_segundos = int(duracion)

        # Mantener compatibilidad con duracion_minutos
        sesion.duracion_minutos = int(duracion / 60)

        sesion.save()

        return Response({
            'mensaje': 'Sesión finalizada correctamente',
            'duracion_segundos': sesion.duracion_segundos,
            'tipo_cierre': sesion.tipo_cierre
        }, status=status.HTTP_200_OK)


class RegistrarTiempoPantallaView(APIView):
    """
    Vista para registrar tiempo en una pantalla específica (Teoría, Ejemplo, Ejercicio).
    Endpoint: POST /api/tracking/tiempo-pantalla/

    Body:
    {
        "tema_id": 1,
        "tipo_contenido": "TEORIA" | "EJEMPLO" | "EJERCICIO",
        "numero": 1,
        "contenido_id": 5,  // opcional, para Teoría/Ejemplo
        "ejercicio_id": 10, // opcional, para Ejercicio
        "tiempo_segundos": 45,
        "cambio_pestana": false
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tema_id = request.data.get('tema_id')
        tipo_contenido = request.data.get('tipo_contenido')
        numero = request.data.get('numero')
        tiempo_segundos = request.data.get('tiempo_segundos')

        # Validar campos requeridos
        if not all([tema_id, tipo_contenido, numero is not None, tiempo_segundos is not None]):
            return Response(
                {'error': 'Se requieren: tema_id, tipo_contenido, numero, tiempo_segundos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar tipo_contenido
        tipos_validos = ['TEORIA', 'EJEMPLO', 'EJERCICIO']
        if tipo_contenido not in tipos_validos:
            return Response(
                {'error': f'tipo_contenido debe ser uno de: {", ".join(tipos_validos)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener tema
        tema = get_object_or_404(Tema, id=tema_id)

        # Obtener referencias opcionales
        contenido_id = request.data.get('contenido_id')
        ejercicio_id = request.data.get('ejercicio_id')
        cambio_pestana = request.data.get('cambio_pestana', False)

        # Obtener objetos relacionados si se proporcionan IDs
        contenido = None
        if contenido_id:
            contenido = get_object_or_404(ContenidoTema, id=contenido_id)

        ejercicio = None
        if ejercicio_id:
            from lessons.models import Ejercicio
            ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)

        # Crear registro de tiempo
        tiempo = TiempoPantalla.objects.create(
            usuario=request.user,
            tema=tema,
            contenido=contenido,
            ejercicio=ejercicio,
            tipo_contenido=tipo_contenido,
            numero=numero,
            tiempo_segundos=tiempo_segundos,
            cambio_pestana=cambio_pestana
        )

        return Response({
            'id': tiempo.id,
            'mensaje': 'Tiempo registrado correctamente',
            'nombre_completo': tiempo.nombre_completo,
            'tiempo_segundos': tiempo.tiempo_segundos
        }, status=status.HTTP_201_CREATED)


class RegistrarClicBotonView(APIView):
    """
    Vista para registrar un clic en un botón específico.
    Endpoint: POST /api/tracking/clic-boton/

    Body:
    {
        "tema_id": 1,  // opcional
        "tipo_boton": "REGRESAR" | "IR_EJERCICIOS" | "VOLVER" | "OTRO_EJEMPLO" | "VER_AYUDA"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tipo_boton = request.data.get('tipo_boton')

        # Validar campo requerido
        if not tipo_boton:
            return Response(
                {'error': 'Se requiere tipo_boton'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar tipo_boton
        tipos_validos = ['REGRESAR', 'IR_EJERCICIOS', 'VOLVER', 'OTRO_EJEMPLO', 'VER_AYUDA']
        if tipo_boton not in tipos_validos:
            return Response(
                {'error': f'tipo_boton debe ser uno de: {", ".join(tipos_validos)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener tema (opcional)
        tema_id = request.data.get('tema_id')
        tema = None
        if tema_id:
            tema = get_object_or_404(Tema, id=tema_id)

        # Crear registro de clic
        clic = ClicBoton.objects.create(
            usuario=request.user,
            tema=tema,
            tipo_boton=tipo_boton
        )

        return Response({
            'id': clic.id,
            'mensaje': 'Clic registrado correctamente',
            'tipo_boton': clic.get_tipo_boton_display()
        }, status=status.HTTP_201_CREATED)

