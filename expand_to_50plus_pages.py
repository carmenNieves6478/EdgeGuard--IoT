import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOC_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\documento"
SEC_DIR = os.path.join(DOC_DIR, "secciones")
BASE_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV"

print("[*] Expandiendo documento LaTeX a 50+ páginas con listados de código fuente completos...")

# Helper to read code file content safely and sanitize non-ASCII
def get_code(rel_path):
    full_p = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(full_p):
        with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            # Sanitize emojis and non-ascii
            text = text.replace("🟢", "[OK]").replace("🔴", "[ERR]").replace("⚠️", "[WARN]").replace("🚀", "").replace("⚡", "").replace("🛡️", "").replace("📊", "").replace("🔍", "").replace("⚙️", "").replace("📈", "").replace("📥", "")
            return text.encode('ascii', 'ignore').decode('ascii')
    return "# File not found"

code_process = get_code("process_dataset.py")
code_train_vae = get_code("train_vae_mlp.py")
code_quant = get_code("quantize_and_xai.py")
code_stacking = get_code("train_stacking_ensemble.py")
code_benchmark = get_code("run_benchmark_comparison.py")
code_5phase = get_code("build_complete_5phase_project.py")
code_api = get_code("api/main.py")
code_dash = get_code("dashboard/app.py")
code_sim = get_code("simulator.py")

tex_anexos_full = r"""\section{ANEXOS Y CÓDIGO FUENTE COMPLETO DE PRODUCCIÓN}

\subsection{Enlace Oficial al Repositorio de Código en GitHub}
El repositorio oficial del proyecto \textbf{EdgeGuard-IoT} contiene la totalidad de los archivos de código fuente, scripts de preprocesamiento, cuadernos de Jupyter re-ejecutados y archivos de despliegue Docker:
\begin{center}
\textbf{URL del Repositorio de GitHub}: \url{https://github.com/carmenNieves6478/EdgeGuard--IoT.git}
\end{center}

\subsection{Anexo A: Preprocesamiento e Ingesta por Chunks (\texttt{process\_dataset.py})}
\begin{lstlisting}[language=Python]
""" + code_process + r"""
\end{lstlisting}

\subsection{Anexo B: Arquitectura y Entrenamiento PyTorch VAE-MLP (\texttt{train\_vae\_mlp.py})}
\begin{lstlisting}[language=Python]
""" + code_train_vae + r"""
\end{lstlisting}

\subsection{Anexo C: Cuantificación Pos-Entrenamiento INT8 y SHAP XAI (\texttt{quantize\_and\_xai.py})}
\begin{lstlisting}[language=Python]
""" + code_quant + r"""
\end{lstlisting}

\subsection{Anexo D: Ensamble de Aprendizaje Stacking (\texttt{train\_stacking\_ensemble.py})}
\begin{lstlisting}[language=Python]
""" + code_stacking + r"""
\end{lstlisting}

\subsection{Anexo E: Evaluación Comparativa Estado del Arte (\texttt{run\_benchmark\_comparison.py})}
\begin{lstlisting}[language=Python]
""" + code_benchmark + r"""
\end{lstlisting}

\subsection{Anexo F: Flujo Experimental de 5 Fases (\texttt{build\_complete\_5phase\_project.py})}
\begin{lstlisting}[language=Python]
""" + code_5phase + r"""
\end{lstlisting}

\subsection{Anexo G: Backend API REST FastAPI (\texttt{api/main.py})}
\begin{lstlisting}[language=Python]
""" + code_api + r"""
\end{lstlisting}

\subsection{Anexo H: Interfaz de Usuario Dashboard Streamlit (\texttt{dashboard/app.py})}
\begin{lstlisting}[language=Python]
""" + code_dash + r"""
\end{lstlisting}

\subsection{Anexo I: Simulador de Tráfico IoT en Tiempo Real (\texttt{simulator.py})}
\begin{lstlisting}[language=Python]
""" + code_sim + r"""
\end{lstlisting}
"""

with open(os.path.join(SEC_DIR, "anexos.tex"), "w", encoding="utf-8") as f:
    f.write(tex_anexos_full)

print("[✔] Anexos extendidos guardados exitosamente.")
