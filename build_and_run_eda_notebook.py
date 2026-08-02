import os
import json
import subprocess
import pandas as pd
import numpy as np

# Build a comprehensive Jupyter notebook for Step 1
notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 📊 EdgeGuard-IoT: Step 1 - Professional EDA & Data Preprocessing Pipeline\n",
    "**Dataset:** CIC-IoT-2023  \n",
    "**Objective:** Comprehensive Exploratory Data Analysis (EDA) comparing raw dataset vs balanced preprocessed dataset, mapping 34 attack subcategories into 8 high-level classes, feature normalization, and stratified dataset partitioning."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import glob\n",
    "import json\n",
    "import joblib\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.preprocessing import MinMaxScaler, LabelEncoder\n",
    "\n",
    "sns.set_theme(style='whitegrid', palette='muted')\n",
    "plt.rcParams['figure.figsize'] = (12, 6)\n",
    "plt.rcParams['font.size'] = 11\n",
    "np.random.seed(42)\n",
    "print('[+] Libraries and Seaborn theme loaded successfully.')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 1. Raw Dataset Exploration (ANTES del Preprocesamiento)\n",
    "Analizamos la distribución original del dataset masivo **CIC-IoT-2023** leyendo fragmentos (chunks) de los archivos CSV."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "DATA_DIR = r'E:\\PROYECTO DE INVESTIGACION\\dataset\\MERGED_CSV\\MERGED_CSV'\n",
    "csv_files = glob.glob(os.path.join(DATA_DIR, '*.csv'))\n",
    "print(f'Total de archivos CSV masivos encontrados: {len(csv_files)}')\n",
    "\n",
    "# Sample raw label distribution across first 3 CSV files\n",
    "raw_labels = []\n",
    "for f in csv_files[:3]:\n",
    "    df_chunk = pd.read_csv(f, usecols=['Label'])\n",
    "    raw_labels.append(df_chunk['Label'])\n",
    "\n",
    "df_raw_sample = pd.concat(raw_labels, ignore_index=True)\n",
    "raw_counts = df_raw_sample.value_counts()\n",
    "\n",
    "print(f'Total de muestras analizadas en la muestra RAW: {len(df_raw_sample):,}')\n",
    "print(f'Total de subcategorías únicas de ataques: {len(raw_counts)}')\n",
    "\n",
    "# Bar chart of Raw Subcategories (Before preprocessing)\n",
    "plt.figure(figsize=(14, 7))\n",
    "ax = sns.barplot(x=raw_counts.values, y=raw_counts.index, palette='magma')\n",
    "plt.title('DISTRIBUCIÓN ORIGINAL (RAW) - 34 Subcategorías de Ataques CIC-IoT-2023', fontsize=14, fontweight='bold')\n",
    "plt.xlabel('Número de Registro de Paquetes (Escala Lineal)', fontsize=12)\n",
    "plt.ylabel('Subcategoría de Ataque', fontsize=12)\n",
    "plt.xscale('log')\n",
    "plt.title('DISTRIBUCIÓN ORIGINAL (RAW) - Escala Logarítmica por Desbalance Extremo')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 2. Mapeo de Subcategorías a 8 Clases Principales\n",
    "Agrupamos las 34 subcategorías heterogéneas en **8 clases principales** (`DDoS`, `DoS`, `Mirai`, `Recon`, `Spoofing`, `Brute Force`, `Web-based` y `Benign`)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "LABEL_MAP = {\n",
    "    'DDOS-ICMP_FLOOD': 'DDoS', 'DDOS-UDP_FLOOD': 'DDoS', 'DDOS-TCP_FLOOD': 'DDoS',\n",
    "    'DDOS-PSHACK_FLOOD': 'DDoS', 'DDOS-RSTFINFLOOD': 'DDoS', 'DDOS-SYN_FLOOD': 'DDoS',\n",
    "    'DDOS-SYNONYMOUSIP_FLOOD': 'DDoS', 'DDOS-ICMP_FRAGMENTATION': 'DDoS',\n",
    "    'DDOS-ACK_FRAGMENTATION': 'DDoS', 'DDOS-UDP_FRAGMENTATION': 'DDoS',\n",
    "    'DDOS-HTTP_FLOOD': 'DDoS', 'DDOS-SLOWLORIS': 'DDoS',\n",
    "    'DOS-UDP_FLOOD': 'DoS', 'DOS-TCP_FLOOD': 'DoS', 'DOS-SYN_FLOOD': 'DoS', 'DOS-HTTP_FLOOD': 'DoS',\n",
    "    'MIRAI-GREETH_FLOOD': 'Mirai', 'MIRAI-UDPPLAIN': 'Mirai', 'MIRAI-GREIP_FLOOD': 'Mirai',\n",
    "    'VULNERABILITYSCAN': 'Recon', 'RECON-HOSTDISCOVERY': 'Recon', 'RECON-OSSCAN': 'Recon',\n",
    "    'RECON-PORTSCAN': 'Recon', 'RECON-PINGSWEEP': 'Recon',\n",
    "    'MITM-ARPSPOOFING': 'Spoofing', 'DNS_SPOOFING': 'Spoofing',\n",
    "    'DICTIONARYBRUTEFORCE': 'Brute Force',\n",
    "    'BROWSERHIJACKING': 'Web-based', 'SQLINJECTION': 'Web-based', 'COMMANDINJECTION': 'Web-based',\n",
    "    'XSS': 'Web-based', 'BACKDOOR_MALWARE': 'Web-based', 'UPLOADING_ATTACK': 'Web-based',\n",
    "    'BENIGN': 'Benign'\n",
    "}\n",
    "\n",
    "df_raw_sample['Category'] = df_raw_sample.map(LABEL_MAP)\n",
    "cat_raw_counts = df_raw_sample['Category'].value_counts()\n",
    "\n",
    "print('Distribución agrupada ANTES del Balanceo:')\n",
    "for cat, cnt in cat_raw_counts.items():\n",
    "    print(f' - {cat:12s}: {cnt:,} muestras ({cnt/len(df_raw_sample)*100:.2f}%)')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 3. Dataset Procesado y Balanceado (DESPUÉS del Preprocesamiento)\n",
    "Cargamos los datasets `.parquet` procesados y balanceados para comparar visualmente el ANTES vs DESPUÉS."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "train_df = pd.read_parquet('../data/processed/train.parquet')\n",
    "val_df = pd.read_parquet('../data/processed/val.parquet')\n",
    "test_df = pd.read_parquet('../data/processed/test.parquet')\n",
    "label_encoder = joblib.load('../models/label_encoder.joblib')\n",
    "with open('../models/meta_info.json') as f:\n",
    "    meta_info = json.load(f)\n",
    "\n",
    "feature_cols = meta_info['feature_names']\n",
    "classes = meta_info['classes']\n",
    "\n",
    "# Combine for total counts\n",
    "all_df = pd.concat([train_df, val_df, test_df], ignore_index=True)\n",
    "balanced_counts = all_df['target'].map(dict(enumerate(classes))).value_counts()\n",
    "\n",
    "# Comparison Plot: Before vs After Balancing\n",
    "fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n",
    "\n",
    "sns.barplot(x=cat_raw_counts.values, y=cat_raw_counts.index, ax=axes[0], palette='Reds_r')\n",
    "axes[0].set_title('ANTES: Desbalance Extremo en Dataset RAW', fontsize=13, fontweight='bold')\n",
    "axes[0].set_xlabel('Muestras (Escala Logarítmica)')\n",
    "axes[0].set_xscale('log')\n",
    "\n",
    "sns.barplot(x=balanced_counts.values, y=balanced_counts.index, ax=axes[1], palette='viridis')\n",
    "axes[1].set_title('DESPUÉS: Dataset Balanceado Optimizado (.parquet)', fontsize=13, fontweight='bold')\n",
    "axes[1].set_xlabel('Muestras Totales')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 4. Análisis de Características Numéricas y Normalización (MinMaxScaler)\n",
    "Visualizamos el impacto del escalamiento `MinMaxScaler` en las 39 características de flujo de red."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "sample_features = ['Header_Length', 'Rate', 'Tot sum', 'Tot size', 'Variance', 'IAT']\n",
    "\n",
    "plt.figure(figsize=(14, 6))\n",
    "sns.boxplot(data=train_df[sample_features], palette='Set2')\n",
    "plt.title('Distribución Normalizada (MinMaxScaler [0, 1]) de Características Clave de Red', fontsize=13, fontweight='bold')\n",
    "plt.ylabel('Valor Escala [0, 1]')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 5. Matriz de Correlación de Características de Red\n",
    "Analizamos la correlación lineal entre las características numéricas principales del tráfico IoT."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "top_15_features = ['Header_Length', 'Protocol Type', 'Time_To_Live', 'Rate', 'fin_flag_number', 'syn_flag_number',\n",
    "                    'psh_flag_number', 'ack_flag_number', 'HTTP', 'HTTPS', 'TCP', 'UDP', 'Tot sum', 'AVG', 'Variance']\n",
    "\n",
    "corr_matrix = train_df[top_15_features].corr()\n",
    "\n",
    "plt.figure(figsize=(12, 9))\n",
    "sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)\n",
    "plt.title('Matriz de Correlación de Características Top-15 (CIC-IoT-2023)', fontsize=13, fontweight='bold')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 6. Resumen de la Partición Estratificada (Train / Val / Test)\n",
    "Verificamos la división estratificada generada para los experimentos de Deep Learning."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "split_sizes = {'Train (70%)': len(train_df), 'Validation (15%)': len(val_df), 'Test (15%)': len(test_df)}\n",
    "\n",
    "plt.figure(figsize=(7, 7))\n",
    "plt.pie(split_sizes.values(), labels=split_sizes.keys(), autopct='%1.1f%%', colors=['#2b5c8f', '#d95f02', '#7570b3'], startangle=140, explode=(0.05, 0, 0))\n",
    "plt.title('Partición Estratificada del Dataset EdgeGuard-IoT', fontsize=13, fontweight='bold')\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "print(f'Train shape:      {train_df.shape}')\n",
    "print(f'Validation shape: {val_df.shape}')\n",
    "print(f'Test shape:       {test_df.shape}')\n",
    "print(f'[+] Artefactos generados: scaler.joblib, label_encoder.joblib, meta_info.json')"
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

# Write notebook file
nb_path = "E:/PROYECTO DE INVESTIGACION/dataset/MERGED_CSV/notebooks/01_EDA_and_Preprocessing.ipynb"
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print("[+] Archivo 01_EDA_and_Preprocessing.ipynb escrito correctamente. Ejecutando nbconvert...")
