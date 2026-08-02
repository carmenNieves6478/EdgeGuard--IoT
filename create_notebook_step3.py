import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# EdgeGuard-IoT: Step 3 - Post-Training Quantization (INT8) & Explainable AI (SHAP)\n",
    "**Objective:** Export PyTorch model to ONNX, apply INT8 dynamic quantization for Edge AI deployment, evaluate compression & latency speedups, and calculate SHAP feature importances."
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
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import onnxruntime as ort\n",
    "import shap\n",
    "\n",
    "print(\"Libraries loaded for Step 3 Quantization & XAI.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Quantization & Latency Benchmark Comparison"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "size_fp32 = os.path.getsize('../models/vae_mlp.onnx') / 1024\n",
    "size_int8 = os.path.getsize('../models/vae_mlp_quantized.onnx') / 1024\n",
    "\n",
    "print(f\"ONNX Float32 Model Size: {size_fp32:.2f} KB\")\n",
    "print(f\"ONNX INT8 Quantized Size: {size_int8:.2f} KB\")\n",
    "print(f\"Storage Compression:     {((size_fp32 - size_int8)/size_fp32)*100:.2f}%\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Explainable AI (SHAP) Feature Importance Visualization"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists('../models/shap_summary_plot.png'):\n",
    "    from IPython.display import Image\n",
    "    display(Image('../models/shap_summary_plot.png'))\n",
    "\n",
    "with open('../models/shap_importances.json') as f:\n",
    "    shap_dict = json.load(f)\n",
    "\n",
    "sorted_shap = sorted(shap_dict.items(), key=lambda x: x[1], reverse=True)[:10]\n",
    "print(\"Top-10 Features by SHAP Importance:\")\n",
    "for feat, val in sorted_shap:\n",
    "    print(f\" - {feat:25s}: {val:.6f}\")"
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

with open("E:/PROYECTO DE INVESTIGACION/dataset/MERGED_CSV/notebooks/03_Quantization_and_XAI.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)
print("Notebook 03 created successfully.")
