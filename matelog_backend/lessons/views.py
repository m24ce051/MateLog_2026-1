# lessons/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import models, transaction


from .models import (
    Leccion, Tema, ContenidoTema, Ejercicio
)
from tracking.models import (
    ProgresoLeccion, ProgresoTema, RespuestaEjercicio
)
from .serializers import (
    LeccionListSerializer,
    LeccionDetailSerializer,
    TemaDetailSerializer,
    EjercicioValidacionSerializer,
)


# Custom throttle class for answer validation
class ValidarRespuestaThrottle(UserRateThrottle):
    """Rate limit for answer validation: 100 requests per minute (ajustado para desarrollo)"""
    rate = '100/minute'


def calcular_porcentaje_leccion(usuario, leccion):
    """
    Calcula el porcentaje de completado de una lección basándose en:
    - Progreso de contenido (teoría/ejemplos) de cada tema
    - Progreso de ejercicios de cada tema

    Fórmula: Promedio del progreso de todos los temas
    Progreso de tema = (progreso_contenido * 0.5) + (porcentaje_acierto * 0.5)

    OPTIMIZADO: Usa prefetch_related para evitar N+1 queries
    """
    # Obtener temas con sus progresos en una sola query
    temas = leccion.temas.filter(is_active=True).prefetch_related(
        models.Prefetch(
            'progresotema_set',
            queryset=ProgresoTema.objects.filter(usuario=usuario).prefetch_related('contenidos_vistos'),
            to_attr='progreso_usuario'
        )
    )

    if not temas.exists():
        return 0

    progreso_total = 0

    for tema in temas:
        # Obtener o crear progreso (ya está prefetched)
        if hasattr(tema, 'progreso_usuario') and tema.progreso_usuario:
            progreso_tema = tema.progreso_usuario[0]
        else:
            # Crear si no existe (caso raro)
            progreso_tema, _ = ProgresoTema.objects.get_or_create(
                usuario=usuario,
                tema=tema
            )

        # Progreso de contenido (teoría/ejemplos)
        progreso_contenido = progreso_tema.calcular_progreso_contenido()

        # Progreso de ejercicios
        progreso_ejercicios = float(progreso_tema.porcentaje_acierto or 0)

        # Promedio ponderado: 50% contenido, 50% ejercicios
        progreso_tema_total = (progreso_contenido * 0.5) + (progreso_ejercicios * 0.5)

        progreso_total += progreso_tema_total

    return progreso_total / temas.count()

class LeccionListView(APIView):
    """
    Vista para listar todas las lecciones disponibles.
    Endpoint: GET /api/lecciones/
    """
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        # OPTIMIZADO: Prefetch progresos para evitar N+1 queries
        lecciones = Leccion.objects.filter(is_active=True).prefetch_related(
            models.Prefetch(
                'progreso_usuarios',
                queryset=ProgresoLeccion.objects.filter(usuario=request.user),
                to_attr='progreso_usuario'
            )
        ).order_by('orden')

        # Obtener el progreso del usuario para cada lección
        lecciones_data = []
        for leccion in lecciones:
            # Obtener progreso (ya está prefetched)
            progreso = leccion.progreso_usuario[0] if leccion.progreso_usuario else None

            serializer = LeccionListSerializer(leccion)
            leccion_dict = serializer.data

            if progreso:
                leccion_dict['progreso'] = {
                    'estado': progreso.estado,
                    'porcentaje_completado': float(progreso.porcentaje_completado)
                }
            else:
                leccion_dict['progreso'] = {
                    'estado': 'SIN_INICIAR',
                    'porcentaje_completado': 0.0
                }

            lecciones_data.append(leccion_dict)

        return Response(lecciones_data, status=status.HTTP_200_OK)




class LeccionDetailView(APIView):
    """
    Vista para obtener el detalle de una lección y sus temas.
    Endpoint: GET /api/lecciones/<id>/
    FIX: Usa serializer actualizado que incluye progreso con contenidos_vistos.
    """
    permission_classes = [IsAuthenticated]
   
    def get(self, request, leccion_id):
        leccion = get_object_or_404(Leccion, id=leccion_id, is_active=True)
       
        # Crear o actualizar progreso de la lección
        progreso_leccion, created = ProgresoLeccion.objects.get_or_create(
            usuario=request.user,
            leccion=leccion,
            defaults={'estado': 'INICIADA', 'fecha_inicio': timezone.now()}
        )
       
        if created or progreso_leccion.estado == 'SIN_INICIAR':
            progreso_leccion.estado = 'INICIADA'
            if not progreso_leccion.fecha_inicio:
                progreso_leccion.fecha_inicio = timezone.now()
            progreso_leccion.save()
       
        # Desbloquear primer tema si no está desbloqueado
        primer_tema = leccion.temas.filter(is_active=True).order_by('orden').first()
        if primer_tema:
            progreso_primer_tema, _ = ProgresoTema.objects.get_or_create(
                usuario=request.user,
                tema=primer_tema
            )
            if not progreso_primer_tema.desbloqueado:
                progreso_primer_tema.desbloqueado = True
                progreso_primer_tema.save()
       
        # Serializar con contexto para incluir progreso
        serializer = LeccionDetailSerializer(leccion, context={'request': request})
        leccion_data = serializer.data
       
        leccion_data['progreso'] = {
            'estado': progreso_leccion.estado,
            'porcentaje_completado': float(progreso_leccion.porcentaje_completado)
        }
       
        return Response(leccion_data, status=status.HTTP_200_OK)




class TemaDetailView(APIView):
    """
    Vista para obtener el contenido completo de un tema.
    Endpoint: GET /api/temas/<id>/
    """
    permission_classes = [IsAuthenticated]
   
    def get(self, request, tema_id):
        tema = get_object_or_404(Tema, id=tema_id, is_active=True)
       
        # Verificar que el tema esté desbloqueado
        progreso_tema, created = ProgresoTema.objects.get_or_create(
            usuario=request.user,
            tema=tema
        )
       
        if not progreso_tema.desbloqueado and tema.orden != 1:
            return Response(
                {'error': 'Este tema aún no está desbloqueado'},
                status=status.HTTP_403_FORBIDDEN
            )
       
        # Actualizar estado si es necesario
        if progreso_tema.estado == 'SIN_INICIAR':
            progreso_tema.estado = 'INICIADO'
            progreso_tema.fecha_inicio = timezone.now()
            progreso_tema.save()
       
        # Serializar el tema
        serializer = TemaDetailSerializer(tema)
        tema_data = serializer.data
       
        # Obtener respuestas previas
        respuestas_previas = RespuestaEjercicio.objects.filter(
            usuario=request.user,
            progreso_tema=progreso_tema
        ).select_related('ejercicio')
       
        # Crear diccionario de ejercicios respondidos
        ejercicios_respondidos = {}
        for respuesta in respuestas_previas:
            ejercicios_respondidos[respuesta.ejercicio.id] = {
                'respuesta': respuesta.respuesta_usuario,
                'es_correcta': respuesta.es_correcta,
                'uso_ayuda': respuesta.uso_ayuda
            }
       
        # Determinar índice del siguiente ejercicio sin responder
        siguiente_ejercicio_index = 0
        for idx, ejercicio in enumerate(tema_data['ejercicios']):
            if ejercicio['id'] not in ejercicios_respondidos:
                siguiente_ejercicio_index = idx
                break
       
        # Si todos están respondidos, mantener en el primero
        if len(ejercicios_respondidos) == len(tema_data['ejercicios']):
            siguiente_ejercicio_index = 0
       
        # Agregar información de progreso
        tema_data['ejercicios_respondidos'] = ejercicios_respondidos
        tema_data['siguiente_ejercicio_index'] = siguiente_ejercicio_index
        tema_data['total_ejercicios_respondidos'] = len(ejercicios_respondidos)

        # Agregar información de aprobación del tema
        tema_data['progreso'] = {
            'estado': progreso_tema.estado,
            'porcentaje_acierto': float(progreso_tema.porcentaje_acierto) if progreso_tema.porcentaje_acierto else 0.0,
            'aprobado': progreso_tema.estado == 'COMPLETADO',  # Tema aprobado si está completado
        }

        return Response(tema_data, status=status.HTTP_200_OK)




class RegistrarContenidoVistoView(APIView):
    """
    NUEVA VISTA: Registra cuando un usuario ve un contenido.
    Endpoint: POST /api/contenido/<id>/visto/
   
    FIX: Solo registra si NO es EJEMPLO_EXTRA.
    """
    permission_classes = [IsAuthenticated]
   
    def post(self, request, contenido_id):
        try:
            contenido = get_object_or_404(ContenidoTema, id=contenido_id)
           
            # Obtener o crear progreso del tema
            progreso_tema, _ = ProgresoTema.objects.get_or_create(
                usuario=request.user,
                tema=contenido.tema,
                defaults={
                    'desbloqueado': True,
                    'estado': 'INICIADO',
                    'fecha_inicio': timezone.now()
                }
            )
           
            # IMPORTANTE: Solo registrar si NO es EJEMPLO_EXTRA
            if contenido.tipo != 'EJEMPLO_EXTRA':
                # Agregar a contenidos vistos (si no está ya)
                progreso_tema.contenidos_vistos.add(contenido)
               
                # Calcular progreso
                porcentaje_progreso = progreso_tema.calcular_progreso_contenido()
                
                # Actualizar progreso de la lección
                progreso_leccion, _ = ProgresoLeccion.objects.get_or_create(
                    usuario=request.user,
                    leccion=contenido.tema.leccion
                )
                progreso_leccion.porcentaje_completado = calcular_porcentaje_leccion(
                    request.user,
                    contenido.tema.leccion
                )
                if progreso_leccion.estado == 'SIN_INICIAR':
                    progreso_leccion.estado = 'EN_PROGRESO'
                    progreso_leccion.fecha_inicio = timezone.now()
                progreso_leccion.save()
               
                return Response({
                    'mensaje': 'Contenido registrado como visto',
                    'progreso_contenido': porcentaje_progreso,
                    'contenidos_vistos': progreso_tema.contenido_completado,
                    'contenidos_totales': progreso_tema.contenidos_count,
                    'porcentaje_leccion':float(progreso_leccion.porcentaje_completado)
                }, status=status.HTTP_200_OK)
            else:
                # EJEMPLO_EXTRA: no registrar
                return Response({
                    'mensaje': 'EJEMPLO_EXTRA no cuenta para progreso',
                    'progreso_contenido': progreso_tema.calcular_progreso_contenido(),
                    'contenidos_vistos': progreso_tema.contenido_completado,
                    'contenidos_totales': progreso_tema.contenidos_count
                }, status=status.HTTP_200_OK)
           
        except Exception as e:
            return Response(
                {'error': f'Error al registrar contenido: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )








class ValidarRespuestaView(APIView):
    """
    Vista para validar la respuesta de un ejercicio.
    Endpoint: POST /api/ejercicios/validar/
    Rate limited: 20 requests per minute
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ValidarRespuestaThrottle]
   
    def post(self, request):
        try:
            serializer = EjercicioValidacionSerializer(data=request.data)
           
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
            ejercicio_id = serializer.validated_data['ejercicio_id']
            respuesta_usuario = serializer.validated_data['respuesta']
            uso_ayuda = serializer.validated_data.get('uso_ayuda', False)
            tiempo_respuesta = serializer.validated_data.get('tiempo_respuesta_segundos', 0)
           
            # Obtener ejercicio
            try:
                ejercicio = Ejercicio.objects.get(id=ejercicio_id)
            except Ejercicio.DoesNotExist:
                return Response(
                    {'error': 'Ejercicio no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
           
            # Obtener o crear progreso del tema
            progreso_tema, created = ProgresoTema.objects.get_or_create(
                usuario=request.user,
                tema=ejercicio.tema,
                defaults={
                    'desbloqueado': True,
                    'estado': 'INICIADO',
                    'fecha_inicio': timezone.now()
                }
            )
           
            # Si el progreso ya existía pero no tenía fecha de inicio, establecerla
            if not created and not progreso_tema.fecha_inicio:
                progreso_tema.fecha_inicio = timezone.now()
                progreso_tema.estado = 'INICIADO'
                progreso_tema.save()
           
            # Validar respuesta
            es_correcta = ejercicio.validar_respuesta(respuesta_usuario)
           
            # Verificar si ya existe una respuesta para este ejercicio en el progreso actual
            respuesta_existente = RespuestaEjercicio.objects.filter(
                usuario=request.user,
                ejercicio=ejercicio,
                progreso_tema=progreso_tema
            ).first()
           
            if respuesta_existente:
                # Ya existe una respuesta, devolver el resultado anterior
                response_data = {
                    'es_correcta': respuesta_existente.es_correcta,
                }
               
                if respuesta_existente.es_correcta and ejercicio.retroalimentacion_correcta:
                    response_data['retroalimentacion'] = ejercicio.retroalimentacion_correcta
                elif not respuesta_existente.es_correcta and ejercicio.retroalimentacion_incorrecta:
                    response_data['retroalimentacion'] = ejercicio.retroalimentacion_incorrecta
               
                return Response(response_data, status=status.HTTP_200_OK)
           
            # Registrar nueva respuesta
            RespuestaEjercicio.objects.create(
                usuario=request.user,
                ejercicio=ejercicio,
                progreso_tema=progreso_tema,
                respuesta_usuario=respuesta_usuario,
                es_correcta=es_correcta,
                uso_ayuda=uso_ayuda,
                tiempo_respuesta_segundos=tiempo_respuesta
            )
           
            # Preparar respuesta
            response_data = {
                'es_correcta': es_correcta,
            }
           
            # Agregar retroalimentación si existe
            if es_correcta and ejercicio.retroalimentacion_correcta:
                response_data['retroalimentacion'] = ejercicio.retroalimentacion_correcta
            elif not es_correcta and ejercicio.retroalimentacion_incorrecta:
                response_data['retroalimentacion'] = ejercicio.retroalimentacion_incorrecta
           
            return Response(response_data, status=status.HTTP_200_OK)
           
        except Exception as e:
            # Log del error para debugging
            import traceback
            print("=" * 80)
            print("ERROR EN VALIDAR RESPUESTA:")
            print(f"Usuario: {request.user.username}")
            print(f"Ejercicio ID: {request.data.get('ejercicio_id')}")
            print(f"Respuesta: {request.data.get('respuesta')}")
            print(f"Error: {str(e)}")
            print(traceback.format_exc())
            print("=" * 80)
           
            return Response(
                {'error': f'Error al procesar respuesta: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class FinalizarTemaView(APIView):
    """
    Vista para finalizar un tema y calcular el progreso.
    Endpoint: POST /api/temas/<id>/finalizar/
    """
    permission_classes = [IsAuthenticated]
   
    @transaction.atomic
    def post(self, request, tema_id):
        try:
            tema = get_object_or_404(Tema, id=tema_id, is_active=True)

            # PROTECCIÓN: Bloquear progreso_tema para evitar race conditions
            # select_for_update() bloquea el registro hasta que termine la transacción
            try:
                progreso_tema = ProgresoTema.objects.select_for_update().get(
                    usuario=request.user,
                    tema=tema
                )
            except ProgresoTema.DoesNotExist:
                progreso_tema = ProgresoTema.objects.create(
                    usuario=request.user,
                    tema=tema,
                    desbloqueado=True,
                    estado='INICIADO',
                    fecha_inicio=timezone.now()
                )
           
            # Obtener todas las respuestas del usuario para este tema
            respuestas = RespuestaEjercicio.objects.filter(
                usuario=request.user,
                progreso_tema=progreso_tema
            )

            # MateLog-AE: Calcular total de ejercicios según grupo del usuario
            try:
                perfil = request.user.perfil
                grupo = perfil.grupo

                if grupo == 'CONTROL':
                    # Control: solo ejercicios obligatorios
                    total_ejercicios = tema.ejercicios.filter(obligatorio=True).count()

                elif grupo == 'EXPERIMENTAL':
                    # Experimental: ejercicios basados en clasificación de autoeficacia
                    clasificacion = perfil.clasificacion_autoeficacia
                    ejercicios_query = tema.ejercicios.filter(obligatorio=True)

                    if clasificacion == 'ALTO':
                        ejercicios_adicionales = tema.ejercicios.filter(
                            obligatorio=False,
                            dificultad__in=['INTERMEDIO', 'DIFICIL']
                        )
                        total_ejercicios = (ejercicios_query | ejercicios_adicionales).distinct().count()
                    elif clasificacion == 'MEDIO':
                        ejercicios_adicionales = tema.ejercicios.filter(
                            obligatorio=False,
                            dificultad='INTERMEDIO'
                        )
                        total_ejercicios = (ejercicios_query | ejercicios_adicionales).distinct().count()
                    elif clasificacion == 'BAJO':
                        ejercicios_adicionales = tema.ejercicios.filter(
                            obligatorio=False,
                            dificultad__in=['FACIL', 'INTERMEDIO']
                        )
                        total_ejercicios = (ejercicios_query | ejercicios_adicionales).distinct().count()
                    else:
                        # Sin clasificación: solo obligatorios
                        total_ejercicios = ejercicios_query.count()
                else:
                    # Sin grupo: todos los ejercicios
                    total_ejercicios = tema.ejercicios.count()

            except AttributeError:
                # Usuario sin perfil: todos los ejercicios
                total_ejercicios = tema.ejercicios.count()

            # Calcular estadísticas
            ejercicios_correctos = respuestas.filter(es_correcta=True).count()
            ejercicios_incorrectos = respuestas.filter(es_correcta=False).count()
            ejercicios_con_ayuda = respuestas.filter(uso_ayuda=True).count()
           
            # Calcular porcentaje de aciertos
            if total_ejercicios > 0:
                porcentaje_acierto = (ejercicios_correctos / total_ejercicios) * 100
            else:
                porcentaje_acierto = 0
           
            # Calcular tiempos
            tiempo_total_segundos = respuestas.aggregate(
                total=models.Sum('tiempo_respuesta_segundos')
            )['total'] or 0
           
            tiempo_promedio_por_ejercicio = (
                tiempo_total_segundos // total_ejercicios if total_ejercicios > 0 else 0
            )
           
            # Determinar si aprobó (80% o más)
            aprobado = porcentaje_acierto >= 80
           
            # Incrementar contador de intentos
            progreso_tema.intentos_realizados += 1
           
            # Actualizar progreso del tema
            progreso_tema.porcentaje_acierto = porcentaje_acierto
           
            siguiente_tema_id = None
            siguiente_tema_info = None
           
            if aprobado:
                progreso_tema.estado = 'COMPLETADO'
                progreso_tema.fecha_completado = timezone.now()
               
                # Desbloquear el siguiente tema
                siguiente_tema = Tema.objects.filter(
                    leccion=tema.leccion,
                    orden=tema.orden + 1,
                    is_active=True
                ).first()
               
                if siguiente_tema:
                    ProgresoTema.objects.get_or_create(
                        usuario=request.user,
                        tema=siguiente_tema,
                        defaults={'desbloqueado': True}
                    )
                    siguiente_tema_id = siguiente_tema.id
                    siguiente_tema_info = {
                        'id': siguiente_tema.id,
                        'titulo': siguiente_tema.titulo,
                        'orden': siguiente_tema.orden
                    }
               
                # Actualizar progreso de la lección
                progreso_leccion, _ = ProgresoLeccion.objects.get_or_create(
                    usuario=request.user,
                    leccion=tema.leccion
                )
               
                temas_totales = tema.leccion.temas.filter(is_active=True).count()
                temas_completados = ProgresoTema.objects.filter(
                    usuario=request.user,
                    tema__leccion=tema.leccion,
                    estado='COMPLETADO'
                ).count()
               
                if temas_totales > 0:
                    progreso_leccion.porcentaje_completado = calcular_porcentaje_leccion(
                        request.user,
                        tema.leccion
                    )
               
                if temas_completados == temas_totales:
                    progreso_leccion.estado = 'COMPLETADA'
                    progreso_leccion.fecha_completado = timezone.now()
               
                progreso_leccion.save()
           
            progreso_tema.save()
           
            return Response({
                'aprobado': aprobado,
                'porcentaje_acierto': float(porcentaje_acierto),
                'ejercicios_correctos': ejercicios_correctos,
                'ejercicios_totales': total_ejercicios,
                'leccion_id': tema.leccion.id,
                'tema_id': tema.id,
                'siguiente_tema_id': siguiente_tema_id,
                'siguiente_tema': siguiente_tema_info,
                'numero_intento': progreso_tema.intentos_realizados,
            }, status=status.HTTP_200_OK)
           
        except Exception as e:
            import traceback
            print("=" * 80)
            print("ERROR EN FINALIZAR TEMA:")
            print(f"Usuario: {request.user.username}")
            print(f"Tema ID: {tema_id}")
            print(f"Error: {str(e)}")
            print(traceback.format_exc())
            print("=" * 80)
           
            return Response(
                {'error': f'Error al finalizar tema: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class VolverAlTemaView(APIView):
    """
    Vista para registrar cuando un usuario vuelve desde ejercicios al contenido del tema.
    Endpoint: POST /api/temas/<id>/volver/
    """
    permission_classes = [IsAuthenticated]
   
    def post(self, request, tema_id):
        tema = get_object_or_404(Tema, id=tema_id, is_active=True)
       
        # Simplemente confirmamos que el usuario puede volver
        # No hacemos cambios en el progreso
       
        return Response({
            'mensaje': 'Puede volver al contenido del tema',
            'tema_id': tema.id
        }, status=status.HTTP_200_OK)




class ReintentarTemaView(APIView):
    """
    Vista para reintentar un tema.
    Borra las respuestas del intento actual y resetea el progreso.
    Endpoint: POST /api/temas/<id>/reintentar/
    """
    permission_classes = [IsAuthenticated]
   
    def post(self, request, tema_id):
        try:
            tema = get_object_or_404(Tema, id=tema_id, is_active=True)
           
            # Obtener progreso del tema
            progreso_tema = get_object_or_404(
                ProgresoTema,
                usuario=request.user,
                tema=tema
            )
           
            # Borrar todas las respuestas del intento actual
            RespuestaEjercicio.objects.filter(
                usuario=request.user,
                progreso_tema=progreso_tema
            ).delete()
           
            # Resetear estado del progreso (no incrementar intentos aún)
            progreso_tema.estado = 'INICIADO'
            progreso_tema.fecha_inicio = timezone.now()
            # NO modificar intentos_realizados aquí, se incrementa en finalizar
            progreso_tema.save()
           
            return Response({
                'mensaje': 'Tema reiniciado correctamente',
                'tema_id': tema.id
            }, status=status.HTTP_200_OK)
           
        except Exception as e:
            import traceback
            print("=" * 80)
            print("ERROR EN REINTENTAR TEMA:")
            print(f"Usuario: {request.user.username}")
            print(f"Tema ID: {tema_id}")
            print(f"Error: {str(e)}")
            print(traceback.format_exc())
            print("=" * 80)
           
            return Response(
                {'error': f'Error al reintentar tema: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


