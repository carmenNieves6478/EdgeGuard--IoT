import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

RESULTS_DIR = r"E:\PROYECTO DE INVESTIGACION\dataset\MERGED_CSV\results\reports_and_plots"
os.makedirs(RESULTS_DIR, exist_ok=True)

fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
ax.axis('off')

# Background styling
fig.patch.set_facecolor('#F8F9FA')

# Draw Architecture Layers as Colored Boxes
def draw_box(ax, x, y, w, h, label, color, sublabel=""):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3",
                                fc=color, ec="#003366", lw=2, zorder=2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2 + (0.15 if sublabel else 0), label,
            ha='center', va='center', color='white', fontweight='bold', fontsize=11, zorder=3)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.2, sublabel,
                ha='center', va='center', color='#E2E8F0', fontsize=9, zorder=3)

def draw_arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#003366", lw=2.5, mutation_scale=18), zorder=1)
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, label, ha='center', va='center',
                fontsize=9, fontweight='bold', color='#0F2D59')

# Title
ax.text(7, 7.3, "ARQUITECTURA DEL MODELO EDGEGUARD VAE-MLP",
        ha='center', va='center', fontsize=16, fontweight='bold', color='#003366')
ax.text(7, 6.9, "Compresión Latente en el Borde (16 dims) + Clasificador Multiclase (8 Clases)",
        ha='center', va='center', fontsize=11, color='#0F2D59')

# 1. Input Layer
draw_box(ax, 0.5, 3.2, 1.8, 1.6, "Entrada Red\nIoT Flow", "#0F2D59", "39 Características")

# 2. Encoder Layer
draw_box(ax, 3.2, 3.2, 2.0, 1.6, "Encoder VAE", "#003366", "39 -> 64 -> 32")
draw_arrow(ax, 2.3, 4.0, 3.2, 4.0)

# 3. Latent Bottleneck (Mu / Logvar)
draw_box(ax, 6.0, 4.5, 2.0, 1.4, "Espacio Latente\n(mu, logvar)", "#D4AF37", "16 Dimensiones")
draw_box(ax, 6.0, 2.0, 2.0, 1.4, "Truco Reparam.\nz = mu + eps*sigma", "#D4AF37", "z ~ N(mu, sigma^2)")
draw_arrow(ax, 5.2, 4.0, 6.0, 5.2)
draw_arrow(ax, 6.0, 4.5, 6.0, 3.4, "Muestreo")

# 4. Decoder Path (Reconstruction)
draw_box(ax, 9.0, 4.8, 2.2, 1.4, "Decoder VAE", "#2563EB", "16 -> 32 -> 64 -> 39")
draw_box(ax, 12.0, 4.8, 1.6, 1.4, "Reconstrucción\nx_hat", "#059669", "MSE Loss")
draw_arrow(ax, 8.0, 5.2, 9.0, 5.5)
draw_arrow(ax, 11.2, 5.5, 12.0, 5.5)

# 5. Classifier Path (Multiclass Prediction)
draw_box(ax, 9.0, 1.8, 2.2, 1.6, "Clasificador MLP\n(BatchNorm + Drop 0.2)", "#7C3AED", "16 -> 32 -> 16 -> 8")
draw_box(ax, 12.0, 1.8, 1.6, 1.6, "Predicción\n8 Clases", "#DC2626", "Softmax Logits")
draw_arrow(ax, 8.0, 2.7, 9.0, 2.6)
draw_arrow(ax, 11.2, 2.6, 12.0, 2.6)

plt.tight_layout()
output_path = os.path.join(RESULTS_DIR, "vae_mlp_architecture_diagram.png")
plt.savefig(output_path, bbox_inches='tight', facecolor=fig.get_facecolor(), dpi=300)
plt.close()

print(f"[+] Diagrama visual de la arquitectura VAE-MLP guardado en: {output_path}")
