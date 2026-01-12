import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { lessonService } from '../api/lessonService';
import { mlAdaptiveService } from '../api/mlAdaptiveService';
import { useScreenTracking } from '../hooks/useScreenTracking';
import './LessonsPage.css';
import './HTMLContent.css'; // Importar estilos para HTML


const LessonsPage = () => {
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [checkingEvaluations, setCheckingEvaluations] = useState(true);


  const { user, logout } = useAuth();
  const navigate = useNavigate();

  // Tracking de pantalla
  useScreenTracking('LISTA_LECCIONES');


  useEffect(() => {
    checkEvaluationsAndLoadLessons();
  }, []);


  const checkEvaluationsAndLoadLessons = async () => {
    try {
      setCheckingEvaluations(true);

      // Verificar estado de evaluaciones
      const estadoEvaluaciones = await mlAdaptiveService.getEvaluationStatus();

      // Si no ha completado la autoeficacia PRE, redirigir
      if (!estadoEvaluaciones.completo_autoeficacia_pre) {
        navigate('/cuestionario-inicial');
        return;
      }

      // Si no ha completado el examen diagnóstico, redirigir
      if (!estadoEvaluaciones.completo_diagnostico) {
        navigate('/examen-diagnostico');
        return;
      }

      // Si ya completó ambos, cargar lecciones normalmente
      await loadLessons();

    } catch (err) {
      console.error('Error verificando evaluaciones:', err);
      // Si hay error, intentar cargar lecciones de todos modos
      await loadLessons();
    } finally {
      setCheckingEvaluations(false);
    }
  };


  const loadLessons = async () => {
    try {
      setLoading(true);
      const data = await lessonService.getAllLessons();
      setLessons(data);
    } catch (err) {
      setError('Error al cargar las lecciones. Verifica tu conexión.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };


  const handleLessonClick = (lesson) => {
    // Verificar si la lección está disponible (orden secuencial)
    if (lesson.orden === 1) {
      navigate(`/leccion/${lesson.id}`);
      return;
    }


    // Verificar si la lección anterior está completada
    const previousLesson = lessons.find(l => l.orden === lesson.orden - 1);
    if (previousLesson && previousLesson.progreso.completada) {
      navigate(`/leccion/${lesson.id}`);
    } else {
      alert('Debes completar la lección anterior primero');
    }
  };


  const handleLogout = async () => {
    await logout();
    navigate('/');
  };


  if (loading || checkingEvaluations) {
    return (
      <div className="lessons-container">
        <div className="loading">
          {checkingEvaluations ? 'Verificando evaluaciones...' : 'Cargando lecciones...'}
        </div>
      </div>
    );
  }


  if (error) {
    return (
      <div className="lessons-container">
        <div className="error-box">{error}</div>
      </div>
    );
  }


  return (
    <div className="lessons-container">
      <header className="lessons-header">
        <div className="header-content">
          <h1>MateLog</h1>
          <div className="user-info">
            <span>Hola, {user?.username}</span>
            <button onClick={handleLogout} className="logout-btn">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>


      <main className="lessons-content">
        <div className="lessons-intro">
          <h2>Mis Lecciones</h2>
          <p>Selecciona una lección para comenzar. Debes completar las lecciones en orden.</p>
        </div>

        {/* Mostrar botones de evaluaciones finales si todas las lecciones están completadas */}
        {lessons.length > 0 && lessons.every(l => l.progreso.completada) && (
          <div className="final-evaluations-banner">
            <h3>¡Felicidades! Has completado todas las lecciones</h3>
            <p>Ahora puedes realizar las evaluaciones finales:</p>
            <div className="evaluation-buttons">
              <button
                onClick={() => navigate('/cuestionario-final')}
                className="evaluation-btn"
              >
                Cuestionario Final
              </button>
              <button
                onClick={() => navigate('/examen-final')}
                className="evaluation-btn"
              >
                Examen Final
              </button>
            </div>
          </div>
        )}

        <div className="lessons-grid">
          {lessons.map((lesson) => {
            const isLocked = lesson.orden > 1 &&
              !lessons.find(l => l.orden === lesson.orden - 1)?.progreso.completada;
            const progress = lesson.progreso.porcentaje_completado || 0;


            return (
              <div
                key={lesson.id}
                className={`lesson-card ${isLocked ? 'locked' : ''}`}
                onClick={() => !isLocked && handleLessonClick(lesson)}
              >
                <div className="lesson-number">Lección {lesson.orden}</div>
               
                {isLocked && (
                  <div className="lock-icon">🔒</div>
                )}
               
                <h3 className="lesson-title">{lesson.titulo}</h3>
               
                {/* FIX: Renderizar descripción como HTML */}
                <div
                  className="lesson-description content-text"
                  dangerouslySetInnerHTML={{ __html: lesson.descripcion }}
                />
               
                <div className="lesson-footer">
                  <div className="progress-info">
                    <span className="progress-label">Progreso</span>
                    <span className="progress-percentage">{Math.round(progress)}%</span>
                  </div>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                </div>


                {lesson.progreso.completada && (
                  <div className="completed-badge">✓ Completada</div>
                )}
              </div>
            );
          })}
        </div>


        {lessons.length === 0 && (
          <div className="empty-state">
            <p>No hay lecciones disponibles en este momento.</p>
          </div>
        )}
      </main>
    </div>
  );
};


export default LessonsPage;


