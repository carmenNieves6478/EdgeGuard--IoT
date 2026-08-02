import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# EdgeGuard-IoT: Step 1 - EDA & Data Preprocessing\n",
    "**Dataset:** CIC-IoT-2023  \n",
    "**Objective:** Process massive merged CSV dataset, map attack categories, balance classes, normalize numeric features with MinMaxScaler, encode target classes, and export clean datasets (`train.parquet`, `val.parquet`, `test.parquet`)."
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
    "np.random.seed(42)\n",
    "print(\"Libraries loaded successfully.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Mapping Attack Subcategories to 8 High-Level Classes"
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
    "print(f\"Total mapped subcategories: {len(LABEL_MAP)}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Load Processed Dataset Metadata & Class Distribution Visualization"
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
    "\n",
    "print(f\"Train shape: {train_df.shape}\")\n",
    "print(f\"Val shape:   {val_df.shape}\")\n",
    "print(f\"Test shape:  {test_df.shape}\")\n",
    "\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.countplot(x=train_df['target'].map(dict(enumerate(label_encoder.classes_))), palette='viridis')\n",
    "plt.title('Balanced Class Distribution (Train Set)')\n",
    "plt.xticks(rotation=45)\n",
    "plt.ylabel('Count')\n",
    "plt.tight_layout()\n",
    "plt.show()"
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

with open("E:/PROYECTO DE INVESTIGACION/dataset/MERGED_CSV/notebooks/01_EDA_and_Preprocessing.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)
print("Notebook created successfully.")
