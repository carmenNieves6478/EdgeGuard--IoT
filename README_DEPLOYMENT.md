# 🚀 EdgeGuard-IoT: Deployment & Execution Guide

## 📌 Guía de Despliegue y Ejecución Local / Cloud

Este documento describe los pasos completos para ejecutar localmente o desplegar en la nube (Render / Docker) el proyecto **"EdgeGuard-IoT: Sistema Adaptativo de Detección de Botnets Multiclase mediante VAE-MLP y XAI en el Borde"**.

---

## 💻 1. Ejecución Local (Miniconda / Python)

### Step 1: Iniciar el Backend API (FastAPI)
```bash
conda activate investigacion
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
* **Endpoint interactivo Swagger Docs:** `http://localhost:8000/docs`
* **Endpoint de Salud:** `http://localhost:8000/health`

### Step 2: Iniciar el Dashboard Frontend (Streamlit)
En otra terminal:
```bash
conda activate investigacion
streamlit run dashboard/app.py --server.port 8501
```
* **URL Dashboard:** `http://localhost:8501`

### Step 3: Iniciar el Simulador de Tráfico IoT
En una tercera terminal para generar flujo continuo de paquetes:
```bash
conda activate investigacion
python simulator.py
```

---

## 🐳 2. Ejecución Local con Docker Compose

Para levantar ambos servicios en contenedores Docker aislados:

```bash
# Construir e Iniciar Contenedores
docker build -t edgeguard-backend -f Dockerfile .
docker run -d -p 8000:8000 --name backend edgeguard-backend

docker build -t edgeguard-frontend -f Dockerfile.frontend .
docker run -d -p 8501:8501 -e API_URL="http://host.docker.internal:8000" --name frontend edgeguard-frontend
```

---

## ☁️ 3. Despliegue en Render (Web Services Gratuitos)

### Método A: Despliegue Automático con `render.yaml` (Blueprint)
1. Conecta tu repositorio de GitHub a tu cuenta de **Render.com**.
2. En el panel de Render, selecciona **Blueprints** $\rightarrow$ **New Blueprint Instance**.
3. Selecciona tu repositorio `EdgeGuard-IoT`. Render detectará automáticamente el archivo `render.yaml` y creará ambos Web Services (`edgeguard-backend` y `edgeguard-frontend`).
4. Haz clic en **Apply**.

### Método B: Despliegue Manual en Render

#### Backend Service (`edgeguard-backend`):
1. Crear **New Web Service** en Render.
2. Conectar repositorio GitHub.
3. Configuración:
   - **Name:** `edgeguard-backend`
   - **Environment:** `Docker`
   - **Dockerfile Path:** `Dockerfile`
   - **Plan:** Free
4. Guardar y Desplegar. Copiar la URL pública asignada (ejemplo: `https://edgeguard-backend.onrender.com`).

#### Frontend Service (`edgeguard-frontend`):
1. Crear **New Web Service** en Render.
2. Conectar repositorio GitHub.
3. Configuración:
   - **Name:** `edgeguard-frontend`
   - **Environment:** `Docker`
   - **Dockerfile Path:** `Dockerfile.frontend`
   - **Plan:** Free
4. En **Environment Variables**:
   - `API_URL`: `https://edgeguard-backend.onrender.com` (la URL del backend).
5. Guardar y Desplegar.

---

## 🛡️ Estructura Completa del Proyecto
```
MERGED_CSV/
├── data/
│   └── processed/
│       ├── train.parquet
│       ├── val.parquet
│       └── test.parquet
├── models/
│   ├── scaler.joblib
│   ├── label_encoder.joblib
│   ├── meta_info.json
│   ├── vae_mlp_best.pt
│   ├── vae_mlp.onnx
│   ├── vae_mlp_quantized.onnx
│   ├── shap_summary_plot.png
│   └── confusion_matrix.png
├── notebooks/
│   ├── 01_EDA_and_Preprocessing.ipynb
│   ├── 02_Model_Training_VAE_MLP.ipynb
│   └── 03_Quantization_and_XAI.ipynb
├── api/
│   └── main.py
├── dashboard/
│   └── app.py
├── process_dataset.py
├── train_vae_mlp.py
├── quantize_and_xai.py
├── simulator.py
├── requirements.txt
├── Dockerfile
├── Dockerfile.frontend
├── render.yaml
└── README_DEPLOYMENT.md
```
