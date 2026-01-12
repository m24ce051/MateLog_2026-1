# lessons/urls.py
from django.urls import path
from .views import (
    LeccionListView,
    LeccionDetailView,
    TemaDetailView,
    ValidarRespuestaView,
    FinalizarTemaView,
    VolverAlTemaView,
    ReintentarTemaView,
    RegistrarContenidoVistoView,  # NUEVO
)


urlpatterns = [
    # Lecciones
    path('lecciones/', LeccionListView.as_view(), name='leccion-list'),
    path('lecciones/<int:leccion_id>/', LeccionDetailView.as_view(), name='leccion-detail'),
   
    # Temas
    path('temas/<int:tema_id>/', TemaDetailView.as_view(), name='tema-detail'),
    path('temas/<int:tema_id>/finalizar/', FinalizarTemaView.as_view(), name='finalizar-tema'),
    path('temas/<int:tema_id>/reintentar/', ReintentarTemaView.as_view(), name='reintentar-tema'),
    path('temas/<int:tema_id>/volver/', VolverAlTemaView.as_view(), name='volver-tema'),
   
    # Contenido (NUEVO)
    path('contenido/<int:contenido_id>/visto/', RegistrarContenidoVistoView.as_view(), name='registrar-contenido-visto'),
   
    # Ejercicios
    path('ejercicios/validar/', ValidarRespuestaView.as_view(), name='validar-ejercicio'),
]


