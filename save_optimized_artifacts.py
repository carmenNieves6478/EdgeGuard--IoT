import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.utils.class_weight import compute_class_weight
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from onnxruntime.quantization import quantize_dynamic, QuantType

sys.stdout.reconfigure(encoding='utf-8')
torch.manual_seed(42)
np.random.seed(42)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
MODELS_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\models"
DATA_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\data\processed"

# Load metadata
with open(os.path.join(MODELS_DIR, "meta_info.json"), "r") as f:
    meta = json.load(f)

feature_cols = meta["feature_names"]
classes = meta["classes"]
num_features = meta["num_features"]
num_classes = meta["num_classes"]

print("[*] Re-entrenando y guardando artefactos optimizados (40 épocas + LightGBM Stacking)...")
train_df = pd.read_parquet(os.path.join(DATA_DIR, "train.parquet"))
test_df  = pd.read_parquet(os.path.join(DATA_DIR, "test.parquet"))

X_train = train_df[feature_cols].values.astype(np.float32)
y_train = train_df['target'].values.astype(np.int64)

X_test = test_df[feature_cols].values.astype(np.float32)
y_test = test_df['target'].values.astype(np.int64)

# 1. Train 40-Epoch VAE-MLP
class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(y_train), y=y_train)
class_weights_tensor = torch.tensor(class_weights, dtype=torch.float32).to(device)

from train_vae_mlp import VAE_MLP, TabularDataset, DataLoader
full_model = VAE_MLP(input_dim=num_features, latent_dim=16, num_classes=num_classes).to(device)
optimizer = optim.AdamW(full_model.parameters(), lr=2e-3, weight_decay=1e-4)
criterion_cls = nn.CrossEntropyLoss(weight=class_weights_tensor)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=40)

train_loader = DataLoader(TabularDataset(os.path.join(DATA_DIR, "train.parquet")), batch_size=256, shuffle=True)

for epoch in range(1, 41):
    full_model.train()
    for bx, by in train_loader:
        bx, by = bx.to(device), by.to(device)
        optimizer.zero_grad()
        recon_x, mu, logvar, logits, z = model_out = full_model(bx)
        v_loss = nn.functional.mse_loss(recon_x, bx, reduction='sum') / bx.size(0)
        c_loss = criterion_cls(logits, by)
        loss = 0.3 * v_loss + 1.0 * c_loss
        loss.backward()
        optimizer.step()
    scheduler.step()

# Save PyTorch checkpoint
best_model_path = os.path.join(MODELS_DIR, "vae_mlp_best.pt")
torch.save(full_model.state_dict(), best_model_path)
print(f"[+] Pesos VAE-MLP (40 épocas) guardados en: {best_model_path}")

# 2. Export ONNX & Quantize to INT8
full_model.eval()
full_model.to('cpu')
dummy_input = torch.randn(1, num_features, dtype=torch.float32)
onnx_path = os.path.join(MODELS_DIR, "vae_mlp.onnx")
quantized_onnx_path = os.path.join(MODELS_DIR, "vae_mlp_quantized.onnx")

class VAE_MLP_InferenceWrapper(nn.Module):
    def __init__(self, m):
        super().__init__()
        self.m = m
    def forward(self, x):
        _, _, _, logits, _ = self.m(x)
        return logits

wrapper = VAE_MLP_InferenceWrapper(full_model)

torch.onnx.export(
    wrapper,
    dummy_input,
    onnx_path,
    export_params=True,
    opset_version=17,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['logits'],
    dynamic_axes={'input': {0: 'batch_size'}, 'logits': {0: 'batch_size'}},
    dynamo=False
)

quantize_dynamic(
    model_input=onnx_path,
    model_output=quantized_onnx_path,
    weight_type=QuantType.QUInt8
)
print(f"[+] Modelo ONNX INT8 optimizado guardado en: {quantized_onnx_path}")

# 3. Train & Save Stacking Ensemble (LGBM Meta-Learner)
print("[*] Entrenando Stacking Ensemble con LightGBM Meta-Learner...")
import onnxruntime as ort
ort_session = ort.InferenceSession(quantized_onnx_path, providers=['CPUExecutionProvider'])
def softmax(x): e_x = np.exp(x - np.max(x, axis=1, keepdims=True)); return e_x / np.sum(e_x, axis=1, keepdims=True)

vae_probs_train = softmax(ort_session.run(None, {'input': X_train})[0])
vae_probs_test  = softmax(ort_session.run(None, {'input': X_test})[0])

rf = RandomForestClassifier(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42)
rf.fit(X_train, y_train)
rf_probs_train = rf.predict_proba(X_train)
rf_probs_test  = rf.predict_proba(X_test)

xgb = XGBClassifier(n_estimators=150, max_depth=7, learning_rate=0.05, eval_metric='mlogloss', tree_method='hist', random_state=42)
xgb.fit(X_train, y_train)
xgb_probs_train = xgb.predict_proba(X_train)
xgb_probs_test  = xgb.predict_proba(X_test)

lgbm = LGBMClassifier(n_estimators=150, max_depth=7, learning_rate=0.05, num_leaves=31, random_state=42, verbose=-1)
lgbm.fit(X_train, y_train)
lgbm_probs_train = lgbm.predict_proba(X_train)
lgbm_probs_test  = lgbm.predict_proba(X_test)

meta_X_train = np.hstack([vae_probs_train, rf_probs_train, xgb_probs_train, lgbm_probs_train])
meta_X_test  = np.hstack([vae_probs_test, rf_probs_test, xgb_probs_test, lgbm_probs_test])

meta_lgbm = LGBMClassifier(n_estimators=100, max_depth=4, learning_rate=0.03, verbose=-1, random_state=42)
meta_lgbm.fit(meta_X_train, y_train)

joblib.dump(rf, os.path.join(MODELS_DIR, "rf_stacking.joblib"))
joblib.dump(xgb, os.path.join(MODELS_DIR, "xgb_stacking.joblib"))
joblib.dump(lgbm, os.path.join(MODELS_DIR, "lgbm_stacking.joblib"))
joblib.dump(meta_lgbm, os.path.join(MODELS_DIR, "meta_learner.joblib"))

meta_preds = meta_lgbm.predict(meta_X_test)
acc = accuracy_score(y_test, meta_preds)
f1_mac = f1_score(y_test, meta_preds, average='macro')

print("\n" + "="*65)
print("     RESULTADOS FINALES ENSAMBLE STACKING OPTIMIZADO (LIGHTGBM)")
print("="*65)
print(f" -> Accuracy Global: {acc*100:.2f}%")
print(f" -> F1-Score Macro:  {f1_mac:.4f}")
print("="*65)
