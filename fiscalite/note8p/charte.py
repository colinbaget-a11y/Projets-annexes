"""Charte graphique de la note de 8 pages (note8p/CADRE.md, section « Graphiques »).

Gris = système actuel ; bleu clair = réforme naïve ou variante ; bleu foncé = notre proposition ;
ocre brique = hausse d'impôt ou arbitrage important. Titres et sources dans le LaTeX, jamais dans l'image.
Usage : import sys; sys.path.insert(0, "note8p"); from charte import *
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

AUJ = "#8a8a8a"      # aujourd'hui
NAIF = "#8fb4e3"     # réforme naïve, variante
PROP = "#173f8a"     # proposition
HAUSSE = "#b8642a"   # hausse d'impôt, perdant, arbitrage
ENCRE, ENCRE2, GRILLE = "#1a1a1a", "#555555", "#e6e6e6"

# Largeurs d'impression (pouces) : pleine largeur 6,3 ; demi-largeur 3,05. Hauteur ≤ 2,6 (pleine) ou ≤ 2,4 (demi).
PLEINE, DEMI = 6.3, 3.05

plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5, "legend.frameon": False,
    "axes.edgecolor": "#8a8984", "axes.linewidth": 0.6, "lines.linewidth": 1.8,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.03, "pdf.fonttype": 42,
})


def _fr(v, d=0):
    s = f"{v:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


euros = FuncFormatter(lambda v, _: _fr(v) + " €")
pct = FuncFormatter(lambda v, _: _fr(v) + " %")
milliers = FuncFormatter(lambda v, _: _fr(v / 1000) + " k€")


def axes(ax, grille="y"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=ENCRE2, length=2.5)
    if grille:
        ax.grid(axis=grille, color=GRILLE, lw=0.6, zorder=0)
    ax.set_axisbelow(True)


def sauver(fig, nom, source, note=""):
    """Écrit note8p/figures/<nom>.pdf et <nom>_source.tex (source puis note éventuelle, une ligne chacune)."""
    from pathlib import Path
    d = Path(__file__).parent / "figures"
    fig.savefig(d / f"{nom}.pdf")
    fig.savefig(d / f"{nom}.png", dpi=150)
    import re
    txt = "Source : " + source + ("\\par " + note if note else "")
    txt = re.sub(r"(?<!\\)_", r"\\_", txt)
    txt = re.sub(r"(?<!\\)%", r"\\%", txt)
    (d / f"{nom}_source.tex").write_text(txt + "\n", encoding="utf-8")
    plt.close(fig)
