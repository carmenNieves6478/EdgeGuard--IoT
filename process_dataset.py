import os
import glob
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Set random seed
np.random.seed(42)

# Define directories
DATA_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\MERGED_CSV"
PROCESSED_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\data\processed"
MODELS_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\models"

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# 7 attack categories + Benign mapping (CIC-IoT-2023)
LABEL_MAP = {
    # DDoS
    'DDOS-ICMP_FLOOD': 'DDoS',
    'DDOS-UDP_FLOOD': 'DDoS',
    'DDOS-TCP_FLOOD': 'DDoS',
    'DDOS-PSHACK_FLOOD': 'DDoS',
    'DDOS-RSTFINFLOOD': 'DDoS',
    'DDOS-SYN_FLOOD': 'DDoS',
    'DDOS-SYNONYMOUSIP_FLOOD': 'DDoS',
    'DDOS-ICMP_FRAGMENTATION': 'DDoS',
    'DDOS-ACK_FRAGMENTATION': 'DDoS',
    'DDOS-UDP_FRAGMENTATION': 'DDoS',
    'DDOS-HTTP_FLOOD': 'DDoS',
    'DDOS-SLOWLORIS': 'DDoS',
    # DoS
    'DOS-UDP_FLOOD': 'DoS',
    'DOS-TCP_FLOOD': 'DoS',
    'DOS-SYN_FLOOD': 'DoS',
    'DOS-HTTP_FLOOD': 'DoS',
    # Mirai
    'MIRAI-GREETH_FLOOD': 'Mirai',
    'MIRAI-UDPPLAIN': 'Mirai',
    'MIRAI-GREIP_FLOOD': 'Mirai',
    # Recon
    'VULNERABILITYSCAN': 'Recon',
    'RECON-HOSTDISCOVERY': 'Recon',
    'RECON-OSSCAN': 'Recon',
    'RECON-PORTSCAN': 'Recon',
    'RECON-PINGSWEEP': 'Recon',
    # Spoofing
    'MITM-ARPSPOOFING': 'Spoofing',
    'DNS_SPOOFING': 'Spoofing',
    # Brute Force
    'DICTIONARYBRUTEFORCE': 'Brute Force',
    # Web-based
    'BROWSERHIJACKING': 'Web-based',
    'SQLINJECTION': 'Web-based',
    'COMMANDINJECTION': 'Web-based',
    'XSS': 'Web-based',
    'BACKDOOR_MALWARE': 'Web-based',
    'UPLOADING_ATTACK': 'Web-based',
    # Benign
    'BENIGN': 'Benign'
}

def load_and_balance_dataset(max_samples_per_class=25000, chunksize=100000):
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    print(f"[*] Encontrados {len(csv_files)} archivos CSV en {DATA_DIR}")

    category_buckets = {cat: [] for cat in set(LABEL_MAP.values())}
    category_counts = {cat: 0 for cat in set(LABEL_MAP.values())}
    
    print("[*] Leyendo archivos CSV en fragmentos (chunks) y balanceando clases...")
    
    for f_idx, csv_file in enumerate(csv_files, 1):
        print(f" -> Procesando archivo [{f_idx}/{len(csv_files)}]: {os.path.basename(csv_file)}")
        for chunk in pd.read_csv(csv_file, chunksize=chunksize):
            if 'Label' not in chunk.columns:
                continue
            
            chunk['Category'] = chunk['Label'].map(LABEL_MAP)
            chunk = chunk.dropna(subset=['Category'])
            
            for cat, group in chunk.groupby('Category'):
                needed = max_samples_per_class - category_counts[cat]
                if needed > 0:
                    sample = group.head(needed)
                    category_buckets[cat].append(sample)
                    category_counts[cat] += len(sample)
        
        # Check if all categories reached the cap
        if all(cnt >= max_samples_per_class for cnt in category_counts.values()):
            print("[+] Se alcanzó la cuota de muestras para todas las clases.")
            break

    print("\n[+] Conteo final de muestras por categoría:")
    for cat, count in category_counts.items():
        print(f"    - {cat}: {count:,} muestras")

    # Concatenate all collected buckets
    all_dfs = []
    for cat, list_df in category_buckets.items():
        if list_df:
            all_dfs.append(pd.concat(list_df, ignore_index=True))

    df_balanced = pd.concat(all_dfs, ignore_index=True)
    return df_balanced

def preprocess_and_split(df):
    print("\n[*] Limpiando y normalizando características numéricas...")
    
    # Target column
    target_col = 'Category'
    drop_cols = ['Label', target_col]
    
    feature_cols = [c for c in df.columns if c not in drop_cols]
    
    # Handle infinite and NaN values
    X = df[feature_cols].copy()
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())
    
    y = df[target_col].values

    # Train / Val / Test split (70% Train, 15% Val, 15% Test)
    X_train_raw, X_temp, y_train_raw, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    X_val_raw, X_test_raw, y_val_raw, y_test_raw = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )

    print(f"[+] Splits generados:")
    print(f"    - Train: {len(X_train_raw):,} filas")
    print(f"    - Val:   {len(X_val_raw):,} filas")
    print(f"    - Test:  {len(X_test_raw):,} filas")

    # Fit MinMaxScaler on Train set ONLY
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train_raw)
    X_val_scaled = scaler.transform(X_val_raw)
    X_test_scaled = scaler.transform(X_test_raw)

    # Encode labels
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train_raw)
    y_val = label_encoder.transform(y_val_raw)
    y_test = label_encoder.transform(y_test_raw)

    # Convert scaled features back to DataFrame with target for Parquet export
    train_df = pd.DataFrame(X_train_scaled, columns=feature_cols)
    train_df['target'] = y_train
    
    val_df = pd.DataFrame(X_val_scaled, columns=feature_cols)
    val_df['target'] = y_val

    test_df = pd.DataFrame(X_test_scaled, columns=feature_cols)
    test_df['target'] = y_test

    # Save to parquet
    print("\n[*] Guardando datasets en formato .parquet...")
    train_df.to_parquet(os.path.join(PROCESSED_DIR, "train.parquet"), index=False)
    val_df.to_parquet(os.path.join(PROCESSED_DIR, "val.parquet"), index=False)
    test_df.to_parquet(os.path.join(PROCESSED_DIR, "test.parquet"), index=False)

    # Save artifacts (Scaler, LabelEncoder, Feature Names)
    print("[*] Guardando artefactos (Scaler, LabelEncoder, Feature Names)...")
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.joblib"))
    joblib.dump(label_encoder, os.path.join(MODELS_DIR, "label_encoder.joblib"))
    
    meta_info = {
        "feature_names": feature_cols,
        "classes": label_encoder.classes_.tolist(),
        "num_features": len(feature_cols),
        "num_classes": len(label_encoder.classes_)
    }
    with open(os.path.join(MODELS_DIR, "meta_info.json"), "w") as f:
        json.dump(meta_info, f, indent=4)

    print("\n[+] Preprocesamiento completado exitosamente.")
    print(f"    - Data procesada guardada en: {PROCESSED_DIR}")
    print(f"    - Artefactos guardados en: {MODELS_DIR}")
    print(f"    - Clases detectadas: {label_encoder.classes_.tolist()}")

if __name__ == "__main__":
    df_balanced = load_and_balance_dataset(max_samples_per_class=25000)
    preprocess_and_split(df_balanced)
