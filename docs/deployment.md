# Deployment & Hosting Guide

This document describes how to deploy the **Eenadu 4C Lipika Translator Web Application** to Render, Railway, Vercel, or local Docker environments.

---

## 1. Render Deployment (Recommended)

Render offers quick, direct integration from GitHub repositories.

### Using Blueprint (one-click deployment)
The repository contains a `render.yaml` file. Render will automatically parse it when you link your repository.

### Manual Render Setup:
1. Log into your account at [Render](https://render.com).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository.
4. Set the following parameters:
   - **Name**: `eenadu-4c-translator`
   - **Environment**: `Python`
   - **Region**: Select the region closest to your users.
   - **Branch**: `main` (or `master`)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Click **Advanced** and add these Environment Variables:
   - `PORT`: `8000` (or leave default, Render will supply this automatically)
   - `LOG_LEVEL`: `INFO`
6. Click **Deploy Web Service**. Render will install dependencies and start the app at `https://[your-service-name].onrender.com`.

---

## 2. Railway Deployment

Railway deploys standard Docker/Python templates automatically.

1. Log into [Railway](https://railway.app).
2. Click **New Project** → **Deploy from GitHub repo**.
3. Choose the translator repository.
4. Click **Deploy Now**. Railway will read the `Procfile` or `Dockerfile` and provision Uvicorn.
5. Under service settings, click **Generate Domain** to get a public URL.

---

## 3. Vercel Deployment

Vercel is optimized for static sites but supports Python Serverless Functions.

To deploy on Vercel:
1. Create a `vercel.json` file in the root if serverless setup is required.
   *(Since this is a full FastAPI server handling docx binary uploads, deploying to a persistent Render or Railway web service is recommended over Vercel's serverless size/execution-time limits).*

---

## 4. Local Docker Setup

You can run the web app in a containerized environment locally.

### Dockerfile Run
```bash
# Build the container
docker build -t telugu-translator .

# Start the container
docker run -p 8000:8000 telugu-translator
```
Open `http://localhost:8000` to access the application.

### Docker Compose Run
```bash
# Start container orchestration
docker-compose up --build
```
This mounts local folders for active logging (`logs/`) and user preferences (`sandbox/`) outside the container.
