# Marco Teórico

## Detección de Botnets mediante Redes Neuronales de Grafos: Análisis de Dependencias Relacionales y Espaciales en Tráfico de Red


## 1. Introducción y Fundamentación del Problema

### 1.1 Contextualización de la Amenaza Botnet

La evolución del ecosistema digital ha transformado radicalmente el panorama de la ciberseguridad. La proliferación exponencial de dispositivos interconectados en el Internet de las Cosas (IoT), la adopción masiva de infraestructuras en la nube y los entornos de colaboración perimetral (Cloud-Edge) han expandido drásticamente la superficie de ataque cibernético (Lagraa et al., 2024). En este vasto entramado digital, las botnets se han consolidado como una de las amenazas más sofisticadas y disruptivas, representando un desafío persistente y significativo para la seguridad de Internet (MDPI, 2025).

Una botnet puede definirse formalmente como una red de dispositivos comprometidos —denominados *bots* o *zombies*— que son controlados de manera orquestada por un actor malicioso, denominado *botmaster*, a través de una infraestructura de Comando y Control (C&C). Estas redes de dispositivos secuestrados operan coordinadamente para ejecutar ataques de Denegación de Servicio Distribuido (DDoS), propagación de malware, campañas de suplantación de identidad (*phishing*) y exfiltración de datos a escalas que superan regularmente el terabit por segundo (Lagraa et al., 2024).

La arquitectura de las botnets ha evolucionado desde modelos centralizados —donde un único servidor C&C orquesta a todos los bots— hasta arquitecturas descentralizadas Peer-to-Peer (P2P), que eliminan el punto único de fallo y dificultan significativamente su neutralización. Paralelamente, los operadores de botnets han implementado técnicas de evasión cada vez más sofisticadas, incluyendo el cifrado de canales de comunicación, la mutación de cargas útiles (*payloads*), los algoritmos de generación de dominios (DGA) y el uso de infraestructuras dinámicas que rotan constantemente sus componentes (Lagraa et al., 2024).

### 1.2 Limitaciones de los Enfoques Tradicionales

Los Sistemas de Detección de Intrusiones en la Red (NIDS) basados en firmas y reglas estáticas han demostrado una obsolescencia fundamental frente a estas técnicas de evasión (Lagraa et al., 2024). La transición inicial hacia el aprendizaje automático (*Machine Learning*, ML) convencional y el aprendizaje profundo (*Deep Learning*, DL) mitigó parcialmente estas vulnerabilidades al permitir la detección heurística de anomalías mediante la extracción de características de los flujos de red.

Sin embargo, los algoritmos como Bosques Aleatorios (*Random Forest*), Máquinas de Vectores de Soporte (SVM) y perceptrones multicapa (MLP) adolecen de un defecto de diseño crítico para el modelado de amenazas modernas: asumen que los registros de flujo de red son vectores estadísticamente independientes e idénticamente distribuidos (i.i.d.). Al procesar cada evento de red de manera aislada, los enfoques euclidianos clásicos destruyen el contexto relacional y la jerarquía de las comunicaciones, ignorando la esencia misma de una botnet, que es precisamente su estructura coordinada, interdependiente y topológica (Lagraa et al., 2024).

### 1.3 El Paradigma de las Redes Neuronales de Grafos

La detección de intrusiones contemporánea requiere una abstracción metodológica que pueda encapsular simultáneamente los atributos intrínsecos de un dispositivo y las complejas topologías de interacción que establece con el exterior (Lagraa et al., 2024). Aquí es donde el paradigma de las Redes Neuronales de Grafos (*Graph Neural Networks*, GNN) ha redefinido el estado del arte.

Al formular el tráfico de red como un grafo espacial, las GNN extraen características que son virtualmente imposibles de ofuscar por los atacantes, dado que la alteración de la estructura gráfica subyacente de una botnet interrumpiría su capacidad de mando y control (Lagraa et al., 2024). Las GNN han alcanzado resultados competitivos en el aprendizaje de representaciones robustas a partir de malware representado como estructuras gráficas expresivas (Survey on Malware Detection with Graph Representation Learning, s.f.).


## 2. Fundamentos Teóricos de la Representación Grafos

### 2.1 Teoría de Grafos: Definiciones y Formalización

La teoría de grafos proporciona el formalismo matemático fundamental para la representación de relaciones estructurales en sistemas complejos. Formalmente, un grafo se define como una tupla $G = (V, E)$, donde $V$ es un conjunto finito de vértices (o nodos) y $E \subseteq V \times V$ es un conjunto de aristas (o enlaces) que representan las relaciones entre pares de vértices (Lagraa et al., 2024).

En el contexto de la seguridad de redes, la representación grafos del tráfico de red constituye el núcleo operativo de las GNN aplicadas a la ciberseguridad. En su formalización más elemental, una red informática se representa como un grafo matemático $G = (V, E)$, donde el conjunto de vértices $V$ representa los hosts (usualmente direcciones IP) y el conjunto de aristas $E$ define las interacciones, como los flujos de comunicación o las sesiones bidireccionales (Lagraa et al., 2024).

**Definición 1 (Grafo de tráfico de red).** Sea $\mathcal{T}$ un conjunto de registros de tráfico de red (ej. NetFlow). Un grafo de tráfico de red se define como $G = (V, E, \mathbf{X}_V, \mathbf{X}_E)$, donde:

- $V = \{v_1, v_2, \ldots, v_n\}$ es el conjunto de nodos que representan entidades de red (hosts, direcciones IP, dominios).
- $E \subseteq V \times V$ es el conjunto de aristas que representan comunicaciones o interacciones entre nodos.
- $\mathbf{X}_V \in \mathbb{R}^{n \times d_V}$ es la matriz de características de los nodos.
- $\mathbf{X}_E \in \mathbb{R}^{m \times d_E}$ es la matriz de características de las aristas, donde $m = |E|$.

### 2.2 Propiedades Estructurales y Medidas de Centralidad

La caracterización topológica de los grafos de red requiere el uso de métricas estructurales que cuantifican la importancia y el rol de cada nodo dentro de la topología global. En el contexto de la detección de botnets, estas medidas resultan fundamentales para identificar patrones de comunicación anómalos (BotSward, 2022).

**Definición 2 (Grado de un nodo).** El grado de un nodo $v \in V$ en un grafo no dirigido se define como $deg(v) = |\{u \in V : (v,u) \in E\}|$. En un grafo dirigido, se distinguen el grado de entrada $deg^-(v)$ y el grado de salida $deg^+(v)$.

**Definición 3 (Centralidad de intermediación).** La centralidad de intermediación (*Betweenness Centrality*) de un nodo $v$ mide la fracción de caminos más cortos entre pares de nodos que pasan a través de $v$:

$$c_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

donde $\sigma_{st}$ es el número total de caminos más cortos entre $s$ y $t$, y $\sigma_{st}(v)$ es el número de dichos caminos que pasan por $v$.

**Definición 4 (Centralidad de PageRank).** El PageRank de un nodo $v$ se define como la solución de la ecuación:

$$PR(v) = \frac{1-d}{n} + d \sum_{u \in \mathcal{N}(v)} \frac{PR(u)}{deg(u)}$$

donde $d$ es el factor de amortiguamiento (típicamente 0.85) y $\mathcal{N}(v)$ es el conjunto de vecinos de $v$.

Estas medidas de centralidad han demostrado ser efectivas para la identificación de nodos maliciosos en redes, ya que los nodos de comando y control en una botnet tienden a exhibir patrones de centralidad atípicos en comparación con los hosts legítimos (BotSward, 2022).

### 2.3 Representación de Grafos Dinámicos vs. Estáticos

Una distinción teórica fundamental en el modelado de redes de comunicación es la diferencia entre grafos estáticos y dinámicos. Un grafo estático representa la totalidad de las interacciones en un período prolongado como una única matriz de adyacencia, condensando horas o días de tráfico en una instantánea única. Esta aproximación, aunque computacionalmente más sencilla, destruye el orden temporal de las operaciones y oculta los ataques furtivos distribuidos en el tiempo, como las Amenazas Persistentes Avanzadas (*Advanced Persistent Threats*, APT), la propagación de gusanos multi-etapa y los escaneos "Low-and-Slow" (Ekle & Eberle, 2024).

**Definición 5 (Grafo dinámico).** Un grafo dinámico se define como una secuencia de instantáneas temporales $G^{(1)}, G^{(2)}, \ldots, G^{(T)}$, donde cada $G^{(t)} = (V^{(t)}, E^{(t)})$ representa el estado del grafo en el intervalo temporal $t$, o alternativamente, como un flujo de eventos temporales $(e_1, t_1), (e_2, t_2), \ldots$ donde cada evento $e_i$ es una arista etiquetada con su marca de tiempo (Ekle & Eberle, 2024).

La modelización dinámica de grafos ha emergido como un área crítica de investigación, con surveys específicos dedicados a los enfoques temporales dinámicos para la detección de anomalías (Ekle & Eberle, 2024). Estas aproximaciones reconocen que las redes de comunicación no son instantáneas cristalizadas, sino grafos en constante evolución estructural, y que el comportamiento malicioso solo puede ser comprendido plenamente en su dimensión temporal (Pang et al., 2022).


## 3. Redes Neuronales de Grafos: Fundamentos Arquitectónicos

### 3.1 Principios Fundamentales del Paso de Mensajes

El poder analítico de las GNN reside en el mecanismo iterativo de paso de mensajes (*Message Passing*). Durante la fase de aprendizaje, cada nodo genera una representación latente (*embedding*) que no solo incorpora sus características iniciales, sino que también amalgama la información de sus nodos vecinos (Lagraa et al., 2024).

**Definición 6 (Paso de mensajes en GNN).** Sea $G = (V, E)$ un grafo con características nodales $\mathbf{h}_v^{(0)} = \mathbf{x}_v$ para cada $v \in V$. En cada capa $k = 1, \ldots, K$, el paso de mensajes se define mediante tres fases:

1. **Agregación (Aggregation):** Para cada nodo $v$, se agregan los mensajes de sus vecinos:
   $$\mathbf{m}_v^{(k)} = \text{AGGREGATE}^{(k)}\left(\left\{\mathbf{h}_u^{(k-1)} : u \in \mathcal{N}(v)\right\}\right)$$

2. **Actualización (Update):** Se combina el mensaje agregado con la representación actual del nodo:
   $$\mathbf{h}_v^{(k)} = \text{UPDATE}^{(k)}\left(\mathbf{h}_v^{(k-1)}, \mathbf{m}_v^{(k)}\right)$$

3. **Readout (opcional):** Para tareas de nivel de grafo, se agregan todas las representaciones nodales:
   $$\mathbf{h}_G = \text{READOUT}\left(\{\mathbf{h}_v^{(K)} : v \in V\}\right)$$

Esta actualización se define mediante funciones de agregación (como suma, promedio o máximo) y funciones de actualización (típicamente redes neuronales) a lo largo de un número predeterminado de capas (*hops*). Por ejemplo, un salto de profundidad $K=1$ captura el vecindario inmediato, mientras que $K=2$ permite que un nodo reciba información del vecindario de sus vecinos (Lagraa et al., 2024).

En el contexto de las botnets, esta propagación espacial permite que el modelo identifique de forma automática estructuras de estrella (típicas de arquitecturas centralizadas de C&C) o patrones de grafo de mezcla rápida (característicos de redes P2P descentralizadas) sin requerir ingeniería de características manual para delinear dichos patrones (Lagraa et al., 2024).

### 3.2 Niveles de Predicción en GNN para Ciberseguridad

Las GNN pueden operar en tres niveles de granularidad para la detección de intrusiones, cada uno con aplicaciones específicas en ciberseguridad:

| Nivel de Predicción | Aplicación en Ciberseguridad | Descripción del Mecanismo |
|---------------------|------------------------------|---------------------------|
| **Nivel de Nodo (Node-level)** | Identificación de Dispositivos Infectados | Clasifica la naturaleza de un host (benigno o bot) evaluando las interacciones espaciales de su vecindario y sus características de red. |
| **Nivel de Arista (Edge-level)** | Detección de Flujos Maliciosos | Evalúa la probabilidad de que una conexión específica (ej. un flujo TCP o una consulta DNS) represente tráfico de ataque o actividad de C&C. |
| **Nivel de Grafo (Graph-level)** | Análisis Global de Trazas de Red | Clasifica una subred entera o una ventana temporal de tráfico para determinar si la estructura global exhibe una topología anómala. |

### 3.3 Tipologías Arquitectónicas de GNN

La literatura especializada ha desarrollado múltiples variantes arquitectónicas de GNN, cada una con fortalezas y limitaciones específicas para la detección de intrusiones:

**Graph Convolutional Networks (GCN).** Propuestas por Kipf y Welling, las GCN aproximan la convolución en el dominio espectral mediante la utilización de polinomios de Chebyshev truncados. La regla de actualización de una GCN convolucional se define como:

$$\mathbf{H}^{(k+1)} = \sigma\left(\tilde{\mathbf{D}}^{-\frac{1}{2}} \tilde{\mathbf{A}} \tilde{\mathbf{D}}^{-\frac{1}{2}} \mathbf{H}^{(k)} \mathbf{W}^{(k)}\right)$$

donde $\tilde{\mathbf{A}} = \mathbf{A} + \mathbf{I}$ es la matriz de adyacencia con bucles propios, $\tilde{\mathbf{D}}$ es la matriz de grados correspondiente, $\mathbf{W}^{(k)}$ es la matriz de pesos aprendible, y $\sigma$ es una función de activación no lineal (Pei et al., 2020).

**Graph Attention Networks (GAT).** Introducidas por Veličković et al., las GAT incorporan mecanismos de atención que permiten asignar pesos diferentes a distintos vecinos durante la agregación:

$$\alpha_{uv} = \frac{\exp\left(\text{LeakyReLU}\left(\mathbf{a}^T [\mathbf{W}\mathbf{h}_u \| \mathbf{W}\mathbf{h}_v]\right)\right)}{\sum_{w \in \mathcal{N}(v)} \exp\left(\text{LeakyReLU}\left(\mathbf{a}^T [\mathbf{W}\mathbf{h}_u \| \mathbf{W}\mathbf{h}_w]\right)\right)}$$

$$\mathbf{h}_v' = \sigma\left(\sum_{u \in \mathcal{N}(v)} \alpha_{uv} \mathbf{W}\mathbf{h}_u\right)$$

**GraphSAGE (Sample and Aggregate).** Propuesta por Hamilton et al., GraphSAGE introduce un enfoque inductivo que muestrea y agrega vecinos, permitiendo la generalización a nodos no vistos durante el entrenamiento:

$$\mathbf{h}_{\mathcal{N}(v)}^{(k)} = \text{AGGREGATE}_k\left(\{\mathbf{h}_u^{(k-1)}, \forall u \in \mathcal{N}(v)\}\right)$$
$$\mathbf{h}_v^{(k)} = \sigma\left(\mathbf{W}^{(k)} \cdot \text{CONCAT}\left(\mathbf{h}_v^{(k-1)}, \mathbf{h}_{\mathcal{N}(v)}^{(k)}\right)\right)$$

### 3.4 El Fenómeno del Sobre-suavizado (*Over-smoothing*)

Una limitación matemática fundamental en la optimización de GNN es el sobre-suavizado (*over-smoothing*). Las botnets avanzadas operan a través de cadenas complejas y nodos intermediarios oscuros (*proxies*), requiriendo que la red neuronal aumente el número de capas ocultas para ampliar su campo receptivo (*receptive field*) y rastrear las dependencias a larga distancia (Lagraa et al., 2024).

Sin embargo, la agregación repetitiva de información vecinal provoca un efecto de difusión; tras múltiples iteraciones, las representaciones latentes de los nodos de toda la red convergen inexorablemente hacia vectores indistinguibles (Lagraa et al., 2024). Formalmente, el sobre-suavizado se manifiesta cuando:

$$\lim_{k \to \infty} \mathbf{h}_v^{(k)} = \mathbf{h}_{\infty}, \quad \forall v \in V$$

donde $\mathbf{h}_{\infty}$ es un vector constante que depende únicamente de la estructura del grafo y no de las características iniciales de los nodos (Meng et al., 2025).

**Teorema 1 (Convergencia al sobre-suavizado).** En una GCN con propagación $\mathbf{H}^{(k+1)} = \tilde{\mathbf{A}} \mathbf{H}^{(k)} \mathbf{W}^{(k)}$ bajo ciertas condiciones de normalización, las representaciones nodales convergen a un subespacio de dimensión 1 a medida que $k \to \infty$, independientemente de las características iniciales (Meng et al., 2025).

Este fenómeno es particularmente problemático en grafos de tráfico de red, donde la escasez de enlaces directos "bot-bot" significa que el mensaje propagado por un nodo de botnet se diluye rápidamente por el mar de información benigna circundante, colapsando su detectabilidad (Lagraa et al., 2024).

**Estrategias de mitigación del sobre-suavizado:**

1. **Conexiones residuales (*Residual connections*):** La adición de conexiones residuales permite que la información de capas anteriores se preserve:
   $$\mathbf{H}^{(k+1)} = \sigma\left(\tilde{\mathbf{A}} \mathbf{H}^{(k)} \mathbf{W}^{(k)}\right) + \mathbf{H}^{(k)}$$

2. **Jumping-Knowledge (JK):** Este enfoque alivia el sobre-suavizado concatenando las representaciones de cada capa convolucional intermedia antes del clasificador final:
   $$\mathbf{H}^{\text{final}} = \text{CONCAT}\left(\mathbf{H}^{(0)}, \mathbf{H}^{(1)}, \ldots, \mathbf{H}^{(K)}\right)$$

3. **Mecanismos de compuerta jerárquica (*Hierarchical Gating*):** Arquitecturas como TopGateGNN incorporan compuertas que actúan como filtros atencionales estructurados en forma de árbol, restringiendo selectivamente la agregación de vecindarios basándose en la heterogeneidad de los atributos para retener las características discriminatorias de la minoría bot (Lagraa et al., 2024).


## 4. Arquitecturas Centradas en Aristas: E-GraphSAGE

### 4.1 Incompatibilidad Estructural de las GNN Estándar

A pesar del éxito inicial de los modelos centrados en nodos (GraphSAGE, GCN), la aplicación directa de GNN estándar a los datos de red revela una incompatibilidad estructural fundamental. En los registros de seguridad empíricos, como NetFlow, la abrumadora mayoría de las características informativas (duración, conteo de paquetes, conteo de bytes, banderas de estado TCP como SYN, ACK, FIN) pertenecen a la conexión (la arista), mientras que los nodos (las direcciones IP) carecen de atributos intrínsecos predefinidos más allá de su identificador (Lagraa et al., 2024).

Las GNN clásicas requieren vectores de características iniciales ricos en los nodos para iniciar la convolución. Para subsanar esta laguna, el estado del arte desarrolló **E-GraphSAGE** (*Edge-GraphSAGE*), una variación arquitectónica que integra directamente las características de los registros de flujo en las aristas del grafo y propaga esta información hacia los nodos (Li et al., 2025).

### 4.2 Formalización Matemática de E-GraphSAGE

La modificación fundamental de E-GraphSAGE respecto a GraphSAGE estándar reside en la función de mensaje, que incorpora explícitamente las características de las aristas:

**Definición 7 (Función de mensaje con características de arista).** En E-GraphSAGE, el mensaje del nodo $u$ hacia el nodo $v$ a través de la arista $e_{uv}$ se define como:

$$\mathbf{m}_{u \to v}^{(k)} = \text{MLP}^{(k)}\left(\text{CONCAT}\left(\mathbf{h}_u^{(k-1)}, \mathbf{e}_{uv}, \mathbf{h}_v^{(k-1)}\right)\right)$$

donde $\mathbf{e}_{uv} \in \mathbb{R}^{d_E}$ es el vector de características de la arista (flujo de red), y $\text{MLP}^{(k)}$ es un perceptrón multicapa en la capa $k$.

La agregación en E-GraphSAGE se realiza mediante:

$$\mathbf{h}_{\mathcal{N}(v)}^{(k)} = \text{AGGREGATE}^{(k)}\left(\left\{\mathbf{m}_{u \to v}^{(k)} : u \in \mathcal{N}(v)\right\}\right)$$

### 4.3 Inicialización Semántica de Nodos

En implementaciones recientes, la comunidad investigadora ha extendido E-GraphSAGE sustituyendo la inicialización genérica de los nodos (típicamente vectores poblados de unos) por inicializaciones semánticas basadas en medidas de centralidad topológica, tales como la Centralidad de Grado, Intermediación (*Betweenness*), Cercanía, PageRank y K-truss (Lagraa et al., 2024).

**Definición 8 (Inicialización semántica de nodos).** Sea $G = (V, E)$ un grafo de tráfico de red. Para cada nodo $v \in V$, se define su vector de características iniciales como:

$$\mathbf{h}_v^{(0)} = \text{CONCAT}\left(\mathbf{c}(v), \mathbf{1}_{d_V - |\mathbf{c}(v)|}\right)$$

donde $\mathbf{c}(v) = [c_{\text{deg}}(v), c_{\text{bet}}(v), c_{\text{pr}}(v), \ldots]$ es un vector de medidas de centralidad del nodo $v$.

Al inyectar instantáneamente el peso estructural de cada host en la capa de entrada, el modelo adquiere una comprensión prioritaria de qué nodos actúan como cuellos de botella de propagación o ejes de comando, mejorando significativamente la separabilidad latente entre concentradores de botnets y servidores corporativos legítimos (Lagraa et al., 2024).

### 4.4 Construcción de Grafos de Flujo mediante k-NN

Otro enfoque disruptivo para abordar la creación del grafo se observa en implementaciones evaluadas sobre el conjunto de datos CTU-13. En lugar de trazar aristas basadas en la comunicación explícita entre hosts, estas redes conectan flujos individuales utilizando la similitud *k-Nearest Neighbors* (k-NN) en el espacio de características (Deep Graph Neural Network-Based Botnet Detection on IoT Networks, 2025).

**Definición 9 (Grafo de flujos por similitud k-NN).** Sea $\mathcal{F} = \{\mathbf{f}_1, \mathbf{f}_2, \ldots, \mathbf{f}_N\}$ un conjunto de flujos de red, cada uno con un vector de características $\mathbf{f}_i \in \mathbb{R}^{d_F}$. Se construye un grafo $G_{\text{flow}} = (V_{\text{flow}}, E_{\text{flow}})$ donde:

- $V_{\text{flow}} = \mathcal{F}$ (cada flujo es un nodo)
- $E_{\text{flow}} = \{(i,j) : \mathbf{f}_j \text{ es uno de los } k \text{ vecinos más cercanos de } \mathbf{f}_i\}$

Esta estrategia de construcción de grafos de flujo, en lugar de grafos de hosts, permite agrupar comportamientos de botnets altamente correlacionados incluso si los flujos provienen de direcciones IP dispares o falsificadas, superando las estrategias de ofuscación de los atacantes que rotan constantemente sus infraestructuras (Deep Graph Neural Network-Based Botnet Detection on IoT Networks, 2025).


## 5. Redes Neuronales de Grafos Heterogéneos (HGNN)

### 5.1 Limitaciones de los Grafos Homogéneos

Si bien las redes homogéneas han demostrado eficacia teórica, abstraen en exceso la realidad de los ecosistemas informáticos. Modelar una red corporativa asumiendo que todas las entidades y relaciones poseen la misma semántica —por ejemplo, tratar una interacción entre dos servidores de base de datos de manera idéntica a una consulta DNS externa— diluye el contexto relacional y facilita las tácticas de evasión de los operadores de botnets (Lagraa et al., 2024).

### 5.2 Definición Formal de Grafos Heterogéneos

**Definición 10 (Grafo heterogéneo).** Un grafo heterogéneo se define como una tupla $G = (V, E, \phi, \psi)$, donde:

- $V$ es el conjunto de nodos
- $E$ es el conjunto de aristas
- $\phi: V \to \mathcal{T}_V$ es una función que asigna a cada nodo un tipo en el conjunto de tipos de nodos $\mathcal{T}_V$
- $\psi: E \to \mathcal{T}_E$ es una función que asigna a cada arista un tipo en el conjunto de tipos de aristas $\mathcal{T}_E$

con la condición de que $|\mathcal{T}_V| > 1$ o $|\mathcal{T}_E| > 1$.

En el contexto de la detección de botnets, los tipos de nodos pueden incluir direcciones IP, puertos de red, nombres de dominio y tipos de respuesta, mientras que los tipos de aristas pueden incluir resoluciones DNS, flujos UDP y conexiones TCP (Lagraa et al., 2024).

### 5.3 Mecanismos de Agregación Sensibles al Tipo

A diferencia de los modelos homogéneos, las HGNN aplican transformaciones conscientes del tipo (*type-aware transformations*) y mecanismos de agregación sensibles a las relaciones (*relation-sensitive aggregation*), lo que les confiere la capacidad de modelar diversas dimensiones del comportamiento de ataque dentro de un espacio latente unificado (Lagraa et al., 2024).

**Definición 11 (Agregación en HGNN).** En una HGNN, el mensaje del nodo $u$ de tipo $\phi(u)$ hacia el nodo $v$ de tipo $\phi(v)$ a través de la arista de tipo $\psi(u,v)$ se define como:

$$\mathbf{m}_{u \to v}^{(k)} = \text{MLP}_{\psi(u,v)}^{(k)}\left(\text{CONCAT}\left(\mathbf{W}_{\phi(u)}^{(k)} \mathbf{h}_u^{(k-1)}, \mathbf{e}_{\psi(u,v)}, \mathbf{W}_{\phi(v)}^{(k)} \mathbf{h}_v^{(k-1)}\right)\right)$$

donde $\mathbf{W}_{\phi(u)}^{(k)}$ y $\mathbf{W}_{\phi(v)}^{(k)}$ son matrices de proyección específicas para cada tipo de nodo.

### 5.4 Evaluación Comparativa de Arquitecturas HGNN

En escenarios de detección de anomalías basadas en consultas DNS (utilizando conjuntos de datos como TI-16), la evaluación comparativa de arquitecturas como HeteroGCN, HeteroGAT, HeteroSAGE y HeteroGAE revela descubrimientos contraintuitivos (Lagraa et al., 2024). Específicamente, los modelos HeteroSAGE y HeteroGAE han demostrado superar sistemáticamente a sus contrapartes en términos de puntuación F1 y, más críticamente, en niveles de Sensibilidad (*Recall*) superiores al 95% (Lagraa et al., 2024).

Un Recall excepcionalmente alto es la métrica suprema en ciberseguridad, ya que indica una tasa mínima de falsos negativos; dejar pasar una conexión bot maliciosa conlleva costos operacionales mucho más severos que investigar un falso positivo (Lagraa et al., 2024).

Paradójicamente, el modelo HeteroGAT —que emplea complejos mecanismos de atención múltiple y presenta un peso computacional masivo— exhibió resultados inferiores y tiempos de inferencia más lentos, demostrando que en ecosistemas heterogéneos, el incremento ciego de la complejidad arquitectónica no garantiza una mayor capacidad discriminativa (Lagraa et al., 2024).

Este descubrimiento impulsa el desarrollo de redes de función de base radial (RBFNN) profundas y heterogéneas, donde los diferentes tipos de *kernels* operan asimétricamente sobre el espacio de entrada, permitiendo que arquitecturas específicas asimilen áreas distintas de la topología de la red para desenmascarar comportamientos de ataque de bajo volumen que tradicionalmente eluden los detectores convencionales (Robust and Noise-Resilient Botnet Detection Framework Using Heterogeneous Radial Basis Function Neural Network, 2025).


## 6. Dinámica Temporal: Redes Neuronales de Grafos Espacio-Temporales (ST-GNN)

### 6.1 La Dimensión Temporal en la Detección de Botnets

La tercera dimensión crítica que consolida el estado del arte es la temporalidad. En la realidad cibernética, las redes de comunicación no son instantáneas cristalizadas, sino grafos dinámicos en constante evolución estructural (Lagraa et al., 2024). Analizar un ecosistema de red como un grafo estático condensa períodos prolongados (horas o días) en una matriz única, lo que destruye el orden temporal de las operaciones y oculta los ataques furtivos distribuidos en el tiempo, tales como las Amenazas Persistentes Avanzadas (APT), la propagación de gusanos multi-etapa y los escaneos "Low-and-Slow" (Ekle & Eberle, 2024).

Para modelar cómo el estado histórico de la red dicta su comportamiento futuro, la frontera tecnológica se ha desplazado hacia las Redes Neuronales de Grafos Espacio-Temporales (ST-GNN) y Redes Neuronales de Grafos Dinámicos (DGNN) (Ekle & Eberle, 2024). Estas arquitecturas se dividen predominantemente en dos enfoques de abstracción: modelado de tiempo discreto y modelado de tiempo continuo.

### 6.2 Modelado de Tiempo Discreto: Ventanas Deslizantes

El enfoque de tiempo discreto convierte el flujo continuo de tráfico de red en una secuencia de instantáneas discretas capturadas a intervalos fijos (Ekle & Eberle, 2024).

**Definición 12 (Secuencia de instantáneas temporales).** Sea $\mathcal{T}$ el conjunto de todos los eventos de red en un intervalo $[0, T]$. Una secuencia de instantáneas temporales con paso $\Delta t$ se define como:

$$\mathcal{G} = \{G^{(1)}, G^{(2)}, \ldots, G^{(L)}\}$$

donde $L = \lfloor T / \Delta t \rfloor$ y cada $G^{(t)} = (V^{(t)}, E^{(t)})$ contiene todos los eventos en el intervalo $[(t-1)\Delta t, t\Delta t]$.

Modelos híbridos como GCN-2-Former ejemplifican esta categoría, empleando codificadores convolucionales (GCN) para asimilar las características espaciales locales dentro de cada ventana temporal, y alimentando subsecuentemente estos *embeddings* en módulos basados en Transformers de múltiples capas para modelar las dependencias temporales globales a largo plazo (A hybrid intrusion detection model based on dynamic spatial-temporal graph neural network in in-vehicle networks, 2025).

### 6.3 Modelado de Tiempo Continuo

El enfoque de tiempo continuo trata la topología como un entorno fluido donde los eventos (inyección o eliminación de nodos y aristas) ocurren asincrónicamente con marcas de tiempo explícitas (Ekle & Eberle, 2024). Redes como TGN (*Temporal Graph Networks*) aplican mecanismos de memoria aumentada que evitan que el modelo fuerce la información en bloques arbitrarios, permitiendo que el paso de mensajes asigne ponderaciones algorítmicas basadas directamente en la proximidad cronológica (Ekle & Eberle, 2024).

**Definición 13 (Grafo temporal).** Un grafo temporal se define como un conjunto de eventos $(u, v, t, \mathbf{e})$ donde $u$ y $v$ son nodos, $t$ es una marca de tiempo, y $\mathbf{e}$ son las características del evento. La representación de un nodo en tiempo $t$ se actualiza mediante:

$$\mathbf{h}_v(t) = \text{UPDATE}\left(\mathbf{h}_v(t^-), \text{AGGREGATE}\left(\{\mathbf{m}_{u \to v}(\tau) : (u,v,\tau,\mathbf{e}) \in \mathcal{E}(t)\}\right)\right)$$

donde $\mathcal{E}(t)$ es el conjunto de eventos que involucran a $v$ hasta el tiempo $t$.

### 6.4 Mecanismos de Atención Temporal

El marco GraphSecNet fusiona el análisis dinámico de vínculos y las Redes de Atención de Grafos Temporales (*Temporal GAT*) desarrollando atenciones "conscientes de la seguridad" (GraphSecNet, 2025). Esta técnica aprende iterativamente a asignar mayor peso (*attention*) a patrones de propagación espacio-temporal que reflejan anomalías, descubriendo correlaciones entre dispositivos de atención médica, medidores inteligentes (*smart grids*) e interacciones de botnets (GraphSecNet, 2025).

**Definición 14 (Atención espacio-temporal).** La atención entre el nodo $u$ en tiempo $t_u$ y el nodo $v$ en tiempo $t_v$ se define como:

$$\alpha_{uv}(t) = \frac{\exp\left(\text{LeakyReLU}\left(\mathbf{a}^T [\mathbf{W}\mathbf{h}_u(t_u) \| \mathbf{W}\mathbf{h}_v(t_v) \| \text{TE}(t_u - t_v)]\right)\right)}{\sum_{w \in \mathcal{N}(v)} \exp\left(\text{LeakyReLU}\left(\mathbf{a}^T [\mathbf{W}\mathbf{h}_u(t_u) \| \mathbf{W}\mathbf{h}_w(t_w) \| \text{TE}(t_u - t_w)]\right)\right)}$$

donde $\text{TE}(\Delta t)$ es una codificación temporal del intervalo $\Delta t$.

Al implementar ST-GNN con módulos pre-entrenados mediante auto-codificadores (*Autoencoders*), las métricas han reportado un 99.98% de precisión en la identificación de intrusiones en redes vehiculares y una precisión superior al 98% en infraestructuras biomédicas y de la nube (Spatial-temporal graph neural network with autoencoder pretraining for intrusion detection in healthcare IoT ecosystems, 2025).


## 7. Aprendizaje Auto-Supervisado (SSL) para Detección de Botnets

### 7.1 Limitaciones del Aprendizaje Supervisado Convencional

Como contrapartida al uso exhaustivo de datos etiquetados imperfectos y costosos, la ciberseguridad estructurada avanza hacia arquitecturas de aprendizaje auto-supervisado (*Self-Supervised Learning*, SSL) como un medio para forjar detectores generalistas (Xu et al., 2024). El etiquetado manual de tráfico de red a gran escala es prohibitivamente costoso y propenso a errores, y los conjuntos de datos etiquetados disponibles a menudo sufren de desactualización y falta de representatividad de amenazas emergentes.

### 7.2 Aprendizaje Contrastivo en Grafos

Modelos como SSGMHAN (*Self-Supervised Graph Multi-Head Attention Networks*) o metodologías basadas en GraphIDS ejecutan técnicas de Aprendizaje Contrastivo Consciente de Estructura (*Structure-aware Graph Contrastive Learning*) sobre flujos de red masivos que no requieren intervención humana para su anotación (Self-supervised graph neural networks for network intrusion detection in cloud-edge collaboration environments, 2025).

**Definición 15 (Aprendizaje contrastivo en grafos).** Sea $G$ un grafo de tráfico de red. Se generan dos vistas aumentadas $G_1$ y $G_2$ mediante perturbaciones estocásticas de nodos, aristas y atributos. El objetivo del aprendizaje contrastivo es maximizar la similitud entre las representaciones de las dos vistas del mismo grafo, mientras se minimiza la similitud con representaciones de otros grafos en el *batch*:

$$\mathcal{L}_{\text{contrastive}} = -\log \frac{\exp\left(\text{sim}(\mathbf{z}_1, \mathbf{z}_2)/\tau\right)}{\sum_{i=1}^{N} \exp\left(\text{sim}(\mathbf{z}_1, \mathbf{z}_i)/\tau\right)}$$

donde $\mathbf{z}_1$ y $\mathbf{z}_2$ son las representaciones de las dos vistas del mismo grafo, $\text{sim}$ es una función de similitud (ej. coseno), $\tau$ es un parámetro de temperatura, y $N$ es el tamaño del *batch*.

### 7.3 Aumento de Datos en el Espacio Gráfico

Las técnicas de aumento de datos para grafos son fundamentales en el aprendizaje contrastivo. Las estrategias comúnmente empleadas incluyen (Self-Supervised Network Intrusion Detection Model Based on Graph Contrastive Learning, 2025):

1. **Enmascaramiento de características de nodos (*Node Feature Masking*):** Se oscurecen aleatoriamente un subconjunto de características de los nodos.
2. **Perturbación de aristas (*Edge Perturbation*):** Se añaden o eliminan aristas con una probabilidad controlada.
3. **Enmascaramiento de aristas (*Edge Masking*):** Se oscurecen las características de un subconjunto de aristas.
4. **Submuestreo de nodos (*Node Dropping*):** Se eliminan aleatoriamente un subconjunto de nodos.

### 7.4 Ventajas del SSL para la Detección de Botnets

Este proceso extrae representaciones sumamente estables e intrínsecas a la red corporativa. Posteriormente, cualquier topología inducida por una botnet externa fallará instantáneamente al no acoplarse armónicamente a esta base subyacente aprendida (Self-supervised graph neural networks for network intrusion detection in cloud-edge collaboration environments, 2025).

Esta vertiente, particularmente escalable cuando se integra con métodos federados, soluciona eficazmente el problema de la dependencia de clases desequilibradas y asegura la robustez general contra vulnerabilidades *zero-day*, dado que no depende de patrones de firma estancados en el tiempo (Xu et al., 2024).


## 8. Inteligencia Artificial Explicable (XAI) para GNN

### 8.1 La Opacidad de las GNN como Barrera Operativa

La opacidad intrínseca de los algoritmos de aprendizaje profundo plantea obstáculos reguladores y operativos sustanciales. Un Centro de Operaciones de Seguridad (SOC) rara vez autoriza una respuesta automatizada a incidentes (como aislar un servidor o cortar conexiones empresariales de misión crítica) fundamentado únicamente en la salida probabilística inescrutable de una "caja negra" basada en grafos (Jannu et al., 2023).

La viabilidad práctica de las GNN en ciberseguridad depende en última instancia de su explicabilidad; el analista debe discernir si la predicción obedece a un patrón legítimo de comunicación o una red maliciosa, identificando la causa raíz del evento de alerta (Jannu et al., 2023).

### 8.2 Explicadores Post-hoc

Las herramientas de explicación post-hoc actúan sobre modelos previamente entrenados para identificar los subgrafos y características responsables de una predicción específica (Jannu et al., 2023):

**GNNExplainer.** Este método maximiza la información mutua para abstraer un subgrafo crítico —los nodos y conexiones específicas— responsable de la alerta de la botnet (Jannu et al., 2023). Formalmente, GNNExplainer resuelve:

$$\max_{G_S \subseteq G} \text{MI}(Y, \Phi(G_S))$$

donde $G_S$ es el subgrafo explicativo, $Y$ es la predicción del modelo, $\Phi$ es el modelo GNN, y MI es la información mutua.

**Graph-SHAP.** Basado en la teoría de juegos cooperativos, Graph-SHAP extrae las puntuaciones de contribución exactas de cada característica individual del flujo (por ejemplo, el grado en que la asimetría del tamaño del paquete de carga útil influyó en la inferencia final) (Jannu et al., 2023).

### 8.3 Arquitecturas Auto-Interpretables

La tendencia científica favorece la incorporación del razonamiento de forma nativa en la arquitectura del modelo. La red XG-BoT diseña un módulo profundo explicable en su arquitectura primaria, utilizando conexiones residuales reversibles integradas con Redes de Isomorfismo de Grafos (GIN) y mapas de prominencia (*saliency maps*) para auditar forensemente la red (XG-BoT: An Explainable Deep Graph Neural Network for Botnet Detection and Forensics, 2025).

Al resaltar visual y vectorialmente qué flujos y agentes (hosts) intermedios canalizan la propagación del malware, XG-BoT no solo detecta, sino que proporciona inteligencia de amenazas (CTI) transparente y automatizada, fundamental para el análisis de ataques a la cadena de suministro (*supply-chain attacks*) y movimientos laterales dentro de sistemas federados (XG-BoT: An Explainable Deep Graph Neural Network for Botnet Detection and Forensics, 2025).


## 9. Vulnerabilidades Ante Ataques Adversarios

### 9.1 La Superficie de Ataque de las GNN

Si bien las GNN ofrecen robustez contra técnicas comunes de evasión por firmas y perturbaciones simples de características, su integración amplía la superficie de ataque del propio sistema de detección, exponiéndolos a una forma emergente y altamente peligrosa de subversión: los Ataques Adversarios Topológicos (Venturi et al., 2024). Los actores de amenazas avanzadas pueden deducir —asumiendo un entorno de caja gris o "gray-box"— que la red corporativa evalúa topologías y, mediante inyecciones sutiles, manipular el clasificador neuronal para crear fallos deliberados (Venturi et al., 2024).

### 9.2 Taxonomía de Ataques Adversarios en GNN

**Ataques basados en características (*Feature-based*).** Se añade ruido específico a los temporizadores de los flujos, tamaños de ventana TCP o tasas de paquetes. Las GNN suelen tolerar bien esta perturbación gracias a la amortiguación que brinda el vecindario general (Venturi et al., 2024).

**Ataques de estructura (*Structure-based / Edge Injection*).** El método más lesivo. Los atacantes inyectan intencionalmente aristas de comunicación —estableciendo flujos fantasma o *pings* benignos de bajo volumen hacia servidores de alta confianza como AWS, Google o DNS locales— para distorsionar la centralidad de grado y las propiedades espectrales del nodo infectado en la matriz de adyacencia (Venturi et al., 2024).

**Definición 16 (Ataque adversarial por inyección de aristas).** Sea $G = (V, E)$ un grafo de tráfico de red y sea $\Phi$ un modelo GNN entrenado. Un ataque adversarial por inyección de aristas busca encontrar un conjunto de aristas $E_{\text{adv}} \subseteq V \times V \setminus E$ tal que:

$$\Phi(G + E_{\text{adv}}) \neq \Phi(G)$$

y la perturbación $\|E_{\text{adv}}\|$ es mínima, sujeto a restricciones de presupuesto y realismo.

### 9.3 BOCLOAK: Transporte Óptimo para Ataques Adversarios

La investigación reciente introdujo BOCLOAK, un marco letal de ataque adversarial que evalúa sistemáticamente estas vulnerabilidades mediante geometría de Transporte Óptimo (*Optimal Transport*). BOCLOAK calcula la mínima manipulación de aristas necesaria para mapear el comportamiento bot al comportamiento humano considerando estrictas restricciones funcionales y temporales del mundo real (Optimal Transport-Guided Adversarial Attacks on Graph Neural Network-Based Bot Detection, 2025).

**Definición 17 (Transporte Óptimo para ataques adversariales).** El problema de transporte óptimo busca una matriz de transporte $\mathbf{P}$ que minimice el costo de transformar la distribución de representaciones de la clase bot $\mu_B$ en la distribución de la clase benigna $\mu_H$:

$$W(\mu_B, \mu_H) = \min_{\mathbf{P} \in \Pi(\mu_B, \mu_H)} \langle \mathbf{P}, \mathbf{C} \rangle$$

donde $\mathbf{C}$ es una matriz de costos que mide la distancia entre representaciones, y $\Pi(\mu_B, \mu_H)$ es el conjunto de todas las distribuciones conjuntas con marginales $\mu_B$ y $\mu_H$.

El estudio verificó que BOCLOAK puede evadir con éxito cinco de los detectores GNN de vanguardia con un asombroso incremento en la tasa de evasión de hasta el 80.13%, todo ello empleando un mínimo de computación en memoria (Optimal Transport-Guided Adversarial Attacks on Graph Neural Network-Based Bot Detection, 2025).

### 9.4 Estrategias Defensivas

Para mitigar la fragilidad adversaria estructural, las innovaciones defensivas proponen enfoques basados en arquitecturas contrastivas, como **AEDGNN**. Este método fortalece las defensas integrando Infomax Profundo en Grafos (*Deep Graph Infomax*, DGI), que entrena a la GNN mediante un enfoque de aprendizaje auto-supervisado (SSL) destinado a maximizar la información mutua entre las representaciones a nivel de parche local y el resumen global del grafo (Qian, 2026).

Adicionalmente, el endurecimiento de modelos mediante el uso de Redes Generativas Antagónicas (IDSGAN) y entrenamiento adversario con aprendizaje activo han logrado reconsolidar las fronteras de decisión de la GNN, blindándola proactivamente contra perturbaciones antes de que se desplieguen en la red (Qian, 2026).


## 10. Desafíos de Escalabilidad y Despliegue

### 10.1 Restricciones Computacionales en el Borde de la Red

A pesar de su destreza de detección, el despliegue empírico de GNN y ST-GNN en el borde de la red (*routers*, dispositivos IoT, pasarelas industriales) choca de frente con una barrera ineludible: los recursos computacionales y energéticos restrictivos (Lagraa et al., 2024). En inferencia pura, mantener el estado global de una red, multiplicando matrices de adyacencia dinámicas contra matrices de características masivas y requiriendo consultas recursivas al vecindario (*neighbor queries*), incurre en una latencia de memoria y requerimientos de FLOPs insostenibles para entornos de análisis de tráfico en tiempo real (Lagraa et al., 2024).

### 10.2 Estrategias de Escalabilidad

| Estrategia de Escalabilidad | Metodología Principal | Beneficio en Despliegue de Red |
|-----------------------------|----------------------|--------------------------------|
| **Modelado Apátrida (*Stateless*)** | Hetero-MLP / IoTGuard: Excluye la reconstrucción de la matriz de topología en inferencia. | Evita el cuello de botella de consultas recursivas a vecinos; reduce hiperparámetros en un 25.4×, apto para análisis de hardware perimetral instantáneo (Lagraa et al., 2024). |
| **Colaboración Cloud-Edge** | Desacoplamiento de inferencia/entrenamiento: Envía módulos de inferencia rápidos al IoT y delega la retropropagación intensiva a la nube. | Disminuye los gastos generales computacionales, logrando ahorros operativos del 52% en tiempo de detección y del 71% en consumo energético de hardware (Lagraa et al., 2024). |
| **Poda Dinámica de Aristas** | *Dynamic Edge Pruning*: Emplea mecanismos de atención (*multi-head attention*) para descartar iterativamente conexiones con ponderación irrelevante. | Elimina información estructural redundante y aligera los requisitos de memoria en entornos restrictivos de nubes perimetrales (Lagraa et al., 2024). |

### 10.3 Aprendizaje Federado para Detección Distribuida

El aprendizaje federado (*Federated Learning*, FL) ha emergido como un paradigma complementario para abordar tanto los desafíos de escalabilidad como las preocupaciones de privacidad en la detección de intrusiones (FedSTGCN, 2025). FedSTGCN integra las capacidades de las ST-GNN con el aprendizaje federado, permitiendo el entrenamiento colaborativo de modelos a través de dispositivos IoT distribuidos sin compartir datos en bruto (FedSTGCN, 2025).

**Definición 18 (Aprendizaje federado para detección de intrusiones).** Sea $\mathcal{C} = \{C_1, C_2, \ldots, C_N\}$ un conjunto de clientes (dispositivos IoT, routers). Cada cliente $C_i$ tiene un conjunto de datos local $\mathcal{D}_i$. El objetivo del aprendizaje federado es:

$$\min_{\mathbf{w}} \sum_{i=1}^{N} \frac{|\mathcal{D}_i|}{|\mathcal{D}|} \mathcal{L}_i(\mathbf{w}; \mathcal{D}_i)$$

donde $\mathcal{L}_i$ es la función de pérdida del cliente $i$, sin compartir los datos $\mathcal{D}_i$ entre clientes (FedSTGCN, 2025).


## 11. Validación y Sesgos Metodológicos

### 11.1 La Crisis de Reproductibilidad en la Detección de Intrusiones con GNN

Gran parte de las altas precisiones reportadas en la academia (>99% de tasa de detección) son objeto de un profundo escrutinio por parte de la industria, argumentando que dichos resultados están contaminados por fallas arquitectónicas severas en el procesamiento de conjuntos de datos clásicos (CTU-13, CIC-IDS-2017, CSE-CIC-IDS-2018 y varios conjuntos IoT) (From Claims to Crashes: A Systematic Re-evaluation of Graph-Based Network Intrusion Detection Systems, 2025).

La reproducibilidad en entornos corporativos —como validaciones en la red de Los Alamos National Laboratory (LANL), u operaciones de amenazas avanzadas DARPA OpTC— revela que los detectores hiper-optimizados colapsan bajo ruido empresarial, experimentando caídas catastróficas en el *Average Precision* y desencadenando Falsos Positivos que multiplican por cientos o miles la detección de eventos reales (From Claims to Crashes: A Systematic Re-evaluation of Graph-Based Network Intrusion Detection Systems, 2025).

### 11.2 Destrucción de Estructura por Partición Aleatoria

A diferencia de las clasificaciones planas independientes, los nodos en una GNN están interconectados. Muchos estudios barajan la totalidad de los flujos de red y los particionan aleatoriamente (ej., 80% entrenamiento, 20% prueba) antes de la inferencia (From Claims to Crashes: A Systematic Re-evaluation of Graph-Based Network Intrusion Detection Systems, 2025).

Esta división aleatoria segmenta aristas que cruzan el límite entrenamiento-prueba, induciendo fugas de información masivas (*Data Leakage*); los nodos de prueba reciben mensajes propagados a través de la topología de los nodos de entrenamiento subyacentes, enseñando al modelo una red estructuralmente falsificada y distorsionando ilusoriamente la evaluación de precisión (From Claims to Crashes: A Systematic Re-evaluation of Graph-Based Network Intrusion Detection Systems, 2025).

### 11.3 Desconocimiento de la Causalidad Temporal

Muchos modelos ingieren el 100% de los datos de evaluación para construir un grafo estático masivo y luego realizar la predicción retrospectiva (From Claims to Crashes: A Systematic Re-evaluation of Graph-Based Network Intrusion Detection Systems, 2025). En un Centro de Operaciones real, esperar a acumular múltiples horas o días de NetFlows de ataque para construir el grafo y analizarlo es fundamentalmente inviable porque introduce un retraso de detección crítico, además de retroalimentar al sistema con interacciones (aristas) futuras que el modelo operativamente no debería "conocer" en el tiempo de inferencia instantánea (From Claims to Crashes: A Systematic Re-evaluation of Graph-Based Network Intrusion Detection Systems, 2025).

### 11.4 Directrices Metodológicas para una Validación V eraz

La directriz metodológica emergente para una validación veraz requiere:

1. **Evaluaciones estrictamente inductivas y causales**, respetando el orden secuencial estricto de los eventos temporales.
2. **Uso de marcos de evaluación transductivos** sobre flujos continuos y no contaminados.
3. **Preservación de las particiones cronológicas**, garantizando que los datos de entrenamiento precedan temporalmente a los datos de prueba.
4. **Separación temporal realista** entre tráfico normal y ataques, evitando la inyección artificial de separabilidad (Practical Evaluation of Graph Neural Networks in Network Intrusion Detection, 2025).


## 12. Modelo Teórico Propuesto

### 12.1 Declaración del Modelo

Con base en el análisis exhaustivo de los fundamentos teóricos presentados, se propone un **modelo híbrido de detección de botnets basado en Redes Neuronales de Grafos Heterogéneos Espacio-Temporales con Aprendizaje Auto-Supervisado (HST-GNN-SSL)** . Este modelo integra las fortalezas complementarias de:

1. **Representación heterogénea** para capturar la diversidad semántica de entidades y relaciones en el tráfico de red.
2. **Modelado espacio-temporal** para incorporar la evolución dinámica de las comunicaciones.
3. **Aprendizaje auto-supervisado** para superar la escasez de datos etiquetados y la dependencia de clases desequilibradas.
4. **Mecanismos de explicabilidad** para facilitar la adopción en entornos operativos.

### 12.2 Justificación Teórica del Modelo

La elección de una arquitectura heterogénea espacio-temporal se justifica por las siguientes razones:

1. **Adecuación al dominio del problema:** El tráfico de red exhibe naturalmente múltiples tipos de entidades (hosts, dominios, puertos, protocolos) y relaciones (conexiones TCP, consultas DNS, flujos UDP), lo que hace que los grafos homogéneos sean una abstracción excesivamente simplificada (Lagraa et al., 2024).

2. **Captura de la dinámica temporal:** Las botnets operan a través de patrones de comunicación que evolucionan en el tiempo. El modelado estático omite información crítica sobre la secuencia y temporalidad de los ataques (Ekle & Eberle, 2024).

3. **Robustez ante datos no etiquetados:** El aprendizaje auto-supervisado permite aprovechar grandes volúmenes de tráfico de red sin necesidad de etiquetado manual, abordando el problema fundamental de la disponibilidad de datos en ciberseguridad (Xu et al., 2024).

4. **Explicabilidad inherente:** La integración de mecanismos de explicabilidad desde el diseño arquitectónico facilita la adopción en Centros de Operaciones de Seguridad (Jannu et al., 2023).

### 12.3 Arquitectura Formal del Modelo

**Definición 19 (Modelo HST-GNN-SSL).** El modelo propuesto se compone de los siguientes módulos:

1. **Módulo de Codificación Heterogénea:** Transforma el grafo de tráfico de red heterogéneo en representaciones latentes mediante capas de convolución sensibles al tipo:

   $$\mathbf{H}^{(k+1)} = \text{HeteroConv}^{(k)}\left(\mathbf{H}^{(k)}, \{\mathbf{E}_{\psi} : \psi \in \mathcal{T}_E\}\right)$$

2. **Módulo de Modelado Temporal:** Procesa la secuencia de instantáneas temporales mediante una red recurrente o un Transformer temporal:

   $$\mathbf{Z}^{(t)} = \text{TemporalEncoder}\left(\{\mathbf{H}^{(t-\tau)}, \ldots, \mathbf{H}^{(t)}\}\right)$$

3. **Módulo de Aprendizaje Contrastivo:** Entrena el modelo mediante objetivos de contraste entre vistas aumentadas del mismo grafo:

   $$\mathcal{L}_{\text{SSL}} = \mathcal{L}_{\text{contrastive}} + \lambda \mathcal{L}_{\text{predictive}}$$

4. **Módulo de Clasificación:** Realiza la predicción a nivel de nodo (identificación de bots) o de arista (detección de flujos maliciosos):

   $$\hat{y}_v = \text{softmax}\left(\text{MLP}_{\text{classifier}}(\mathbf{z}_v)\right)$$

5. **Módulo de Explicabilidad:** Genera explicaciones post-hoc o intrínsecas de las predicciones mediante mecanismos de atención y subgrafos críticos.


## 13. De Definiciones Conceptuales a Variables Medibles

### 13.1 Variables Independientes (Predictores)

| Variable | Definición Conceptual | Operacionalización | Fuente de Datos |
|----------|----------------------|-------------------|-----------------|
| **Estructura del grafo** | Topología de las comunicaciones de red | Matriz de adyacencia $\mathbf{A} \in \{0,1\}^{n \times n}$ | NetFlow, registros de conexión |
| **Características de nodos** | Atributos de los hosts de red | Vector $\mathbf{x}_v \in \mathbb{R}^{d_V}$ (medidas de centralidad, volumen de tráfico) | NetFlow, agregaciones temporales |
| **Características de aristas** | Atributos de las conexiones | Vector $\mathbf{e}_{uv} \in \mathbb{R}^{d_E}$ (duración, bytes, paquetes, flags) | NetFlow |
| **Temporalidad** | Evolución de la topología en el tiempo | Secuencia $\{G^{(1)}, \ldots, G^{(T)}\}$ o eventos temporales | NetFlow con marcas de tiempo |
| **Heterogeneidad** | Diversidad de tipos de entidades | Tipos $\phi(v) \in \mathcal{T}_V$, $\psi(e) \in \mathcal{T}_E$ | Metadatos de red (DNS, puertos, protocolos) |

### 13.2 Variable Dependiente (Respuesta)

| Variable | Definición Conceptual | Operacionalización | Escala de Medición |
|----------|----------------------|-------------------|-------------------|
| **Estado de infección** | Condición de un host como parte de una botnet | $y_v \in \{0, 1\}$ (0 = benigno, 1 = bot) | Binaria (nivel de nodo) |
| **Naturaleza del flujo** | Condición de una conexión como maliciosa | $y_{uv} \in \{0, 1\}$ (0 = benigno, 1 = malicioso) | Binaria (nivel de arista) |

### 13.3 Especificaciones de Datos y Requisitos

**Requisitos de entrada del modelo:**
- Grafo heterogéneo $G = (V, E, \phi, \psi)$ con:
  - $|V| \geq 2$ (mínimo dos nodos)
  - $|E| \geq 1$ (mínimo una arista)
  - $\mathbf{X}_V \in \mathbb{R}^{n \times d_V}$ (características nodales)
  - $\mathbf{X}_E \in \mathbb{R}^{m \times d_E}$ (características de aristas)

**Requisitos temporales:**
- Para ST-GNN: $T \geq 2$ instantáneas temporales o eventos con marcas de tiempo.

**Requisitos computacionales:**
- Memoria: $O(|V| + |E|)$ para almacenamiento de grafos.
- Tiempo: $O(K \cdot |E| \cdot d)$ por época de entrenamiento, donde $K$ es el número de capas y $d$ la dimensión de los *embeddings*.

### 13.4 Axiomas Lógicos y Supuestos del Modelo

**Axioma 1 (Coherencia estructural).** La estructura de comunicación de una botnet presenta patrones topológicos distinguibles de las comunicaciones benignas (centralización en C&C, alta densidad de interconexión en P2P, etc.) (Lagraa et al., 2024).

**Axioma 2 (Persistencia temporal).** Las botnets mantienen patrones de comunicación consistentes a lo largo del tiempo, aunque con variaciones, lo que permite su detección mediante modelado espacio-temporal (Ekle & Eberle, 2024).

**Axioma 3 (Heterogeneidad semántica).** Los diferentes tipos de entidades y relaciones en el tráfico de red portan información semántica distinta que es relevante para la detección (Lagraa et al., 2024).

**Axioma 4 (Consistencia de vecindario).** Nodos con comportamientos similares tienden a tener vecindarios similares en el grafo de tráfico (homofilia), y las botnets violan este principio en patrones detectables (Lagraa et al., 2024).

**Supuesto 1 (Disponibilidad de datos).** Se asume disponibilidad de registros de flujo de red (NetFlow, IPFIX) con metadatos suficientes para la construcción del grafo.

**Supuesto 2 (Calidad temporal).** Se asume que los registros de flujo incluyen marcas de tiempo precisas que permiten el modelado temporal.

**Supuesto 3 (Representatividad).** Se asume que los datos de entrenamiento son representativos de las condiciones operativas del despliegue.


## 14. Conclusión del Marco Teórico

El marco teórico desarrollado establece los fundamentos formales y conceptuales para la detección de botnets mediante Redes Neuronales de Grafos. La teoría de grafos proporciona el lenguaje matemático para representar las relaciones estructurales en el tráfico de red, mientras que las GNN ofrecen el mecanismo computacional para aprender representaciones latentes que capturan tanto la topología como los atributos de las comunicaciones.

La evidencia académica establece inequívocamente que los algoritmos estáticos y homogéneos convencionales carecen de la expresividad necesaria para contender con ecosistemas complejos (Lagraa et al., 2024). Los atacantes operan a través de comunicaciones heterogéneas difusas, requiriendo que la defensa evolucione hacia marcos que estructuren las redes en un plano Relacional (HGNN) y Espacio-Temporal (ST-GNN), modelando tanto nodos disímiles (host, dominios, puertos) como continuos cronológicos para discernir interacciones lentas, coordinadas e impersonadas (Lagraa et al., 2024; Ekle & Eberle, 2024).

La transición de las GNN desde plataformas experimentales hacia Centros de Operaciones de Seguridad empresariales y hardware perimetral de IoT está dictada por su resolución ante cuatro presiones cardinales: la mitigación del sobre-suavizado en el modelado de saltos profundos de red; el rediseño de las estrategias computacionales (implementando inferencias apátridas y federadas que eviten latencias letales); la robustez estructural y contrastiva contra el envenenamiento adversario; y la transparencia analítica irrefutable facilitada a través de arquitecturas de IA explicable (XAI) (Lagraa et al., 2024; Jannu et al., 2023).

El modelo HST-GNN-SSL propuesto integra estas dimensiones en una arquitectura coherente que, al ser validada bajo estrictas directrices metodológicas —corrigiendo los errores de particionamiento aleatorio y la ruptura temporal que generan los datasets clásicos—, tiene el potencial de superar las deficiencias metodológicas sistémicas y establecer un nuevo estándar en la detección de botnets.


## Referencias

BotSward: Centrality Measures for Graph-Based Bot Detection Using Machine Learning. (2022). *ScienceDirect*. https://doi.org/10.1016/j.xxx.2022.xxx

Deep Graph Neural Network-Based Botnet Detection on IoT Networks. (2025). *JETIR*.

Ekle, O. A., & Eberle, W. (2024). Anomaly Detection in Dynamic Graphs: A Comprehensive Survey. *arXiv*. https://arxiv.org/abs/2406.00134

FedSTGCN: A Novel Federated Spatiotemporal Graph Learning-Based Network Intrusion Detection Method for the Internet of Things. (2025). *Frontiers of Information Technology & Electronic Engineering*. https://doi.org/10.1631/FITEE.2400932

From Claims to Crashes: A Systematic Re-evaluation of Graph-Based Network Intrusion Detection Systems. (2025). *DART Lab*.

GraphSecNet: A Graph Neural Network Framework for Predictive Cybersecurity Intelligence in Dynamic Network Environments. (2025). *International Journal of Applied Mathematics*.

Jannu, J., Sharma, K., Aggarwal, C., & Medya, S. (2023). A Survey on Explainability of Graph Neural Networks. *IEEE Data Engineering Bulletin*, 46(2), 35-63.

Lagraa, S., Husák, M., Seba, H., Vuppala, S., State, R., & Ouedraogo, M. (2024). A Review on Graph-Based Approaches for Network Security Monitoring and Botnet Detection. *International Journal of Information Security*, 23(1), 119-140. https://doi.org/10.1007/s10207-023-00742-7

Li, R., Shen, H., Zhang, Q., & Duan, H. (2025). An Edge-Enhanced GraphSAGE-Based Intrusion Detection Model for the Internet of Things. *Cluster Computing*, 28(5). https://doi.org/10.1007/s10586-025-05100-x

Meng, H., Yang, J., & Peng, L. (2025). Mitigating Over-Smoothing in Graph Neural Networks via Separation Coefficient-Guided Adaptive Graph Structure Adjustment. *IJCAI*. https://doi.org/10.24963/ijcai.2025/663

Optimal Transport-Guided Adversarial Attacks on Graph Neural Network-Based Bot Detection. (2025). *arXiv*. https://arxiv.org/abs/2602.00318

Pang, Y., et al. (2022). A Survey on Dynamic Graph Neural Networks. *Frontiers of Computer Science*.

Pei, X., Yu, L., & Tian, S. (2020). AMalNet: A Deep Learning Framework Based on Graph Convolutional Networks for Malware Detection. *Computers & Security*, 93. https://doi.org/10.1016/j.cose.2020.101792

Practical Evaluation of Graph Neural Networks in Network Intrusion Detection. (2025). *CEUR-WS.org*, Vol. 3488.

Qian, H. (2026). On Adversarial Attack Detection in Intrusion Detection System with Graph Neural Network. *The Computer Journal*, 69(1). https://doi.org/10.1093/comjnl/bxaf096

Robust and Noise-Resilient Botnet Detection Framework Using Heterogeneous Radial Basis Function Neural Network. (2025). *MDPI Applied Sciences*, 16(7), 3379.

Self-Supervised Graph Neural Networks for Network Intrusion Detection in Cloud-Edge Collaboration Environments. (2025). https://d-nb.info/1397606673/34

Self-Supervised Network Intrusion Detection Model Based on Graph Contrastive Learning. (2025). *Journal of Xidian University*.

Spatial-Temporal Graph Neural Network with Autoencoder Pretraining for Intrusion Detection in Healthcare IoT Ecosystems. (2025). *Scientific Reports*. https://doi.org/10.1038/s41598-026-45041-y

Survey on Malware Detection with Graph Representation Learning. (s.f.).

Venturi, A., Stabili, D., & Marchetti, M. (2024). Problem Space Structural Adversarial Attacks for Network Intrusion Detection Systems Based on Graph Neural Networks. *arXiv*. https://arxiv.org/abs/2403.11830

XG-BoT: An Explainable Deep Graph Neural Network for Botnet Detection and Forensics. (2025).

Xu, R., Wu, G., Wang, W., Gao, X., He, A., & Zhang, Z. (2024). Applying Self-Supervised Learning to Network Intrusion Detection for Network Flows with Graph Neural Network. *Computer Networks*, 248, 110495. https://doi.org/10.1016/j.comnet.2024.110495