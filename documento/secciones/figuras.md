# Puntos Específicos para Diagramas, Pseudocódigo y Elementos Visuales

## Marco Teórico: Detección de Botnets mediante Redes Neuronales de Grafos

A continuación, se detallan los puntos específicos del marco teórico donde se recomienda incorporar elementos visuales (diagramas de arquitectura, flujos de proceso, esquemas de datos), pseudocódigo o tablas formales para facilitar la comprensión y la representación gráfica de los conceptos. Estos puntos han sido identificados estratégicamente en función de la complejidad matemática, la necesidad de mostrar flujos de datos o la comparación estructural entre enfoques.

---

## Sección 2: Fundamentos Teóricos de la Representación Grafos

**2.1 Teoría de Grafos: Definiciones y Formalización**

- **Figura 1:** Representación gráfica de un grafo de tráfico de red.
  - *Descripción sugerida:* Grafo no dirigido/dirigido donde los nodos representan direcciones IP (hosts) y las aristas representan flujos de comunicación (NetFlow). Debe diferenciar visualmente nodos (con colores según tipo: servidor, cliente, dispositivo IoT) y aristas (con grosor según volumen de tráfico).

**2.2 Propiedades Estructurales y Medidas de Centralidad**

- **Tabla 1:** Resumen comparativo de las métricas de centralidad (Grado, Intermediación, PageRank, Cercanía).
  - *Descripción sugerida:* Tabla con columnas: Métrica, Fórmula resumida, Interpretación en ciberseguridad, Aplicación en detección de botnets (ej. identificación de C&C).

---

## Sección 3: Redes Neuronales de Grafos: Fundamentos Arquitectónicos

**3.1 Principios Fundamentales del Paso de Mensajes**

- **Pseudocódigo 1:** Algoritmo general de paso de mensajes en una GNN (Message Passing Neural Network).
  - *Descripción sugerida:* Pseudocódigo estructurado que muestre el bucle de capas (k = 1 a K) con las fases de **Agregación** (función AGGREGATE) y **Actualización** (función UPDATE), finalizando con la operación READOUT para nivel de grafo.

- **Figura 2:** Diagrama de flujo del mecanismo de paso de mensajes.
  - *Descripción sugerida:* Representación visual de un nodo central `v` recibiendo mensajes de sus vecinos `u1, u2, u3`. Flechas que muestran la agregación (suma/promedio) y la actualización (capa MLP) para generar el nuevo embedding `h_v^{(k)}`.

**3.3 Tipologías Arquitectónicas de GNN**

- **Figura 3:** Comparativa arquitectónica de GCN, GAT y GraphSAGE.
  - *Descripción sugerida:* Tres diagramas de bloques paralelos mostrando cómo cada modelo procesa el vecindario de un nodo. Para GCN (convolución espectral con matriz laplaciana), para GAT (mecanismo de atención con pesos alpha), para GraphSAGE (muestreo aleatorio de vecinos y agregación).

**3.4 El Fenómeno del Sobre-suavizado (Over-smoothing)**

- **Figura 4:** Visualización del efecto de sobre-suavizado en embeddings de nodos.
  - *Descripción sugerida:* Gráfico de proyección en 2D (t-SNE o UMAP) de los embeddings nodales en tres momentos: capa inicial (separados por clases), capas intermedias (mezcla parcial) y capas profundas (colapso total a un solo cluster indistinguible).

- **Figura 5:** Esquema de estrategias de mitigación.
  - *Descripción sugerida:* Diagrama de bloques comparativo mostrando (a) Conexiones residuales (salto de capa), (b) Jumping-Knowledge (concatenación de todas las capas intermedias) y (c) Compuertas jerárquicas (TopGateGNN).

---

## Sección 4: Arquitecturas Centradas en Aristas: E-GraphSAGE

**4.1 Incompatibilidad Estructural de las GNN Estándar**

- **Figura 6:** Comparación entre una GNN estándar y E-GraphSAGE.
  - *Descripción sugerida:* Dos columnas. Izquierda: GNN estándar con nodos que tienen características ricas, aristas sin características. Derecha: E-GraphSAGE con nodos sin características (o vectores de unos) y aristas con vectores densos de características de flujo (duración, bytes, flags).

**4.2 Formalización Matemática de E-GraphSAGE**

- **Pseudocódigo 2:** Función de mensaje con características de arista en E-GraphSAGE.
  - *Descripción sugerida:* Pseudocódigo que toma como entrada los embeddings del nodo origen, del nodo destino y el vector de características de la arista (flujo), los concatena y los pasa por un MLP para generar el mensaje `m_{u->v}^{(k)}`.

**4.4 Construcción de Grafos de Flujo mediante k-NN**

- **Figura 7:** Proceso de construcción de grafo de flujos por similitud k-NN.
  - *Descripción sugerida:* Diagrama de flujo que parte de registros NetFlow individuales, extrae sus vectores de características, calcula la matriz de distancias (ej. Euclidiana) y conecta cada flujo con sus k vecinos más cercanos para formar un grafo donde los nodos son flujos y las aristas representan similitud comportamental.

---

## Sección 5: Redes Neuronales de Grafos Heterogéneos (HGNN)

**5.2 Definición Formal de Grafos Heterogéneos**

- **Figura 8:** Modelado de un grafo heterogéneo de tráfico de red.
  - *Descripción sugerida:* Grafo con diferentes formas geométricas para los nodos (círculos para IPs, rectángulos para dominios, triángulos para puertos). Diferentes estilos de línea para aristas (línea continua para TCP, discontinua para UDP, punteada para DNS). Incluir leyenda de tipos.

**5.3 Mecanismos de Agregación Sensibles al Tipo**

- **Figura 9:** Esquema de agregación en HGNN (paso de mensajes con proyecciones específicas por tipo).
  - *Descripción sugerida:* Diagrama que muestra cómo un nodo de tipo "IP" recibe mensajes de un vecino "Dominio" a través de una arista "DNS", y cómo la proyección `W_{IP}` y `W_{Dominio}` transforman los embeddings antes de la agregación.

---

## Sección 6: Dinámica Temporal: Redes Neuronales de Grafos Espacio-Temporales (ST-GNN)

**6.2 Modelado de Tiempo Discreto: Ventanas Deslizantes**

- **Figura 10:** Representación de secuencia de instantáneas temporales (ventanas deslizantes).
  - *Descripción sugerida:* Línea de tiempo continua `[0, T]` dividida en ventanas `Δt`. Cada ventana genera un grafo `G^{(1)}`, `G^{(2)}`, ..., `G^{(L)}`. Flechas que indican la alimentación de los embeddings espaciales al módulo Transformer temporal.

**6.3 Modelado de Tiempo Continuo**

- **Figura 11:** Diagrama de eventos asíncronos en un grafo temporal (TGN).
  - *Descripción sugerida:* Eje Y con nodos (A, B, C), eje X con tiempo. Eventos representados como puntos o líneas que conectan nodos en momentos específicos (`t1`, `t2`, `t3`). Mostrar el mecanismo de memoria que actualiza el estado del nodo en cada evento.

---

## Sección 7: Aprendizaje Auto-Supervisado (SSL) para Detección de Botnets

**7.2 Aprendizaje Contrastivo en Grafos**

- **Figura 12:** Esquema del aprendizaje contrastivo en grafos (vistas aumentadas).
  - *Descripción sugerida:* Un grafo original `G` del cual se generan dos vistas aumentadas `G1` (con enmascaramiento de nodos) y `G2` (con perturbación de aristas). Ambas vistas pasan por un codificador GNN compartido, generando embeddings `z1` y `z2`. Diagrama de la función de pérdida contrastiva (InfoNCE) que maximiza similitud entre `z1` y `z2`, y minimiza con otros grafos del batch.

**7.3 Aumento de Datos en el Espacio Gráfico**

- **Figura 13:** Ejemplos visuales de técnicas de aumento de datos en grafos.
  - *Descripción sugerida:* Cuatro paneles mostrando el grafo original y los efectos de: (a) Enmascaramiento de características de nodos (nodos atenuados), (b) Perturbación de aristas (añadir/eliminar líneas), (c) Enmascaramiento de aristas (líneas punteadas), (d) Submuestreo de nodos (nodos eliminados).

---

## Sección 8: Inteligencia Artificial Explicable (XAI) para GNN

**8.2 Explicadores Post-hoc**

- **Figura 14:** Proceso de extracción de subgrafo explicativo con GNNExplainer.
  - *Descripción sugerida:* Un grafo completo de entrada con nodos de colores (bot/benigno). Una máscara de atención que selecciona un subconjunto de nodos y aristas (resaltados en color cálido) que son responsables de la predicción (ej. un nodo bot conectado a un C&C). El subgrafo explicativo extraído al lado.

**8.3 Arquitecturas Auto-Interpretables**

- **Figura 15:** Arquitectura de XG-BoT (conexiones residuales reversibles y mapas de prominencia).
  - *Descripción sugerida:* Diagrama de bloques del modelo XG-BoT mostrando la entrada del grafo, las capas GIN reversibles, la generación de mapas de prominencia (saliency maps) y la salida de clasificación junto con la ruta de auditoría forense (flujos y agentes intermedios).

---

## Sección 9: Vulnerabilidades Ante Ataques Adversarios

**9.2 Taxonomía de Ataques Adversarios en GNN**

- **Figura 16:** Ejemplo de ataque de inyección de aristas (Edge Injection).
  - *Descripción sugerida:* Grafo original con un nodo bot (rojo) conectado a su C&C. Se superponen flechas punteadas que representan aristas inyectadas (hacia servidores legítimos como AWS o Google) para distorsionar la centralidad del nodo bot y enmascararlo como benigno.

**9.3 BOCLOAK: Transporte Óptimo para Ataques Adversarios**

- **Figura 17:** Esquema conceptual de transporte óptimo aplicado a ataques.
  - *Descripción sugerida:* Dos distribuciones de embeddings: `μ_B` (clase bot) y `μ_H` (clase benigna). Flechas que representan el transporte óptimo `P` que transforma la distribución bot en la distribución benigna, con un costo mínimo. El costo está asociado a la manipulación de aristas.

---

## Sección 10: Desafíos de Escalabilidad y Despliegue

**10.2 Estrategias de Escalabilidad**

- **Figura 18:** Arquitectura de colaboración Cloud-Edge para inferencia.
  - *Descripción sugerida:* Diagrama de despliegue con dispositivos IoT (sensores, routers) en el borde que ejecutan módulos de inferencia rápida (apátridas). Flechas que envían gradientes o actualizaciones de modelo a la nube, donde se realiza el entrenamiento intensivo. Mostrar los ahorros operativos (52% tiempo, 71% energía) con anotaciones.

- **Pseudocódigo 3:** Algoritmo de poda dinámica de aristas (Dynamic Edge Pruning) con atención multi-cabeza.
  - *Descripción sugerida:* Pseudocódigo que calcula los pesos de atención para cada arista, filtra aquellas con peso por debajo de un umbral, y reconstruye el grafo reducido para la siguiente capa.

---

## Sección 12: Modelo Teórico Propuesto

**12.3 Arquitectura Formal del Modelo**

- **Figura 19:** Arquitectura completa del modelo propuesto HST-GNN-SSL.
  - *Descripción sugerida:* Diagrama de bloques modular. Entrada: Grafo heterogéneo y secuencia temporal.
    - **Módulo 1:** Codificador Heterogéneo (capas HeteroConv).
    - **Módulo 2:** Codificador Temporal (Transformer o LSTM procesando secuencia de embeddings).
    - **Módulo 3:** Cabezal Contrastivo SSL (generación de vistas aumentadas y cálculo de pérdida contrastiva).
    - **Módulo 4:** Clasificador (MLP para clasificación de nodos/aristas).
    - **Módulo 5:** Explicador (GNNExplainer integrado para generar subgrafos críticos).
  - *Nota:* Este es el punto central, el diagrama debe ser detallado y mostrar las conexiones entre módulos.

---

## Sección 13: De Definiciones Conceptuales a Variables Medibles

**13.1 Variables Independientes (Predictores)**

- **Tabla 2:** Matriz de variables independientes con especificaciones operacionales.
  - *Descripción sugerida:* Tabla formal con columnas: Variable, Definición Conceptual, Operacionalización (notación matemática), Fuente de Datos y Tipo de Dato. Incluir las filas: Estructura del grafo (`A`), Características de nodos (`x_v`), Características de aristas (`e_{uv}`), Temporalidad (`G^{(t)}`), Heterogeneidad (`φ`, `ψ`).

**13.2 Variable Dependiente (Respuesta)**

- **Tabla 3:** Matriz de variables dependientes.
  - *Descripción sugerida:* Tabla con columnas: Variable, Definición Conceptual, Operacionalización y Escala de Medición (Binaria para estado de infección y naturaleza del flujo).

---

## Resumen de Elementos Visuales Solicitados

| Tipo de Elemento | Ubicación (Sección) | Cantidad Sugerida |
| :--- | :--- | :--- |
| **Pseudocódigo** | 3.1, 4.2, 10.2 | 3 |
| **Diagrama de Arquitectura de Red/Modelo** | 3.3, 4.1, 5.3, 12.3 | 4 |
| **Diagrama de Flujo de Proceso/Datos** | 3.1, 4.4, 6.2, 7.2, 8.2 | 5 |
| **Esquema Conceptual / Visualización de Datos** | 2.1, 3.4, 5.2, 6.3, 7.3, 9.2, 9.3, 10.2 | 8 |
| **Tablas Comparativas o de Especificación** | 2.2, 13.1, 13.2 | 3 |

**Total de elementos visuales sugeridos:** 23 elementos (entre figuras, pseudocódigos y tablas) distribuidos estratégicamente para cubrir todos los pilares del marco teórico.
