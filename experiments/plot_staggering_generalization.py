"""Static scientific figure for the solved local row model (not a 3D tube)."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

from src.discovery.periodic_staggering import flat_gap


def main():
    examples = [
        ("Période 2 : alternance", [0, .5], "#18786f"),
        ("Période 3 : pas uniforme", [0, 1/3, 2/3], "#4876a8"),
        ("Période 3 : un défaut", [0, .5, 0], "#c07725"),
        ("Vraie période 4 : quarts de pas", [0, .25, .5, .75], "#86619b"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(14, 5), constrained_layout=True)
    for ax, (title, phases, color) in zip(axes, examples):
        y = 0
        for row in range(5):
            if row:
                y += float(flat_gap(phases[row % len(phases)] - phases[(row-1) % len(phases)]))
            shift = 2 * phases[row % len(phases)]
            for column in range(-1, 4):
                ax.add_patch(Circle((2*column+shift, y), 1,
                                    facecolor=color, edgecolor=color, alpha=.23, lw=1.2))
                ax.plot(2*column+shift, y, ".", color=color, ms=3)
        mean = float(np.mean(flat_gap(np.diff([*phases, phases[0]]))))
        ax.set_title(f"{title}\nEspacement moyen : {mean:.6f}", fontsize=10)
        ax.set_aspect("equal")
        ax.set_xlim(-1.15, 6.2)
        ax.set_ylim(-1.2, 9.3)
        ax.set_xlabel("Direction tangentielle")
        ax.spines[["right", "top"]].set_visible(False)
    axes[0].set_ylabel("Direction radiale")
    fig.suptitle("Staggering : modèle local à disques de rayon 1\n"
                 "Une période plus longue n’assure pas une meilleure densité", fontsize=14)
    out = ROOT / "results/staggering_generalization_20260913"
    fig.savefig(out / "periodic_patterns.png", dpi=170)
    fig.savefig(out / "periodic_patterns.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
