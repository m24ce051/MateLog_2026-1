import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { mlAdaptiveService } from '../api/mlAdaptiveService';
import { useAuth } from '../context/AuthContext';
import './AutoeficaciaScalePage.css';


const AutoeficaciaScalePage = ({ tipo = 'PRE' }) => {
  const [preguntas, setPreguntas] = useState([]);
  const [opciones, setOpciones] = useState([]);
  const [respuestas, setRespuestas] = useState({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const navigate = useNavigate();
  const { user } = useAuth();


  useEffect(() => {
    loadQuestions();
  }, []);


  const loadQuestions = async () => {
    try {
      setLoading(true);
      const data = await mlAdaptiveService.getAutoeficaciaQuestions();
      setPreguntas(data.preguntas);
      setOpciones(data.opciones);
    } catch (err) {
      setError('Error al cargar las preguntas. Por favor, intenta de nuevo.');
      console.error('Error cargando preguntas de autoeficacia:', err);
    } finally {
      setLoading(false);
    }
  };


  const handleAnswerSelect = (valor) => {
    const currentPregunta = preguntas[currentQuestionIndex];
    setRespuestas(prev => ({
      ...prev,
      [currentPregunta.numero]: valor
    }));
  };


  const handleNext = () => {
    const currentPregunta = preguntas[currentQuestionIndex];

    // Validar que la pregunta actual esté respondida
    if (!respuestas[currentPregunta.numero]) {
      alert('Por favor, selecciona una opción antes de continuar.');
      return;
    }

    // Si es la última pregunta, enviar respuestas
    if (currentQuestionIndex === preguntas.length - 1) {
      handleSubmit();
    } else {
      // Scroll hacia arriba ANTES de cambiar de pregunta
      window.scrollTo({ top: 0, behavior: 'instant' });

      // Avanzar a la siguiente pregunta
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };


  const handleSubmit = async () => {
    try {
      setSubmitting(true);

      // Convertir respuestas a formato esperado por el backend
      const respuestasArray = Object.entries(respuestas).map(([preguntaNumero, valor]) => ({
        pregunta_numero: parseInt(preguntaNumero),
        respuesta: valor
      }));

      const resultado = await mlAdaptiveService.saveAutoeficaciaAnswers(tipo, respuestasArray);

      // NO mostrar clasificación al usuario (mantener ciego el estudio)
      // Simplemente redirigir

      // Redirigir según el tipo de escala
      if (tipo === 'PRE') {
        navigate('/examen-diagnostico');
      } else {
        navigate('/examen-final');
      }

    } catch (err) {
      setError('Error al guardar las respuestas. Por favor, intenta de nuevo.');
      console.error('Error guardando respuestas:', err);
      setSubmitting(false);
    }
  };


  if (loading) {
    return (
      <div className="autoeficacia-container">
        <div className="loading">Cargando cuestionario...</div>
      </div>
    );
  }


  if (error) {
    return (
      <div className="autoeficacia-container">
        <div className="error-box">{error}</div>
        <button onClick={loadQuestions} className="retry-button">
          Reintentar
        </button>
      </div>
    );
  }


  if (preguntas.length === 0) {
    return (
      <div className="autoeficacia-container">
        <div className="loading">No hay preguntas disponibles.</div>
      </div>
    );
  }


  const currentPregunta = preguntas[currentQuestionIndex];
  const totalPreguntas = preguntas.length;
  const respondidas = Object.keys(respuestas).length;


  return (
    <div className="autoeficacia-container">
      <div className="autoeficacia-header">
        <h1>Cuestionario de Personalidad</h1>
        <p className="autoeficacia-instrucciones">
          Por favor, lee cada afirmación cuidadosamente y selecciona la opción que mejor describa
          tu nivel de acuerdo. No hay respuestas correctas o incorrectas.
        </p>
      </div>

      <div className="question-card">
        <div className="question-number-badge">
          Pregunta {currentPregunta.numero}
        </div>

        <p className="question-text">{currentPregunta.texto}</p>

        <div className="options-container">
          <p className="options-label">Selecciona tu nivel de acuerdo:</p>
          {opciones.map((opcion) => (
            <label
              key={opcion.valor}
              className={`option-item ${respuestas[currentPregunta.numero] === opcion.valor ? 'selected' : ''}`}
            >
              <input
                type="radio"
                name={`pregunta-${currentPregunta.numero}`}
                value={opcion.valor}
                checked={respuestas[currentPregunta.numero] === opcion.valor}
                onChange={() => handleAnswerSelect(opcion.valor)}
              />
              <span className="option-label">{opcion.etiqueta}</span>
            </label>
          ))}
        </div>

        <div className="bottom-section">
          <button
            onClick={handleNext}
            className="next-button"
            disabled={submitting || !respuestas[currentPregunta.numero]}
          >
            {submitting
              ? 'Enviando...'
              : currentQuestionIndex === preguntas.length - 1
                ? 'Finalizar Cuestionario'
                : 'Siguiente'}
          </button>
          <div className="progress-indicator">
            Pregunta {currentQuestionIndex + 1} de {totalPreguntas}
          </div>
        </div>
      </div>
    </div>
  );
};


export default AutoeficaciaScalePage;
