import os
import sys
import time
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
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

# Load Data
print("[*] Cargando datasets para el entrenamiento del Ensamble Stacking...")
train_df = pd.read_parquet(os.path.join(DATA_DIR, "train.parquet"))
test_df  = pd.read_parquet(os.path.join(DATA_DIR, "test.parquet"))

X_train = train_df[feature_cols].values.astype(np.float32)
y_train = train_df['target'].values.astype(np.int64)

X_test = test_df[feature_cols].values.astype(np.float32)
y_test = test_df['target'].values.astype(np.int64)

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / np.sum(e_x, axis=1, keepdims=True)

# 1. Base Learner A: VAE-MLP INT8 ONNX Model
print("\n[1/3] Extrayendo predicciones del Nivel 0 (Model A: VAE-MLP INT8)...")
onnx_path = os.path.join(MODELS_DIR, "vae_mlp_quantized.onnx")
ort_session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])

vae_probs_train = softmax(ort_session.run(None, {'input': X_train})[0])
vae_probs_test  = softmax(ort_session.run(None, {'input': X_test})[0])

# 2. Base Learner B: Random Forest
print("[2/3] Entrenando Aprendices Base del Nivel 0 (Model B: Random Forest & Model C: XGBoost)...")
rf_model = RandomForestClassifier(n_estimators=60, max_depth=12, n_jobs=-1, random_state=42)
rf_model.fit(X_train, y_train)
rf_probs_train = rf_model.predict_proba(X_train)
rf_probs_test  = rf_model.predict_proba(X_test)

# 3. Base Learner C: XGBoost
xgb_model = XGBClassifier(
    n_estimators=60,
    max_depth=6,
    learning_rate=0.1,
    eval_metric='mlogloss',
    tree_method='hist',
    random_state=42
)
xgb_model.fit(X_train, y_train)
xgb_probs_train = xgb_model.predict_proba(X_train)
xgb_probs_test  = xgb_model.predict_proba(X_test)

# 4. Meta-Learner (Nivel 1): Logistic Regression
print("[3/3] Entrenando el Meta-Learner de Nivel 1 (Stacking Ensemble)...")
meta_X_train = np.hstack([vae_probs_train, rf_probs_train, xgb_probs_train])
meta_X_test  = np.hstack([vae_probs_test, rf_probs_test, xgb_probs_test])

meta_learner = LogisticRegression(max_iter=500, C=1.0)
meta_learner.fit(meta_X_train, y_train)

# Evaluation
stacking_preds = meta_learner.predict(meta_X_test)

acc = accuracy_score(y_test, stacking_preds)
f1_mac = f1_score(y_test, stacking_preds, average='macro')
f1_wei = f1_score(y_test, stacking_preds, average='weighted')

print("\n" + "="*65)
print("     RESULTADOS DEL ENSAMBLE HÍBRIDO STACKING (VAE-MLP + RF + XGB)")
print("="*65)
print(f" -> Accuracy Global:    {acc*100:.2f}%")
print(f" -> F1-Score Macro:     {f1_mac:.4f}")
print(f" -> F1-Score Weighted:  {f1_wei:.4f}")
print("="*65)

# Save artifacts
print("\n[*] Guardando artefactos del Ensamble Stacking...")
joblib.dump(rf_model, os.path.join(MODELS_DIR, "rf_stacking.joblib"))
joblib.dump(xgb_model, os.path.join(MODELS_DIR, "xgb_stacking.joblib"))
joblib.dump(meta_learner, os.path.join(MODELS_DIR, "meta_learner.joblib"))

stacking_meta = {
    "accuracy": float(acc),
    "f1_macro": float(f1_mac),
    "f1_weighted": float(f1_wei),
    "components": ["VAE-MLP INT8", "Random Forest", "XGBoost"]
}
with open(os.path.join(MODELS_DIR, "stacking_metrics.json"), "w") as f:
    json.dump(stacking_meta, f, indent=4)

print("[+] Ensamble Stacking guardado exitosamente en models/")
