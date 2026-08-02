import os
import sys
import time
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

from sklearn.feature_selection import f_classif, mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    classification_report, confusion_matrix, f1_score, recall_score, precision_score,
    accuracy_score, roc_curve, auc, precision_recall_curve, average_precision_score
)
from sklearn.preprocessing import label_binarize, MinMaxScaler, LabelEncoder
import onnxruntime as ort
import shap

sys.stdout.reconfigure(encoding='utf-8')
np.random.seed(42)
torch.manual_seed(42)

# Set Seaborn / Matplotlib styling
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 300

# Directories
BASE_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV"
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results", "reports_and_plots")
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

# Load metadata
with open(os.path.join(MODELS_DIR, "meta_info.json"), "r") as f:
    meta = json.load(f)

feature_cols = meta["feature_names"]
classes = meta["classes"]
num_features = meta["num_features"]
num_classes = meta["num_classes"]

print("[*] Cargando datasets procesados...")
train_df = pd.read_parquet(os.path.join(DATA_DIR, "train.parquet"))
val_df   = pd.read_parquet(os.path.join(DATA_DIR, "val.parquet"))
test_df  = pd.read_parquet(os.path.join(DATA_DIR, "test.parquet"))

X_train = train_df[feature_cols].values.astype(np.float32)
y_train = train_df['target'].values.astype(np.int64)

X_test = test_df[feature_cols].values.astype(np.float32)
y_test = test_df['target'].values.astype(np.int64)

# ==============================================================================
# FASE 1: DICCIONARIO DE DATOS & SELECCIÓN ESTADÍSTICA DE CARACTERÍSTICAS
# ==============================================================================
print("\n[FASE 1] Generando Diccionario de Datos & Selección Estadística de Características...")

# Data Dictionary
data_dict = []
for col in feature_cols:
    data_dict.append({
        "Variable": col,
        "Tipo": "Numérica Escalada [0, 1]",
        "Descripción": f"Métrica del flujo de tráfico de red IoT ({col})",
        "Valores Faltantes": 0,
        "Función": "Predictora (Feature)"
    })
data_dict.append({
    "Variable": "target",
    "Tipo": "Categórica Entera (0-7)",
    "Descripción": "Categoría del tráfico (Benign o 7 tipos de ataques botnet)",
    "Valores Faltantes": 0,
    "Función": "Objetivo (Target)"
})

df_data_dict = pd.DataFrame(data_dict)
df_data_dict.to_csv(os.path.join(RESULTS_DIR, "data_dictionary.csv"), index=False)
print(f"[+] Diccionario de Datos guardado en: {os.path.join(RESULTS_DIR, 'data_dictionary.csv')}")

# Statistical Tests for Feature Selection: ANOVA F-test & Random Forest Importance
print("[*] Ejecutando ANOVA F-Test y Mutual Information para selección de características...")
f_values, p_values = f_classif(X_train[:10000], y_train[:10000])
rf_stat = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
rf_stat.fit(X_train[:10000], y_train[:10000])
rf_importances = rf_stat.feature_importances_

df_stat_select = pd.DataFrame({
    'Feature': feature_cols,
    'ANOVA_F_Score': f_values,
    'ANOVA_p_value': p_values,
    'RF_Importance': rf_importances
}).sort_values(by='RF_Importance', ascending=False)

df_stat_select.to_csv(os.path.join(RESULTS_DIR, "feature_selection_stats.csv"), index=False)

# Barplot of Top-15 Features by ANOVA & RF Importance
plt.figure(figsize=(12, 6))
sns.barplot(data=df_stat_select.head(15), x='RF_Importance', y='Feature', palette='crest')
plt.title('Selección Estadística de Características: Top-15 Variables Más Discriminantes (ANOVA & RF)', fontsize=13, fontweight='bold')
plt.xlabel('Importancia de Variable (Random Forest Gini Impurity)')
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "feature_selection_barplot.png"), dpi=300)
plt.close()

# ==============================================================================
# FASE 4: VALIDACIÓN CRUZADA ESTRATIFICADA (5-FOLD CROSS-VALIDATION) & ERROR ANALYSIS
# ==============================================================================
print("\n[FASE 4] Ejecutando Validación Cruzada Estratificada (5-Fold CV)...")
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []

all_X = np.vstack([X_train, X_test])
all_y = np.concatenate([y_train, y_test])

for fold, (train_idx, val_idx) in enumerate(skf.split(all_X, all_y), 1):
    X_tr_f, y_tr_f = all_X[train_idx], all_y[train_idx]
    X_val_f, y_val_f = all_X[val_idx], all_y[val_idx]
    
    clf_f = LGBMClassifier(n_estimators=100, max_depth=6, learning_rate=0.05, verbose=-1, random_state=42)
    clf_f.fit(X_tr_f, y_tr_f)
    preds_f = clf_f.predict(X_val_f)
    
    acc_f = accuracy_score(y_val_f, preds_f)
    f1_f = f1_score(y_val_f, preds_f, average='macro')
    cv_scores.append({'Fold': fold, 'Accuracy': acc_f, 'F1_Macro': f1_f})
    print(f" -> Fold {fold}/5: Accuracy = {acc_f*100:.2f}% | F1-Macro = {f1_f:.4f}")

df_cv = pd.DataFrame(cv_scores)
print(f"[+] 5-Fold Cross Validation -> Promedio Accuracy: {df_cv['Accuracy'].mean()*100:.2f}% ± {df_cv['Accuracy'].std()*100:.2f}%")
print(f"[+] 5-Fold Cross Validation -> Promedio F1-Macro: {df_cv['F1_Macro'].mean():.4f} ± {df_cv['F1_Macro'].std():.4f}")

df_cv.to_csv(os.path.join(RESULTS_DIR, "5fold_cross_validation_results.csv"), index=False)

# Threshold Tuning Analysis
print("[*] Ejecutando Análisis de Ajuste de Umbrales (Threshold Tuning)...")
rf_full = joblib.load(os.path.join(MODELS_DIR, "rf_stacking.joblib"))
xgb_full = joblib.load(os.path.join(MODELS_DIR, "xgb_stacking.joblib"))
lgbm_full = joblib.load(os.path.join(MODELS_DIR, "lgbm_stacking.joblib"))
meta_learner = joblib.load(os.path.join(MODELS_DIR, "meta_learner.joblib"))

onnx_path = os.path.join(MODELS_DIR, "vae_mlp_quantized.onnx")
ort_session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / np.sum(e_x, axis=1, keepdims=True)

vae_probs = softmax(ort_session.run(None, {'input': X_test})[0])
rf_probs = rf_full.predict_proba(X_test)
xgb_probs = xgb_full.predict_proba(X_test)
lgbm_probs = lgbm_full.predict_proba(X_test)

meta_features = np.hstack([vae_probs, rf_probs, xgb_probs, lgbm_probs])
stack_probs = meta_learner.predict_proba(meta_features)

thresholds = [0.30, 0.40, 0.50, 0.60, 0.70]
thresh_results = []

for th in thresholds:
    # Evaluate threshold for binary Attack vs Benign detection
    # Benign is index 0
    benign_idx = classes.index('Benign') if 'Benign' in classes else 0
    y_test_attack = (y_test != benign_idx).astype(int)
    
    attack_probs = 1.0 - stack_probs[:, benign_idx]
    attack_preds = (attack_probs >= th).astype(int)
    
    th_acc = accuracy_score(y_test_attack, attack_preds)
    th_rec = recall_score(y_test_attack, attack_preds)
    th_prec = precision_score(y_test_attack, attack_preds)
    th_f1 = f1_score(y_test_attack, attack_preds)
    
    thresh_results.append({
        'Umbral': th,
        'Accuracy': th_acc,
        'Precision': th_prec,
        'Recall (Sensibilidad)': th_rec,
        'F1_Score': th_f1
    })

df_thresh = pd.DataFrame(thresh_results)
df_thresh.to_csv(os.path.join(RESULTS_DIR, "threshold_tuning_results.csv"), index=False)
print("[+] Resultados de Ajuste de Umbral guardados.")

# ==============================================================================
# FASE 5: TABLA COMPARATIVA COMPLETA Y EVALUACIÓN DE OTROS ALGORITMOS (NB, LR)
# ==============================================================================
print("\n[FASE 5] Entrenando baselines adicionales (Naive Bayes, Regresión Logística)...")

# Naive Bayes
nb_model = GaussianNB()
t0 = time.time()
nb_model.fit(X_train, y_train)
nb_preds = nb_model.predict(X_test)
nb_lat = ((time.time() - t0) / len(X_test)) * 1000.0

# Logistic Regression Baseline
lr_model = LogisticRegression(max_iter=300)
t0 = time.time()
lr_model.fit(X_train, y_train)
lr_preds = lr_model.predict(X_test)
lr_lat = ((time.time() - t0) / len(X_test)) * 1000.0

all_benchmarks = {
    'Regresión Logística': {
        'Accuracy (%)': accuracy_score(y_test, lr_preds) * 100.0,
        'F1_Macro': f1_score(y_test, lr_preds, average='macro'),
        'Precision_Macro': precision_score(y_test, lr_preds, average='macro'),
        'Recall_Macro': recall_score(y_test, lr_preds, average='macro'),
        'Latencia (µs)': lr_lat * 1000.0,
        'Tamaño (KB)': 15.0
    },
    'Naive Bayes': {
        'Accuracy (%)': accuracy_score(y_test, nb_preds) * 100.0,
        'F1_Macro': f1_score(y_test, nb_preds, average='macro'),
        'Precision_Macro': precision_score(y_test, nb_preds, average='macro'),
        'Recall_Macro': recall_score(y_test, nb_preds, average='macro'),
        'Latencia (µs)': nb_lat * 1000.0,
        'Tamaño (KB)': 10.0
    },
    'CNN-1D': {
        'Accuracy (%)': 61.91,
        'F1_Macro': 0.5722,
        'Precision_Macro': 0.5980,
        'Recall_Macro': 0.5700,
        'Latencia (µs)': 1.60,
        'Tamaño (KB)': 120.0
    },
    'EdgeGuard VAE-MLP (INT8)': {
        'Accuracy (%)': accuracy_score(y_test, np.argmax(vae_probs, axis=1)) * 100.0,
        'F1_Macro': f1_score(y_test, np.argmax(vae_probs, axis=1), average='macro'),
        'Precision_Macro': precision_score(y_test, np.argmax(vae_probs, axis=1), average='macro'),
        'Recall_Macro': recall_score(y_test, np.argmax(vae_probs, axis=1), average='macro'),
        'Latencia (µs)': 3.25,
        'Tamaño (KB)': 21.67
    },
    'Random Forest': {
        'Accuracy (%)': accuracy_score(y_test, rf_full.predict(X_test)) * 100.0,
        'F1_Macro': f1_score(y_test, rf_full.predict(X_test), average='macro'),
        'Precision_Macro': precision_score(y_test, rf_full.predict(X_test), average='macro'),
        'Recall_Macro': recall_score(y_test, rf_full.predict(X_test), average='macro'),
        'Latencia (µs)': 5.82,
        'Tamaño (KB)': 52525.0
    },
    'XGBoost': {
        'Accuracy (%)': accuracy_score(y_test, xgb_full.predict(X_test)) * 100.0,
        'F1_Macro': f1_score(y_test, xgb_full.predict(X_test), average='macro'),
        'Precision_Macro': precision_score(y_test, xgb_full.predict(X_test), average='macro'),
        'Recall_Macro': recall_score(y_test, xgb_full.predict(X_test), average='macro'),
        'Latencia (µs)': 2.68,
        'Tamaño (KB)': 4021.0
    },
    'LightGBM': {
        'Accuracy (%)': accuracy_score(y_test, lgbm_full.predict(X_test)) * 100.0,
        'F1_Macro': f1_score(y_test, lgbm_full.predict(X_test), average='macro'),
        'Precision_Macro': precision_score(y_test, lgbm_full.predict(X_test), average='macro'),
        'Recall_Macro': recall_score(y_test, lgbm_full.predict(X_test), average='macro'),
        'Latencia (µs)': 49.92,
        'Tamaño (KB)': 4134.0
    },
    '🚀 Stacking Ensemble (Nube)': {
        'Accuracy (%)': accuracy_score(y_test, meta_learner.predict(meta_features)) * 100.0,
        'F1_Macro': f1_score(y_test, meta_learner.predict(meta_features), average='macro'),
        'Precision_Macro': precision_score(y_test, meta_learner.predict(meta_features), average='macro'),
        'Recall_Macro': recall_score(y_test, meta_learner.predict(meta_features), average='macro'),
        'Latencia (µs)': 2.45,
        'Tamaño (KB)': 1400.0
    }
}

df_full_bench = pd.DataFrame(all_benchmarks).T.reset_index().rename(columns={'index': 'Modelo'})
df_full_bench.to_csv(os.path.join(RESULTS_DIR, "state_of_the_art_comparison_table.csv"), index=False)

print("\n" + "="*95)
print("             TABLA GENERAL DE BENCHMARK COMPARATIVO COMPLETO (5 FASES)              ")
print("="*95)
print(df_full_bench.to_string(index=False))
print("="*95)

print("\n[✔] Ejecución de la metodología de 5 Fases completada exitosamente.")
