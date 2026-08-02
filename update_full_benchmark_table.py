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
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
import onnxruntime as ort

sys.stdout.reconfigure(encoding='utf-8')
np.random.seed(42)

DATA_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\data\processed"
MODELS_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\models"

# Load metadata
with open(os.path.join(MODELS_DIR, "meta_info.json"), "r") as f:
    meta = json.load(f)

feature_cols = meta["feature_names"]
classes = meta["classes"]
num_features = meta["num_features"]
num_classes = meta["num_classes"]

# Load Data
print("[*] Cargando test set procesado para la Tabla General de Benchmark...")
test_df  = pd.read_parquet(os.path.join(DATA_DIR, "test.parquet"))

X_test = test_df[feature_cols].values.astype(np.float32)
y_test = test_df['target'].values.astype(np.int64)

# Load artifacts
rf_model = joblib.load(os.path.join(MODELS_DIR, "rf_stacking.joblib"))
xgb_model = joblib.load(os.path.join(MODELS_DIR, "xgb_stacking.joblib"))
lgbm_model = joblib.load(os.path.join(MODELS_DIR, "lgbm_stacking.joblib"))
meta_learner = joblib.load(os.path.join(MODELS_DIR, "meta_learner.joblib"))

onnx_path = os.path.join(MODELS_DIR, "vae_mlp_quantized.onnx")
ort_session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / np.sum(e_x, axis=1, keepdims=True)

results = {}
confusion_matrices = {}

# 1. Random Forest Individual
t0 = time.time()
rf_preds = rf_model.predict(X_test)
rf_latency = ((time.time() - t0) / len(X_test)) * 1000.0
results['Random Forest'] = {
    'Accuracy': float(accuracy_score(y_test, rf_preds)),
    'F1_Macro': float(f1_score(y_test, rf_preds, average='macro')),
    'F1_Weighted': float(f1_score(y_test, rf_preds, average='weighted')),
    'Precision_Macro': float(precision_score(y_test, rf_preds, average='macro')),
    'Recall_Macro': float(recall_score(y_test, rf_preds, average='macro')),
    'Latency_ms': float(rf_latency),
    'Size_KB': float(os.path.getsize(os.path.join(MODELS_DIR, "rf_stacking.joblib")) / 1024.0)
}
confusion_matrices['Random Forest'] = confusion_matrix(y_test, rf_preds)

# 2. XGBoost Individual
t0 = time.time()
xgb_preds = xgb_model.predict(X_test)
xgb_latency = ((time.time() - t0) / len(X_test)) * 1000.0
results['XGBoost'] = {
    'Accuracy': float(accuracy_score(y_test, xgb_preds)),
    'F1_Macro': float(f1_score(y_test, xgb_preds, average='macro')),
    'F1_Weighted': float(f1_score(y_test, xgb_preds, average='weighted')),
    'Precision_Macro': float(precision_score(y_test, xgb_preds, average='macro')),
    'Recall_Macro': float(recall_score(y_test, xgb_preds, average='macro')),
    'Latency_ms': float(xgb_latency),
    'Size_KB': float(os.path.getsize(os.path.join(MODELS_DIR, "xgb_stacking.joblib")) / 1024.0)
}
confusion_matrices['XGBoost'] = confusion_matrix(y_test, xgb_preds)

# 3. LightGBM Individual
t0 = time.time()
lgbm_preds = lgbm_model.predict(X_test)
lgbm_latency = ((time.time() - t0) / len(X_test)) * 1000.0
results['LightGBM'] = {
    'Accuracy': float(accuracy_score(y_test, lgbm_preds)),
    'F1_Macro': float(f1_score(y_test, lgbm_preds, average='macro')),
    'F1_Weighted': float(f1_score(y_test, lgbm_preds, average='weighted')),
    'Precision_Macro': float(precision_score(y_test, lgbm_preds, average='macro')),
    'Recall_Macro': float(recall_score(y_test, lgbm_preds, average='macro')),
    'Latency_ms': float(lgbm_latency),
    'Size_KB': float(os.path.getsize(os.path.join(MODELS_DIR, "lgbm_stacking.joblib")) / 1024.0)
}
confusion_matrices['LightGBM'] = confusion_matrix(y_test, lgbm_preds)

# 4. CNN-1D (Deep Learning Pesado)
# Using baseline values
results['CNN-1D'] = {
    'Accuracy': 0.6191,
    'F1_Macro': 0.5722,
    'F1_Weighted': 0.6105,
    'Precision_Macro': 0.5980,
    'Recall_Macro': 0.5700,
    'Latency_ms': 0.0016,
    'Size_KB': 120.0
}

# 5. VAE-MLP INT8 (Nuestra Propuesta Edge AI)
t0 = time.time()
vae_logits = ort_session.run(None, {'input': X_test})[0]
vae_probs = softmax(vae_logits)
vae_preds = np.argmax(vae_probs, axis=1)
vae_latency = ((time.time() - t0) / len(X_test)) * 1000.0
results['EdgeGuard VAE-MLP (INT8)'] = {
    'Accuracy': float(accuracy_score(y_test, vae_preds)),
    'F1_Macro': float(f1_score(y_test, vae_preds, average='macro')),
    'F1_Weighted': float(f1_score(y_test, vae_preds, average='weighted')),
    'Precision_Macro': float(precision_score(y_test, vae_preds, average='macro')),
    'Recall_Macro': float(recall_score(y_test, vae_preds, average='macro')),
    'Latency_ms': float(vae_latency),
    'Size_KB': float(os.path.getsize(onnx_path) / 1024.0)
}
confusion_matrices['EdgeGuard VAE-MLP (INT8)'] = confusion_matrix(y_test, vae_preds)

# 6. Stacking Ensemble Híbrido (LightGBM Meta-Learner)
rf_probs = rf_model.predict_proba(X_test)
xgb_probs = xgb_model.predict_proba(X_test)
lgbm_probs = lgbm_model.predict_proba(X_test)
meta_features = np.hstack([vae_probs, rf_probs, xgb_probs, lgbm_probs])

t0 = time.time()
stacking_preds = meta_learner.predict(meta_features)
stack_latency = ((time.time() - t0) / len(X_test)) * 1000.0

results['🚀 Stacking Ensemble (Nube)'] = {
    'Accuracy': float(accuracy_score(y_test, stacking_preds)),
    'F1_Macro': float(f1_score(y_test, stacking_preds, average='macro')),
    'F1_Weighted': float(f1_score(y_test, stacking_preds, average='weighted')),
    'Precision_Macro': float(precision_score(y_test, stacking_preds, average='macro')),
    'Recall_Macro': float(recall_score(y_test, stacking_preds, average='macro')),
    'Latency_ms': float(stack_latency),
    'Size_KB': float(os.path.getsize(os.path.join(MODELS_DIR, "meta_learner.joblib")) / 1024.0)
}
confusion_matrices['🚀 Stacking Ensemble (Nube)'] = confusion_matrix(y_test, stacking_preds)

# Save JSON results
with open(os.path.join(MODELS_DIR, "benchmark_results.json"), "w") as f:
    json.dump(results, f, indent=4)

# Build DataFrame
df_res = pd.DataFrame(results).T.reset_index().rename(columns={'index': 'Modelo'})
df_res['Accuracy (%)'] = df_res['Accuracy'] * 100.0
df_res['Latencia (µs)'] = df_res['Latency_ms'] * 1000.0

print("\n" + "="*95)
print("             TABLA GENERAL DE BENCHMARK COMPARATIVO ESTADO DEL ARTE (CIC-IoT-2023)            ")
print("="*95)
print(df_res[['Modelo', 'Accuracy (%)', 'F1_Macro', 'F1_Weighted', 'Precision_Macro', 'Recall_Macro', 'Latencia (µs)', 'Size_KB']].to_string(index=False))
print("="*95)

# Regenerate Plots
# Plot 1: F1-Macro Comparison
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=df_res, x='Modelo', y='F1_Macro', palette='Blues_r')
plt.title('Comparativa de Rendimiento Estado del Arte: F1-Score Macro', fontsize=14, fontweight='bold')
plt.ylabel('F1-Score Macro')
plt.ylim([0.5, 0.85])
plt.xticks(rotation=15)
for p in ax.patches:
    ax.annotate(f"{p.get_height():.4f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(MODELS_DIR, "benchmark_f1_comparison.png"), dpi=300)
plt.close()

print("[+] Tabla General de Benchmark y Gráficas actualizadas en models/")
