# tracking/admin_urls.py
# URLs para las vistas personalizadas del admin de tracking

from django.urls import path
from .admin_views import resumen_tiempos_view, resumen_clics_view

urlpatterns = [
    path('resumen-tiempos/', resumen_tiempos_view, name='admin_resumen_tiempos'),
    path('resumen-clics/', resumen_clics_view, name='admin_resumen_clics'),
]
