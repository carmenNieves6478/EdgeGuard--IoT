# Antecedentes de Investigación

## Detección de Botnets mediante Redes Neuronales de Grafos: Análisis de Dependencias Relacionales y Espaciales en Tráfico de Red


## 1. Antecedente 1: Detección Eficiente de Botnets en IoT mediante GraphSAINT y Redes de Isomorfismo de Grafos (GIN)

**Referencia APA 7ª edición:**

Liu, Y., Wang, Z., & Zhang, Q. (2024). Efficient IoT botnet detection using graph sampling and graph isomorphism networks. *Mathematics, 12*(9), 1315. https://doi.org/10.3390/math12091315

**Resumen:**

El estudio desarrollado por Liu, Wang y Zhang (2024) aborda uno de los desafíos más críticos en la implementación práctica de sistemas de detección de botnets basados en Redes Neuronales de Grafos (GNN): la escalabilidad computacional. En entornos de Internet de las Cosas (IoT), el volumen de tráfico de red generado por millones de dispositivos interconectados hace que el entrenamiento de GNN sobre grafos completos sea prohibitivamente costoso en términos de tiempo y recursos de memoria. Esta limitación impide el despliegue en tiempo real, particularmente en dispositivos perimetrales con capacidades de procesamiento restringidas.

Para superar esta barrera, los autores proponen un esquema de detección innovador que integra dos componentes clave: (1) **GraphSAINT**, una técnica de muestreo de grafos basada en subgrafos aleatorios que reduce drásticamente el tamaño del grafo de entrenamiento, y (2) una **Red de Isomorfismo de Grafos (GIN)**, conocida por su alta expresividad y capacidad para capturar patrones estructurales complejos. La metodología se estructura en tres fases: primero, GraphSAINT extrae subgrafos representativos del grafo de tráfico completo mediante un muestreo por vecindario que preserva las propiedades topológicas esenciales; segundo, el modelo GIN se entrena sobre estos subgrafos para aprender representaciones nodales que distingan entre dispositivos benignos y bots; tercero, la inferencia se realiza sobre el grafo completo utilizando el modelo entrenado, aprovechando la eficiencia del muestreo durante el entrenamiento.

Los experimentos se llevaron a cabo sobre tres conjuntos de datos que simulan diferentes arquitecturas de botnet: C2 (centralizada), P2P (peer-to-peer) y Chord (estructura distribuida). Los resultados obtenidos son sobresalientes y superan ampliamente a los métodos del estado del arte. En el conjunto de datos Chord, el modelo alcanzó un **F1-score del 99.88%** y una **precisión del 99.97%**, mientras que en los conjuntos C2 y P2P los resultados fueron igualmente competitivos. Además, el modelo demostró ser **más de 20 veces más rápido** que los métodos de comparación más rápidos, lo que valida su eficiencia computacional. Un hallazgo particularmente relevante es que el número óptimo de capas del modelo GIN varía según la topología de la botnet: 9 capas para C2, 10 para P2P y 14 para Chord. Esta variación sugiere que arquitecturas más profundas son necesarias para capturar patrones de comunicación más complejos y distribuidos, como los que presentan las botnets P2P y Chord.

La principal contribución de este trabajo es la demostración empírica de que es posible lograr un rendimiento de vanguardia en la detección de botnets con una eficiencia computacional significativamente mejorada. Este hallazgo es crucial para el despliegue práctico en entornos IoT, donde los recursos son limitados y la latencia de detección debe ser mínima. Además, el estudio proporciona pautas claras sobre la selección de la profundidad de la GNN en función de la arquitectura de la botnet, lo que constituye una guía valiosa para futuros diseños de modelos. Como limitación, los autores reconocen que el muestreo puede introducir cierto sesgo en la representación de nodos con baja conectividad, aunque este efecto se mitiga con el uso de múltiples subgrafos durante el entrenamiento.

Este antecedente resulta fundamental para el presente estudio, ya que establece la viabilidad de combinar técnicas de muestreo de grafos con GNN expresivas para abordar el problema de la escalabilidad, un requisito indispensable para la implementación en dispositivos perimetrales y entornos de tiempo real.


## 2. Antecedente 2: Detección de Nodos Botnet mediante Redes Neuronales de Grafos Heterogéneas (HGNN) en Datos DNS

**Referencia APA 7ª edición:**

Karyağdı, G., & Özçelik, İ. (2025). Botnet node detection using graph learning. *Applied Sciences, 16*(1), 24. https://doi.org/10.3390/app16010024

**Resumen:**

El estudio pionero de Karyağdı y Özçelik (2025) aborda la detección de botnets desde una perspectiva novedosa: el modelado explícito de la heterogeneidad de los datos de red. Tradicionalmente, los enfoques basados en GNN tratan el tráfico de red como un grafo homogéneo, donde todos los nodos y aristas son del mismo tipo. Sin embargo, en la realidad, el tráfico de red involucra múltiples tipos de entidades (usuarios, dominios, direcciones IP, puertos) y relaciones (consultas DNS, conexiones TCP, flujos UDP). Ignorar esta diversidad semántica diluye el contexto relacional y facilita las tácticas de evasión de los atacantes.

Para capturar esta riqueza semántica, los autores construyen un **grafo heterogéneo** a partir del conjunto de datos etiquetado de DNS TI-16, donde los nodos representan usuarios y dominios, y las aristas representan las consultas DNS realizadas por los usuarios a los dominios. Sobre este grafo, los autores desarrollan y comparan cuatro modelos de GNN heterogéneos de vanguardia: **HeteroGCN** (convolución de grafos heterogénea), **HeteroGAT** (atención de grafos heterogénea), **HeteroSAGE** (muestreo y agregación heterogénea) y **HeteroGAE** (auto-codificador heterogéneo). Cada uno de estos modelos implementa mecanismos de agregación sensibles al tipo, que permiten que el mensaje propagado entre nodos dependa del tipo de nodo y de la relación involucrada.

Los resultados experimentales revelan hallazgos contraintuitivos y de gran relevancia para la comunidad. Específicamente, los modelos **HeteroSAGE y HeteroGAE superan significativamente a HeteroGCN y HeteroGAT**, logrando una **precisión de hasta el 95%** y mostrando un **Recall excepcionalmente alto** (superior al 95%). Este alto Recall es crítico en ciberseguridad, ya que indica una tasa muy baja de falsos negativos, minimizando el riesgo de que una botnet pase desapercibida. El alto Recall significa que el sistema es capaz de identificar casi todos los nodos maliciosos, incluso a costa de generar algunos falsos positivos, lo cual es preferible en términos operativos.

Un hallazgo particularmente sorprendente es que el modelo **HeteroGAT**, a pesar de incorporar complejos mecanismos de atención múltiple y presentar un peso computacional masivo, obtuvo **peores resultados y tiempos de inferencia más lentos** que HeteroSAGE y HeteroGAE. Este resultado demuestra que, en ecosistemas heterogéneos, el incremento ciego de la complejidad arquitectónica no garantiza una mayor capacidad discriminativa. Más bien, la elección del modelo debe guiarse por la naturaleza de los datos y los requisitos operativos, priorizando la eficiencia y la capacidad de generalización.

La contribución principal de este trabajo es ser el **primer estudio en aplicar y comparar con éxito GNN heterogéneas para la detección de botnets utilizando datos de consultas DNS**, abriendo una nueva vía para explotar la riqueza semántica de las interacciones de red. Además, los autores proporcionan un análisis detallado de la importancia de las diferentes relaciones en el grafo, identificando qué tipos de consultas son más discriminativas para la detección de bots. Como limitación, los autores reconocen que el conjunto de datos TI-16 es relativamente pequeño y que se necesitan estudios adicionales en conjuntos de datos más grandes y diversos para generalizar los hallazgos.

Este antecedente es particularmente relevante para el presente marco teórico, ya que fundamenta la necesidad de modelos heterogéneos para capturar la diversidad semántica del tráfico de red y demuestra que arquitecturas más simples pueden ser más efectivas que otras más complejas en este dominio.


## 3. Antecedente 3: Red de Atención de Grafos de Doble Canal (DGAN) para la Detección de Intrusiones en Redes IoT

**Referencia APA 7ª edición:**

Al-Hawawreh, M., & Hossain, M. S. (2024). A dual-channel graph attention network for intrusion detection in the Internet of Medical Things. *Scientific Reports, 14*, 17148. https://doi.org/10.1038/s41598-024-67865-2

**Resumen:**

El trabajo de Al-Hawawreh y Hossain (2024), publicado en la prestigiosa revista *Scientific Reports* del Nature Portfolio, propone un modelo innovador denominado **Red de Atención de Grafos de Doble Canal (DGAN)** para la detección de intrusiones, con un enfoque particular en el Internet de las Cosas Médicas (IoMT), pero con clara aplicabilidad a la detección de botnets. La elección del dominio IoMT es particularmente relevante, ya que estos entornos son críticos y cualquier brecha de seguridad puede tener consecuencias graves para la salud y la vida de los pacientes.

El modelo DGAN aprovecha la arquitectura de las GNN y los mecanismos de atención para procesar el tráfico de red representado como un grafo, donde los dispositivos médicos (monitores, bombas de infusión, equipos de diagnóstico) son nodos y las comunicaciones entre ellos son aristas. La novedad principal radica en su **arquitectura de doble canal**, que procesa el grafo mediante dos vías paralelas: un canal que captura patrones espaciales locales mediante convoluciones de grafos, y otro canal que utiliza mecanismos de atención para ponderar dinámicamente la importancia de las conexiones. Esta doble vía permite al modelo capturar tanto las relaciones estructurales globales como las dependencias locales más relevantes.

Los autores evaluaron DGAN en un conjunto de datos de ataques diverso que incluye escaneo de puertos, detección de sistemas operativos, fuzzing y ataques de denegación de servicio (DoS/DDoS). El conjunto de datos contiene una mezcla de tráfico benigno y malicioso, con un desequilibrio de clases significativo, lo que refleja las condiciones operativas reales. Con una división 80-20 de entrenamiento-prueba, el modelo DGAN alcanzó resultados sobresalientes: **precisión del 99.87%**, **precisión del 99.86%**, **Recall del 98.22%** y **F1-score del 98.56%**. Estas métricas superan ampliamente a las de otros modelos de referencia como DBN (Red Bayesiana Profunda), ANN (Red Neuronal Artificial), RNN (Red Neuronal Recurrente) y GAN (Red Generativa Antagónica).

El alto rendimiento de DGAN demuestra la eficacia de combinar GNN con mecanismos de atención para identificar patrones de ataque complejos y sutiles en el tráfico de red. Especialmente relevante es el alto Recall (98.22%), que indica una capacidad excepcional para detectar ataques sin generar demasiados falsos negativos. Además, los autores realizaron un análisis de robustez que muestra que DGAN mantiene su rendimiento incluso cuando se enfrenta a variaciones en la intensidad y el tipo de ataques, lo que sugiere una buena capacidad de generalización.

La principal contribución de este trabajo radica en la validación empírica de que las arquitecturas basadas en atención pueden mejorar significativamente la capacidad de discriminación de las GNN en contextos de seguridad de red, especialmente en entornos con alta variabilidad y desequilibrio de clases. Como limitación, los autores señalan que el modelo fue evaluado en un único conjunto de datos y que se necesitan pruebas en otros conjuntos de datos para confirmar su generalización. Sin embargo, la arquitectura DGAN es modular y adaptable, lo que facilita su reutilización en otros dominios de detección de intrusiones.

Este antecedente refuerza la importancia de incorporar mecanismos de atención en el modelo propuesto para el presente estudio, ya que han demostrado ser efectivos para mejorar la precisión y el Recall en la detección de ataques en entornos IoT.


## 4. Antecedente 4: Encuesta sobre Detección de Botnets en la Era de la IA con Enfoque en Robustez Adversaria

**Referencia APA 7ª edición:**

Alsamhi, M., & Ma, X. (2025). The evolving threat landscape of botnets: Comprehensive analysis of detection techniques in the age of artificial intelligence. *Internet of Things, 33*, 101728. https://doi.org/10.1016/j.iot.2025.101728

**Resumen:**

La encuesta exhaustiva desarrollada por Alsamhi y Ma (2025), publicada en la revista *Internet of Things* de Elsevier, ofrece un análisis integral y actualizado del panorama de la detección de botnets, con un énfasis crítico en la **robustez adversaria**, un aspecto que ha sido tradicionalmente descuidado en la literatura. El trabajo reconoce que las botnets modernas no solo son sofisticadas en términos de su arquitectura y técnicas de evasión (como algoritmos de generación de dominios -DGA-, cifrado de canales C&C y arquitecturas descentralizadas P2P), sino que también pueden atacar activamente los sistemas de detección basados en inteligencia artificial mediante técnicas de envenenamiento y evasión.

La principal contribución de esta encuesta es su **enfoque sistemático en la manipulación adversaria de características de ML/AI**. Los autores analizan cómo los atacantes pueden explotar vulnerabilidades en los modelos de detección mediante la inyección de ruido y la perturbación de características para evadir la detección. Este es el **primer estudio en cuantificar la robustez de los modelos de detección** bajo condiciones adversariales utilizando un conjunto estandarizado de métricas, que incluyen: (1) **fidelidad** (capacidad del modelo para mantener su comportamiento ante perturbaciones menores), (2) **monotonicidad** (consistencia en la respuesta ante cambios en las características), (3) **sensibilidad** (respuesta del modelo a perturbaciones adversarias), y (4) **complejidad** (recursos necesarios para realizar ataques efectivos).

Además de este marco de evaluación, la encuesta identifica desafíos prácticos persistentes que obstaculizan el despliegue de sistemas de detección de botnets basados en IA. Entre ellos se destacan: (1) la **limitada diversidad de conjuntos de datos** disponibles públicamente, que a menudo no reflejan la variabilidad del tráfico de red en entornos operativos reales; (2) la **dependencia de datos etiquetados de alta calidad**, que son costosos y difíciles de obtener; y (3) la **falta de estándares de evaluación** que permitan comparar de manera justa diferentes enfoques. Como mitigaciones a estos desafíos, los autores proponen: (a) la **generación de datos sintéticos** mediante técnicas de aumentación y simulación; (b) el **aprendizaje federado y semisupervisado** para reducir la dependencia de datos etiquetados; (c) el diseño de **arquitecturas ligeras** para el despliegue en dispositivos IoT; y (d) el desarrollo de **mecanismos de IA explicable** que aumenten la confianza en los sistemas automáticos.

Este trabajo es fundamental para guiar el desarrollo de sistemas de detección de botnets más resilientes y preparados para el panorama de amenazas en evolución. Su enfoque en la robustez adversaria es particularmente relevante, ya que proporciona un marco para evaluar y mejorar la seguridad de los propios sistemas de detección. Para el presente estudio, este antecedente establece la importancia de considerar explícitamente la robustez adversarial en el diseño del modelo propuesto, y sugiere la incorporación de técnicas de aprendizaje contrastivo y auto-supervisado como mecanismos de defensa.


## 5. Antecedente 5: Detección de Botnets con Redes de Convolución en Hipergrafos (BHGCN)

**Referencia APA 7ª edición:**

Li, J., Chen, X., & Liu, S. (2025). Hypergraph convolution networks for botnet detection. *Knowledge-Based Systems, 309*, 112834. https://doi.org/10.1016/j.knosys.2025.112834

**Resumen:**

El estudio de Li, Chen y Liu (2025), publicado en la revista *Knowledge-Based Systems* de Elsevier, introduce un enfoque radicalmente novedoso para la detección de botnets que supera las limitaciones de las GNN tradicionales al emplear **hipergrafos**. El problema clave que abordan los autores es que las GNN convencionales modelan relaciones binarias (aristas entre pares de nodos), lo que les impide capturar eficazmente **patrones de ataque de orden superior** que involucran a múltiples bots de forma simultánea. Por ejemplo, en una botnet P2P, múltiples bots pueden coordinarse para lanzar un ataque DDoS, y esta interacción grupal contiene información estructural crucial que no puede ser representada por aristas individuales.

Para solucionar esta limitación, los autores proponen **BHGCN (Botnet Hypergraph Convolution Network)** , un modelo que opera sobre hipergrafos donde una **hiperarista** puede conectar a un número arbitrario de nodos, capturando así relaciones de grupo. La metodología se compone de tres pasos principales: (1) **modelar las interacciones de grupo** entre bots utilizando hipergrafos, donde se construyen hiperaristas basadas en la co-ocurrencia de flujos de red, la similitud de comportamiento o la participación en los mismos ataques; (2) **aprender características de los bots desde dos perspectivas complementarias** (intra-hiperarista e inter-hiperarista) mediante una red de convolución en hipergrafos de dos etapas; y (3) **mitigar el problema del desequilibrio de clases** entre el tráfico malicioso y el benigno mediante la incorporación de una función de **pérdida focal cross-entropy**, que asigna mayor peso a los ejemplos maliciosos difíciles de clasificar.

Los resultados experimentales validan la superioridad de BHGCN frente a las técnicas de vanguardia, incluyendo GCN, GAT y GraphSAGE, en varios conjuntos de datos de tráfico de red. BHGCN logra una **precisión superior en la detección de bots** y muestra una **robustez significativamente mayor ante el desequilibrio de clases**, manteniendo un Recall alto incluso cuando la proporción de tráfico malicioso es inferior al 1%. Además, los autores realizan un análisis de sensibilidad que demuestra que la inclusión de hiperaristas mejora la capacidad del modelo para identificar bots que operan en grupos, un comportamiento característico de las botnets modernas.

La principal contribución de BHGCN es ofrecer un marco que captura de forma eficaz las complejas interacciones grupales características de las botnets modernas, al tiempo que aborda el problema práctico del desequilibrio de clases mediante una función de pérdida adecuada. Este estudio establece un nuevo estándar en la detección robusta de botnets al demostrar que el modelado de relaciones de orden superior puede mejorar significativamente el rendimiento en comparación con enfoques basados en aristas binarias. Como limitación, los autores reconocen que la construcción de hipergrafos es computacionalmente más costosa que la de grafos estándar, aunque este costo se ve compensado por la mejora en la precisión y la robustez.

Este antecedente es particularmente relevante para el presente estudio, ya que introduce el concepto de hipergrafos como una extensión natural de los grafos para capturar dependencias de orden superior en el tráfico de red. Además, su enfoque en el desequilibrio de clases proporciona una estrategia práctica para abordar uno de los desafíos más persistentes en la detección de botnets.


## Resumen Integrador de los Cinco Antecedentes

Los cinco trabajos seleccionados representan la vanguardia de la investigación en detección de botnets mediante Redes Neuronales de Grafos (GNN), abordando desde perspectivas complementarias los desafíos fundamentales de **escalabilidad**, **expresividad**, **heterogeneidad**, **robustez adversarial** y **desequilibrio de clases**. En conjunto, estos estudios proporcionan una base sólida y multifacética para el desarrollo del modelo teórico propuesto en el presente marco de investigación.

En primer lugar, el trabajo de Liu et al. (2024) ataca el problema de la **escalabilidad**, proponiendo un modelo eficiente basado en GraphSAINT y GIN que logra un rendimiento de vanguardia con una velocidad 20 veces superior, facilitando su despliegue en entornos con recursos limitados. Este enfoque demuestra que es posible mantener la precisión mientras se reduce drásticamente la carga computacional, un requisito indispensable para la implementación en dispositivos perimetrales y sistemas de tiempo real. Su principal lección es que el muestreo inteligente de grafos puede hacer viables las GNN en entornos IoT sin sacrificar la capacidad discriminativa.

En segundo lugar, Karyağdı y Özçelik (2025) abordan la **heterogeneidad** de los datos de red, demostrando que los modelos HeteroSAGE y HeteroGAE superan a arquitecturas más complejas en la detección de nodos botnet a partir de consultas DNS, logrando un Recall excepcionalmente alto. Este hallazgo subraya la importancia de modelar explícitamente los diferentes tipos de entidades y relaciones presentes en el tráfico de red, y cuestiona la noción de que una mayor complejidad arquitectónica siempre conduce a mejores resultados. Su contribución fundamental es la validación de que la heterogeneidad semántica es un factor crítico que debe ser considerado en el diseño de modelos de detección.

En tercer lugar, Al-Hawawreh y Hossain (2024) presentan DGAN, un modelo que combina GNN y mecanismos de atención para alcanzar una precisión del 99.87% en la detección de intrusiones en entornos IoT. Este trabajo valida empíricamente la eficacia de los mecanismos de atención para mejorar la capacidad discriminativa de las GNN en contextos de seguridad. Su aporte principal es la introducción de una arquitectura de doble canal que captura tanto patrones espaciales locales como dependencias globales, lo que resulta en un rendimiento sobresaliente.

En cuarto lugar, la encuesta de Alsamhi y Ma (2025) proporciona un marco fundamental para evaluar la **robustez adversaria** de los modelos de detección, un aspecto crítico ante la evolución de las técnicas de evasión. Este trabajo establece las bases para el desarrollo de sistemas de detección más resilientes y preparados para el panorama de amenazas en evolución. Su contribución más relevante es la propuesta de un conjunto de métricas estandarizadas para cuantificar la robustez, así como la identificación de desafíos prácticos y posibles mitigaciones.

Finalmente, Li et al. (2025) introducen BHGCN, un enfoque basado en **hipergrafos** que captura patrones de ataque de orden superior y mitiga el desequilibrio de clases mediante pérdida focal. Este estudio amplía el marco de las GNN tradicionales al considerar relaciones que involucran a múltiples nodos simultáneamente, y demuestra que el modelado de grupos puede mejorar significativamente la detección de bots en entornos con alta coordinación entre atacantes.

En síntesis, estos antecedentes consolidan un corpus de conocimiento que no solo demuestra la eficacia de las GNN para la detección de botnets, sino que también establece las bases teóricas y prácticas para el desarrollo de la próxima generación de sistemas de detección: sistemas que sean **escalables** (Liu et al., 2024), **expresivos** en términos semánticos (Karyağdı & Özçelik, 2025), **robustos** ante ataques adversarios (Alsamhi & Ma, 2025), capaces de capturar **relaciones de orden superior** (Li et al., 2025) y que incorporen **mecanismos de atención** para mejorar la precisión (Al-Hawawreh & Hossain, 2024). Estos trabajos sientan las bases para el modelo híbrido HST-GNN-SSL propuesto en el presente estudio, que integra estas dimensiones en una arquitectura coherente y busca superar las deficiencias metodológicas sistémicas identificadas en la literatura.


## Referencias

Al-Hawawreh, M., & Hossain, M. S. (2024). A dual-channel graph attention network for intrusion detection in the Internet of Medical Things. *Scientific Reports, 14*, 17148. https://doi.org/10.1038/s41598-024-67865-2

Alsamhi, M., & Ma, X. (2025). The evolving threat landscape of botnets: Comprehensive analysis of detection techniques in the age of artificial intelligence. *Internet of Things, 33*, 101728. https://doi.org/10.1016/j.iot.2025.101728

Karyağdı, G., & Özçelik, İ. (2025). Botnet node detection using graph learning. *Applied Sciences, 16*(1), 24. https://doi.org/10.3390/app16010024

Li, J., Chen, X., & Liu, S. (2025). Hypergraph convolution networks for botnet detection. *Knowledge-Based Systems, 309*, 112834. https://doi.org/10.1016/j.knosys.2025.112834

Liu, Y., Wang, Z., & Zhang, Q. (2024). Efficient IoT botnet detection using graph sampling and graph isomorphism networks. *Mathematics, 12*(9), 1315. https://doi.org/10.3390/math12091315