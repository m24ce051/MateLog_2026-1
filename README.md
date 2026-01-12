# MateLog - Ambiente Inteligente de Aprendizaje para enseñar Lógica Matemática

Esta plataforma web está diseñada para apoyar el aprendizaje de lógica matemática en estudiantes de nivel medio superior. Al ingresar por primera vez, los usuarios completan un cuestionario de personalidad y un examen diagnóstico que permite identificar sus conocimientos iniciales. Durante el curso, el sistema registra de manera continua el progreso y las actividades realizadas, generando información valiosa para su análisis. Con base en estos datos, se diseñan lecciones personalizadas y contenidos adaptables, ajustados al perfil y las necesidades de cada alumno. Al concluir el curso, los estudiantes responden nuevamente el cuestionario de personalidad y realizan un examen final, con el propósito de evaluar el conocimiento adquirido y medir su avance.


## Stack por realizar

- **Backend:** Django 5.0.1 + DRF + PostgreSQL
- **Frontend:** React 18 + Vite
- **Deployment:** Render + Vercel

## Instalación Local

### Backend
```bash
cd matelog_backend
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd matelog-frontend
npm install
npm run dev
