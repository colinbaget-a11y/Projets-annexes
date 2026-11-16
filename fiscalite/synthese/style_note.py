"""Couleurs et petits réglages communs à toutes les figures de la note fusionnée (CHARTE_NOTE.md).

Aujourd'hui, réforme naïve, proposition et variante gardent la même couleur dans toute la note. Palette validée
(skill dataviz, validate_palette.js, toutes paires) : bleu #1d4ba6, ocre #c79100, brique #993333 ; l'ocre a un
contraste faible sur fond clair : toujours l'accompagner d'une étiquette ou d'une légende.
Usage : from style_note import AUJ, NAIF, PROP, VAR, SEC, NUANCES_BLEU, axes_propres, euros, pct
"""
from matplotlib.ticker import FuncFormatter

AUJ = "#3d3d3d"     # situation actuelle
NAIF = "#993333"    # réforme naïve
PROP = "#1d4ba6"    # proposition
VAR = "#c79100"     # variante, arbitrage
SEC = "#b8b8b8"     # élément secondaire
GRILLE = "#e4e3df"
ENCRE, ENCRE2 = "#0b0b0b", "#52514e"
NUANCES_BLEU = ["#0b2a61", "#1d4ba6", "#4369b4", "#7691c8", "#aabbdd", "#d4ddf0"]
COULEURS = {"auj": AUJ, "naif": NAIF, "prop": PROP, "var": VAR}
NOMS = {"auj": "Aujourd'hui", "naif": "Réforme naïve", "prop": "Proposition"}


def _fr(v, d=0):
    s = f"{v:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


euros = FuncFormatter(lambda v, _: _fr(v) + " €")
pct = FuncFormatter(lambda v, _: _fr(v) + " %")
nombre = FuncFormatter(lambda v, _: _fr(v))


def axes_propres(ax, grille="y"):
    """Axes discrets : pas de cadre haut et droit, grille légère, encre secondaire."""
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#8a8984")
    ax.tick_params(colors=ENCRE2, length=3)
    if grille:
        ax.grid(axis=grille, color=GRILLE, lw=0.6, zorder=0)
    ax.set_axisbelow(True)
