# Deployment Guide

## 1. Frontend (Netlify)

The frontend is ready to search on Netlify.

1. Push this repository to GitHub.
2. Connect the repository to Netlify.
3. Netlify will detect the `netlify.toml` and configure the build automatically:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`

## 2. Backend (Render / Railway)

The backend uses `pandas` and `scikit-learn`, which are too large for Netlify Functions (AWS Lambda). You should deploy the backend to a container-based service like Render.com or Railway.app.

### Deploying to Render:

1. Create a new "Web Service" on Render connected to your repo.
2. Root Directory: `backend`
3. Environment: `Python 3`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Add an Environment Variable `PYTHON_VERSION` = `3.9.0` (or matching your local version).

### Connect Frontend to Backend:

Once the backend is deployed (e.g., `https://my-flask-app.onrender.com`), update the frontend API URL.
In `frontend/src/App.jsx`, change:

```javascript
const response = await fetch('/predict', ...
```

to

```javascript
const response = await fetch('https://my-flask-app.onrender.com/predict', ...
```

(Or use an environment variable `VITE_API_URL` and update the fetch call).
