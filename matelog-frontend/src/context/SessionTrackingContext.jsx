import { createContext, useContext, useEffect, useRef, useState } from 'react';
import { useAuth } from './AuthContext';
import { trackingService } from '../api/trackingService';

const SessionTrackingContext = createContext(null);

// Inactivity timeout: 10 minutes
const SESSION_INACTIVITY_TIMEOUT = 10 * 60 * 1000;

export const SessionTrackingProvider = ({ children }) => {
  const { sessionId, isAuthenticated, logout } = useAuth();
  const heartbeatIntervalRef = useRef(null);
  const hasSetupBeforeUnload = useRef(false);
  const [lastActivity, setLastActivity] = useState(Date.now());

  // Configurar heartbeat cada 2 minutos
  useEffect(() => {
    if (!isAuthenticated || !sessionId) {
      return;
    }

    // Limpiar intervalo anterior si existe
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current);
    }

    // Configurar nuevo intervalo de heartbeat
    heartbeatIntervalRef.current = setInterval(async () => {
      try {
        await trackingService.updateSessionActivity(sessionId);
        console.log('Heartbeat enviado');
      } catch (error) {
        console.error('Error al enviar heartbeat:', error);
      }
    }, 2 * 60 * 1000); // 2 minutos

    // Cleanup al desmontar
    return () => {
      if (heartbeatIntervalRef.current) {
        clearInterval(heartbeatIntervalRef.current);
      }
    };
  }, [isAuthenticated, sessionId]);

  // Detectar cierre de ventana/pestaña
  useEffect(() => {
    if (!isAuthenticated || !sessionId || hasSetupBeforeUnload.current) {
      return;
    }

    const handleBeforeUnload = async (event) => {
      // Enviar señal de cierre de ventana
      try {
        // Usar sendBeacon para envío asíncrono durante unload
        const data = JSON.stringify({
          sesion_id: sessionId,
          tipo_cierre: 'CIERRE_VENTANA'
        });

        // Intentar con sendBeacon primero (más confiable durante unload)
        const blob = new Blob([data], { type: 'application/json' });
        const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const url = `${baseURL}/api/tracking/sesion/finalizar-mejorada/`;

        if (navigator.sendBeacon) {
          navigator.sendBeacon(url, blob);
        } else {
          // Fallback: request síncrona (no recomendado pero funcional)
          await trackingService.endSessionImproved(sessionId, 'CIERRE_VENTANA');
        }
      } catch (error) {
        console.error('Error al registrar cierre de ventana:', error);
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    hasSetupBeforeUnload.current = true;

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      hasSetupBeforeUnload.current = false;
    };
  }, [isAuthenticated, sessionId]);

  // Detectar cambio de pestaña (visibilitychange)
  useEffect(() => {
    if (!isAuthenticated) {
      return;
    }

    const handleVisibilityChange = () => {
      if (document.hidden) {
        console.log('Usuario cambió de pestaña (salió)');
        // Aquí se podría registrar que el usuario cambió de pestaña
        // pero NO finalizamos la sesión, solo lo registramos como información
      } else {
        console.log('Usuario volvió a la pestaña');
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [isAuthenticated]);

  // Detectar inactividad del usuario
  useEffect(() => {
    if (!isAuthenticated || !sessionId) {
      return;
    }

    // Resetear timer de actividad con eventos del usuario
    const resetTimer = () => {
      setLastActivity(Date.now());
    };

    // Escuchar eventos de actividad
    const events = ['mousemove', 'keypress', 'click', 'scroll', 'touchstart'];
    events.forEach(event => {
      window.addEventListener(event, resetTimer);
    });

    // Verificar inactividad cada minuto
    const inactivityCheckInterval = setInterval(async () => {
      const inactive = Date.now() - lastActivity;

      if (inactive > SESSION_INACTIVITY_TIMEOUT) {
        console.log('Usuario inactivo por 10 minutos, cerrando sesión...');

        // Finalizar sesión por inactividad
        try {
          if (sessionId) {
            await trackingService.endSessionImproved(sessionId, 'INACTIVIDAD');
          }
          logout();
        } catch (error) {
          console.error('Error al finalizar sesión por inactividad:', error);
          logout(); // Cerrar sesión de todas formas
        }
      }
    }, 60 * 1000); // Verificar cada minuto

    // Cleanup
    return () => {
      events.forEach(event => {
        window.removeEventListener(event, resetTimer);
      });
      clearInterval(inactivityCheckInterval);
    };
  }, [isAuthenticated, sessionId, lastActivity, logout]);

  return (
    <SessionTrackingContext.Provider value={{}}>
      {children}
    </SessionTrackingContext.Provider>
  );
};

export const useSessionTracking = () => {
  const context = useContext(SessionTrackingContext);
  if (!context) {
    throw new Error('useSessionTracking debe usarse dentro de un SessionTrackingProvider');
  }
  return context;
};

export default SessionTrackingContext;
