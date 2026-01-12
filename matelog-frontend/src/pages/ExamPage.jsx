import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { mlAdaptiveService } from '../api/mlAdaptiveService';
import './ExamPage.css';


// Preguntas del examen diagnóstico (Lógica Matemática)
const PREGUNTAS_DIAGNOSTICO = [
  {
    numero: 1,
    texto: '¿Cuál de las siguientes afirmaciones es una proposición lógica?',
    opciones: [
      { id: 'a', texto: '¿Qué hora es?', correcta: false },
      { id: 'b', texto: 'La Tierra es plana', correcta: true },
      { id: 'c', texto: '¡Qué día tan hermoso!', correcta: false },
      { id: 'd', texto: 'x + 5', correcta: false }
    ]
  },
  {
    numero: 2,
    texto: 'Si p es verdadero y q es falso, ¿cuál es el valor de verdad de p ∧ q?',
    opciones: [
      { id: 'a', texto: 'Verdadero', correcta: false },
      { id: 'b', texto: 'Falso', correcta: true },
      { id: 'c', texto: 'No se puede determinar', correcta: false },
      { id: 'd', texto: 'Depende del contexto', correcta: false }
    ]
  },
  {
    numero: 3,
    texto: '¿Cuál es la negación de "Todos los estudiantes aprobaron"?',
    opciones: [
      { id: 'a', texto: 'Ningún estudiante aprobó', correcta: false },
      { id: 'b', texto: 'Todos los estudiantes reprobaron', correcta: false },
      { id: 'c', texto: 'Al menos un estudiante no aprobó', correcta: true },
      { id: 'd', texto: 'Algunos estudiantes aprobaron', correcta: false }
    ]
  },
  {
    numero: 4,
    texto: 'Si p → q es verdadero y p es verdadero, ¿qué podemos concluir sobre q?',
    opciones: [
      { id: 'a', texto: 'q es verdadero', correcta: true },
      { id: 'b', texto: 'q es falso', correcta: false },
      { id: 'c', texto: 'q puede ser verdadero o falso', correcta: false },
      { id: 'd', texto: 'No se puede determinar', correcta: false }
    ]
  },
  {
    numero: 5,
    texto: '¿Cuál de las siguientes es una tautología?',
    opciones: [
      { id: 'a', texto: 'p ∧ q', correcta: false },
      { id: 'b', texto: 'p ∨ ¬p', correcta: true },
      { id: 'c', texto: 'p → q', correcta: false },
      { id: 'd', texto: 'p ∧ ¬q', correcta: false }
    ]
  },
  {
    numero: 6,
    texto: 'En un conjunto A = {1, 2, 3}, ¿cuántos subconjuntos tiene A?',
    opciones: [
      { id: 'a', texto: '3', correcta: false },
      { id: 'b', texto: '6', correcta: false },
      { id: 'c', texto: '8', correcta: true },
      { id: 'd', texto: '9', correcta: false }
    ]
  },
  {
    numero: 7,
    texto: 'Si A = {1, 2, 3} y B = {3, 4, 5}, ¿cuál es A ∩ B?',
    opciones: [
      { id: 'a', texto: '{1, 2, 3, 4, 5}', correcta: false },
      { id: 'b', texto: '{3}', correcta: true },
      { id: 'c', texto: '{1, 2}', correcta: false },
      { id: 'd', texto: '∅', correcta: false }
    ]
  },
  {
    numero: 8,
    texto: '¿Cuál es el complemento de p → q?',
    opciones: [
      { id: 'a', texto: 'q → p', correcta: false },
      { id: 'b', texto: '¬p → ¬q', correcta: false },
      { id: 'c', texto: 'p ∧ ¬q', correcta: true },
      { id: 'd', texto: '¬p ∨ q', correcta: false }
    ]
  },
  {
    numero: 9,
    texto: 'Si ∀x P(x) es falso, ¿qué podemos concluir?',
    opciones: [
      { id: 'a', texto: '∃x ¬P(x) es verdadero', correcta: true },
      { id: 'b', texto: '∃x P(x) es falso', correcta: false },
      { id: 'c', texto: '∀x ¬P(x) es verdadero', correcta: false },
      { id: 'd', texto: 'No se puede concluir nada', correcta: false }
    ]
  },
  {
    numero: 10,
    texto: '¿Cuál de las siguientes relaciones es una función de A = {1, 2, 3} en B = {a, b, c}?',
    opciones: [
      { id: 'a', texto: '{(1,a), (1,b), (2,c)}', correcta: false },
      { id: 'b', texto: '{(1,a), (2,b), (3,c)}', correcta: true },
      { id: 'c', texto: '{(1,a), (2,b)}', correcta: false },
      { id: 'd', texto: '{(1,a), (2,a), (3,a), (3,b)}', correcta: false }
    ]
  }
];


// Preguntas del examen final (similar estructura, más avanzadas)
const PREGUNTAS_FINAL = [
  {
    numero: 1,
    texto: 'En lógica proposicional, ¿cuál es la forma normal conjuntiva (FNC) de (p ∨ q) ∧ (p ∨ ¬r)?',
    opciones: [
      { id: 'a', texto: '(p ∨ q) ∧ (p ∨ ¬r)', correcta: true },
      { id: 'b', texto: 'p ∨ (q ∧ ¬r)', correcta: false },
      { id: 'c', texto: '(p ∧ q) ∨ (p ∧ ¬r)', correcta: false },
      { id: 'd', texto: 'p ∧ q ∧ ¬r', correcta: false }
    ]
  },
  {
    numero: 2,
    texto: 'Si tenemos la función f: ℝ → ℝ definida como f(x) = x², ¿es f inyectiva?',
    opciones: [
      { id: 'a', texto: 'Sí, porque cada valor de x tiene una imagen única', correcta: false },
      { id: 'b', texto: 'No, porque f(2) = f(-2) = 4', correcta: true },
      { id: 'c', texto: 'Sí, porque es continua', correcta: false },
      { id: 'd', texto: 'Depende del dominio', correcta: false }
    ]
  },
  {
    numero: 3,
    texto: 'En un grafo con 5 vértices, ¿cuál es el número máximo de aristas posibles (grafo simple)?',
    opciones: [
      { id: 'a', texto: '5', correcta: false },
      { id: 'b', texto: '10', correcta: true },
      { id: 'c', texto: '20', correcta: false },
      { id: 'd', texto: '25', correcta: false }
    ]
  },
  {
    numero: 4,
    texto: '¿Cuál es el principio del palomar (Pigeonhole Principle)?',
    opciones: [
      { id: 'a', texto: 'Si n objetos se colocan en m contenedores y n > m, al menos un contenedor tiene más de un objeto', correcta: true },
      { id: 'b', texto: 'Todo conjunto finito tiene un elemento mínimo', correcta: false },
      { id: 'c', texto: 'La unión de conjuntos finitos es finita', correcta: false },
      { id: 'd', texto: 'Dos conjuntos disjuntos no tienen elementos comunes', correcta: false }
    ]
  },
  {
    numero: 5,
    texto: 'En teoría de conjuntos, ¿cuál es la cardinalidad del conjunto potencia de A si |A| = 4?',
    opciones: [
      { id: 'a', texto: '4', correcta: false },
      { id: 'b', texto: '8', correcta: false },
      { id: 'c', texto: '16', correcta: true },
      { id: 'd', texto: '32', correcta: false }
    ]
  },
  {
    numero: 6,
    texto: '¿Cuál es la negación de ∀x ∃y P(x, y)?',
    opciones: [
      { id: 'a', texto: '∃x ∀y ¬P(x, y)', correcta: true },
      { id: 'b', texto: '∀x ∃y ¬P(x, y)', correcta: false },
      { id: 'c', texto: '∃x ∃y ¬P(x, y)', correcta: false },
      { id: 'd', texto: '∀x ∀y ¬P(x, y)', correcta: false }
    ]
  },
  {
    numero: 7,
    texto: 'Si R es una relación de equivalencia en A, ¿qué propiedad NO debe cumplir?',
    opciones: [
      { id: 'a', texto: 'Reflexiva', correcta: false },
      { id: 'b', texto: 'Simétrica', correcta: false },
      { id: 'c', texto: 'Transitiva', correcta: false },
      { id: 'd', texto: 'Antisimétrica', correcta: true }
    ]
  },
  {
    numero: 8,
    texto: '¿Cuántos números de 4 dígitos se pueden formar con los dígitos {1,2,3,4,5} sin repetición?',
    opciones: [
      { id: 'a', texto: '20', correcta: false },
      { id: 'b', texto: '60', correcta: false },
      { id: 'c', texto: '120', correcta: true },
      { id: 'd', texto: '625', correcta: false }
    ]
  },
  {
    numero: 9,
    texto: 'En inducción matemática, ¿qué paso es esencial después del caso base?',
    opciones: [
      { id: 'a', texto: 'Demostrar para n = 2', correcta: false },
      { id: 'b', texto: 'Asumir P(k) es verdadero y demostrar P(k+1)', correcta: true },
      { id: 'c', texto: 'Demostrar para todos los números pares', correcta: false },
      { id: 'd', texto: 'Encontrar un contraejemplo', correcta: false }
    ]
  },
  {
    numero: 10,
    texto: 'Si un árbol binario tiene altura h, ¿cuál es el número máximo de nodos?',
    opciones: [
      { id: 'a', texto: 'h', correcta: false },
      { id: 'b', texto: '2h', correcta: false },
      { id: 'c', texto: '2^h - 1', correcta: false },
      { id: 'd', texto: '2^(h+1) - 1', correcta: true }
    ]
  }
];


const ExamPage = ({ tipo = 'DIAGNOSTICO' }) => {
  const [preguntas, setPreguntas] = useState([]);
  const [respuestas, setRespuestas] = useState({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isOpenExam, setIsOpenExam] = useState(false);

  const navigate = useNavigate();


  useEffect(() => {
    const loadExam = async () => {
      try {
        setLoading(true);

        if (tipo === 'DIAGNOSTICO') {
          setPreguntas(PREGUNTAS_DIAGNOSTICO);
          setIsOpenExam(false);
        } else if (tipo === 'FINAL') {
          // Para el examen final, cargar preguntas abiertas desde el backend
          const data = await mlAdaptiveService.getOpenExamQuestions();
          setPreguntas(data.preguntas || []);
          setIsOpenExam(true);
        } else {
          setPreguntas(PREGUNTAS_FINAL);
          setIsOpenExam(false);
        }
      } catch (err) {
        console.error('Error cargando examen:', err);
        alert('Error al cargar el examen. Por favor, recarga la página.');
      } finally {
        setLoading(false);
      }
    };

    loadExam();
  }, [tipo]);


  const handleAnswerSelect = (opcionId) => {
    const currentPregunta = preguntas[currentQuestionIndex];
    setRespuestas(prev => ({
      ...prev,
      [currentPregunta.numero]: opcionId
    }));
  };


  const handleTextAnswer = (texto) => {
    const currentPregunta = preguntas[currentQuestionIndex];
    setRespuestas(prev => ({
      ...prev,
      [currentPregunta.numero]: texto
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

      if (isOpenExam) {
        // Para examen con respuestas abiertas
        const respuestasAbiertas = preguntas.map(pregunta => ({
          pregunta_numero: pregunta.numero,
          respuesta: respuestas[pregunta.numero] || ''
        }));

        const resultadoExamen = await mlAdaptiveService.saveOpenExamAnswers(respuestasAbiertas);
        setResultado(resultadoExamen);
        setShowResults(true);
      } else {
        // Para examen de opción múltiple
        const respuestasEvaluadas = preguntas.map(pregunta => {
          const opcionSeleccionada = respuestas[pregunta.numero];
          const opcionCorrecta = pregunta.opciones.find(opt => opt.correcta);

          return {
            pregunta_numero: pregunta.numero,
            correcta: opcionSeleccionada === opcionCorrecta?.id
          };
        });

        const resultadoExamen = await mlAdaptiveService.saveExamAnswers(tipo, respuestasEvaluadas);
        setResultado(resultadoExamen);
        setShowResults(true);
      }

    } catch (err) {
      alert('Error al guardar las respuestas. Por favor, intenta de nuevo.');
      console.error('Error guardando examen:', err);
      setSubmitting(false);
    }
  };


  const handleContinue = () => {
    if (tipo === 'DIAGNOSTICO') {
      // Después del examen diagnóstico, ir a las lecciones
      navigate('/lecciones');
    } else {
      // Después del examen final, ir a página de finalización
      navigate('/lecciones');
    }
  };


  if (showResults && resultado) {
    return (
      <div className="exam-container">
        <div className="exam-results">
          <h1>¡Examen {tipo === 'DIAGNOSTICO' ? 'Diagnóstico' : 'Final'} Completado!</h1>

          {tipo === 'DIAGNOSTICO' ? (
            // Para el examen diagnóstico, NO mostrar resultados
            <p className="results-message">
              No te preocupes si no entendiste alguna pregunta, enseguida comienza el curso de Lógica Matemática para aprender más
            </p>
          ) : (
            // Para el examen final, SÍ mostrar resultados
            <>
              <div className="results-summary">
                <div className="result-item">
                  <span className="result-label">Total de preguntas:</span>
                  <span className="result-value">{resultado.total_preguntas}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Respuestas correctas:</span>
                  <span className="result-value">{resultado.respuestas_correctas}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Porcentaje:</span>
                  <span className="result-value score">{resultado.porcentaje}%</span>
                </div>
              </div>

              <p className="results-message">
                {resultado.porcentaje >= 70
                  ? '¡Excelente trabajo! Has demostrado un buen dominio de los conceptos.'
                  : 'Continúa estudiando para mejorar tu comprensión de los temas.'
                }
              </p>
            </>
          )}

          <button onClick={handleContinue} className="continue-button">
            {tipo === 'DIAGNOSTICO' ? 'Iniciar curso' : 'Continuar'}
          </button>
        </div>
      </div>
    );
  }


  if (loading || preguntas.length === 0) {
    return (
      <div className="exam-container">
        <div className="loading">Cargando examen...</div>
      </div>
    );
  }

  const currentPregunta = preguntas[currentQuestionIndex];
  const totalPreguntas = preguntas.length;

  return (
    <div className="exam-container">
      <div className="exam-header">
        <h1>Examen {tipo === 'DIAGNOSTICO' ? 'Diagnóstico' : 'Final'}</h1>
        <p className="exam-instrucciones">
          {tipo === 'DIAGNOSTICO'
            ? 'Este examen evaluará tus conocimientos previos en Lógica Matemática. Selecciona la respuesta correcta para cada pregunta.'
            : isOpenExam
              ? 'Este examen evaluará lo que has aprendido durante las lecciones. Responde cada pregunta con tus propias palabras de manera clara y completa.'
              : 'Este examen evaluará lo que has aprendido durante las lecciones. Selecciona la respuesta correcta para cada pregunta.'
          }
        </p>
      </div>

      <div className="pregunta-card">
        <div className="pregunta-numero-badge">
          Pregunta {currentPregunta.numero}
        </div>

        <p className="pregunta-texto">{currentPregunta.texto}</p>

        {isOpenExam ? (
          // Respuesta abierta con textarea
          <div className="respuesta-abierta-container">
            <textarea
              className="respuesta-abierta-textarea"
              placeholder="Escribe tu respuesta aquí..."
              value={respuestas[currentPregunta.numero] || ''}
              onChange={(e) => handleTextAnswer(e.target.value)}
              rows={8}
            />
            <div className="textarea-helper">
              {respuestas[currentPregunta.numero]?.length || 0} caracteres
            </div>
          </div>
        ) : (
          // Opciones múltiples con radio buttons
          <div className="opciones-container">
            {currentPregunta.opciones.map((opcion) => (
              <label
                key={opcion.id}
                className={`opcion-radio ${respuestas[currentPregunta.numero] === opcion.id ? 'selected' : ''}`}
              >
                <input
                  type="radio"
                  name={`pregunta-${currentPregunta.numero}`}
                  value={opcion.id}
                  checked={respuestas[currentPregunta.numero] === opcion.id}
                  onChange={() => handleAnswerSelect(opcion.id)}
                />
                <span className="opcion-letra">{opcion.id.toUpperCase()})</span>
                <span className="opcion-texto">{opcion.texto}</span>
              </label>
            ))}
          </div>
        )}

        <div className="bottom-section">
          <button
            onClick={handleNext}
            className="next-button"
            disabled={submitting || !respuestas[currentPregunta.numero]}
          >
            {submitting
              ? 'Enviando...'
              : currentQuestionIndex === preguntas.length - 1
                ? 'Finalizar Examen'
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


export default ExamPage;
