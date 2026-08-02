import sys
import os
import time
import json

sys.stdout.reconfigure(encoding='utf-8')
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
import onnx
import onnxruntime as ort
from onnxruntime.quantization import quantize_dynamic, QuantType
import shap

# Set seeds
torch.manual_seed(42)
np.random.seed(42)

# Directories
MODELS_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\models"
DATA_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\data\processed"

# Load metadata
with open(os.path.join(MODELS_DIR, "meta_info.json"), "r") as f:
    meta_info = json.load(f)

feature_cols = meta_info["feature_names"]
classes = meta_info["classes"]
num_features = meta_info["num_features"]
num_classes = meta_info["num_classes"]

# Model Architectures
class VAE(nn.Module):
    def __init__(self, input_dim=39, latent_dim=16):
        super(VAE, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.bn1 = nn.BatchNorm1d(64)
        self.fc2 = nn.Linear(64, 32)
        self.bn2 = nn.BatchNorm1d(32)
        self.fc_mu = nn.Linear(32, latent_dim)
        self.fc_logvar = nn.Linear(32, latent_dim)
        self.fc3 = nn.Linear(latent_dim, 32)
        self.bn3 = nn.BatchNorm1d(32)
        self.fc4 = nn.Linear(32, 64)
        self.bn4 = nn.BatchNorm1d(64)
        self.fc5 = nn.Linear(64, input_dim)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def encode(self, x):
        h = self.relu(self.bn1(self.fc1(x)))
        h = self.relu(self.bn2(self.fc2(h)))
        return self.fc_mu(h), self.fc_logvar(h)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        h = self.relu(self.bn3(self.fc3(z)))
        h = self.relu(self.bn4(self.fc4(h)))
        return self.sigmoid(self.fc5(h))

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar, z

class MLPClassifier(nn.Module):
    def __init__(self, latent_dim=16, num_classes=8):
        super(MLPClassifier, self).__init__()
        self.fc1 = nn.Linear(latent_dim, 32)
        self.bn1 = nn.BatchNorm1d(32)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(32, 16)
        self.bn2 = nn.BatchNorm1d(16)
        self.out = nn.Linear(16, num_classes)

    def forward(self, z):
        h = self.dropout(self.relu(self.bn1(self.fc1(z))))
        h = self.relu(self.bn2(self.fc2(h)))
        return self.out(h)

class VAE_MLP(nn.Module):
    def __init__(self, input_dim=39, latent_dim=16, num_classes=8):
        super(VAE_MLP, self).__init__()
        self.vae = VAE(input_dim, latent_dim)
        self.classifier = MLPClassifier(latent_dim, num_classes)

    def forward(self, x):
        mu, logvar = self.vae.encode(x)
        z = self.vae.reparameterize(mu, logvar)
        recon_x = self.vae.decode(z)
        logits = self.classifier(z)
        return logits

def export_and_quantize():
    print("[*] Cargando modelo PyTorch entrenado...")
    model_path = os.path.join(MODELS_DIR, "vae_mlp_best.pt")
    
    # Load PyTorch model for inference
    full_model = VAE_MLP(input_dim=num_features, latent_dim=16, num_classes=num_classes)
    
    # Load state dict
    state_dict = torch.load(model_path, map_location='cpu')
    full_model.load_state_dict(state_dict)
    full_model.eval()

    # Define dummy input for ONNX export
    dummy_input = torch.randn(1, num_features, dtype=torch.float32)
    onnx_path = os.path.join(MODELS_DIR, "vae_mlp.onnx")

    print("[*] Exportando modelo a formato ONNX...")
    torch.onnx.export(
        full_model,
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
    print(f"[+] Modelo ONNX exportado en: {onnx_path}")

    # Quantize model to INT8
    quantized_onnx_path = os.path.join(MODELS_DIR, "vae_mlp_quantized.onnx")
    print("[*] Aplicando Cuantificación Pos-Entrenamiento (INT8 Dynamic Quantization)...")
    
    quantize_dynamic(
        model_input=onnx_path,
        model_output=quantized_onnx_path,
        weight_type=QuantType.QUInt8
    )
    print(f"[+] Modelo Cuantizado INT8 guardado en: {quantized_onnx_path}")

    # Compare File Sizes
    size_fp32 = os.path.getsize(onnx_path) / 1024
    size_int8 = os.path.getsize(quantized_onnx_path) / 1024
    print(f"\n[+] Comparativa de Tamaño de Archivo:")
    print(f"    - Modelo ONNX (Float32):  {size_fp32:.2f} KB")
    print(f"    - Modelo ONNX (INT8):     {size_int8:.2f} KB")
    print(f"    - Compresión:             {((size_fp32 - size_int8)/size_fp32)*100:.2f}% de reducción")

    # Benchmark Inference Latency
    print("\n[*] Realizando Benchmark de Latencia en Inferencia (1,000 muestras)...")
    test_df = pd.read_parquet(os.path.join(DATA_DIR, "test.parquet"))
    sample_data = test_df[feature_cols].head(1000).values.astype(np.float32)

    # PyTorch CPU inference benchmark
    t0 = time.time()
    with torch.no_grad():
        _ = full_model(torch.tensor(sample_data))
    t_pytorch = (time.time() - t0) * 1000

    # ONNX FP32 inference benchmark
    ort_session_fp32 = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
    t0 = time.time()
    _ = ort_session_fp32.run(None, {'input': sample_data})
    t_onnx_fp32 = (time.time() - t0) * 1000

    # ONNX INT8 inference benchmark
    ort_session_int8 = ort.InferenceSession(quantized_onnx_path, providers=['CPUExecutionProvider'])
    t0 = time.time()
    _ = ort_session_int8.run(None, {'input': sample_data})
    t_onnx_int8 = (time.time() - t0) * 1000

    print(f"    - Tiempo Inferencia PyTorch (CPU):    {t_pytorch:.2f} ms")
    print(f"    - Tiempo Inferencia ONNX (Float32):   {t_onnx_fp32:.2f} ms")
    print(f"    - Tiempo Inferencia ONNX (INT8):      {t_onnx_int8:.2f} ms")

    return full_model, ort_session_int8

def compute_xai_shap(full_model):
    print("\n[*] Inicializando Explicabilidad XAI con SHAP...")
    test_df = pd.read_parquet(os.path.join(DATA_DIR, "test.parquet"))
    
    X_test = test_df[feature_cols].values.astype(np.float32)
    y_test = test_df['target'].values

    # Select background dataset for KernelExplainer / DeepExplainer (50 samples for fast execution)
    background_indices = np.random.choice(len(X_test), 50, replace=False)
    background_data = X_test[background_indices]

    def model_predict_probs(x_array):
        full_model.eval()
        with torch.no_grad():
            tensor_x = torch.tensor(x_array, dtype=torch.float32)
            logits = full_model(tensor_x)
            probs = torch.softmax(logits, dim=1).numpy()
        return probs

    print("[*] Creando explainer KernelExplainer de SHAP...")
    explainer = shap.KernelExplainer(model_predict_probs, background_data)

    # Pick 20 test samples representing different attack categories for SHAP calculation
    sample_indices = []
    for c in range(num_classes):
        idx_c = np.where(y_test == c)[0]
        if len(idx_c) > 0:
            sample_indices.extend(idx_c[:3])
    
    test_samples = X_test[sample_indices]

    print(f"[*] Calculando valores SHAP para {len(test_samples)} muestras de prueba...")
    shap_values = explainer.shap_values(test_samples)

    # Save summary plot for Class 0 / Overall
    print("[*] Generando gráfico de interpretabilidad SHAP Summary Plot...")
    plt.figure(figsize=(12, 8))
    
    # shap_values shape is (num_samples, num_features, num_classes)
    feature_importance = np.mean(np.abs(shap_values), axis=(0, 2)) # shape (39,)
    top_indices = np.argsort(feature_importance)[::-1][:10]
    top_features = [feature_cols[i] for i in top_indices]
    top_scores = feature_importance[top_indices]

    plt.barh(top_features[::-1], top_scores[::-1], color='#3182bd')
    plt.xlabel('SHAP Value (Impacto Promedio en la Predicción del Ataque)')
    plt.title('Top-10 Características Más Relevantes (XAI EdgeGuard-IoT)')
    plt.tight_layout()
    
    shap_plot_path = os.path.join(MODELS_DIR, "shap_summary_plot.png")
    plt.savefig(shap_plot_path, dpi=300)
    plt.close()
    print(f"[+] Gráfico SHAP guardado en: {shap_plot_path}")

    # Save SHAP feature importances dictionary as JSON
    shap_dict = {feature_cols[i]: float(feature_importance[i]) for i in range(num_features)}
    with open(os.path.join(MODELS_DIR, "shap_importances.json"), "w") as f:
        json.dump(shap_dict, f, indent=4)

    print("\n[+] Proceso de Cuantificación y XAI completado exitosamente.")

if __name__ == "__main__":
    full_model, ort_session = export_and_quantize()
    compute_xai_shap(full_model)
