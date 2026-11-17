"""Figure gpal_revenus_irreguliers : à revenu cumulé égal (250 000 € en 5 ans), impôt payé par A (50 000 € par an) et
par B (10, 20, 30, 70, 120 k€), avec le barème final du nouvel impôt, et effet d'un lissage sur 3 ou 5 ans.
Charte note8p (gris = référence, ocre = surcoût, bleu clair = variante, bleu foncé = proposition) ; étiquettes directes
sur chaque barre (l'identité ne repose pas sur la seule couleur). Lancer après pal_calculs.py ou seul.
"""
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path[:0] = [str(ICI.parent), str(ICI)]
from charte import AUJ, NAIF, PROP, HAUSSE, ENCRE, ENCRE2, PLEINE, plt, axes, sauver, euros, _fr  # noqa: E402
import pal_revenus as PR  # noqa: E402


def trace(R=None):
    R = R or PR.calcule()
    g = R["regimes"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(PLEINE, 2.4), gridspec_kw={"width_ratios": [1.25, 1]})
    # panneau 1 : impôt de chaque année, droit commun (impôt annuel)
    x = range(1, 6)
    w = 0.38
    ia, ib = g["annuel"]["A"]["par_annee"], g["annuel"]["B"]["par_annee"]
    a1.bar([v - w / 2 - 0.01 for v in x], ia, w, color=AUJ, zorder=2)
    a1.bar([v + w / 2 + 0.01 for v in x], ib, w, color=HAUSSE, zorder=2)
    for v, ya, yb, rb in zip(x, ia, ib, PR.B):
        a1.text(v + w / 2, yb + 600, _fr(yb / 1000, 1) if yb < 10_000 else _fr(yb / 1000), ha="center", fontsize=6.5,
                color=ENCRE)
    a1.text(1 - w / 2, ia[0] + 600, _fr(ia[0] / 1000, 1), ha="center", fontsize=6.5, color=ENCRE)
    a1.set_xticks(list(x))
    a1.set_xticklabels([f"An {v}\n{_fr(r/1000)} k€" for v, r in zip(x, PR.B)], fontsize=6.8)
    a1.yaxis.set_major_formatter(lambda v, _: _fr(v / 1000) + " k€")
    a1.set_ylim(0, 41_000)
    a1.text(0.55, 38_500, "Impôt payé chaque année", fontsize=7, color=ENCRE2)
    a1.text(1.55, 15_500, "A : 50 k€ chaque année", fontsize=7, color=ENCRE2)
    a1.text(3.0, 26_000, "B (revenu de l'année\nsous l'axe)", fontsize=7, color=HAUSSE, ha="center")
    axes(a1)
    # panneau 2 : total sur cinq ans
    lab = ["A", "B, impôt annuel", "B, lissage sur 3 ans", "B, lissage sur 5 ans"]
    val = [g["annuel"]["A"]["total"], g["annuel"]["B"]["total"], g["glissant_3"]["B"]["total"],
           g["quotient_5"]["B"]["total"]]
    col = [AUJ, HAUSSE, NAIF, PROP]
    y = list(range(len(lab)))[::-1]
    a2.barh(y, val, 0.62, color=col, zorder=2)
    for yy, v in zip(y, val):
        d = v - val[0]
        s = _fr(v / 1000, 1) + " k€" + ((f"  (+{_fr(d / 1000, 1)} k€)" if d > 0.5 else "  (même impôt que A)") if yy != y[0] else "")
        a2.text(v + 800, yy, s, va="center", fontsize=6.8, color=ENCRE)
    a2.set_yticks(y)
    a2.set_yticklabels(lab, fontsize=7)
    a2.set_xlim(0, 85_000)
    a2.xaxis.set_major_formatter(lambda v, _: _fr(v / 1000) + " k€")
    a2.text(0, 3.55, "Impôt total sur cinq ans (écart avec A)", fontsize=7, color=ENCRE2)
    axes(a2, grille="x")
    fig.tight_layout(w_pad=1.5)
    src = (r"calculs des auteurs, \texttt{note8p/calculs/pal\_revenus.py}, barème final du nouvel impôt ("
           + R["bareme"]["source"].replace("_", r"\_") + ").")
    note = (r"Personne seule, revenus après cotisations, cumul de 250\,000~€ sur cinq ans pour A et B. Lissage sur 3 ans :"
            r" sur toute période de trois ans, l'impôt payé est celui de trois années au revenu moyen. Lissage sur 5 ans :"
            r" option pour cinq ans, impôt total égal à cinq fois l'impôt du revenu moyen, payé au fil des années.")
    sauver(fig, "gpal_revenus_irreguliers", src, note)
    return val


if __name__ == "__main__":
    print(trace())
