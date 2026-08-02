import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🔬 EdgeGuard-IoT: Step 04b - State-of-the-Art Benchmark Comparison\n",
    "**Objective:** Empirical comparison of our proposed **EdgeGuard VAE-MLP (INT8 Quantized)** against standard baseline architectures on the CIC-IoT-2023 dataset:\n",
    "1. **Random Forest (RF)** (Classic ML Baseline)\n",
    "2. **XGBoost (XGB)** (Gradient Boosting Baseline)\n",
    "3. **CNN-1D** (Heavy Deep Learning Baseline)\n",
    "4. **EdgeGuard VAE-MLP (INT8)** (Our Latent Compressed Edge AI Architecture)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import json\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from IPython.display import Image, display\n",
    "\n",
    "print('[+] Libraries loaded for Benchmark Analysis.')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 1. Empirical Results Table (Metrics & Resource Footprint)\n",
    "Cargamos las métricas extraídas durante la evaluación empírica en el Test Set (27,949 muestras)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "with open('../models/benchmark_results.json') as f:\n",
    "    results = json.load(f)\n",
    "\n",
    "df_results = pd.DataFrame(results).T\n",
    "df_results['Accuracy (%)'] = df_results['Accuracy'] * 100.0\n",
    "df_results['Latencia (µs/muestra)'] = df_results['Latency_ms'] * 1000.0\n",
    "\n",
    "print('========================================================================================')\n",
    "print('                   TABLA COMPARATIVA ESTADO DEL ARTE (CIC-IoT-2023)                     ')\n",
    "print('========================================================================================')\n",
    "display(df_results[['Accuracy (%)', 'F1_Macro', 'F1_Weighted', 'Latencia (µs/muestra)', 'Size_KB']])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 2. Comparativa Visual: Macro F1-Score"
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
    "--- \n",
    "## 3. Trade-Off Edge AI: Latencia vs Rendimiento vs Tamaño en Disco"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../models/benchmark_latency_tradeoff.png'):\n",
    "    display(Image('../models/benchmark_latency_tradeoff.png'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 4. Cuadrícula de Matrices de Confusión (2x2 Grid)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../models/benchmark_confusion_grid.png'):\n",
    "    display(Image('../models/benchmark_confusion_grid.png'))"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("E:/PROYECTO DE INVESTIGACION/dataset/MERGED_CSV/notebooks/04b_Benchmark_Comparison.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print("[+] Notebook 04b_Benchmark_Comparison.ipynb creado exitosamente.")
