# ml_adaptive/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
import re
from difflib import SequenceMatcher

from .models import PerfilUsuario, RespuestaEscala, RespuestaExamenAbierta
from users.models import CustomUser


# Preguntas de la Escala de Autoeficacia General (General Self-Efficacy Scale - GSE)
# Basada en Schwarzer & Jerusalem (1995)
PREGUNTAS_AUTOEFICACIA = [
    {
        'numero': 1,
        'texto': 'Puedo encontrar la manera de obtener lo que quiero, aunque alguien se me oponga.'
    },
    {
        'numero': 2,
        'texto': 'Puedo resolver problemas difíciles si me esfuerzo lo suficiente.'
    },
    {
        'numero': 3,
        'texto': 'Me es fácil persistir en lo que me he propuesto hasta llegar a alcanzar mis metas.'
    },
    {
        'numero': 4,
        'texto': 'Tengo confianza en que podría manejar eficazmente eventos inesperados.'
    },
    {
        'numero': 5,
        'texto': 'Gracias a mis cualidades y recursos puedo superar situaciones imprevistas.'
    },
    {
        'numero': 6,
        'texto': 'Cuando me encuentro en dificultades puedo permanecer tranquilo/a porque cuento con las habilidades necesarias para manejar situaciones difíciles.'
    },
    {
        'numero': 7,
        'texto': 'Venga lo que venga, por lo general soy capaz de manejarlo.'
    },
    {
        'numero': 8,
        'texto': 'Puedo resolver la mayoría de los problemas si me esfuerzo lo necesario.'
    },
    {
        'numero': 9,
        'texto': 'Si me encuentro en una situación difícil, generalmente se me ocurre qué debo hacer.'
    },
    {
        'numero': 10,
        'texto': 'Al enfrentarme a un problema, generalmente se me ocurren varias alternativas de cómo resolverlo.'
    },
]

# Opciones Likert para autoeficacia (1-4)
OPCIONES_AUTOEFICACIA = [
    {'valor': 1, 'etiqueta': 'Nunca'},
    {'valor': 2, 'etiqueta': 'Algunas veces'},
    {'valor': 3, 'etiqueta': 'Muchas veces'},
    {'valor': 4, 'etiqueta': 'Siempre'},
]


class ObtenerPreguntasAutoeficaciaView(APIView):
    """
    Vista para obtener las preguntas de la escala de autoeficacia.
    Endpoint: GET /api/ml-adaptive/autoeficacia/preguntas/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retorna las preguntas y opciones de la escala de autoeficacia."""
        return Response({
            'preguntas': PREGUNTAS_AUTOEFICACIA,
            'opciones': OPCIONES_AUTOEFICACIA,
            'instrucciones': 'Lee cada afirmación y selecciona la opción que mejor describa tu nivel de acuerdo con cada una. No hay respuestas correctas o incorrectas.'
        }, status=status.HTTP_200_OK)


class GuardarRespuestasAutoeficaciaView(APIView):
    """
    Vista para guardar respuestas de autoeficacia y calcular clasificación.
    Endpoint: POST /api/ml-adaptive/autoeficacia/guardar/
    """
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        """
        Guarda las respuestas de autoeficacia y calcula la clasificación.

        Body esperado:
        {
            "tipo": "PRE" o "POST",
            "respuestas": [
                {"pregunta_numero": 1, "respuesta": 3},
                {"pregunta_numero": 2, "respuesta": 4},
                ...
            ]
        }
        """
        tipo = request.data.get('tipo', 'PRE')
        respuestas = request.data.get('respuestas', [])

        if not respuestas or len(respuestas) != 10:
            return Response({
                'error': 'Se requieren exactamente 10 respuestas'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validar que todas las respuestas estén en el rango 1-4
        for resp in respuestas:
            if not (1 <= resp.get('respuesta', 0) <= 4):
                return Response({
                    'error': 'Todas las respuestas deben estar entre 1 y 4'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Obtener perfil del usuario
        try:
            perfil = request.user.perfil
        except PerfilUsuario.DoesNotExist:
            return Response({
                'error': 'El usuario no tiene un perfil de MateLog-AE. Debe registrarse con un código de acceso.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Determinar tipo de escala
        tipo_escala = 'AUTOEFICACIA_PRE' if tipo == 'PRE' else 'AUTOEFICACIA_POST'

        # Guardar respuestas
        for resp in respuestas:
            RespuestaEscala.objects.update_or_create(
                usuario=request.user,
                tipo_escala=tipo_escala,
                pregunta_numero=resp['pregunta_numero'],
                defaults={'respuesta': resp['respuesta']}
            )

        # Calcular puntaje total (suma de todas las respuestas)
        puntaje_total = sum(r['respuesta'] for r in respuestas)

        # Clasificar según puntaje (escala de 10-40)
        # Basado en terciles aproximados
        if puntaje_total >= 35:  # 87.5% o más
            clasificacion = 'ALTO'
        elif puntaje_total >= 28:  # 70% o más
            clasificacion = 'MEDIO'
        else:
            clasificacion = 'BAJO'

        # Si es PRE-test, actualizar clasificación del perfil (solo la primera vez)
        if tipo == 'PRE' and not perfil.clasificacion_autoeficacia:
            perfil.clasificacion_autoeficacia = clasificacion
            perfil.completo_autoeficacia_pre = True
            perfil.save()

        # Si es POST-test, solo marcar como completado
        if tipo == 'POST':
            perfil.completo_autoeficacia_post = True
            perfil.save()

        return Response({
            'mensaje': f'Respuestas de autoeficacia {tipo.lower()}-test guardadas exitosamente',
            'puntaje_total': puntaje_total,
            'clasificacion': clasificacion,
            'tipo': tipo,
            'puede_continuar': True
        }, status=status.HTTP_201_CREATED)


class ObtenerEstadoEvaluacionesView(APIView):
    """
    Vista para obtener el estado de completitud de las evaluaciones del usuario.
    Endpoint: GET /api/ml-adaptive/estado-evaluaciones/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retorna qué evaluaciones ha completado el usuario."""
        try:
            perfil = request.user.perfil

            return Response({
                'completo_autoeficacia_pre': perfil.completo_autoeficacia_pre,
                'completo_diagnostico': perfil.completo_diagnostico,
                'completo_autoeficacia_post': perfil.completo_autoeficacia_post,
                'completo_final': perfil.completo_final,
                'clasificacion_autoeficacia': perfil.clasificacion_autoeficacia,
                'grupo': perfil.grupo,
                'puede_acceder_lecciones': perfil.completo_autoeficacia_pre and perfil.completo_diagnostico
            }, status=status.HTTP_200_OK)

        except PerfilUsuario.DoesNotExist:
            return Response({
                'error': 'El usuario no tiene un perfil de MateLog-AE'
            }, status=status.HTTP_404_NOT_FOUND)


class GuardarRespuestasExamenView(APIView):
    """
    Vista para guardar respuestas de examen diagnóstico o final.
    Endpoint: POST /api/ml-adaptive/examen/guardar/
    """
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        """
        Guarda las respuestas del examen diagnóstico o final.

        Body esperado:
        {
            "tipo": "DIAGNOSTICO" o "FINAL",
            "respuestas": [
                {"pregunta_numero": 1, "correcta": true},
                {"pregunta_numero": 2, "correcta": false},
                ...
            ]
        }
        """
        tipo = request.data.get('tipo', 'DIAGNOSTICO')
        respuestas = request.data.get('respuestas', [])

        if not respuestas:
            return Response({
                'error': 'Se requieren las respuestas del examen'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Obtener perfil del usuario
        try:
            perfil = request.user.perfil
        except PerfilUsuario.DoesNotExist:
            return Response({
                'error': 'El usuario no tiene un perfil de MateLog-AE'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Guardar respuestas (1 = correcta, 0 = incorrecta)
        for resp in respuestas:
            RespuestaEscala.objects.update_or_create(
                usuario=request.user,
                tipo_escala=tipo,
                pregunta_numero=resp['pregunta_numero'],
                defaults={'respuesta': 1 if resp.get('correcta', False) else 0}
            )

        # Calcular puntaje
        total_preguntas = len(respuestas)
        correctas = sum(1 for r in respuestas if r.get('correcta', False))
        porcentaje = (correctas / total_preguntas * 100) if total_preguntas > 0 else 0

        # Actualizar perfil
        if tipo == 'DIAGNOSTICO':
            perfil.completo_diagnostico = True
        else:  # FINAL
            perfil.completo_final = True

        perfil.save()

        return Response({
            'mensaje': f'Examen {tipo.lower()} guardado exitosamente',
            'total_preguntas': total_preguntas,
            'respuestas_correctas': correctas,
            'porcentaje': round(porcentaje, 2),
            'tipo': tipo
        }, status=status.HTTP_201_CREATED)


# ========== PREGUNTAS DEL EXAMEN FINAL CON RESPUESTAS ABIERTAS ==========

PREGUNTAS_EXAMEN_FINAL_ABIERTO = [
    {
        'numero': 1,
        'texto': '¿Qué es una proposición lógica y cuál es su importancia en matemáticas?',
        'respuesta_esperada': 'Una proposición lógica es una afirmación que puede ser verdadera o falsa, pero no ambas. Es importante en matemáticas porque permite construir razonamientos formales y demostrar teoremas mediante el uso de reglas lógicas.'
    },
    {
        'numero': 2,
        'texto': 'Explica con tus propias palabras la diferencia entre una tautología y una contradicción.',
        'respuesta_esperada': 'Una tautología es una proposición que siempre es verdadera sin importar los valores de verdad de sus componentes. Una contradicción es una proposición que siempre es falsa. La tautología representa verdades universales mientras que la contradicción representa imposibilidades lógicas.'
    },
    {
        'numero': 3,
        'texto': 'Define qué es un conjunto y da un ejemplo de la vida cotidiana.',
        'respuesta_esperada': 'Un conjunto es una colección bien definida de objetos distintos llamados elementos. Por ejemplo, el conjunto de frutas en una canasta: {manzana, pera, naranja}, donde cada fruta es un elemento del conjunto.'
    },
    {
        'numero': 4,
        'texto': '¿Cuál es la diferencia entre una función inyectiva y una función sobreyectiva?',
        'respuesta_esperada': 'Una función inyectiva asigna elementos diferentes del dominio a elementos diferentes del codominio, es decir, no hay dos elementos que tengan la misma imagen. Una función sobreyectiva cubre todo el codominio, cada elemento del codominio tiene al menos una preimagen en el dominio.'
    },
    {
        'numero': 5,
        'texto': 'Explica el principio de inducción matemática en tus propias palabras.',
        'respuesta_esperada': 'La inducción matemática es un método de demostración que funciona en dos pasos: primero se demuestra que una propiedad es verdadera para un caso base (usualmente n=1), luego se demuestra que si es verdadera para n=k, también es verdadera para n=k+1. Esto garantiza que la propiedad es verdadera para todos los números naturales.'
    },
]


def calcular_similitud_texto(texto1, texto2):
    """
    Calcula la similitud entre dos textos usando SequenceMatcher.
    Retorna un porcentaje de similitud (0-100).
    """
    # Normalizar textos: minúsculas y eliminar puntuación extra
    def normalizar(texto):
        texto = texto.lower().strip()
        # Eliminar puntuación múltiple
        texto = re.sub(r'[.,;:!?]+', ' ', texto)
        # Eliminar espacios múltiples
        texto = re.sub(r'\s+', ' ', texto)
        return texto

    texto1_norm = normalizar(texto1)
    texto2_norm = normalizar(texto2)

    # Calcular similitud usando SequenceMatcher
    similitud = SequenceMatcher(None, texto1_norm, texto2_norm).ratio()

    # Convertir a porcentaje
    return round(similitud * 100, 2)


class ObtenerPreguntasExamenAbiertoView(APIView):
    """
    Vista para obtener las preguntas del examen final con respuestas abiertas.
    Endpoint: GET /api/ml-adaptive/examen-abierto/preguntas/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retorna las preguntas del examen final abierto."""
        # Solo enviar número y texto, NO la respuesta esperada
        preguntas_publicas = [
            {
                'numero': p['numero'],
                'texto': p['texto']
            }
            for p in PREGUNTAS_EXAMEN_FINAL_ABIERTO
        ]

        return Response({
            'preguntas': preguntas_publicas,
            'instrucciones': 'Responde cada pregunta con tus propias palabras. Tus respuestas serán evaluadas automáticamente y revisadas por el instructor.',
            'total_preguntas': len(preguntas_publicas)
        }, status=status.HTTP_200_OK)


class GuardarRespuestasExamenAbiertoView(APIView):
    """
    Vista para guardar respuestas del examen final abierto.
    Endpoint: POST /api/ml-adaptive/examen-abierto/guardar/
    """
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        """
        Guarda las respuestas del examen abierto y las evalúa automáticamente.

        Body esperado:
        {
            "respuestas": [
                {"pregunta_numero": 1, "respuesta": "texto de la respuesta..."},
                {"pregunta_numero": 2, "respuesta": "texto de la respuesta..."},
                ...
            ]
        }
        """
        respuestas = request.data.get('respuestas', [])

        if not respuestas:
            return Response({
                'error': 'Se requieren las respuestas del examen'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Obtener perfil del usuario
        try:
            perfil = request.user.perfil
        except PerfilUsuario.DoesNotExist:
            return Response({
                'error': 'El usuario no tiene un perfil de MateLog-AE'
            }, status=status.HTTP_400_BAD_REQUEST)

        resultados = []
        total_similitud = 0

        # Procesar cada respuesta
        for resp in respuestas:
            pregunta_num = resp.get('pregunta_numero')
            respuesta_estudiante = resp.get('respuesta', '').strip()

            # Buscar la pregunta correspondiente
            pregunta_data = next(
                (p for p in PREGUNTAS_EXAMEN_FINAL_ABIERTO if p['numero'] == pregunta_num),
                None
            )

            if not pregunta_data:
                continue

            # Validar que la respuesta no esté vacía
            if len(respuesta_estudiante) < 10:
                return Response({
                    'error': f'La respuesta a la pregunta {pregunta_num} es demasiado corta. Escribe al menos 10 caracteres.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Calcular similitud con la respuesta esperada
            similitud = calcular_similitud_texto(
                respuesta_estudiante,
                pregunta_data['respuesta_esperada']
            )

            # Determinar aprobación automática (70% de similitud o más)
            aprobada_auto = similitud >= 70.0

            # Guardar en base de datos
            respuesta_obj, created = RespuestaExamenAbierta.objects.update_or_create(
                usuario=request.user,
                tipo_examen='FINAL',
                pregunta_numero=pregunta_num,
                defaults={
                    'pregunta_texto': pregunta_data['texto'],
                    'respuesta_esperada': pregunta_data['respuesta_esperada'],
                    'respuesta_estudiante': respuesta_estudiante,
                    'similitud_automatica': similitud,
                    'aprobada_automatica': aprobada_auto,
                    'estado_revision': 'PENDIENTE' if not aprobada_auto else 'APROBADA'
                }
            )

            resultados.append({
                'pregunta_numero': pregunta_num,
                'similitud': similitud,
                'aprobada_automaticamente': aprobada_auto
            })

            total_similitud += similitud

        # Calcular similitud promedio
        similitud_promedio = total_similitud / len(respuestas) if respuestas else 0

        # Contar respuestas aprobadas automáticamente
        aprobadas_auto = sum(1 for r in resultados if r['aprobada_automaticamente'])

        # Marcar examen final como completado
        perfil.completo_final = True
        perfil.save()

        return Response({
            'mensaje': 'Examen final enviado exitosamente',
            'total_preguntas': len(respuestas),
            'similitud_promedio': round(similitud_promedio, 2),
            'aprobadas_automaticamente': aprobadas_auto,
            'requiere_revision_manual': aprobadas_auto < len(respuestas),
            'nota': 'Tus respuestas han sido guardadas. El instructor revisará aquellas que requieran evaluación manual.'
        }, status=status.HTTP_201_CREATED)
