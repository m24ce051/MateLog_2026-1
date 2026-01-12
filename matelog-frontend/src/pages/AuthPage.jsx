import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useScreenTracking } from '../hooks/useScreenTracking';
import { fetchCSRFToken } from '../api/axios';
import Toast from '../components/Toast';
import './AuthPage.css';

// Constantes para valores iniciales y opciones
const INITIAL_FORM_DATA = {
  username: '',
  password: '',
  password_confirm: '',
  codigo_participacion: '',
  grupo: '',
  especialidad: '',
  genero: '',
  edad: '',
};

const GRUPOS = [
  { value: 'A', label: 'Grupo A' },
  { value: 'B', label: 'Grupo B' },
  { value: 'C', label: 'Grupo C' },
  { value: 'D', label: 'Grupo D' },
];

const ESPECIALIDADES = [
  { value: 'INFORMATICA', label: 'Informática' },
  { value: 'AGRONOMIA', label: 'Agronomía' },
  { value: 'ADMINISTRACION', label: 'Administración' },
  { value: 'ELECTRONICA', label: 'Electrónica' },
];

const GENEROS = [
  { value: 'M', label: 'Masculino' },
  { value: 'F', label: 'Femenino' },
  { value: 'O', label: 'Otro' },
  { value: 'N', label: 'Prefiero no decir' },
];

const EDADES = [
  { value: '14', label: '14 años' },
  { value: '15', label: '15 años' },
  { value: '16', label: '16 años' },
  { value: '17', label: '17 años' },
  { value: '18', label: '18 años' },
];

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState(INITIAL_FORM_DATA);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const usernameInputRef = useRef(null);


  const { login, register } = useAuth();
  const navigate = useNavigate();
 
  // Tracking de pantalla
  useScreenTracking(isLogin ? 'LOGIN' : 'REGISTRO');


  // Obtener CSRF token al montar el componente y enfocar input
  useEffect(() => {
    fetchCSRFToken();
    if (usernameInputRef.current) {
      usernameInputRef.current.focus();
    }
  }, []);


  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Limpiar error del campo al escribir
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };


  const validateForm = () => {
    const newErrors = {};


    if (!formData.username.trim()) {
      newErrors.username = 'El usuario es requerido';
    }


    if (!formData.password) {
      newErrors.password = 'La contraseña es requerida';
    } else if (formData.password.length < 6) {
      newErrors.password = 'La contraseña debe tener al menos 6 caracteres';
    }


    if (!isLogin) {
      if (formData.password !== formData.password_confirm) {
        newErrors.password_confirm = 'Las contraseñas no coinciden';
      }


      if (!formData.codigo_participacion.trim()) {
        newErrors.codigo_participacion = 'El código de participación es requerido';
      }


      if (!formData.grupo.trim()) {
        newErrors.grupo = 'Selecciona tu grupo';
      }


      if (!formData.especialidad.trim()) {
        newErrors.especialidad = 'Selecciona tu especialidad';
      }


      if (!formData.genero) {
        newErrors.genero = 'Selecciona tu género';
      }


      if (!formData.edad) {
        newErrors.edad = 'Selecciona tu edad';
      }
    }


    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };


  const showToast = (message, type = 'success') => {
    setToast({ message, type });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setErrors({});

    try {
      if (isLogin) {
        const result = await login({
          username: formData.username,
          password: formData.password
        });

        if (result.success) {
          showToast('¡Inicio de sesión exitoso!', 'success');
          navigate('/lecciones');
        } else {
          const errorMessage = result.error || 'Error al iniciar sesión';
          if (errorMessage.includes('credenciales') || errorMessage.includes('usuario') || errorMessage.includes('contraseña')) {
            setErrors({ general: 'Usuario o contraseña incorrectos. Por favor, verifica tus datos.' });
          } else if (errorMessage.includes('red') || errorMessage.includes('conexión')) {
            setErrors({ general: 'Error de conexión con el servidor. Por favor, verifica tu conexión a internet.' });
          } else {
            setErrors({ general: errorMessage });
          }
        }
      } else {
        const result = await register(formData);

        if (result.success) {
          showToast('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success');
          setIsLogin(true);
          setFormData({
            ...INITIAL_FORM_DATA,
            username: formData.username
          });
        } else {
          if (typeof result.error === 'object') {
            setErrors(result.error);
          } else {
            const errorMessage = result.error || 'Error al registrar usuario';
            if (errorMessage.includes('ya existe') || errorMessage.includes('duplicado')) {
              setErrors({ general: 'Este nombre de usuario ya está registrado. Por favor, elige otro.' });
            } else if (errorMessage.includes('red') || errorMessage.includes('conexión')) {
              setErrors({ general: 'Error de conexión con el servidor. Por favor, verifica tu conexión a internet.' });
            } else {
              setErrors({ general: errorMessage });
            }
          }
        }
      }
    } catch (error) {
      const errorMessage = error.message || '';
      if (errorMessage.includes('fetch') || errorMessage.includes('Network')) {
        setErrors({ general: 'No se pudo conectar con el servidor. Verifica tu conexión a internet y vuelve a intentarlo.' });
      } else {
        setErrors({ general: 'Ocurrió un error inesperado. Por favor, intenta nuevamente.' });
      }
    } finally {
      setLoading(false);
    }
  };


  const switchMode = () => {
    setIsLogin(!isLogin);
    setFormData({
      ...INITIAL_FORM_DATA,
      username: formData.username
    });
    setErrors({});
  };


  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>MateLog</h1>
          <p>Aprendizaje de Lógica Matemática</p>
        </div>


        <div className="auth-tabs">
          <button
            className={`tab ${isLogin ? 'active' : ''}`}
            onClick={() => !isLogin && switchMode()}
          >
            Iniciar Sesión
          </button>
          <button
            className={`tab ${!isLogin ? 'active' : ''}`}
            onClick={() => isLogin && switchMode()}
          >
            Registrarse
          </button>
        </div>


        <form onSubmit={handleSubmit} className="auth-form">
          {errors.general && (
            <div className="error-message">{errors.general}</div>
          )}


          <div className="form-group">
            <label htmlFor="username">Usuario</label>
            <input
              ref={usernameInputRef}
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Ingresa tu usuario"
              disabled={loading}
            />
            {errors.username && <span className="error-text">{errors.username}</span>}
          </div>


          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Mínimo 6 caracteres"
              disabled={loading}
            />
            {errors.password && <span className="error-text">{errors.password}</span>}
          </div>


          {!isLogin && (
            <>
              <div className="form-group">
                <label htmlFor="password_confirm">Confirmar Contraseña</label>
                <input
                  type="password"
                  id="password_confirm"
                  name="password_confirm"
                  value={formData.password_confirm}
                  onChange={handleChange}
                  placeholder="Repite tu contraseña"
                  disabled={loading}
                />
                {errors.password_confirm && (
                  <span className="error-text">{errors.password_confirm}</span>
                )}
              </div>


              <div className="form-group">
                <label htmlFor="codigo_participacion">Código de Participación</label>
                <input
                  type="text"
                  id="codigo_participacion"
                  name="codigo_participacion"
                  value={formData.codigo_participacion}
                  onChange={handleChange}
                  placeholder="Código proporcionado por tu instructor"
                  disabled={loading}
                  maxLength={10}
                  
                />
                {errors.codigo_participacion && (
                  <span className="error-text">{errors.codigo_participacion}</span>
                )}
              </div>


              <div className="form-group">
                <label htmlFor="grupo">Grupo</label>
                <select
                  id="grupo"
                  name="grupo"
                  value={formData.grupo}
                  onChange={handleChange}
                  disabled={loading}
                >
                  <option value="">Selecciona tu grupo</option>
                  {GRUPOS.map(grupo => (
                    <option key={grupo.value} value={grupo.value}>{grupo.label}</option>
                  ))}
                </select>
                {errors.grupo && <span className="error-text">{errors.grupo}</span>}
              </div>


              <div className="form-group">
                <label htmlFor="especialidad">Especialidad</label>
                <select
                  id="especialidad"
                  name="especialidad"
                  value={formData.especialidad}
                  onChange={handleChange}
                  disabled={loading}
                >
                  <option value="">Selecciona tu especialidad</option>
                  {ESPECIALIDADES.map(esp => (
                    <option key={esp.value} value={esp.value}>{esp.label}</option>
                  ))}
                </select>
                {errors.especialidad && <span className="error-text">{errors.especialidad}</span>}
              </div>


              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="genero">Género</label>
                  <select
                    id="genero"
                    name="genero"
                    value={formData.genero}
                    onChange={handleChange}
                    disabled={loading}
                  >
                    <option value="">Selecciona...</option>
                    {GENEROS.map(gen => (
                      <option key={gen.value} value={gen.value}>{gen.label}</option>
                    ))}
                  </select>
                  {errors.genero && <span className="error-text">{errors.genero}</span>}
                </div>


                <div className="form-group">
                  <label htmlFor="edad">Edad</label>
                  <select
                    id="edad"
                    name="edad"
                    value={formData.edad}
                    onChange={handleChange}
                    disabled={loading}
                  >
                    <option value="">Selecciona...</option>
                    {EDADES.map(edad => (
                      <option key={edad.value} value={edad.value}>{edad.label}</option>
                    ))}
                  </select>
                  {errors.edad && <span className="error-text">{errors.edad}</span>}
                </div>
              </div>
            </>
          )}


          <button
            type="submit"
            className="submit-btn"
            disabled={loading}
          >
            {loading ? (isLogin ? 'Iniciando sesión...' : 'Registrando usuario...') : (isLogin ? 'Iniciar Sesión' : 'Registrarse')}
          </button>
        </form>
      </div>

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};


export default AuthPage;



