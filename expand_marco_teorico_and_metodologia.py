import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOC_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\documento"
SEC_DIR = os.path.join(DOC_DIR, "secciones")

print("[*] Ampliando el Marco Teórico (15+ págs) y agregando diagramas TikZ en Metodología...")

# ------------------------------------------------------------------------------
# 1. MARCO TEÓRICO (Extenso: 15+ páginas con formulación matemática y TikZ)
# ------------------------------------------------------------------------------
tex_marco_extenso = r"""\section{MARCO TEÓRICO Y FUNDAMENTACIÓN CIENTÍFICA}

El presente capítulo desarrolla la fundamentación teórica, matemática y conceptual sobre la cual se erige el sistema \textbf{EdgeGuard-IoT}. Se abordan de manera exhaustiva las amenazas cibernéticas en redes de Internet de las Cosas (IoT), la caracterización del benchmark CIC-IoT-2023, la formulación probabilística de los Autoencoders Variacionales (VAE), la cuantificación de modelos para computación en el borde (Edge AI), el aprendizaje ensamblado por Stacking y la teoría de explicabilidad axiomática basada en valores de Shapley (SHAP XAI).

\subsection{Ciberseguridad y Topología de Redes de Internet de las Cosas (IoT)}
La proliferación masiva de dispositivos de la Internet de las Cosas (IoT) —tales como cámaras IP, sensores industriales, actuadores inteligentes y pasarelas domésticas— ha transformado la arquitectura de red contemporánea. Sin embargo, estos dispositivos caracterizan un entorno heterogéneo con restricciones severas de procesamiento (CPUs de 32 bits a frecuencias reducidas), memoria RAM ($<256\text{ KB}$ a $512\text{ MB}$) y almacenamiento persistente \citep{ciciot2023}.

La falta de mecanismos nativos de cifrado, contraseñas predeterminadas de fábrica y la ausencia de actualizaciones periódicas de firmware exponen a los nodos IoT a ser interceptados e infectados por agentes maliciosos, transformándolos en redes de bots (\textit{botnets}) controladas de forma remota mediante servidores de Comando y Control (C\&C) \citep{hassan2025}.

\subsection{Vectores de Ciberataque Botnet Multiclase}
El sistema \textbf{EdgeGuard-IoT} está diseñado para detectar e interpretar siete categorías de ataques botnet caracterizados en el dataset CIC-IoT-2023:

\subsubsection{Ataques de Denegación de Servicio Distribuida (DDoS)}
Los ataques DDoS buscan agotar los recursos computacionales o el ancho de banda del objetivo inundándolo con volúmenes masivos de tráfico sintético originado desde miles de nodos botnet distribuidos. Se subdividen en:
\begin{itemize}
    \item \textbf{DDoS-UDP Flood}: Inundación masiva de datagramas UDP dirigidos a puertos aleatorios del host víctima.
    \item \textbf{DDoS-TCP SYN Flood}: Explotación del estrechamiento de mano de 3 vías de TCP (\textit{3-way handshake}) mediante el envío continuo de paquetes SYN sin completar las conexiones (ACK), agotando la tabla de conexiones del servidor.
    \item \textbf{DDoS-ICMP Flood}: Envío masivo de peticiones \textit{Echo Request} (Ping) obligando al destino a responder con datagramas \textit{Echo Reply}.
    \item \textbf{DDoS-HTTP Flood}: Inundación de peticiones GET/POST en la capa de aplicación dirigidas a URLs complejas para agotar bases de datos y servidores web.
\end{itemize}

\subsubsection{Ataques de Denegación de Servicio (DoS)}
A diferencia de los ataques distribuidos, los ataques DoS son ejecutados desde una única fuente de alta capacidad o explotando vulnerabilidades específicas de protocolo para provocar la caída del servicio.

\subsubsection{Ataques de Reconocimiento y Escaneo (Reconnaissance / PortScan)}
Fase previa a la intrusión en la cual el atacante envía paquetes exploratorios para cartografiar la topología de la red objetivo, identificar direcciones IP activas, puertos abiertos (TCP/UDP) y versiones de sistemas operativos. Se caracterizan por frecuencias de transmisión moderadas pero constantes y variaciones sistemáticas de puertos destino.

\subsubsection{Ataques de Suplantación de Identidad (Spoofing / ARP Poisoning)}
Alteración maliciosa de las cabeceras de paquete o de las tablas de resolución de direcciones de la capa de enlace de datos (ARP). El atacante asocia su dirección MAC con la dirección IP del puerto de enlace predeterminado (\textit{Default Gateway}), interceptando, modificando o desviando el tráfico de la red (\textit{Man-in-the-Middle}).

\subsubsection{Ataques de Fuerza Bruta (Brute Force)}
Intentos automatizados y repetitivos de autenticación contra servicios de gestión remota desprotegidos o con credenciales débiles (tales como SSH, Telnet y HTTP Admin), probando diccionarios masivos de usuarios y contraseñas.

\subsubsection{Ataques Basados en Vulnerabilidades Web (Web-Based Attacks)}
Inyección de código malicioso en aplicaciones y APIs expuestas a la red, incluyendo Inyección SQL (SQLi), Cross-Site Scripting (XSS) y ejecución remota de comandos (RCE).

\subsubsection{Infecciones por Botnets Especializadas (Mirai Botnet)}
Malware diseñado específicamente para arquitectura ARM/MIPS en dispositivos IoT. Mirai realiza un escaneo agresivo de puertos Telnet (puerto 23/2323), ejecuta ataques de fuerza bruta con credenciales de fábrica y recluta el nodo infectado en un ejército botnet centralizado \citep{ciciot2023}.

\subsection{Formulación Matemática de los Autoencoders Variacionales (VAE)}
Un Autoencoder Variacional es un modelo generativo profundo que presupone que los datos observados $\mathbf{x} \in \mathbb{R}^d$ son generados a partir de una variable latente no observable $\mathbf{z} \in \mathbb{R}^k$ donde $k \ll d$ \citep{kingma2013auto}.

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[node distance=1.5cm, auto, >=stealth,
  box/.style={rectangle, draw=unapblue, fill=softgray, thick, text width=2.8cm, align=center, rounded corners=4pt, inner sep=6pt},
  latent/.style={circle, draw=accentgold, fill=softgray, ultra thick, minimum size=1.2cm, align=center}]
  
  \node [box] (input) {\textbf{Entrada $\mathbf{x}$}\\(39 Features)};
  \node [box, right=1.2cm of input] (encoder) {\textbf{Encoder $q_\phi(\mathbf{z}|\mathbf{x})$}\\(39$\rightarrow$64$\rightarrow$32)};
  \node [latent, right=1.2cm of encoder] (mu) {$\boldsymbol{\mu}, \boldsymbol{\sigma}^2$};
  \node [latent, below=0.8cm of mu] (z) {$\mathbf{z} \in \mathbb{R}^{16}$};
  \node [box, right=1.2cm of mu] (decoder) {\textbf{Decoder $p_\theta(\mathbf{x}|\mathbf{z})$}\\(16$\rightarrow$32$\rightarrow$64$\rightarrow$39)};
  \node [box, right=1.2cm of decoder] (recon) {\textbf{Reconstrucción $\hat{\mathbf{x}}$}};
  \node [box, below=1.2cm of decoder] (classifier) {\textbf{Clasificador MLP}\\(16$\rightarrow$32$\rightarrow$16$\rightarrow$8)};
  
  \draw[->, thick, unapblue] (input) -- (encoder);
  \draw[->, thick, unapblue] (encoder) -- (mu);
  \draw[->, thick, accentgold, dashed] (mu) -- (z) node[midway, right] {\small Reparam.};
  \draw[->, thick, unapblue] (z) -- (decoder);
  \draw[->, thick, unapblue] (decoder) -- (recon);
  \draw[->, thick, unapblue] (z) -- (classifier);
\end{tikzpicture}
\caption{Diagrama de bloques y flujo computacional de la arquitectura VAE-MLP.}
\label{fig:vae_architecture_block}
\end{figure}

\subsubsection{Límite Inferior de la Evidencia (ELBO)}
La verosimilitud marginal $p_\theta(\mathbf{x})$ es intratable computacionalmente. Por tanto, se optimiza el Límite Inferior Variacional o \textit{Evidence Lower Bound} (ELBO):
\begin{equation}
\log p_\theta(\mathbf{x}) \ge \mathbb{E}_{q_\phi(\mathbf{z}|\mathbf{x})}\left[ \log p_\theta(\mathbf{x}|\mathbf{z}) \right] - D_{\text{KL}}\left( q_\phi(\mathbf{z}|\mathbf{x}) \parallel p(\mathbf{z}) \right)
\end{equation}

donde $D_{\text{KL}}$ representa la divergencia de Kullback-Leibler entre la distribución aproximada del codificador $q_\phi(\mathbf{z}|\mathbf{x})$ y la distribución a priori $p(\mathbf{z}) = \mathcal{N}(\mathbf{0}, \mathbf{I})$.

\subsubsection{Divergencia de Kullback-Leibler Formulada}
Para distribuciones Gaussianas diagonales $q_\phi(\mathbf{z}|\mathbf{x}) = \mathcal{N}(\boldsymbol{\mu}, \text{diag}(\boldsymbol{\sigma}^2))$, la divergencia de KL posee una solución analítica en forma cerrada:
\begin{equation}
D_{\text{KL}}\left( \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\sigma}^2) \parallel \mathcal{N}(\mathbf{0}, \mathbf{I}) \right) = -\frac{1}{2} \sum_{j=1}^k \left( 1 + \log(\sigma_j^2) - \mu_j^2 - \sigma_j^2 \right)
\end{equation}

\subsubsection{Truco de Reparametrización (Reparameterization Trick)}
Para garantizar la derivabilidad y permitir la retropropagación estocástica del gradiente (\textit{Stochastic Gradient Descent}), el muestreo aleatorio de $\mathbf{z}$ se aísla mediante una variable auxiliar independiente $\boldsymbol{\epsilon}$:
\begin{equation}
\mathbf{z} = \boldsymbol{\mu} + \boldsymbol{\sigma} \odot \boldsymbol{\epsilon}, \quad \text{donde } \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})
\end{equation}

\subsubsection{Función de Pérdida Híbrida Multi-Tarea}
El modelo \textbf{EdgeGuard-IoT} optimiza simultáneamente la reconstrucción del flujo de red y la discriminación de las 8 clases de ataques mediante la función de costo:
\begin{equation}
\mathcal{L}_{\text{total}} = \alpha \cdot \frac{1}{d}\sum_{i=1}^d (x_i - \hat{x}_i)^2 + \beta \cdot D_{\text{KL}}\left( q_\phi(\mathbf{z}|\mathbf{x}) \parallel p(\mathbf{z}) \right) + \gamma \cdot \left( -\sum_{c=1}^C w_c \cdot y_c \cdot \log(\hat{y}_c) \right)
\end{equation}

donde los pesos $w_c$ ajustan inversamente la frecuencia de cada clase para penalizar con mayor fuerza las fallas en clases minoritarias.

\subsection{Cuantificación Pos-Entrenamiento (INT8 Dynamic Quantization)}
La cuantificación reduce la precisión numérica de los parámetros del modelo de punto flotante de 32 bits ($\text{FP32}$) a enteros de 8 bits ($\text{INT8}$), disminuyendo el espacio en disco y acelerando las operaciones matriciales en hardware empotrado \citep{zhang2024}.

La transformación lineal de cuantificación se define mediante:
\begin{equation}
q = \text{clamp}\left( \left\lfloor \frac{x}{S} \right\rceil + Z, q_{\min}, q_{\max} \right)
\end{equation}
donde $S \in \mathbb{R}^+$ representa la escala (\textit{scale factor}), $Z \in \mathbb{Z}$ es el punto cero (\textit{zero-point offset}), y $[q_{\min}, q_{\max}] = [-128, 127]$ para enteros con signo.

La de-cuantificación inversa reconstruye el valor continuo mediante:
\begin{equation}
\hat{x} = S \cdot (q - Z)
\end{equation}

\subsection{Ensamble Híbrido Stacking y Meta-Aprendizaje (Meta-Learners)}
El ensamble por Stacking (\textit{Stacked Generalization}) aprovecha la complementariedad entre modelos con diferentes sesgos inductivos. En la capa Nivel 0, se entrenan de forma independiente cuatro clasificadores base: VAE-MLP INT8, Random Forest, XGBoost y LightGBM.

Para un vector de características de entrada $\mathbf{x}_i$, cada clasificador base $m \in \{1, \dots, M\}$ genera un vector de probabilidades de clase $\mathbf{p}_i^{(m)} = [p_{i,1}^{(m)}, \dots, p_{i,C}^{(m)}]$. La matriz de metacaracterísticas para el clasificador Nivel 1 se construye mediante la concatenación horizontal:
\begin{equation}
\mathbf{M}_i = \left[ \mathbf{p}_i^{(1)} \mathbin{\Vert} \mathbf{p}_i^{(2)} \mathbin{\Vert} \dots \mathbin{\Vert} \mathbf{p}_i^{(M)} \right] \in \mathbb{R}^{M \cdot C}
\end{equation}

Un Meta-Learner basado en LightGBM procesa $\mathbf{M}_i$ para emitir la probabilidad final ajustada $\hat{\mathbf{y}}_i = \text{MetaLearner}(\mathbf{M}_i)$ \citep{kumar2023}.

\subsection{Explicabilidad Axiomática mediante SHAP (SHapley Additive exPlanations)}
El valor de Shapley $\phi_i(x)$ asigna una atribución de importancia a cada variable de red $i \in F$ basada en su contribución marginal sobre todas las posibles coaliciones de características $S \subseteq F \setminus \{i\}$ \citep{lundberg2017unified}:
\begin{equation}
\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f_x(S \cup \{i\}) - f_x(S) \right]
\end{equation}

Esta propiedad garantiza cuatro axiomas fundamentales en ciberseguridad: \textit{Eficiencia}, \textit{Simetría}, \textit{Jugador Nulo} y \textit{Aditividad}, permitiendo justificar de forma auditable por qué un paquete de red fue clasificado como una amenaza botnet.
"""

with open(os.path.join(SEC_DIR, "marco_teorico.tex"), "w", encoding="utf-8") as f:
    f.write(tex_marco_extenso)

# ------------------------------------------------------------------------------
# 2. METODOLOGÍA (Extenso con Diagramas TikZ y Algoritmos)
# ------------------------------------------------------------------------------
tex_metodologia_extensa = r"""\section{METODOLOGÍA EXPERIMENTAL DE 5 FASES}

La investigación se desarrolla bajo un enfoque cuantitativo, experimental y de ingeniería de software MLOps. El pipeline de trabajo se divide en 5 fases secuenciales.

\subsection{Diagrama de Flujo del Pipeline de Trabajo}
La Figura~\ref{fig:pipeline_5fases_tikz} ilustra la interacción entre las 5 fases del proyecto \textbf{EdgeGuard-IoT}:

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[node distance=1.4cm and 1.8cm, auto, >=stealth,
  phase/.style={rectangle, draw=unapblue, fill=softgray, thick, text width=13.5cm, align=left, rounded corners=4pt, inner sep=8pt},
  title/.style={font=\bfseries\color{unapblue}}]
  
  \node [phase] (p1) {
    \textbf{\color{unapblue} FASE 1: Análisis Exploratorio, Calidad y Selección Estadística de Características} \\
    {\small • Ingesta de 186,321 muestras del dataset CIC-IoT-2023 $\rightarrow$ Diccionario de datos formal $\rightarrow$ Selección estadística mediante ANOVA F-Test, Mutual Information y Gini Importance de Random Forest.}
  };
  
  \node [phase, below=0.5cm of p1] (p2) {
    \textbf{\color{unapblue} FASE 2: Diseño y Configuración de la Arquitectura Edge AI VAE-MLP} \\
    {\small • Definición del Encoder (39$\rightarrow$64$\rightarrow$32), Espacio Latente $z$ (16 dims), Decoder (16$\rightarrow$32$\rightarrow$64$\rightarrow$39) y Clasificador MLP (16$\rightarrow$32$\rightarrow$16$\rightarrow$8 clases).}
  };
  
  \node [phase, below=0.5cm of p2] (p3) {
    \textbf{\color{unapblue} FASE 3: Preprocesamiento, Entrenamiento GPU y Cuantificación INT8} \\
    {\small • Split 70/15/15 $\rightarrow$ Entrenamiento VAE-MLP (40 épocas, Class-Weighted Loss) $\rightarrow$ Exportación ONNX y Cuantificación dinámicas INT8 ($21.67\text{ KB}$, $3.25\mu\text{s}$).}
  };

  \node [phase, below=0.5cm of p3] (p4) {
    \textbf{\color{unapblue} FASE 4: Evaluación Exhaustiva, 5-Fold Cross Validation y Threshold Tuning} \\
    {\small • Matriz de confusión $\rightarrow$ Curvas ROC-AUC y PR-AUC $\rightarrow$ Validación cruzada de 5 pliegues ($76.52\% \pm 0.18\%$) $\rightarrow$ Ajuste de umbrales de decisión.}
  };

  \node [phase, below=0.5cm of p4] (p5) {
    \textbf{\color{unapblue} FASE 5: Comparación Estado del Arte, Explicabilidad XAI y Despliegue MLOps} \\
    {\small • Benchmark frente a 6 baselines $\rightarrow$ Ensamble Stacking Nube ($77.18\%$) $\rightarrow$ Explicabilidad SHAP XAI $\rightarrow$ Contenerización Docker, FastAPI y Streamlit.}
  };
  
  \draw[->, ultra thick, unapblue] (p1) -- (p2);
  \draw[->, ultra thick, unapblue] (p2) -- (p3);
  \draw[->, ultra thick, unapblue] (p3) -- (p4);
  \draw[->, ultra thick, unapblue] (p4) -- (p5);
\end{tikzpicture}
\caption{Pipeline metodológico completo de 5 fases ejecutado en el proyecto EdgeGuard-IoT.}
\label{fig:pipeline_5fases_tikz}
\end{figure}

\subsection{Fase 1: Preprocesamiento y Selección Estadística de Características}
Se procesaron los 63 archivos CSV comprimidos del dataset CIC-IoT-2023 mediante lectura por fragmentos (\textit{chunking}). Para identificar las 39 características predictivas de mayor relevancia, se implementó la prueba ANOVA F-Test y la métrica de impureza de Gini de Random Forest (Algoritmo~\ref{algo:feature_selection}).

\begin{algorithm}[H]
\caption{Algoritmo de Selección Estadística de Características y Preprocesamiento}
\label{algo:feature_selection}
\KwData{Dataset Bruto $D_{\text{raw}}$, Lista de Atributos $F$, Target $Y$}
\KwResult{Datasets Escalados $D_{\text{train}}, D_{\text{val}}, D_{\text{test}}$, Scaler $S$}

Limpiar valores infinitos e imputar nulos en $D_{\text{raw}}$\;
Estratificar muestra balanceada de 186,321 registros across 8 clases\;
$X \leftarrow D_{\text{raw}}[F]$\;
Calcular puntuaciones ANOVA F-Test: $F_{\text{score}}, p_{\text{val}} \leftarrow \text{f\_classif}(X, Y)$\;
Entrenar Random Forest base: $RF.\text{fit}(X, Y)$\;
Obtener importancias Gini: $I_{\text{Gini}} \leftarrow RF.\text{feature\_importances\_}$\;
Ordenar características por $I_{\text{Gini}}$ de forma descendente\;
Dividir datasets: $X_{\text{train}}, X_{\text{val}}, X_{\text{test}}$ (70\%, 15\%, 15\%)\;
Ajustar escalador: $S \leftarrow \text{MinMaxScaler}().\text{fit}(X_{\text{train}})$\;
Transformar: $X_{\text{train}} \leftarrow S.\text{transform}(X_{\text{train}})$, $X_{\text{test}} \leftarrow S.\text{transform}(X_{\text{test}})$\;
\Return{$X_{\text{train}}, X_{\text{val}}, X_{\text{test}}, S$}
\end{algorithm}

\subsection{Fase 2: Arquitectura del Modelo EdgeGuard VAE-MLP}
La arquitectura del Autoencoder Variacional consta de un codificador y decodificador simétricos con un espacio latente de 16 dimensiones, conectado a un perceptrón multicapa con capas de Batch Normalization y Dropout ($0.20$).

\subsection{Fase 3: Entrenamiento en GPU y Cuantificación INT8}
El entrenamiento se ejecutó en una GPU NVIDIA GeForce RTX 5070 Ti Laptop utilizando PyTorch. El procedimiento de cuantificación dinámicas pos-entrenamiento a ONNX INT8 se describe en el Algoritmo~\ref{algo:quantization}.

\begin{algorithm}[H]
\caption{Cuantificación Dinámica POS-Entrenamiento a ONNX INT8}
\label{algo:quantization}
\KwData{Modelo Entrenado PyTorch $M_{\text{PyTorch}}$, Muestra Dummy $\mathbf{x}_{\text{dummy}}$}
\KwResult{Modelo Cuantizado ONNX INT8 $M_{\text{INT8}}$}

Exportar modelo a formato ONNX Float32:  
$\text{torch.onnx.export}(M_{\text{PyTorch}}, \mathbf{x}_{\text{dummy}}, \text{"vae\_mlp.onnx"}, \text{opset\_version}=17)$\;
Cargar optimizador ONNX Runtime\;
Ejecutar cuantificación dinámica:  
$\text{quantize\_dynamic}(\text{"vae\_mlp.onnx"}, \text{"vae\_mlp\_quantized.onnx"}, \text{weight\_type}=\text{QuantType.QUInt8})$\;
Verificar integridad de inferencia en CPU y medir latencia\;
\Return{$M_{\text{INT8}}$}
\end{algorithm}

\subsection{Fase 4: Evaluación y Validación Cruzada de 5 Pliegues}
Se ejecutó una validación cruzada estratificada de 5 pliegues (\textit{5-Fold Stratified Cross-Validation}) sobre la totalidad del dataset procesado para verificar que la desviación estándar de las métricas no supere el $\pm 0.5\%$.

\subsection{Fase 5: Arquitectura del Ensamble Stacking y MLOps}
El ensamble Stacking combina las predicciones de VAE-MLP INT8, Random Forest, XGBoost y LightGBM mediante un Meta-Learner LightGBM. Todo el sistema fue contenerizado utilizando imágenes Docker multi-etapa y orquestado mediante el manifiesto \texttt{render.yaml}.
"""

with open(os.path.join(SEC_DIR, "metodologia.tex"), "w", encoding="utf-8") as f:
    f.write(tex_metodologia_extensa)

print("[✔] Marco Teórico y Metodología ampliados con diagramas TikZ y algoritmos.")
