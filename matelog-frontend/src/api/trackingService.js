import api from './axios';


// Servicios de tracking
export const trackingService = {
  // ==================== ENDPOINTS ANTIGUOS (mantener compatibilidad) ====================

  // Iniciar tracking de una pantalla
  startActivity: async (activityData) => {
    const response = await api.post('/tracking/iniciar/', activityData);
    return response.data;
  },


  // Finalizar tracking de una pantalla
  endActivity: async (activityId) => {
    const response = await api.post('/tracking/finalizar/', { actividad_id: activityId });
    return response.data;
  },


  // Iniciar sesión de estudio
  startSession: async () => {
    const response = await api.post('/tracking/sesion/iniciar/');
    return response.data;
  },


  // Finalizar sesión de estudio
  endSession: async (sessionId) => {
    const response = await api.post('/tracking/sesion/finalizar/', { sesion_id: sessionId });
    return response.data;
  },


  // Obtener actividades del usuario
  getUserActivities: async () => {
    const response = await api.get('/tracking/actividades/');
    return response.data;
  },


  // Registrar click en botón "Volver" del contenido
  registerVolverContenido: async (activityId) => {
    const response = await api.post('/tracking/volver-contenido/', {
      actividad_id: activityId
    });
    return response.data;
  },


  // Registrar click en "Ver Otro Ejemplo"
  registerVerEjemploExtra: async (activityId) => {
    const response = await api.post('/tracking/ver-ejemplo-extra/', {
      actividad_id: activityId
    });
    return response.data;
  },


  // Registrar click en "Ir a Ejercicios" (directamente desde contenido)
  registerIrAEjercicios: async (activityId) => {
    const response = await api.post('/tracking/ir-a-ejercicios/', {
      actividad_id: activityId
    });
    return response.data;
  },

  // ==================== NUEVOS ENDPOINTS - Sistema de tracking mejorado ====================

  // Actualizar actividad de sesión (heartbeat cada 2 minutos)
  updateSessionActivity: async (sessionId) => {
    const response = await api.post('/tracking/sesion/actividad/', {
      sesion_id: sessionId
    });
    return response.data;
  },

  // Finalizar sesión con tipo de cierre mejorado
  endSessionImproved: async (sessionId, tipoCierre = 'LOGOUT') => {
    const response = await api.post('/tracking/sesion/finalizar-mejorada/', {
      sesion_id: sessionId,
      tipo_cierre: tipoCierre // LOGOUT, INACTIVIDAD, CIERRE_VENTANA
    });
    return response.data;
  },

  // Registrar tiempo en pantalla específica (Teoría, Ejemplo, Ejercicio)
  registerScreenTime: async (data) => {
    const response = await api.post('/tracking/tiempo-pantalla/', {
      tema_id: data.temaId,
      tipo_contenido: data.tipoContenido, // TEORIA, EJEMPLO, EJERCICIO
      numero: data.numero, // Número del contenido dentro del tema
      tiempo_segundos: data.tiempoSegundos,
      contenido_id: data.contenidoId, // Opcional
      ejercicio_id: data.ejercicioId, // Opcional
      cambio_pestana: data.cambioPestana || false
    });
    return response.data;
  },

  // Registrar clic en botón específico
  registerButtonClick: async (data) => {
    const response = await api.post('/tracking/clic-boton/', {
      tema_id: data.temaId,
      tipo_boton: data.tipoBoton // REGRESAR, IR_EJERCICIOS, VOLVER, OTRO_EJEMPLO, VER_AYUDA
    });
    return response.data;
  },
};


export default trackingService;


