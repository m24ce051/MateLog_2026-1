import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { SessionTrackingProvider } from './context/SessionTrackingContext';
import ProtectedRoute from './components/ProtectedRoute';
import AuthPage from './pages/AuthPage';
import LessonsPage from './pages/LessonsPage';
import LessonDetailPage from './pages/LessonDetailPage';
import TopicPage from './pages/TopicPage';
import AutoeficaciaScalePage from './pages/AutoeficaciaScalePage';
import ExamPage from './pages/ExamPage';
import './App.css';


function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <SessionTrackingProvider>
          <Routes>
            {/* Ruta pública - Login/Registro */}
            <Route path="/" element={<AuthPage />} />

            {/* Rutas protegidas - requieren autenticación */}
            <Route
              path="/lecciones"
              element={
                <ProtectedRoute>
                  <LessonsPage />
                </ProtectedRoute>
              }
            />

            <Route
              path="/leccion/:lessonId"
              element={
                <ProtectedRoute>
                  <LessonDetailPage />
                </ProtectedRoute>
              }
            />

            <Route
              path="/tema/:topicId"
              element={
                <ProtectedRoute>
                  <TopicPage />
                </ProtectedRoute>
              }
            />

            {/* Rutas para cuestionarios de personalidad */}
            <Route
              path="/cuestionario-inicial"
              element={
                <ProtectedRoute>
                  <AutoeficaciaScalePage tipo="PRE" />
                </ProtectedRoute>
              }
            />

            <Route
              path="/cuestionario-final"
              element={
                <ProtectedRoute>
                  <AutoeficaciaScalePage tipo="POST" />
                </ProtectedRoute>
              }
            />

            {/* Rutas para exámenes */}
            <Route
              path="/examen-diagnostico"
              element={
                <ProtectedRoute>
                  <ExamPage tipo="DIAGNOSTICO" />
                </ProtectedRoute>
              }
            />

            <Route
              path="/examen-final"
              element={
                <ProtectedRoute>
                  <ExamPage tipo="FINAL" />
                </ProtectedRoute>
              }
            />

            {/* Ruta por defecto - redirigir a auth */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </SessionTrackingProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}


export default App;




