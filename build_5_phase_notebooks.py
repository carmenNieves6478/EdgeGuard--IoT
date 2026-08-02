import os
import json
import subprocess

BASE_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV"
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")

# ------------------------------------------------------------------------------
# NOTEBOOK 01: EDA, Data Quality & Statistical Feature Selection (Phase 1)
# ------------------------------------------------------------------------------
nb01 = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🔍 EdgeGuard-IoT: FASE 1 - Análisis Exploratorio, Diccionario de Datos y Selección Estadística de Características\n",
    "**Dataset:** CIC-IoT-2023 (Tráfico Multiclase de Dispositivos IoT: Benign + 7 Categorías de Ataques Botnet)  \n",
    "**Objetivo:** Verificar la calidad de los datos, crear el diccionario formal de variables, aplicar limpieza rigurosa y ejecutar selección de características mediante **ANOVA F-Test, Mutual Information, Correlación de Pearson y Random Forest Gini Importance**."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os, json, pandas as pd, numpy as np\n",
    "from IPython.display import display, Image\n",
    "\n",
    "print('[*] Cargando Diccionario de Datos Formal (FASE 1)...')\n",
    "df_dict = pd.read_csv('../results/reports_and_plots/data_dictionary.csv')\n",
    "display(df_dict.head(15))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Distribución de Clases (Balanceo Estratificado)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../results/reports_and_plots/class_distribution.png'):\n",
    "    display(Image('../results/reports_and_plots/class_distribution.png'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Selección Estadística de Características (ANOVA F-Score & Random Forest Importance)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_stat = pd.read_csv('../results/reports_and_plots/feature_selection_stats.csv')\n",
    "display(df_stat.head(15))\n",
    "\n",
    "if os.path.exists('../results/reports_and_plots/feature_selection_barplot.png'):\n",
    "    display(Image('../results/reports_and_plots/feature_selection_barplot.png'))"
   ]
  }
 ],
 "metadata": { "language_info": { "name": "python" } },
 "nbformat": 4, "nbformat_minor": 2
}

# ------------------------------------------------------------------------------
# NOTEBOOK 02: Design & Architecture of VAE-MLP Model (Phase 2)
# ------------------------------------------------------------------------------
nb02 = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 📐 EdgeGuard-IoT: FASE 2 - Diseño y Configuración del Modelo Híbrido VAE-MLP\n",
    "**Arquitectura:** Variational Autoencoder (VAE) Latent Compressor (39 → 16 dims) + Clasificador Multiclase MLP.  \n",
    "**Función de Pérdida Combinada:** $\\mathcal{L}_{total} = 0.3 \\cdot \\text{MSE}_{Recon} + 1.0 \\cdot \\text{ClassWeightedCE}$"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os, json, joblib\n",
    "from IPython.display import display, Image\n",
    "\n",
    "print('========================================================================')\n",
    "print('      CONFIGURACIÓN Y PARÁMETROS DEL MODELO EDGEGUARD VAE-MLP          ')\n",
    "print('========================================================================')\n",
    "print(' - Dimensión de Entrada:           39 Características de Red')\n",
    "print(' - Latent Space Bottleneck (z):    16 Dimensiones')\n",
    "print(' - Capas del Encoder VAE:          39 → 64 → 32 → (mu, logvar) 16')\n",
    "print(' - Capas del Decoder VAE:          16 → 32 → 64 → 39')\n",
    "print(' - Capas del Clasificador MLP:     16 → 32 (Dropout 0.20) → 16 → 8 Clases')\n",
    "print(' - Optimizador:                    AdamW (lr=2e-3, weight_decay=1e-4)')\n",
    "print(' - Épocas de Entrenamiento:        40 Épocas sobre CUDA GPU')\n",
    "print('========================================================================')"
   ]
  }
 ],
 "metadata": { "language_info": { "name": "python" } },
 "nbformat": 4, "nbformat_minor": 2
}

# ------------------------------------------------------------------------------
# NOTEBOOK 03: Training, Monitored Curves & INT8 Quantization (Phase 3)
# ------------------------------------------------------------------------------
nb03 = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# ⚡ EdgeGuard-IoT: FASE 3 - Preprocesamiento, Entrenamiento y Cuantificación INT8\n",
    "**Objetivo:** Monitoreo de pérdidas, validación en GPU, exportación a ONNX y cuantificación dinámicas a INT8 para despliegue Edge AI ($21.67\\text{ KB}$)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "from IPython.display import display, Image\n",
    "\n",
    "if os.path.exists('../results/reports_and_plots/training_history_loss_f1.png'):\n",
    "    display(Image('../results/reports_and_plots/training_history_loss_f1.png'))"
   ]
  }
 ],
 "metadata": { "language_info": { "name": "python" } },
 "nbformat": 4, "nbformat_minor": 2
}

# ------------------------------------------------------------------------------
# NOTEBOOK 04: Exhaustive Evaluation, ROC, PR, 5-Fold CV & Threshold Tuning (Phase 4)
# ------------------------------------------------------------------------------
nb04 = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 📈 EdgeGuard-IoT: FASE 4 - Evaluación del Desempeño, Curvas ROC/PR, 5-Fold CV y Ajuste de Umbrales\n",
    "**Objetivo:** Evaluación rigurosa en test set (**27,949 muestras**), análisis de falsos positivos/negativos, validación cruzada de 5 pliegues y sintonización de umbrales de detección."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os, pandas as pd\n",
    "from IPython.display import display, Image\n",
    "\n",
    "print('[1/3] Resultados de Validación Cruzada Estratificada (5-Fold Cross-Validation):')\n",
    "df_cv = pd.read_csv('../results/reports_and_plots/5fold_cross_validation_results.csv')\n",
    "display(df_cv)\n",
    "\n",
    "print('[2/3] Resultados de Ajuste de Umbrales (Threshold Tuning):')\n",
    "df_th = pd.read_csv('../results/reports_and_plots/threshold_tuning_results.csv')\n",
    "display(df_th)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Curvas ROC Multiclase (One-vs-Rest) con AUC por Clase"
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
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Curvas Precision-Recall (PR-AUC)"
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
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Matriz de Confusión Absoluta y Normalizada (%)"
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
  }
 ],
 "metadata": { "language_info": { "name": "python" } },
 "nbformat": 4, "nbformat_minor": 2
}

# ------------------------------------------------------------------------------
# NOTEBOOK 05: Benchmark Comparison, XAI SHAP & Efficacy Determination (Phase 5)
# ------------------------------------------------------------------------------
nb05 = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🔬 EdgeGuard-IoT: FASE 5 - Comparación Estado del Arte, Interpretación XAI (SHAP) y Determinación de la Eficacia\n",
    "**Objetivo:** Enfrantamiento empírico de nuestro **EdgeGuard VAE-MLP INT8** y **Stacking Ensemble** contra 6 baselines (Regresión Logística, Naive Bayes, CNN-1D, Random Forest, XGBoost, LightGBM) en 7 métricas."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os, pandas as pd\n",
    "from IPython.display import display, Image\n",
    "\n",
    "print('========================================================================================')\n",
    "print('             TABLA GENERAL DE BENCHMARK COMPARATIVO COMPLETO ESTADO DEL ARTE           ')\n",
    "print('========================================================================================')\n",
    "df_bench = pd.read_csv('../results/reports_and_plots/state_of_the_art_comparison_table.csv')\n",
    "display(df_bench)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Análisis Trade-Off: Latencia (µs) vs F1-Score vs Tamaño en Disco"
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
    "## 2. Explicabilidad XAI mediante Valores SHAP"
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
  }
 ],
 "metadata": { "language_info": { "name": "python" } },
 "nbformat": 4, "nbformat_minor": 2
}

# Save notebooks
with open(os.path.join(NOTEBOOKS_DIR, "01_EDA_Preprocessing_and_Feature_Selection.ipynb"), "w", encoding="utf-8") as f:
    json.dump(nb01, f, indent=2)

with open(os.path.join(NOTEBOOKS_DIR, "02_Model_Architecture_and_Design.ipynb"), "w", encoding="utf-8") as f:
    json.dump(nb02, f, indent=2)

with open(os.path.join(NOTEBOOKS_DIR, "03_Training_Quantization_and_XAI.ipynb"), "w", encoding="utf-8") as f:
    json.dump(nb03, f, indent=2)

with open(os.path.join(NOTEBOOKS_DIR, "04_Model_Evaluation_and_Error_Analysis.ipynb"), "w", encoding="utf-8") as f:
    json.dump(nb04, f, indent=2)

with open(os.path.join(NOTEBOOKS_DIR, "05_State_of_the_Art_Comparison_and_Efficacy.ipynb"), "w", encoding="utf-8") as f:
    json.dump(nb05, f, indent=2)

print("[+] Los 5 Notebooks correspondientes a las 5 Fases del Proyecto han sido estructurados.")
