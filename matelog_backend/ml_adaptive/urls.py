# ml_adaptive/urls.py
from django.urls import path
from .views import (
    ObtenerPreguntasAutoeficaciaView,
    GuardarRespuestasAutoeficaciaView,
    ObtenerEstadoEvaluacionesView,
    GuardarRespuestasExamenView,
    ObtenerPreguntasExamenAbiertoView,
    GuardarRespuestasExamenAbiertoView,
)

urlpatterns = [
    # Autoeficacia
    path('autoeficacia/preguntas/', ObtenerPreguntasAutoeficaciaView.as_view(), name='obtener-preguntas-autoeficacia'),
    path('autoeficacia/guardar/', GuardarRespuestasAutoeficaciaView.as_view(), name='guardar-respuestas-autoeficacia'),

    # Estado de evaluaciones
    path('estado-evaluaciones/', ObtenerEstadoEvaluacionesView.as_view(), name='obtener-estado-evaluaciones'),

    # Exámenes (opción múltiple)
    path('examen/guardar/', GuardarRespuestasExamenView.as_view(), name='guardar-respuestas-examen'),

    # Examen final (respuestas abiertas)
    path('examen-abierto/preguntas/', ObtenerPreguntasExamenAbiertoView.as_view(), name='obtener-preguntas-examen-abierto'),
    path('examen-abierto/guardar/', GuardarRespuestasExamenAbiertoView.as_view(), name='guardar-respuestas-examen-abierto'),
]
