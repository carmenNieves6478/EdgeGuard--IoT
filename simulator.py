import os
import sys
import time
import glob
import json
import random
import requests
import pandas as pd

# Force UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
DATA_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\MERGED_CSV"
TEST_PARQUET = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\data\processed\test.parquet"
META_INFO = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\models\meta_info.json"

# Load metadata
with open(META_INFO, "r") as f:
    meta = json.load(f)

feature_names = meta["feature_names"]
classes = meta["classes"]

def load_sample_dataset():
    print("[*] Cargando muestras de prueba para la simulación de tráfico IoT en vivo...")
    if os.path.exists(TEST_PARQUET):
        df = pd.read_parquet(TEST_PARQUET)
        print(f"[+] Cargado test set procesado ({len(df):,} filas disponibles).")
        return df
    else:
        csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
        if not csv_files:
            raise FileNotFoundError("No se encontraron archivos CSV de prueba.")
        df = pd.read_csv(csv_files[0], nrows=1000)
        return df

def run_simulation(interval=1.0, max_requests=None):
    df_samples = load_sample_dataset()
    print(f"[*] Iniciando simulador de tráfico IoT -> Backend API: {API_URL}")
    print(f"[*] Frecuencia de envío: {interval} segundo(s) por paquete")
    print("=" * 85)
    print(f"{'#':<5} | {'Etiqueta Real':<15} | {'Predicción API':<15} | {'Confianza':<10} | {'Latencia':<10} | {'Top SHAP'}")
    print("=" * 85)

    req_count = 0
    try:
        while True:
            # Select random sample
            sample = df_samples.sample(1).iloc[0]
            
            if 'target' in sample:
                true_label_idx = int(sample['target'])
                true_label = classes[true_label_idx]
            elif 'Label' in sample:
                true_label = str(sample['Label'])
            else:
                true_label = "Unknown"

            # Build payload
            payload = {}
            for fn in feature_names:
                payload[fn] = float(sample.get(fn, 0.0))

            t0 = time.time()
            try:
                res = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    pred_class = data["predicted_class"]
                    confidence = f"{data['confidence']*100:.1f}%"
                    latency = f"{data['inference_time_ms']:.1f}ms"
                    top_shap = data["top_3_shap_features"][0]["feature"] if data["top_3_shap_features"] else "N/A"

                    # Color coding for terminal output
                    status_prefix = "🟢" if pred_class == "Benign" else "⚠️"
                    print(f"{req_count+1:<5} | {true_label:<15} | {status_prefix} {pred_class:<13} | {confidence:<10} | {latency:<10} | {top_shap}")
                else:
                    print(f"{req_count+1:<5} | Error HTTP {res.status_code}: {res.text}")
            except Exception as e:
                print(f"{req_count+1:<5} | Error de conexión con API: {e}")

            req_count += 1
            if max_requests and req_count >= max_requests:
                break
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[*] Simulación detenida por el usuario.")

if __name__ == "__main__":
    # Run simulation (by default 1 request per second)
    run_simulation(interval=1.0)
