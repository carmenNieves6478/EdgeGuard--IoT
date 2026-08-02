import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# EdgeGuard-IoT: Step 2 - Hybrid VAE-MLP Architecture Training\n",
    "**Objective:** Build and train a Variational Autoencoder (VAE) for dimensionality compression / feature encoding, coupled with a Multi-Layer Perceptron (MLP) multi-class classifier on PyTorch."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import json\n",
    "import joblib\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import torch\n",
    "import torch.nn as nn\n",
    "import torch.optim as optim\n",
    "from torch.utils.data import Dataset, DataLoader\n",
    "from sklearn.metrics import classification_report, confusion_matrix, f1_score\n",
    "\n",
    "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n",
    "print(f\"Using device: {device}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. PyTorch VAE-MLP Model Definitions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "class VAE(nn.Module):\n",
    "    def __init__(self, input_dim=39, latent_dim=16):\n",
    "        super(VAE, self).__init__()\n",
    "        self.fc1 = nn.Linear(input_dim, 64)\n",
    "        self.bn1 = nn.BatchNorm1d(64)\n",
    "        self.fc2 = nn.Linear(64, 32)\n",
    "        self.bn2 = nn.BatchNorm1d(32)\n",
    "        self.fc_mu = nn.Linear(32, latent_dim)\n",
    "        self.fc_logvar = nn.Linear(32, latent_dim)\n",
    "        self.fc3 = nn.Linear(latent_dim, 32)\n",
    "        self.bn3 = nn.BatchNorm1d(32)\n",
    "        self.fc4 = nn.Linear(32, 64)\n",
    "        self.bn4 = nn.BatchNorm1d(64)\n",
    "        self.fc5 = nn.Linear(64, input_dim)\n",
    "        self.relu = nn.ReLU()\n",
    "        self.sigmoid = nn.Sigmoid()\n",
    "\n",
    "    def encode(self, x):\n",
    "        h = self.relu(self.bn1(self.fc1(x)))\n",
    "        h = self.relu(self.bn2(self.fc2(h)))\n",
    "        return self.fc_mu(h), self.fc_logvar(h)\n",
    "\n",
    "    def reparameterize(self, mu, logvar):\n",
    "        std = torch.exp(0.5 * logvar)\n",
    "        eps = torch.randn_like(std)\n",
    "        return mu + eps * std\n",
    "\n",
    "    def decode(self, z):\n",
    "        h = self.relu(self.bn3(self.fc3(z)))\n",
    "        h = self.relu(self.bn4(self.fc4(h)))\n",
    "        return self.sigmoid(self.fc5(h))\n",
    "\n",
    "    def forward(self, x):\n",
    "        mu, logvar = self.encode(x)\n",
    "        z = self.reparameterize(mu, logvar)\n",
    "        return self.decode(z), mu, logvar, z\n",
    "\n",
    "class MLPClassifier(nn.Module):\n",
    "    def __init__(self, latent_dim=16, num_classes=8):\n",
    "        super(MLPClassifier, self).__init__()\n",
    "        self.fc1 = nn.Linear(latent_dim, 32)\n",
    "        self.bn1 = nn.BatchNorm1d(32)\n",
    "        self.relu = nn.ReLU()\n",
    "        self.dropout = nn.Dropout(0.2)\n",
    "        self.fc2 = nn.Linear(32, 16)\n",
    "        self.bn2 = nn.BatchNorm1d(16)\n",
    "        self.out = nn.Linear(16, num_classes)\n",
    "\n",
    "    def forward(self, z):\n",
    "        h = self.dropout(self.relu(self.bn1(self.fc1(z))))\n",
    "        h = self.relu(self.bn2(self.fc2(h)))\n",
    "        return self.out(h)\n",
    "\n",
    "class VAE_MLP(nn.Module):\n",
    "    def __init__(self, input_dim=39, latent_dim=16, num_classes=8):\n",
    "        super(VAE_MLP, self).__init__()\n",
    "        self.vae = VAE(input_dim, latent_dim)\n",
    "        self.classifier = MLPClassifier(latent_dim, num_classes)\n",
    "\n",
    "    def forward(self, x):\n",
    "        mu, logvar = self.vae.encode(x)\n",
    "        z = self.vae.reparameterize(mu, logvar)\n",
    "        recon_x = self.vae.decode(z)\n",
    "        logits = self.classifier(z)\n",
    "        return recon_x, mu, logvar, logits, z"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Model Evaluation & Confusion Matrix"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "with open('../models/meta_info.json') as f:\n",
    "    meta = json.load(f)\n",
    "\n",
    "print('Classes:', meta['classes'])\n",
    "if os.path.exists('../models/confusion_matrix.png'):\n",
    "    from IPython.display import Image\n",
    "    display(Image('../models/confusion_matrix.png'))"
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

with open("E:/PROYECTO DE INVESTIGACION/dataset/MERGED_CSV/notebooks/02_Model_Training_VAE_MLP.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)
print("Notebook 02 created successfully.")
