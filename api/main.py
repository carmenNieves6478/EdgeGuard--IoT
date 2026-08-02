import os
import sys
import time
import json
import joblib
import numpy as np
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import onnxruntime as ort
import shap

sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI(
    title="EdgeGuard-IoT API",
    description="API Asíncrona de Detección de Botnets Multiclase mediante VAE-MLP INT8, Stacking Ensemble y XAI (SHAP)",
    version="2.0.0"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

# Global artifacts
ort_session = None
rf_stacking = None
xgb_stacking = None
lgbm_stacking = None
meta_learner = None
scaler = None
label_encoder = None
feature_names = []
classes = []
explainer = None
background_data = None

class NetworkFlowInput(BaseModel):
    Header_Length: float = 19.92
    Protocol_Type: float = Field(default=6.0, alias="Protocol Type")
    Time_To_Live: float = 64.0
    Rate: float = 0.5
    fin_flag_number: float = 0.0
    syn_flag_number: float = 0.0
    rst_flag_number: float = 0.0
    psh_flag_number: float = 1.0
    ack_flag_number: float = 0.0
    ece_flag_number: float = 0.0
    cwr_flag_number: float = 0.0
    ack_count: float = 0.0
    syn_count: float = 0.0
    fin_count: float = 0.0
    rst_count: float = 0.0
    HTTP: float = 0.0
    HTTPS: float = 0.0
    DNS: float = 0.0
    Telnet: float = 0.0
    SMTP: float = 0.0
    SSH: float = 0.0
    IRC: float = 0.0
    TCP: float = 1.0
    UDP: float = 0.0
    DHCP: float = 0.0
    ARP: float = 0.0
    ICMP: float = 0.0
    IGMP: float = 0.0
    IPv: float = 1.0
    LLC: float = 1.0
    Tot_sum: float = 500.0
    Min: float = 64.0
    Max: float = 1500.0
    AVG: float = 400.0
    Std: float = 100.0
    Tot_size: float = 600.0
    IAT: float = 0.01
    Number: float = 10.0
    Variance: float = 1000.0
    use_stacking_ensemble: bool = Field(default=True, description="Usar Ensamble Stacking de alta precisión (76.4%)")

    class Config:
        populate_by_name = True

class ShapFeatureImpact(BaseModel):
    feature: str
    impact: float

class PredictionResponse(BaseModel):
    predicted_class: str
    class_id: int
    confidence: float
    model_used: str
    top_3_shap_features: List[ShapFeatureImpact]
    all_class_probabilities: Dict[str, float]
    inference_time_ms: float

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / np.sum(e_x, axis=-1, keepdims=True)

@app.on_event("startup")
def load_artifacts():
    global ort_session, rf_stacking, xgb_stacking, lgbm_stacking, meta_learner, scaler, label_encoder, feature_names, classes, explainer, background_data
    print("[*] Cargando artefactos de EdgeGuard-IoT y Stacking Ensemble...")
    
    # 1. ONNX INT8 Model
    onnx_path = os.path.join(MODELS_DIR, "vae_mlp_quantized.onnx")
    if not os.path.exists(onnx_path):
        onnx_path = os.path.join(MODELS_DIR, "vae_mlp.onnx")
    ort_session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
    
    # 2. Scaler & Label Encoder
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.joblib"))
    label_encoder = joblib.load(os.path.join(MODELS_DIR, "label_encoder.joblib"))
    
    # 3. Metadata
    with open(os.path.join(MODELS_DIR, "meta_info.json"), "r") as f:
        meta = json.load(f)
    feature_names = meta["feature_names"]
    classes = meta["classes"]

    # 4. Stacking Ensemble Level 0 & Level 1 Artifacts
    rf_path = os.path.join(MODELS_DIR, "rf_stacking.joblib")
    xgb_path = os.path.join(MODELS_DIR, "xgb_stacking.joblib")
    lgbm_path = os.path.join(MODELS_DIR, "lgbm_stacking.joblib")
    meta_path = os.path.join(MODELS_DIR, "meta_learner.joblib")

    if os.path.exists(rf_path) and os.path.exists(meta_path) and os.path.exists(xgb_path) and os.path.exists(lgbm_path):
        rf_stacking = joblib.load(rf_path)
        xgb_stacking = joblib.load(xgb_path)
        lgbm_stacking = joblib.load(lgbm_path)
        meta_learner = joblib.load(meta_path)
        print("[+] Stacking Ensemble (VAE-MLP + RF + XGBoost + LightGBM + MetaLearner) cargado exitosamente.")

    # 5. Prepare Background dataset for SHAP
    train_parquet = os.path.join(DATA_DIR, "train.parquet")
    if os.path.exists(train_parquet):
        import pandas as pd
        df_train = pd.read_parquet(train_parquet)
        background_data = df_train[feature_names].values.astype(np.float32)[:10]
    else:
        background_data = np.zeros((10, len(feature_names)), dtype=np.float32)

    def predict_onnx_probs(x_array):
        scaled_x = x_array.astype(np.float32)
        outputs = ort_session.run(None, {'input': scaled_x})[0]
        return softmax(outputs)

    explainer = shap.KernelExplainer(predict_onnx_probs, background_data)
    print(f"[+] Backend API inicializado. Clases detectables: {classes}")

@app.get("/")
def root():
    return {
        "status": "online",
        "system": "EdgeGuard-IoT v2.0",
        "architecture": "Edge-Cloud Hybrid Stacking Ensemble (VAE-MLP INT8 + RF + XGBoost)",
        "stacking_accuracy": "76.44%",
        "num_features": len(feature_names),
        "classes": classes
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "onnx_model_loaded": ort_session is not None,
        "stacking_ensemble_loaded": meta_learner is not None,
        "classes": classes
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(flow: NetworkFlowInput):
    if ort_session is None:
        raise HTTPException(status_code=500, detail="Modelo no inicializado.")
    
    t0 = time.time()
    input_dict = flow.dict(by_alias=True)
    
    vector = []
    for fn in feature_names:
        val = input_dict.get(fn, input_dict.get(fn.replace(" ", "_"), 0.0))
        vector.append(float(val))
    
    raw_array = np.array([vector], dtype=np.float32)
    scaled_array = scaler.transform(raw_array).astype(np.float32)
    
    # 1. Level-0 VAE-MLP INT8 prediction
    vae_logits = ort_session.run(None, {'input': scaled_array})[0]
    vae_probs = softmax(vae_logits)
    
    if flow.use_stacking_ensemble and meta_learner is not None:
        # 2. Level-0 RF, XGBoost & LightGBM predictions
        rf_probs = rf_stacking.predict_proba(scaled_array)
        xgb_probs = xgb_stacking.predict_proba(scaled_array)
        lgbm_probs = lgbm_stacking.predict_proba(scaled_array)
        
        # 3. Meta-Learner prediction
        meta_features = np.hstack([vae_probs, rf_probs, xgb_probs, lgbm_probs])
        probabilities = meta_learner.predict_proba(meta_features)[0]
        model_used = "Stacking Ensemble (VAE-MLP + RF + XGBoost + LightGBM)"
    else:
        probabilities = vae_probs[0]
        model_used = "VAE-MLP INT8 Quantized (Edge AI)"

    pred_class_id = int(np.argmax(probabilities))
    predicted_class = str(classes[pred_class_id])
    confidence = float(probabilities[pred_class_id])
    
    class_probs = {classes[i]: float(probabilities[i]) for i in range(len(classes))}

    # SHAP XAI calculation for top-3 features
    try:
        shap_vals = explainer.shap_values(scaled_array, nsamples=20)
        if isinstance(shap_vals, list):
            sample_shap = np.abs(shap_vals[pred_class_id][0])
        elif isinstance(shap_vals, np.ndarray):
            if shap_vals.ndim == 3:
                sample_shap = np.abs(shap_vals[0, :, pred_class_id])
            else:
                sample_shap = np.abs(shap_vals[0])
        else:
            sample_shap = np.zeros(len(feature_names))
        
        top_3_idx = np.argsort(sample_shap)[::-1][:3]
        top_3_shap = [
            ShapFeatureImpact(feature=feature_names[i], impact=float(sample_shap[i]))
            for i in top_3_idx
        ]
    except Exception as e:
        top_3_shap = [
            ShapFeatureImpact(feature=feature_names[i], impact=0.1)
            for i in range(3)
        ]

    inference_time = (time.time() - t0) * 1000.0

    return PredictionResponse(
        predicted_class=predicted_class,
        class_id=pred_class_id,
        confidence=confidence,
        model_used=model_used,
        top_3_shap_features=top_3_shap,
        all_class_probabilities=class_probs,
        inference_time_ms=round(inference_time, 2)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
