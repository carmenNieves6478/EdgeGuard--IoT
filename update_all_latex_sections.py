import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOC_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\documento"
SEC_DIR = os.path.join(DOC_DIR, "secciones")

print("[*] Reconstruyendo secciones teóricas, metodológicas y de anexos en LaTeX para EdgeGuard-IoT...")

# ------------------------------------------------------------------------------
# 1. marco_teorico.tex
# ------------------------------------------------------------------------------
tex_marco = r"""\section{MARCO TEÓRICO Y CONCEPTUAL}

En esta sección se exponen los fundamentos teóricos sobre los cuales se sostiene el sistema \textbf{EdgeGuard-IoT}: ciberseguridad en redes IoT, Autoencoders Variacionales (VAE), cuantificación dinámicas pos-entrenamiento en ONNX INT8, ensambles de aprendizaje Stacking y explicabilidad SHAP.

\subsection{Amenazas y Vectores de Ciberataque en Redes IoT}
Las redes de dispositivos IoT son vulnerables a múltiples vectores de ataque debido a la falta de parches de seguridad y contraseñas por defecto:
\begin{itemize}
    \item \textbf{DDoS / Packet Flood}: Saturación masiva de ancho de banda mediante ráfagas de paquetes TCP/UDP/ICMP.
    \item \textbf{Mirai Botnet}: Infección mediante escaneo automático y reclutamiento de dispositivos para ataques coordinados C\&C.
    \item \textbf{Reconnaissance / PortScan}: Exploración de puertos abiertos y detección de servicios activos.
    \item \textbf{Spoofing / ARP Poisoning}: Suplantación de identidad en la capa de enlace e IP.
    \item \textbf{Fuerza Bruta}: Ataques automatizados contra servicios Telnet y SSH.
\end{itemize}

\subsection{Autoencoders Variacionales (VAE)}
Un Autoencoder Variacional es un modelo generativo latente que mapea la entrada $\mathbf{x} \in \mathbb{R}^d$ hacia una distribución probabilística en el espacio latente $\mathbf{z} \in \mathbb{R}^k$ mediante un codificador $q_\phi(\mathbf{z}|\mathbf{x}) = \mathcal{N}(\boldsymbol{\mu}, \text{diag}(\boldsymbol{\sigma}^2))$.

Para permitir la retropropagación de gradientes a través de muestras estocásticas, se aplica el truco de reparametrización:
\begin{equation}
\mathbf{z} = \boldsymbol{\mu} + \boldsymbol{\sigma} \odot \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})
\end{equation}

La función de pérdida combinada para clasificación supervisada en EdgeGuard-IoT se formula como:
\begin{equation}
\mathcal{L}_{\text{total}} = \alpha \cdot \text{MSE}(\mathbf{x}, \hat{\mathbf{x}}) + \beta \cdot D_{\text{KL}}\left(\mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\sigma}^2) \parallel \mathcal{N}(\mathbf{0}, \mathbf{I})\right) + \gamma \cdot \text{CE}_{\text{weighted}}(\mathbf{y}, \hat{\mathbf{y}})
\end{equation}

\subsection{Cuantificación Pos-Entrenamiento (INT8 Dynamic Quantization)}
Para desplegar redes neuronales en microcontroladores Edge AI con memoria RAM limitada ($< 256\text{ KB}$), convertimos los pesos y activaciones de punto flotante ($\text{FP32}$) a enteros de 8 bits ($\text{INT8}$):
\begin{equation}
q = \text{round}\left(\frac{x}{S}\right) + Z
\end{equation}
donde $S$ es el factor de escala real y $Z$ es el valor cero cuantizado.

\subsection{Aprendizaje Ensamblado Stacking y Meta-Learners}
El aprendizaje por Stacking combina las predicciones de probabilidad de múltiples modelos base de Nivel 0 (VAE-MLP, Random Forest, XGBoost y LightGBM) en una matriz de metacaracterísticas $\mathbf{M} \in \mathbb{R}^{N \times (K \cdot C)}$, la cual es procesada por un Meta-Learner de Nivel 1 (LightGBM) para emitir la clasificación final.

\subsection{Explicabilidad XAI mediante Valores SHAP}
Para proporcionar interpretabilidad forense a las predicciones del modelo, calculamos los valores SHAP basados en la teoría de juegos cooperativos de Shapley:
\begin{equation}
\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f(S \cup \{i\}) - f(S) \right]
\end{equation}
"""

with open(os.path.join(SEC_DIR, "marco_teorico.tex"), "w", encoding="utf-8") as f:
    f.write(tex_marco)

# ------------------------------------------------------------------------------
# 2. metodologia.tex
# ------------------------------------------------------------------------------
tex_metodologia = r"""\section{METODOLOGÍA EXPERIMENTAL Y FASES DE DESARROLLO}

La metodología del proyecto se estructura rigurosamente en las 5 fases consecutivas descritas a continuación.

\subsection{Fase 1: Análisis Exploratorio, Calidad de Datos y Selección Estadística de Características}
\begin{itemize}
    \item \textbf{Limpieza de Datos}: Imputación de nulos, eliminación de infinitos y registros duplicados.
    \item \textbf{Diccionario de Datos}: Documentación formal de las 39 variables de flujo de red (exportado en \texttt{results/reports\_and\_plots/data\_dictionary.csv}).
    \item \textbf{Selección Estadística}: Evaluación discriminatoria mediante ANOVA F-Test, Mutual Information y Gini Importance de Random Forest (exportado en \texttt{results/reports\_and\_plots/feature\_selection\_stats.csv}).
\end{itemize}

\subsection{Fase 2: Diseño y Configuración de la Arquitectura VAE-MLP}
\begin{itemize}
    \item Encoder VAE: $39 \rightarrow 64 \rightarrow 32 \rightarrow \mathbf{z} (16\text{ dims})$.
    \item Decoder VAE: $\mathbf{z} (16) \rightarrow 32 \rightarrow 64 \rightarrow 39\text{ dims}$.
    \item Clasificador MLP: $\mathbf{z} (16) \rightarrow 32\text{ (BatchNorm, Dropout 0.20)} \rightarrow 16 \rightarrow 8\text{ Clases}$.
\end{itemize}

\subsection{Fase 3: Entrenamiento, Monitoreo y Cuantificación INT8}
\begin{itemize}
    \item Entrenamiento en GPU CUDA durante 40 épocas con la función de pérdida con pesos balanceados por clase (\texttt{Class-Weighted CrossEntropy}).
    \item Cuantificación dinámicas ONNX INT8 reduciendo el footprint a **$21.67\text{ KB}$** y latencia a **$3.25\text{ }\mu\text{s}$**.
\end{itemize}

\subsection{Fase 4: Evaluación Exhaustiva, 5-Fold CV y Threshold Tuning}
\begin{itemize}
    \item Evaluación en test set ($27,949$ muestras) calculando Accuracy, Precision, Recall y F1-Macro.
    \item Validación cruzada estratificada de 5 pliegues (5-Fold CV) alcanzando un promedio de **$76.52\% \pm 0.18\%$** de Accuracy.
    \item Ajuste de umbrales (Threshold Tuning) evaluando puntos de decisión desde $0.30$ a $0.70$.
\end{itemize}

\subsection{Fase 5: Comparación Estado del Arte, Interpretación XAI y MLOps}
\begin{itemize}
    \item Enfrentamiento contra 6 baselines (Regresión Logística, Naive Bayes, CNN-1D, Random Forest, XGBoost, LightGBM).
    \item Explicabilidad SHAP XAI para inspección forense.
    \item Contenerización Docker y despliegue en microservicios FastAPI y Streamlit.
\end{itemize}
"""

with open(os.path.join(SEC_DIR, "metodologia.tex"), "w", encoding="utf-8") as f:
    f.write(tex_metodologia)

# ------------------------------------------------------------------------------
# 3. resultados.tex
# ------------------------------------------------------------------------------
tex_resultados = r"""\section{RESULTADOS EXPERIMENTALES Y DISCUSIÓN}

Los experimentos empíricos se llevaron a cabo sobre el test set ($27,949$ muestras) del dataset CIC-IoT-2023.

\subsection{Tabla Comparativa General Estado del Arte}
La Tabla~\ref{tab:benchmark_general} presenta la evaluación comparativa completa de los 8 modelos probados:

\begin{table}[H]
\centering
\caption{Tabla Comparativa General del Estado del Arte (CIC-IoT-2023)}
\label{tab:benchmark_general}
\small
\begin{tabular}{lcccccc}
\toprule
\textbf{Modelo / Arquitectura} & \textbf{Accuracy (\%)} & \textbf{F1-Macro} & \textbf{Precision} & \textbf{Recall} & \textbf{Latencia ($\mu$s)} & \textbf{Tamaño (KB)} \\
\midrule
Regresión Logística & 64.04\% & 0.6233 & 0.6754 & 0.6185 & 185.27 & 15.00 \\
Naive Bayes & 56.87\% & 0.5340 & 0.6229 & 0.5652 & 4.29 & 10.00 \\
CNN-1D (DL Pesado) & 61.91\% & 0.5722 & 0.5980 & 0.5700 & 1.60 & 120.00 \\
\textbf{EdgeGuard VAE-MLP (INT8)} & \textbf{69.73\%} & \textbf{0.6853} & \textbf{0.7103} & \textbf{0.6834} & \textbf{3.25} & \textbf{21.67} \\
Random Forest & 76.61\% & 0.7525 & 0.7812 & 0.7462 & 5.82 & 52525.00 \\
XGBoost & 77.13\% & 0.7585 & 0.7800 & 0.7533 & 2.68 & 4021.00 \\
LightGBM & 77.73\% & 0.7663 & 0.7828 & 0.7617 & 49.92 & 4134.00 \\
\textbf{Stacking Ensemble (Nube)} & \textbf{77.18\%} & \textbf{0.7604} & \textbf{0.7695} & \textbf{0.7576} & \textbf{2.45} & \textbf{1400.00} \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Validación Cruzada Estratificada (5-Fold Cross Validation)}
La evaluación mediante 5-Fold Cross Validation demuestra la estabilidad del modelo:
\begin{itemize}
    \item \textbf{Promedio Accuracy 5-Fold}: $76.52\% \pm 0.18\%$
    \item \textbf{Promedio F1-Score Macro 5-Fold}: $0.7519 \pm 0.0022$
\end{itemize}

\subsection{Registro de Figuras de Alta Resolución}
Todas las figuras producidas durante la experimentación se encuentran almacenadas en el directorio de resultados:
\begin{itemize}
    \item \textbf{Curvas ROC Multiclase (ROC-AUC)}: \texttt{results/reports\_and\_plots/roc\_curves\_multiclass.png}
    \item \textbf{Curvas Precision-Recall}: \texttt{results/reports\_and\_plots/precision\_recall\_curves.png}
    \item \textbf{Matrices de Confusión Combinadas}: \texttt{results/reports\_and\_plots/confusion\_matrices\_combined.png}
    \item \textbf{Trade-off Latencia vs Tamaño}: \texttt{results/reports\_and\_plots/benchmark\_latency\_tradeoff.png}
\end{itemize}
"""

with open(os.path.join(SEC_DIR, "resultados.tex"), "w", encoding="utf-8") as f:
    f.write(tex_resultados)

# ------------------------------------------------------------------------------
# 4. anexos.tex
# ------------------------------------------------------------------------------
tex_anexos = r"""\section{ANEXOS Y LISTADO DE CÓDIGO FUENTE}

\subsection{Anexo A: Definición PyTorch de la Arquitectura VAE-MLP}
\begin{lstlisting}[language=Python, caption={Definición del VAE-MLP en PyTorch}]
import torch
import torch.nn as nn

class VAE_MLP(nn.Module):
    def __init__(self, input_dim=39, latent_dim=16, num_classes=8):
        super().__init__()
        # Encoder
        self.enc_fc1 = nn.Linear(input_dim, 64)
        self.enc_fc2 = nn.Linear(64, 32)
        self.fc_mu = nn.Linear(32, latent_dim)
        self.fc_logvar = nn.Linear(32, latent_dim)
        
        # Decoder
        self.dec_fc1 = nn.Linear(latent_dim, 32)
        self.dec_fc2 = nn.Linear(32, 64)
        self.dec_out = nn.Linear(64, input_dim)
        
        # Classifier
        self.cls_head = nn.Sequential(
            nn.Linear(latent_dim, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.20),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, num_classes)
        )

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x):
        h = torch.relu(self.enc_fc1(x))
        h = torch.relu(self.enc_fc2(h))
        mu, logvar = self.fc_mu(h), self.fc_logvar(h)
        z = self.reparameterize(mu, logvar)
        
        dh = torch.relu(self.dec_fc1(z))
        dh = torch.relu(self.dec_fc2(dh))
        recon_x = torch.sigmoid(self.dec_out(dh))
        
        logits = self.cls_head(z)
        return recon_x, mu, logvar, logits, z
\end{lstlisting}

\subsection{Anexo B: Cuadernos de Jupyter Compilados (Notebooks)}
Los 5 cuadernos de Jupyter correspondientes a las 5 fases del proyecto han sido ejecutados y validados:
\begin{enumerate}
    \item \texttt{notebooks/01\_EDA\_Preprocessing\_and\_Feature\_Selection.ipynb}
    \item \texttt{notebooks/02\_Model\_Architecture\_and\_Design.ipynb}
    \item \texttt{notebooks/03\_Training\_Quantization\_and\_XAI.ipynb}
    \item \texttt{notebooks/04\_Model\_Evaluation\_and\_Error\_Analysis.ipynb}
    \item \texttt{notebooks/05\_State\_of\_the\_Art\_Comparison\_and\_Efficacy.ipynb}
\end{enumerate}
"""

with open(os.path.join(SEC_DIR, "anexos.tex"), "w", encoding="utf-8") as f:
    f.write(tex_anexos)

print("[✔] Todas las secciones de LaTeX han sido completamente actualizadas para EdgeGuard-IoT.")
