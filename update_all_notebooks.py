import json
import os
import subprocess

# -------------------------------------------------------------
# NOTEBOOK 02: VAE-MLP Training & Architecture
# -------------------------------------------------------------
nb02 = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🧠 EdgeGuard-IoT: Step 02 - Hybrid VAE-MLP Model Training & Evaluation\n",
    "**Framework:** PyTorch (GPU accelerated)  \n",
    "**Architecture:** Variational Autoencoder (VAE) Latent Compressor (39 → 16 dimensions) + Multiclass MLP Classifier."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os, json, joblib\n",
    "import numpy as np, pandas as pd\n",
    "import matplotlib.pyplot as plt, seaborn as sns\n",
    "from IPython.display import Image, display\n",
    "\n",
    "print('[+] Visualizaciones y métricas de entrenamiento cargadas.')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Curvas Históricas de Entrenamiento (Pérdida & Val F1-Macro por Época)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../results/reports_and_plots/training_history_loss_f1.png'):\n",
    "    display(Image('../results/reports_and_plots/training_history_loss_f1.png'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Evaluación en Test Set: Matriz de Confusión Absoluta y Normalizada (%)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../results/reports_and_plots/confusion_matrices_combined.png'):\n",
    "    display(Image('../results/reports_and_plots/confusion_matrices_combined.png'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Curvas ROC Multiclase (One-vs-Rest) con Área Bajo la Curva (AUC)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../results/reports_and_plots/roc_curves_multiclass.png'):\n",
    "    display(Image('../results/reports_and_plots/roc_curves_multiclass.png'))"
   ]
  }
 ],
 "metadata": { "language_info": { "name": "python" } },
 "nbformat": 4, "nbformat_minor": 2
}

with open("E:/PROYECTO DE INVESTIGACION/dataset/MERGED_CSV/notebooks/02_Model_Training_VAE_MLP.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb02, f, indent=2)

# -------------------------------------------------------------
# NOTEBOOK 03: Quantization & XAI SHAP
# -------------------------------------------------------------
nb03 = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# ⚡ EdgeGuard-IoT: Step 03 - INT8 Post-Training Quantization & Explainable AI (SHAP)\n",
    "**Objective:** Export PyTorch model to ONNX, apply INT8 dynamic quantization for Edge AI deployment, evaluate compression & latency speedups, and calculate SHAP feature importances."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os, json, numpy as np, pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "from IPython.display import Image, display\n",
    "\n",
    "size_fp32 = os.path.getsize('../models/vae_mlp.onnx') / 1024\n",
    "size_int8 = os.path.getsize('../models/vae_mlp_quantized.onnx') / 1024\n",
    "\n",
    "print('====================================================')\n",
    "print('      MLOps FOOTPRINT DE COMPRESIÓN EN EL BORDE      ')\n",
    "print('====================================================')\n",
    "print(f\" - Modelo ONNX Float32:  {size_fp32:.2f} KB\")\n",
    "print(f\" - Modelo ONNX INT8:     {size_int8:.2f} KB\")\n",
    "print(f\" - Tasa de Compresión:  {((size_fp32 - size_int8)/size_fp32)*100:.2f}%\")\n",
    "print('====================================================')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Explicabilidad XAI en Tiempo Real (SHAP Feature Importance)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../results/reports_and_plots/shap_summary_plot.png'):\n",
    "    display(Image('../results/reports_and_plots/shap_summary_plot.png'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Curvas Precision-Recall (PR Curves) por Categoría de Ataque"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../results/reports_and_plots/precision_recall_curves.png'):\n",
    "    display(Image('../results/reports_and_plots/precision_recall_curves.png'))"
   ]
  }
 ],
 "metadata": { "language_info": { "name": "python" } },
 "nbformat": 4, "nbformat_minor": 2
}

with open("E:/PROYECTO DE INVESTIGACION/dataset/MERGED_CSV/notebooks/03_Quantization_and_XAI.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb03, f, indent=2)

# -------------------------------------------------------------
# NOTEBOOK 04b: Benchmark Comparison State-of-the-Art
# -------------------------------------------------------------
nb04b = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🔬 EdgeGuard-IoT: Step 04b - State-of-the-Art Benchmark & Stacking Ensemble Comparison\n",
    "**Objective:** Empirical evaluation comparing standard baseline algorithms (Random Forest, XGBoost, LightGBM, CNN-1D) against our **EdgeGuard VAE-MLP INT8** and **Hybrid Stacking Ensemble**."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os, json, numpy as np, pandas as pd\n",
    "from IPython.display import Image, display\n",
    "\n",
    "with open('../models/benchmark_results.json') as f:\n",
    "    results = json.load(f)\n",
    "\n",
    "df_results = pd.DataFrame(results).T\n",
    "df_results['Accuracy (%)'] = df_results['Accuracy'] * 100.0\n",
    "df_results['Latencia (µs)'] = df_results['Latency_ms'] * 1000.0\n",
    "\n",
    "print('========================================================================================')\n",
    "print('                   TABLA GENERAL DE BENCHMARK COMPARATIVO ESTADO DEL ARTE              ')\n",
    "print('========================================================================================')\n",
    "display(df_results[['Accuracy (%)', 'F1_Macro', 'F1_Weighted', 'Precision_Macro', 'Recall_Macro', 'Latencia (µs)', 'Size_KB']])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Comparativa de Macro F1-Score entre Algoritmos"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../models/benchmark_f1_comparison.png'):\n",
    "    display(Image('../models/benchmark_f1_comparison.png'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Análisis del Trade-Off Edge AI: Latencia (µs) vs F1-Score vs Footprint en Disco"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../results/reports_and_plots/benchmark_latency_tradeoff.png'):\n",
    "    display(Image('../results/reports_and_plots/benchmark_latency_tradeoff.png'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Desglose de Desempeño por Categoría de Ataque (Precision, Recall, F1-Score)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../results/reports_and_plots/metrics_per_class_barplot.png'):\n",
    "    display(Image('../results/reports_and_plots/metrics_per_class_barplot.png'))"
   ]
  }
 ],
 "metadata": { "language_info": { "name": "python" } },
 "nbformat": 4, "nbformat_minor": 2
}

with open("E:/PROYECTO DE INVESTIGACION/dataset/MERGED_CSV/notebooks/04b_Benchmark_Comparison.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb04b, f, indent=2)

print("[+] Estructuras de los 4 notebooks actualizadas con las visualizaciones Senior.")
