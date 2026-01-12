# MateLog - Ambiente Inteligente de Aprendizaje para enseñar Lógica Matemática

Plataforma web para aprendizaje de lógica matemática con sistema de progreso y tracking.

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
