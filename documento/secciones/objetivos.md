# Objetivos de Investigación

## Detección de Botnets mediante Redes Neuronales de Grafos: Análisis de Dependencias Relacionales y Espaciales en Tráfico de Red


## Objetivo General

Analizar las dependencias relacionales y espaciales en el tráfico de red mediante Redes Neuronales de Grafos (GNN) para la detección temprana y precisa de botnets, integrando arquitecturas heterogéneas, mecanismos de atención y aprendizaje auto-supervisado que permitan superar las limitaciones de escalabilidad, desequilibrio de clases y robustez adversaria identificadas en los enfoques tradicionales.


## Objetivos Específicos

### Objetivo Específico 1

Caracterizar las dependencias relacionales entre dispositivos y dominios en el tráfico de red mediante la construcción de un grafo heterogéneo que represente las múltiples tipologías de nodos (hosts, direcciones IP, puertos, dominios) y aristas (conexiones TCP, flujos UDP, consultas DNS), aplicando métricas de centralidad topológica para la identificación de patrones estructurales de botnets centralizadas y descentralizadas (P2P).

### Objetivo Específico 2

Diseñar un modelo de Red Neuronal de Grafos Espacio-Temporal (ST-GNN) que integre mecanismos de atención y aprendizaje contrastivo auto-supervisado para capturar tanto las dependencias espaciales (topología de comunicaciones) como las dependencias temporales (evolución de los patrones de tráfico en el tiempo) en la detección de comportamientos maliciosos, mitigando el sobre-suavizado y el desequilibrio de clases mediante técnicas de muestreo y pérdida focal.

### Objetivo Específico 3

Evaluar el rendimiento del modelo propuesto mediante un marco de validación inductivo y causal que respete el orden temporal de los datos, comparando sus métricas de precisión, recall y F1-score con los enfoques tradicionales (GCN, GraphSAGE, GAT) y con los modelos de vanguardia identificados (HeteroSAGE, BHGCN, DGAN), así como analizar su robustez ante ataques adversariales estructurales y su explicabilidad mediante técnicas de IA explicable (XAI) como GNNExplainer.