import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import classification_report, confusion_matrix, f1_score, recall_score, precision_score

# Set seeds
torch.manual_seed(42)
np.random.seed(42)

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"[*] Usando dispositivo de entrenamiento: {device}")

# Directories
DATA_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\data\processed"
MODELS_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\models"

# Load metadata
with open(os.path.join(MODELS_DIR, "meta_info.json"), "r") as f:
    meta_info = json.load(f)

feature_cols = meta_info["feature_names"]
classes = meta_info["classes"]
num_features = meta_info["num_features"]
num_classes = meta_info["num_classes"]

# Dataset class
class TabularDataset(Dataset):
    def __init__(self, parquet_path):
        df = pd.read_parquet(parquet_path)
        self.X = torch.tensor(df[feature_cols].values, dtype=torch.float32)
        self.y = torch.tensor(df['target'].values, dtype=torch.long)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# VAE Model Definition
class VAE(nn.Module):
    def __init__(self, input_dim=39, latent_dim=16):
        super(VAE, self).__init__()
        # Encoder
        self.fc1 = nn.Linear(input_dim, 64)
        self.bn1 = nn.BatchNorm1d(64)
        self.fc2 = nn.Linear(64, 32)
        self.bn2 = nn.BatchNorm1d(32)
        self.fc_mu = nn.Linear(32, latent_dim)
        self.fc_logvar = nn.Linear(32, latent_dim)
        
        # Decoder
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
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar

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
        recon_x = self.decode(z)
        return recon_x, mu, logvar, z

# MLP Classifier Definition
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
        logits = self.out(h)
        return logits

# Combined Hybrid VAE-MLP
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
        return recon_x, mu, logvar, logits, z

# Loss function for VAE
def vae_loss_function(recon_x, x, mu, logvar, beta=0.01):
    mse_loss = nn.functional.mse_loss(recon_x, x, reduction='sum')
    # KL Divergence
    kld_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return mse_loss + beta * kld_loss

def train_model():
    print("[*] Cargando DataLoaders...")
    train_dataset = TabularDataset(os.path.join(DATA_DIR, "train.parquet"))
    val_dataset   = TabularDataset(os.path.join(DATA_DIR, "val.parquet"))
    test_dataset  = TabularDataset(os.path.join(DATA_DIR, "test.parquet"))

    batch_size = 256
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader   = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader  = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    model = VAE_MLP(input_dim=num_features, latent_dim=16, num_classes=num_classes).to(device)
    
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    criterion_cls = nn.CrossEntropyLoss()
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)

    epochs = 20
    alpha_recon = 0.5  # Weight for VAE reconstruction loss
    alpha_cls = 1.0    # Weight for classification loss

    best_val_loss = float('inf')
    best_model_path = os.path.join(MODELS_DIR, "vae_mlp_best.pt")

    print(f"\n[*] Entrenando arquitectura VAE-MLP durante {epochs} épocas...")
    history = {"train_loss": [], "val_loss": [], "val_f1": []}

    for epoch in range(1, epochs + 1):
        model.train()
        total_train_loss = 0.0
        
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            
            recon_x, mu, logvar, logits, z = model(batch_x)
            
            v_loss = vae_loss_function(recon_x, batch_x, mu, logvar) / batch_x.size(0)
            c_loss = criterion_cls(logits, batch_y)
            
            loss = alpha_recon * v_loss + alpha_cls * c_loss
            loss.backward()
            optimizer.step()
            
            total_train_loss += loss.item() * batch_x.size(0)

        avg_train_loss = total_train_loss / len(train_dataset)

        # Validation phase
        model.eval()
        total_val_loss = 0.0
        all_val_preds = []
        all_val_targets = []

        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                recon_x, mu, logvar, logits, z = model(batch_x)
                
                v_loss = vae_loss_function(recon_x, batch_x, mu, logvar) / batch_x.size(0)
                c_loss = criterion_cls(logits, batch_y)
                val_loss = alpha_recon * v_loss + alpha_cls * c_loss
                
                total_val_loss += val_loss.item() * batch_x.size(0)
                
                preds = torch.argmax(logits, dim=1)
                all_val_preds.extend(preds.cpu().numpy())
                all_val_targets.extend(batch_y.cpu().numpy())

        avg_val_loss = total_val_loss / len(val_dataset)
        val_f1 = f1_score(all_val_targets, all_val_preds, average='macro')
        
        scheduler.step(avg_val_loss)
        
        history["train_loss"].append(avg_train_loss)
        history["val_loss"].append(avg_val_loss)
        history["val_f1"].append(val_f1)

        print(f"Época [{epoch:02d}/{epochs:02d}] | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f} | Val F1-Macro: {val_f1:.4f}")

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), best_model_path)

    print(f"\n[+] Entrenamiento completado. Mejor modelo guardado en {best_model_path}")

    # Load best model for evaluation on test set
    model.load_state_dict(torch.load(best_model_path))
    model.eval()

    all_test_preds = []
    all_test_targets = []

    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            batch_x = batch_x.to(device)
            _, _, _, logits, _ = model(batch_x)
            preds = torch.argmax(logits, dim=1)
            all_test_preds.extend(preds.cpu().numpy())
            all_test_targets.extend(batch_y.numpy())

    # Evaluation Metrics
    print("\n" + "="*50)
    print("      REPORT DE EVALUACIÓN EN TEST SET (VAE-MLP)")
    print("="*50)
    report = classification_report(all_test_targets, all_test_preds, target_names=classes, digits=4)
    print(report)

    macro_f1 = f1_score(all_test_targets, all_test_preds, average='macro')
    weighted_f1 = f1_score(all_test_targets, all_test_preds, average='weighted')
    macro_recall = recall_score(all_test_targets, all_test_preds, average='macro')
    macro_precision = precision_score(all_test_targets, all_test_preds, average='macro')

    print(f"F1-Score Macro:     {macro_f1:.4f}")
    print(f"F1-Score Weighted:  {weighted_f1:.4f}")
    print(f"Recall Macro:       {macro_recall:.4f}")
    print(f"Precision Macro:    {macro_precision:.4f}")

    # Save metrics report as JSON
    metrics_summary = {
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
        "macro_recall": float(macro_recall),
        "macro_precision": float(macro_precision),
        "classes": classes
    }
    with open(os.path.join(MODELS_DIR, "eval_metrics.json"), "w") as f:
        json.dump(metrics_summary, f, indent=4)

    # Confusion Matrix
    cm = confusion_matrix(all_test_targets, all_test_preds)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Matriz de Confusión - VAE-MLP EdgeGuard-IoT')
    plt.xlabel('Predicción')
    plt.ylabel('Verdadero')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(MODELS_DIR, "confusion_matrix.png"), dpi=300)
    plt.close()
    print(f"[+] Matriz de confusión guardada en {os.path.join(MODELS_DIR, 'confusion_matrix.png')}")

if __name__ == "__main__":
    train_model()
