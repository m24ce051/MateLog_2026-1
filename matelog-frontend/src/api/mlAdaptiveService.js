import api from './axios';


// Servicios para MateLog-AE: Escalas de Autoeficacia y Exámenes
export const mlAdaptiveService = {
  // ==================== AUTOEFICACIA ====================

  // Obtener preguntas de la escala de autoeficacia
  getAutoeficaciaQuestions: async () => {
    const response = await api.get('/ml-adaptive/autoeficacia/preguntas/');
    return response.data;
  },


  // Guardar respuestas de la escala de autoeficacia
  saveAutoeficaciaAnswers: async (tipo, respuestas) => {
    const response = await api.post('/ml-adaptive/autoeficacia/guardar/', {
      tipo,       // 'PRE' o 'POST'
      respuestas  // Array de { pregunta_numero: 1, valor: 3 }
    });
    return response.data;
  },


  // ==================== ESTADO DE EVALUACIONES ====================

  // Obtener estado de todas las evaluaciones del usuario
  getEvaluationStatus: async () => {
    const response = await api.get('/ml-adaptive/estado-evaluaciones/');
    return response.data;
  },


  // ==================== EXÁMENES ====================

  // Guardar respuestas de examen (diagnóstico o final)
  saveExamAnswers: async (tipo, respuestas) => {
    const response = await api.post('/ml-adaptive/examen/guardar/', {
      tipo,       // 'DIAGNOSTICO' o 'FINAL'
      respuestas  // Array de respuestas del examen
    });
    return response.data;
  },


  // ==================== EXAMEN ABIERTO (FINAL) ====================

  // Obtener preguntas del examen final con respuestas abiertas
  getOpenExamQuestions: async () => {
    const response = await api.get('/ml-adaptive/examen-abierto/preguntas/');
    return response.data;
  },

  // Guardar respuestas abiertas del examen final
  saveOpenExamAnswers: async (respuestas) => {
    const response = await api.post('/ml-adaptive/examen-abierto/guardar/', {
      respuestas  // Array de { pregunta_numero: 1, respuesta: "texto de la respuesta..." }
    });
    return response.data;
  },
};


export default mlAdaptiveService;
