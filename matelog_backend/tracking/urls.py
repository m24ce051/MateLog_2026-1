# tracking/urls.py
# ACTUALIZACIÓN: Agregar las nuevas rutas al archivo urls.py existente


from django.urls import path
from .views import (
    IniciarSesionView,
    FinalizarSesionView,
    IniciarActividadView,
    FinalizarActividadView,
    RegistrarVolverContenidoView,
    RegistrarVerEjemploExtraView,
    RegistrarIrAEjerciciosView,
    RegistrarEventoView,
    # NUEVAS VISTAS - Sistema de tracking mejorado
    ActualizarActividadSesionView,
    FinalizarSesionMejoradaView,
    RegistrarTiempoPantallaView,
    RegistrarClicBotonView,
)


urlpatterns = [
    # Sesiones de estudio (antiguos)
    path('sesion/iniciar/', IniciarSesionView.as_view(), name='iniciar-sesion'),
    path('sesion/finalizar/', FinalizarSesionView.as_view(), name='finalizar-sesion'),

    # Actividades de pantalla (antiguos)
    path('iniciar/', IniciarActividadView.as_view(), name='iniciar-actividad'),
    path('finalizar/', FinalizarActividadView.as_view(), name='finalizar-actividad'),

    # Tracking de navegación (antiguos)
    path('volver-contenido/', RegistrarVolverContenidoView.as_view(), name='volver-contenido'),
    path('ver-ejemplo-extra/', RegistrarVerEjemploExtraView.as_view(), name='ver-ejemplo-extra'),
    path('ir-a-ejercicios/', RegistrarIrAEjerciciosView.as_view(), name='ir-a-ejercicios'),
    path('evento/', RegistrarEventoView.as_view(), name='registrar-evento'),

    # ==================== NUEVAS RUTAS - Sistema de tracking mejorado ====================

    # Sesiones mejoradas
    path('sesion/actividad/', ActualizarActividadSesionView.as_view(), name='actualizar-actividad-sesion'),
    path('sesion/finalizar-mejorada/', FinalizarSesionMejoradaView.as_view(), name='finalizar-sesion-mejorada'),

    # Tracking de tiempo y clics
    path('tiempo-pantalla/', RegistrarTiempoPantallaView.as_view(), name='registrar-tiempo-pantalla'),
    path('clic-boton/', RegistrarClicBotonView.as_view(), name='registrar-clic-boton'),
]


