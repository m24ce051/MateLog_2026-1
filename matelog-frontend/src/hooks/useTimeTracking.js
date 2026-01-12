import { useEffect, useRef, useCallback } from 'react';
import { trackingService } from '../api/trackingService';

/**
 * Hook para tracking de tiempo en pantallas específicas (Teoría, Ejemplo, Ejercicio)
 * @param {object} config - Configuración del tracking
 * @param {number} config.temaId - ID del tema actual
 * @param {string} config.tipoContenido - TEORIA, EJEMPLO, o EJERCICIO
 * @param {number} config.numero - Número del contenido dentro del tema (1, 2, 3...)
 * @param {number} config.contenidoId - ID del contenido (opcional)
 * @param {number} config.ejercicioId - ID del ejercicio (opcional)
 * @param {boolean} config.enabled - Si el tracking está habilitado (default: true)
 */
export const useTimeTracking = (config) => {
  const {
    temaId,
    tipoContenido,
    numero,
    contenidoId,
    ejercicioId,
    enabled = true,
  } = config;

  const startTimeRef = useRef(null);
  const visibilityChangeTimeRef = useRef(null);
  const wasHiddenRef = useRef(false);

  // Función para registrar el tiempo transcurrido
  const registerTime = useCallback(async (cambioPestana = false) => {
    if (!startTimeRef.current || !enabled || !temaId) {
      return;
    }

    const endTime = Date.now();
    const tiempoSegundos = Math.floor((endTime - startTimeRef.current) / 1000);

    // Solo registrar si pasó al menos 1 segundo
    if (tiempoSegundos < 1) {
      return;
    }

    try {
      await trackingService.registerScreenTime({
        temaId,
        tipoContenido,
        numero,
        tiempoSegundos,
        contenidoId,
        ejercicioId,
        cambioPestana,
      });

      console.log(`Tiempo registrado: ${tiempoSegundos}s en ${tipoContenido} ${numero}`);

      // Reiniciar el contador para el siguiente registro
      startTimeRef.current = Date.now();
    } catch (error) {
      console.error('Error al registrar tiempo:', error);
    }
  }, [temaId, tipoContenido, numero, contenidoId, ejercicioId, enabled]);

  // Iniciar tracking al montar el componente
  useEffect(() => {
    if (!enabled || !temaId) {
      return;
    }

    startTimeRef.current = Date.now();
    console.log(`Iniciando tracking: ${tipoContenido} ${numero}`);

    // Cleanup al desmontar - registrar tiempo final
    return () => {
      registerTime(false);
    };
  }, [temaId, tipoContenido, numero, enabled]);

  // Detectar cambio de pestaña (Page Visibility API)
  useEffect(() => {
    if (!enabled || !temaId) {
      return;
    }

    const handleVisibilityChange = async () => {
      if (document.hidden) {
        // Usuario cambió de pestaña (salió)
        wasHiddenRef.current = true;
        visibilityChangeTimeRef.current = Date.now();

        // Registrar el tiempo hasta ahora con flag de cambio de pestaña
        await registerTime(true);
      } else {
        // Usuario volvió a la pestaña
        if (wasHiddenRef.current) {
          // Reiniciar el contador desde que volvió
          startTimeRef.current = Date.now();
          wasHiddenRef.current = false;
          console.log('Usuario volvió a la pestaña, reiniciando contador');
        }
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [enabled, temaId, registerTime]);

  // Retornar función para registrar tiempo manualmente si es necesario
  return {
    registerTime,
    getElapsedTime: () => {
      if (!startTimeRef.current) return 0;
      return Math.floor((Date.now() - startTimeRef.current) / 1000);
    },
  };
};

export default useTimeTracking;
