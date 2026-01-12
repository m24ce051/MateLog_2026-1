import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { lessonService } from '../api/lessonService';
import { trackingService } from '../api/trackingService';
import { useTimeTracking } from '../hooks/useTimeTracking';
import Modal from '../components/Modal';
import './TopicPage.css';
import './HTMLContent.css';


const TopicPage = () => {
  const [topic, setTopic] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showingExercises, setShowingExercises] = useState(false);
  const [currentExercise, setCurrentExercise] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [showHelp, setShowHelp] = useState({});
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(true);
  const [startTimes, setStartTimes] = useState({});
  const [viewedExtraExample, setViewedExtraExample] = useState(false);
  const [navigationHistory, setNavigationHistory] = useState([0]); // Historial de índices visitados
  const [modal, setModal] = useState({ isOpen: false, type: 'info', title: '', message: '', onConfirm: null, onCancel: null, confirmText: 'Aceptar', cancelText: 'Cancelar', showCancel: false });

  const { topicId } = useParams();
  const navigate = useNavigate();

  // Determinar tipo de contenido y número para tracking
  const getTrackingInfo = () => {
    if (!topic) return null;

    if (showingExercises) {
      // Tracking para ejercicios
      const exercise = topic.ejercicios[currentExercise];
      return {
        tipoContenido: 'EJERCICIO',
        numero: exercise?.orden || currentExercise + 1,
        ejercicioId: exercise?.id,
      };
    } else {
      // Tracking para contenido (Teoría/Ejemplo)
      const content = topic.contenidos[currentIndex];
      if (!content) return null;

      // Determinar tipo y número
      let tipoContenido = null;
      let numero = 1;

      if (content.tipo === 'TEORIA' || content.tipo === 'EJEMPLO' || content.tipo === 'EJEMPLO_EXTRA') {
        // Contar cuántos del mismo tipo hay antes de este
        tipoContenido = content.tipo === 'TEORIA' ? 'TEORIA' : 'EJEMPLO';
        numero = topic.contenidos
          .slice(0, currentIndex + 1)
          .filter(c => {
            if (tipoContenido === 'TEORIA') {
              return c.tipo === 'TEORIA';
            } else {
              return c.tipo === 'EJEMPLO' || c.tipo === 'EJEMPLO_EXTRA';
            }
          }).length;
      }

      return tipoContenido ? {
        tipoContenido,
        numero,
        contenidoId: content.id,
      } : null;
    }
  };

  const trackingInfo = getTrackingInfo();

  // Hook de tracking de tiempo
  useTimeTracking({
    temaId: topicId ? parseInt(topicId) : null,
    tipoContenido: trackingInfo?.tipoContenido,
    numero: trackingInfo?.numero,
    contenidoId: trackingInfo?.contenidoId,
    ejercicioId: trackingInfo?.ejercicioId,
    enabled: !!trackingInfo,
  });

  useEffect(() => {
    loadTopic();
  }, [topicId]);

  // Restaurar progreso de ejercicios cuando se carga el tema
  useEffect(() => {
    if (topic && topic.siguiente_ejercicio_index !== undefined) {
      const temaAprobado = topic.progreso?.aprobado;

      if (temaAprobado) {
        // Tema APROBADO: Modo revisión
        // - Iniciar en ejercicio 1
        // - Restaurar respuestas y resultados para mostrarlos
        setCurrentExercise(0);

        if (topic.ejercicios_respondidos) {
          const prevAnswers = {};
          const prevResults = {};

          Object.entries(topic.ejercicios_respondidos).forEach(([ejercicioId, respuesta]) => {
            prevAnswers[ejercicioId] = respuesta.respuesta;
            prevResults[ejercicioId] = {
              es_correcta: respuesta.es_correcta
            };
          });

          setUserAnswers(prevAnswers);
          setResults(prevResults);
        }
      } else {
        // Tema NO APROBADO: Modo reintento
        // - Continuar desde el último sin responder
        // - NO restaurar respuestas (ejercicios limpios)
        setCurrentExercise(topic.siguiente_ejercicio_index);
        setUserAnswers({});
        setResults({});
      }
    }
  }, [topic]);


  useEffect(() => {
    if (showingExercises && topic) {
      const exerciseId = topic.ejercicios[currentExercise]?.id;
      if (exerciseId && !startTimes[exerciseId]) {
        setStartTimes(prev => ({ ...prev, [exerciseId]: Date.now() }));
      }
    }
  }, [showingExercises, currentExercise, topic]);

  // Lazy loading for images
  useEffect(() => {
    const images = document.querySelectorAll('.content-text img, .exercise-question img, .exercise-instruction img, .feedback img');
    images.forEach(img => {
      if (!img.hasAttribute('loading')) {
        img.setAttribute('loading', 'lazy');
      }
    });
  }, [currentIndex, currentExercise, showingExercises, topic]);


  const loadTopic = async () => {
    try {
      const data = await lessonService.getTopicContent(topicId);
      setTopic(data);
      // La restauración del progreso se hace en el useEffect que escucha cambios en topic
    } catch (err) {
      setModal({
        isOpen: true,
        type: 'error',
        title: 'Error',
        message: 'No se pudo cargar el tema. Por favor, intenta nuevamente.',
        showCancel: false
      });
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Registrar contenido como visto cuando cambia el índice
  useEffect(() => {
    const registerContent = async () => {
      if (topic && !showingExercises) {
        const currentContent = topic.contenidos[currentIndex];
        
        // Solo registrar si NO es EJEMPLO_EXTRA
        if (currentContent && currentContent.tipo !== 'EJEMPLO_EXTRA') {
          try {
            await lessonService.registerContentViewed(currentContent.id);
            console.log(`Contenido ${currentContent.id} registrado como visto`);
          } catch (err) {
            console.error('Error al registrar contenido visto:', err);
          }
        }
      }
    };
    registerContent();
  }, [currentIndex, topic, showingExercises]);

  const handleContinue = () => {
    const currentContent = topic.contenidos[currentIndex];
   
    // Si el siguiente es EJEMPLO_EXTRA, mostrar opciones
    if (currentIndex < topic.contenidos.length - 1) {
      const nextContent = topic.contenidos[currentIndex + 1];
      if (nextContent.tipo === 'EJEMPLO_EXTRA') {
        // Encontrar cuántos ejemplos extra consecutivos hay
        let consecutiveExtras = 0;
        for (let i = currentIndex + 1; i < topic.contenidos.length; i++) {
          if (topic.contenidos[i].tipo === 'EJEMPLO_EXTRA') {
            consecutiveExtras++;
          } else {
            break;
          }
        }
       
        // Si hay ejemplos extra, no avanzar automáticamente
        return;
      }
    }


    if (currentIndex < topic.contenidos.length - 1) {
      const nextIndex = currentIndex + 1;
      setCurrentIndex(nextIndex);
      setNavigationHistory(prev => [...prev, nextIndex]);
    } else {
      // Terminó el contenido, ir a ejercicios
      setShowingExercises(true);
    }
  };


  const handleShowExtraExample = async () => {
    if (currentIndex < topic.contenidos.length - 1) {
      const nextIndex = currentIndex + 1;
      setCurrentIndex(nextIndex);
      setViewedExtraExample(true);
      setNavigationHistory(prev => [...prev, nextIndex]);

      // Registrar clic en "Otro Ejemplo"
      try {
        await trackingService.registerButtonClick({
          temaId: parseInt(topicId),
          tipoBoton: 'OTRO_EJEMPLO',
        });
      } catch (err) {
        console.error('Error al registrar clic Otro Ejemplo:', err);
      }
    }
  };


  const handleSkipExtraExamples = () => {
    // Saltar todos los ejemplos extra consecutivos
    let nextIndex = currentIndex + 1;
    while (nextIndex < topic.contenidos.length &&
           topic.contenidos[nextIndex].tipo === 'EJEMPLO_EXTRA') {
      nextIndex++;
    }
   
    if (nextIndex < topic.contenidos.length) {
      setCurrentIndex(nextIndex);
      setNavigationHistory(prev => [...prev, nextIndex]);
    } else {
      setShowingExercises(true);
    }
  };


  const handleGoToExercises = async () => {
    // Registrar clic en "Ir a Ejercicios"
    try {
      await trackingService.registerButtonClick({
        temaId: parseInt(topicId),
        tipoBoton: 'IR_EJERCICIOS',
      });
    } catch (err) {
      console.error('Error al registrar clic Ir a Ejercicios:', err);
    }
    setShowingExercises(true);
  };


  const handleRegresarContenido = async () => {
    // Registrar clic en "Regresar"
    try {
      await trackingService.registerButtonClick({
        temaId: parseInt(topicId),
        tipoBoton: 'REGRESAR',
      });
    } catch (err) {
      console.error('Error al registrar clic Regresar:', err);
    }

    // Volver al índice anterior en el historial
    if (navigationHistory.length > 1) {
      const newHistory = [...navigationHistory];
      newHistory.pop(); // Remover el índice actual
      const previousIndex = newHistory[newHistory.length - 1];

      setNavigationHistory(newHistory);
      setCurrentIndex(previousIndex);

      // Si el contenido anterior no es EJEMPLO_EXTRA, resetear la bandera
      if (topic.contenidos[previousIndex]?.tipo !== 'EJEMPLO_EXTRA') {
        setViewedExtraExample(false);
      }
    }
  };


  const handleVolverALeccion = () => {
    // Volver a la lista de temas de la lección
    // FIX: Asegurarse de que topic.leccion existe antes de navegar
    if (topic && topic.leccion) {
      navigate(`/leccion/${topic.leccion}`);
    } else {
      // Fallback: ir a la lista de lecciones
      navigate('/lecciones');
    }
  };


  const handleAnswerChange = (exerciseId, value) => {
    setUserAnswers(prev => ({ ...prev, [exerciseId]: value }));
  };


  const handleSubmitAnswer = async () => {
    const exercise = topic.ejercicios[currentExercise];
    const answer = userAnswers[exercise.id];


    if (!answer || answer.trim() === '') {
      setModal({
        isOpen: true,
        type: 'warning',
        title: 'Atención',
        message: 'Por favor ingresa una respuesta antes de continuar.',
        showCancel: false
      });
      return;
    }


    const timeElapsed = startTimes[exercise.id]
      ? Math.floor((Date.now() - startTimes[exercise.id]) / 1000)
      : 0;


    try {
      const result = await lessonService.validateAnswer({
        ejercicio_id: exercise.id,
        respuesta: answer,
        uso_ayuda: !!showHelp[exercise.id], // Solo si se hizo clic en el botón
        tiempo_respuesta_segundos: timeElapsed,
      });


      setResults(prev => ({ ...prev, [exercise.id]: result }));

      // NO avanzar automáticamente - se hace con botón "Continuar"
    } catch (err) {
      setModal({
        isOpen: true,
        type: 'error',
        title: 'Error',
        message: 'No se pudo validar la respuesta. Por favor, intenta nuevamente.',
        showCancel: false
      });
      console.error(err);
    }
  };


  const handleContinueToNextExercise = () => {
    if (currentExercise < topic.ejercicios.length - 1) {
      setCurrentExercise(currentExercise + 1);
    } else {
      handleFinishExercises();
    }
  };


  const handleFinishExercises = async () => {
    try {
      const result = await lessonService.finalizeTopic(topicId);

      // Verificar si aprobó (>= 80%)
      const aprobo = result.aprobado || result.porcentaje_acierto >= 80;

      if (aprobo) {
        // Aprobó: mensaje de éxito
        const mensaje = `¡Felicidades! Has completado el tema con ${result.porcentaje_acierto.toFixed(1)}% de aciertos.`;

        // Obtener ID del siguiente tema (compatibilidad con ambas versiones del backend)
        const siguienteId = result.siguiente_tema?.id || result.siguiente_tema_id;

        if (siguienteId) {
          // Hay siguiente tema
          setModal({
            isOpen: true,
            type: 'success',
            title: '¡Excelente trabajo!',
            message: `${mensaje}\n\n¿Deseas continuar con el siguiente tema?`,
            confirmText: 'Continuar',
            cancelText: 'Volver a lecciones',
            showCancel: true,
            onConfirm: () => {
              navigate(`/tema/${siguienteId}`);
            },
            onCancel: () => {
              if (topic && topic.leccion) {
                navigate(`/leccion/${topic.leccion}`);
              } else {
                navigate('/lecciones');
              }
            }
          });
        } else {
          // Era el último tema de la lección
          setModal({
            isOpen: true,
            type: 'success',
            title: '¡Felicitaciones!',
            message: `${mensaje}\n\n¡Has completado todos los temas de esta lección!`,
            confirmText: 'Volver a lecciones',
            showCancel: false,
            onConfirm: () => {
              if (topic && topic.leccion) {
                navigate(`/leccion/${topic.leccion}`);
              } else {
                navigate('/lecciones');
              }
            }
          });
        }
      } else {
        // No aprobó: debe reintentar
        setModal({
          isOpen: true,
          type: 'warning',
          title: 'Intenta de nuevo',
          message: `Obtuviste ${result.porcentaje_acierto.toFixed(1)}%. Necesitas al menos 80% para avanzar.\n\n¿Deseas intentarlo de nuevo?`,
          confirmText: 'Reintentar',
          cancelText: 'Volver a lecciones',
          showCancel: true,
          onConfirm: async () => {
            try {
              await lessonService.retryTopic(topicId);
              await loadTopic();
              setShowingExercises(false);
              setCurrentIndex(0);
              setNavigationHistory([0]);
              setViewedExtraExample(false);
              setCurrentExercise(0);
              setUserAnswers({});
              setShowHelp({});
              setResults({});
              setStartTimes({});
            } catch (error) {
              setModal({
                isOpen: true,
                type: 'error',
                title: 'Error',
                message: 'No se pudo reiniciar el tema. Por favor, intenta nuevamente.',
                showCancel: false
              });
              console.error(error);
            }
          },
          onCancel: () => {
            if (topic && topic.leccion) {
              navigate(`/leccion/${topic.leccion}`);
            } else {
              navigate('/lecciones');
            }
          }
        });
      }
    } catch (err) {
      setModal({
        isOpen: true,
        type: 'error',
        title: 'Error',
        message: 'No se pudo finalizar el tema. Por favor, intenta nuevamente.',
        showCancel: false
      });
      console.error(err);
    }
  };


  const handleBackToTopic = async () => {
    try {
      // Registrar clic en "Volver al Tema"
      await trackingService.registerButtonClick({
        temaId: parseInt(topicId),
        tipoBoton: 'VOLVER',
      });

      await lessonService.returnToTopic(topicId);
      setShowingExercises(false);

      // FIX: SIEMPRE volver a la primera pantalla (índice 0)
      setCurrentIndex(0);
      setNavigationHistory([0]);
      setViewedExtraExample(false);
    } catch (err) {
      console.error(err);
    }
  };

  const handleShowHelp = async (exerciseId) => {
    // Solo mostrar ayuda, no toggle
    if (!showHelp[exerciseId]) {
      try {
        await trackingService.registerButtonClick({
          temaId: parseInt(topicId),
          tipoBoton: 'VER_AYUDA',
        });
      } catch (err) {
        console.error('Error al registrar clic Ver Ayuda:', err);
      }

      // Mostrar la ayuda
      setShowHelp(prev => ({ ...prev, [exerciseId]: true }));
    }
  };


  if (loading) {
    return <div className="topic-container"><div className="loading">Cargando...</div></div>;
  }


  if (!topic) {
    return <div className="topic-container"><div className="error-box">Tema no encontrado</div></div>;
  }


  // Vista de contenido (teoría/ejemplos)
  if (!showingExercises) {
    const currentContent = topic.contenidos[currentIndex];
    const hasNextExtraExample = currentIndex < topic.contenidos.length - 1 &&
                                 topic.contenidos[currentIndex + 1]?.tipo === 'EJEMPLO_EXTRA';
    const isFirstScreen = currentIndex === 0;


    return (
      <div className="topic-container">
        <header className="topic-header">
          <div className="topic-header-content">
            <button onClick={handleVolverALeccion} className="back-btn">← Volver</button>
            <h1>{topic.titulo}</h1>
          </div>
        </header>


        <div className="content-box">
          {/* Header del contenido con badge y botón Ver Otro Ejemplo */}
          <div className="content-header">
            <div className="content-type-badge">{currentContent.tipo_display}</div>
            {/* Botón Ver Otro Ejemplo dentro del recuadro, alineado a la derecha */}
            {hasNextExtraExample && (
              <button onClick={handleShowExtraExample} className="btn btn-secondary btn-inline">
                Ver Otro Ejemplo
              </button>
            )}
          </div>


          <div
            className="content-text"
            dangerouslySetInnerHTML={{ __html: currentContent.contenido_texto }}
          />
        </div>


        <div className="navigation-buttons">
          {/* Botón Regresar - Solo si NO es la primera pantalla */}
          {!isFirstScreen && (
            <button onClick={handleRegresarContenido} className="btn btn-back">
              ← Regresar
            </button>
          )}


          {/* Botón Continuar */}
          {hasNextExtraExample ? (
            <button onClick={handleSkipExtraExamples} className="btn btn-primary">
              Continuar
            </button>
          ) : (
            <button onClick={handleContinue} className="btn btn-primary">
              {currentIndex < topic.contenidos.length - 1 ? 'Continuar' : 'Ir a Ejercicios'}
            </button>
          )}


          {/* Botón Ir a Ejercicios - Siempre visible excepto en la última pantalla sin ejemplos extra */}
          {(hasNextExtraExample || currentIndex < topic.contenidos.length - 1) && (
            <button onClick={handleGoToExercises} className="btn btn-accent">
              Ir a Ejercicios
            </button>
          )}
        </div>


        <div className="progress-indicator">
          {currentIndex + 1} / {topic.contenidos.length}
        </div>

        <Modal
          isOpen={modal.isOpen}
          onClose={() => setModal({ ...modal, isOpen: false })}
          onConfirm={modal.onConfirm}
          onCancel={modal.onCancel}
          title={modal.title}
          message={modal.message}
          type={modal.type}
          confirmText={modal.confirmText}
          cancelText={modal.cancelText}
          showCancel={modal.showCancel}
        />
      </div>
    );
  }


  // Vista de ejercicios
  const exercise = topic.ejercicios[currentExercise];
  const result = results[exercise.id];


  return (
    <div className="topic-container">
      <header className="topic-header">
        <div className="topic-header-content">
          <button onClick={handleBackToTopic} className="back-btn">← Volver al Tema</button>
          <h1>Ejercicios - {topic.titulo}</h1>
        </div>
      </header>

      <div className="exercise-box">
        {/* Header del ejercicio con número, dificultad (condicional) y botón Ver Ayuda */}
        <div className="exercise-header">
          <div className="exercise-info-left">
            <span className="exercise-number">Ejercicio {exercise.orden}</span>
            {/* Mostrar dificultad solo si mostrar_dificultad es true */}
            {exercise.mostrar_dificultad && (
              <span className="exercise-difficulty">{exercise.dificultad_display}</span>
            )}
          </div>
          {/* Botón Ver Ayuda dentro del recuadro, alineado a la derecha */}
          {/* Mostrar SOLO si: (1) tiene ayuda, (2) no ha respondido, (3) no ha sido mostrada ya */}
          {exercise.texto_ayuda && !result && !showHelp[exercise.id] && (
            <button
              onClick={() => handleShowHelp(exercise.id)}
              className="btn btn-help btn-inline"
            >
              Ver Ayuda
            </button>
          )}
        </div>
       
        {/* Lógica de visualización según aprobación:
            - NO aprobado + SIN resultado: Mostrar pregunta + opciones + botón enviar
            - NO aprobado + CON resultado: Mostrar SOLO resultado (pantalla completa)
            - SÍ aprobado: Mostrar pregunta + opciones deshabilitadas + resultado inline
        */}

        {!topic?.progreso?.aprobado && result ? (
          /* NO APROBADO + CON RESULTADO: Pantalla completa de resultado */
          <>
            <div className={`result-box ${result.es_correcta ? 'correct' : 'incorrect'}`}>
              <h3>{result.es_correcta ? '¡Correcto!' : 'Incorrecto'}</h3>
              {result.retroalimentacion && (
                <div
                  className="feedback"
                  dangerouslySetInnerHTML={{ __html: result.retroalimentacion }}
                />
              )}
            </div>

            {/* Mostrar ayuda automáticamente cuando es incorrecto */}
            {!result.es_correcta && exercise.texto_ayuda && (
              <div className="help-box help-box-auto">
                <h4>💡 Ayuda</h4>
                <div dangerouslySetInnerHTML={{ __html: exercise.texto_ayuda }} />
              </div>
            )}

            <button
              onClick={handleContinueToNextExercise}
              className="btn btn-primary submit-btn"
            >
              {currentExercise < topic.ejercicios.length - 1 ? 'Continuar' : 'Finalizar'}
            </button>
          </>
        ) : (
          /* MOSTRAR PREGUNTA Y OPCIONES */
          <>
            <div
              className="exercise-instruction"
              dangerouslySetInnerHTML={{ __html: exercise.instruccion }}
            />
            <div
              className="exercise-question"
              dangerouslySetInnerHTML={{ __html: exercise.enunciado }}
            />

            {/* Opciones o input de texto */}
            {exercise.tipo === 'MULTIPLE' ? (
              <div className="options-list">
                {exercise.opciones.map(option => (
                  <label key={option.letra} className="option-item">
                    <input
                      type="radio"
                      name="answer"
                      value={option.letra}
                      checked={userAnswers[exercise.id] === option.letra}
                      onChange={(e) => handleAnswerChange(exercise.id, e.target.value)}
                      disabled={topic?.progreso?.aprobado}
                    />
                    <span>
                      {option.letra}. <span dangerouslySetInnerHTML={{ __html: option.texto }} />
                    </span>
                  </label>
                ))}
              </div>
            ) : (
              <input
                type="text"
                className="answer-input"
                placeholder="Tu respuesta..."
                value={userAnswers[exercise.id] || ''}
                onChange={(e) => handleAnswerChange(exercise.id, e.target.value)}
                disabled={topic?.progreso?.aprobado}
                readOnly={topic?.progreso?.aprobado}
              />
            )}

            {/* Botón enviar (solo si NO hay resultado) */}
            {!result && (
              <>
                {/* Mostrar ayuda solo si el usuario hizo clic en el botón */}
                {showHelp[exercise.id] && exercise.texto_ayuda && (
                  <div
                    className="help-box"
                    dangerouslySetInnerHTML={{ __html: exercise.texto_ayuda }}
                  />
                )}

                <button onClick={handleSubmitAnswer} className="btn btn-primary submit-btn">
                  Enviar Respuesta
                </button>
              </>
            )}

            {/* Resultado inline (solo si APROBADO y tiene resultado) */}
            {topic?.progreso?.aprobado && result && (
              <>
                <div className={`result-box ${result.es_correcta ? 'correct' : 'incorrect'}`}>
                  <h3>{result.es_correcta ? '¡Correcto!' : 'Incorrecto'}</h3>
                  {result.retroalimentacion && (
                    <div
                      className="feedback"
                      dangerouslySetInnerHTML={{ __html: result.retroalimentacion }}
                    />
                  )}
                </div>

                {/* Mostrar ayuda cuando es incorrecto */}
                {!result.es_correcta && exercise.texto_ayuda && (
                  <div className="help-box help-box-auto">
                    <h4>💡 Ayuda</h4>
                    <div dangerouslySetInnerHTML={{ __html: exercise.texto_ayuda }} />
                  </div>
                )}

                <button
                  onClick={handleContinueToNextExercise}
                  className="btn btn-primary submit-btn"
                >
                  {currentExercise < topic.ejercicios.length - 1 ? 'Continuar' : 'Finalizar'}
                </button>
              </>
            )}
          </>
        )}
      </div>


      <div className="progress-indicator">
        Ejercicio {currentExercise + 1} / {topic.ejercicios.length}
      </div>

      <Modal
        isOpen={modal.isOpen}
        onClose={() => setModal({ ...modal, isOpen: false })}
        onConfirm={modal.onConfirm}
        onCancel={modal.onCancel}
        title={modal.title}
        message={modal.message}
        type={modal.type}
        confirmText={modal.confirmText}
        cancelText={modal.cancelText}
        showCancel={modal.showCancel}
      />
    </div>
  );
};


export default TopicPage;



