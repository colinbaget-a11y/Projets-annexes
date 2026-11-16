"""Figures de la partie « Revenus du capital » de la note fusionnée (préfixe pfu_n, refonte du 16/11/2026).

Chiffres : pfu/sorties/calculs_pfu.json (pfu/calculs_pfu.py). Couleurs : synthese/style_note.py (aujourd'hui en
encre grise, réforme naïve en brique, proposition en bleu, variante en ocre, élément secondaire en gris clair).
Lancer depuis fiscalite/, après pfu/calculs_pfu.py :
    python3 pfu/figures_pfu_n.py && FIG_NU=1 python3 pfu/figures_pfu_n.py
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RACINE = HERE.parent
sys.path[:0] = [str(RACINE), str(RACINE / "synthese")]
from graphiques import ECH_TXT, fin, plt  # noqa: E402
from style_note import AUJ, ENCRE, ENCRE2, NAIF, NUANCES_BLEU, PROP, SEC, VAR, _fr, axes_propres  # noqa: E402

J = json.loads((HERE / "sorties/calculs_pfu.json").read_text(encoding="utf-8"))
TXT = 10.3                     # textes mis à l'échelle par graphiques (≈ 8 pt imprimés en mode nu)
plt.rcParams.update({k: TXT * ECH_TXT for k in ("xtick.labelsize", "ytick.labelsize", "axes.labelsize",
                                                 "legend.fontsize")})
SRC_CALC = "calculs de l'auteur (pfu/calculs_pfu.py)."


def sans_cadre(ax, garder=("bottom",)):
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(s in garder)
    ax.spines["bottom"].set_color("#8a8984")
    ax.tick_params(colors=ENCRE2, length=0)


def valeur(ax, x, y, txt, ha="left", dx=4, col=ENCRE, gras=False, va="center"):
    ax.annotate(txt, (x, y), xytext=(dx if ha == "left" else -dx, 0), textcoords="offset points", ha=ha, va=va,
                fontsize=TXT, color=col, fontweight="bold" if gras else "normal", annotation_clip=False)


# ---------------------------------------------------------------------------------------------------------- n01
def n01_assiette():
    a = J["assiette"]
    lignes = [("Dividendes", a["dividendes"], AUJ), ("Intérêts et autres distributions", a["interets"], AUJ),
              ("Plus-values imposées (nettes des pertes)", a["pv"], AUJ),
              ("Plus-values placées en report d'apport-cession", a["report"], SEC),
              ("Reports arrivés à échéance (imposés)", a["expires"], SEC)]
    fig, ax = plt.subplots(figsize=(9.0, 3.0))
    y = np.arange(len(lignes))[::-1]
    for yi, (lab, v, col) in zip(y, lignes):
        ax.barh(yi, v, color=col, height=0.62, zorder=3, edgecolor="white", linewidth=1.2)
        valeur(ax, v, yi, _fr(v, 1) + " Md€")
    ax.set_yticks(y)
    ax.set_yticklabels([l[0] for l in lignes])
    ax.set_xlim(0, 58)
    ax.set_xticks([])
    sans_cadre(ax, ("left",))
    ax.spines["left"].set_color("#8a8984")
    ax.annotate("non imposées l'année de la vente", (a["report"], y[3]), xytext=(48, 0), textcoords="offset points",
                va="center", fontsize=TXT, color=ENCRE2, style="italic")
    fin(fig, "pfu_n01_assiette",
        "Sources : DGFiP, totaux des déclarations 2042 des revenus de 2024 (cases 2DC, 2TR, 2TS, 3VG, 3AN, 3VH, 3WH) ; "
        "Assemblée nationale, rapport n° 3056 (2026), tableau de la DGFiP pour les reports arrivés à échéance ; "
        + SRC_CALC,
        "Note : revenus de 2024 soumis au prélèvement forfaitaire unique (79,6 Md€ au total), y compris ceux des "
        "2,5 millions de foyers qui ont choisi le barème. Les plus-values placées en report sont celles d'entrepreneurs "
        "qui ont apporté leurs titres à leur holding avant de les vendre ; le stock en report atteint 127 à 173 Md€.")


# ---------------------------------------------------------------------------------------------------------- n02
def n02_concentration():
    c = J["concentration"]
    lignes = [("Part des foyers", c["foyers"], SEC), ("Dividendes déclarés (2021)", c["dividendes"], AUJ),
              ("Plus-values mises en report (2023)", c["pv_report_2023"], AUJ),
              ("Plus-values imposées (2021)", c["pv_droit_commun"], AUJ)]
    fig, ax = plt.subplots(figsize=(9.0, 2.5))
    y = np.arange(len(lignes))[::-1]
    for yi, (lab, v, col) in zip(y, lignes):
        ax.barh(yi, max(v, 0.25), color=col, height=0.6, zorder=3)
        valeur(ax, max(v, 0.25), yi, _fr(v, 2 if v < 1 else 0) + " %")
    ax.set_yticks(y)
    ax.set_yticklabels([l[0] for l in lignes])
    ax.set_xlim(0, 85)
    ax.set_xticks([])
    sans_cadre(ax, ("left",))
    ax.spines["left"].set_color("#8a8984")
    fin(fig, "pfu_n02_concentration",
        "Sources : France Stratégie, comité d'évaluation des réformes de la fiscalité du capital, rapport final "
        "(2023), données POTE 2021 ; Assemblée nationale, rapport n° 3056 (2026), d'après la DGFiP, pour les "
        "plus-values mises en report en 2023.",
        "Note : part reçue par les 0,01 % de foyers fiscaux au revenu le plus élevé, soit environ 4 000 foyers. "
        "Le 1 % le plus aisé déclare 96 % des dividendes ; 84 foyers ont mis en report 70 % des plus-values de 2023.")


# ---------------------------------------------------------------------------------------------------------- n03
def n03_taux():
    t = J["taux"]
    lignes = [("Bénéfice distribué, PFU de 31,4 %", t["distribue"], AUJ, 0),
              ("Distribué, foyer à la CEHR (35,4 %)", t["cehr"], AUJ, 1),
              ("Distribué, foyer à la CDHR (38,6 %)", t["cdhr"], AUJ, 2),
              ("Gardé dans une holding (quote-part de 1,25 %)", t["holding"], AUJ, 3.4),
              ("Pour comparaison : salaire, taux marginal supérieur", t["salaire"], SEC, 4.8)]
    fig, ax = plt.subplots(figsize=(9.0, 2.9))
    for lab, v, col, yi in lignes:
        ax.barh(yi, v, color=col, height=0.62, zorder=3)
        valeur(ax, v, yi, _fr(v, 1) + " %")
    ax.set_yticks([l[3] for l in lignes])
    ax.set_yticklabels([l[0] for l in lignes])
    ax.set_ylim(5.4, -0.5)
    ax.set_xlim(0, 64)
    ax.set_xticks([])
    sans_cadre(ax, ("left",))
    ax.spines["left"].set_color("#8a8984")
    fin(fig, "pfu_n03_taux_cumules",
        "Sources : code général des impôts ; LFSS et LF pour 2026 ; " + SRC_CALC,
        "Note : impôt total sur 100 € de bénéfice avant impôt, droit de 2026, pour une société qui paie l'IS de 25 % "
        "et la contribution sociale de 3,3 % (25,8 %). Entre parenthèses, le taux du prélèvement personnel. Le "
        "salaire est imposé au taux marginal supérieur de l'IR, de la CEHR et de la CSG-CRDS, hors cotisations "
        "sociales, qui l'alourdiraient encore (comparaison favorable au capital).")


# ---------------------------------------------------------------------------------------------------------- n04
def n04_europe():
    e = J["europe"]
    noms = {"Ireland": "Irlande", "Denmark": "Danemark", "United Kingdom": "Royaume-Uni", "Norway": "Norvège",
            "Portugal": "Portugal", "Netherlands": "Pays-Bas", "Germany": "Allemagne", "Belgium": "Belgique",
            "Spain": "Espagne", "Italy": "Italie", "Sweden": "Suède", "Switzerland": "Suisse", "Estonia": "Estonie"}
    sel = [(noms[n], v, SEC) for n, v in e["autres"] if n in noms]
    sel += [("France 2026 (IS de 25,8 %)", e["france26"], AUJ), ("France 2025 (IS de 25,8 %)", e["france25"], AUJ),
            ("Moyenne de 31 pays européens", e["moyenne"], ENCRE2)]
    sel.sort(key=lambda x: -x[1])
    fig, ax = plt.subplots(figsize=(9.0, 4.3))
    y = np.arange(len(sel))[::-1]
    for yi, (lab, v, col) in zip(y, sel):
        ax.barh(yi, v, color=col, height=0.68, zorder=3, hatch="////" if lab.startswith("Moyenne") else None,
                edgecolor="white" if not lab.startswith("Moyenne") else "white", linewidth=0.6)
        valeur(ax, v, yi, _fr(v, 1), dx=3)
    ax.set_yticks(y)
    ax.set_yticklabels([s[0] for s in sel])
    for tl, s in zip(ax.get_yticklabels(), sel):
        if s[0].startswith("France"):
            tl.set_fontweight("bold")
    ax.set_xlim(0, 64)
    ax.set_xticks([])
    sans_cadre(ax, ("left",))
    ax.spines["left"].set_color("#8a8984")
    fin(fig, "pfu_n04_europe",
        "Sources : Tax Foundation, « Integrated Tax Rates on Corporate Income in Europe, 2025 » (d'après l'OCDE) ; "
        "taux français recalculés par l'auteur (" + "pfu/calculs_pfu.py).",
        "Note : taux supérieur intégré sur le bénéfice distribué en dividendes : IS + (1 − IS) × taux personnel "
        "supérieur, en %. La Tax Foundation retient pour la France l'IS de 36,1 % que paient, avec la contribution "
        "exceptionnelle, les seuls groupes de plus de 3 Md€ de chiffre d'affaires (57,9 %) ; avec l'IS de droit commun "
        "(25,8 %), la France passe "
        "au 5e rang sur 31 en 2025 (PFU de 30 % et CEHR) et au 4e en 2026 (PFU de 31,4 %). Treize pays représentés ; "
        "la moyenne porte sur les 31 pays, France recalculée.")


# ---------------------------------------------------------------------------------------------------------- n05
def n05_serie():
    s = J["serie"]
    an, d = np.array(s["annees"]), np.array(s["div"])
    fig, ax = plt.subplots(figsize=(9.0, 3.6))
    ax.bar(an, d, color=AUJ, width=0.68, zorder=3)
    for a_, v in zip(an, d):
        ax.text(a_, v + 1.2, _fr(v, 0), ha="center", va="bottom", fontsize=TXT * 0.9 * ECH_TXT, color=ENCRE2)
    notes = [(2013, 2013, "2013 : barème obligatoire\n(−34 %)", 52), (2018, 2018, "2018 : PFU\n(+32 %)", 60),
             (2024, 2021.6, "2024 : CDHR en préparation\n(+23 %, puis −14 % en 2025)", 86)]
    for a_, xt, txt, yy in notes:
        ax.annotate(txt, (a_, d[an == a_][0] + 7.5), xytext=(xt, yy), ha="center", va="bottom", fontsize=TXT,
                    color=ENCRE, arrowprops=dict(arrowstyle="-", color=ENCRE2, lw=0.7, shrinkA=1, shrinkB=1))
    ax.set_ylim(0, 102)
    ax.set_xlim(2009.4, 2025.6)
    ax.set_xticks(an)
    ax.set_xticklabels([str(a_) if a_ % 2 == 0 or a_ in (2013, 2025) else "" for a_ in an])
    ax.set_ylabel("Md€ courants", fontsize=TXT, color=ENCRE2)
    axes_propres(ax)
    fin(fig, "pfu_n05_dividendes",
        "Source : Insee, comptes nationaux annuels (base 2020, mai 2026), tableau 7.401, dividendes (D421) reçus "
        "par les ménages.",
        "Note : rapportés à l'excédent brut d'exploitation des sociétés non financières, ces dividendes passent de "
        "14,0 % en 2012 à 9,0 % en 2013, de 9,2 % en 2017 à 12,1 % en 2018, et de 12,5 % en 2023 à 15,0 % en 2024 "
        "puis 12,9 % en 2025 : les variations ne tiennent pas aux bénéfices. Le bond de 2024 précède la "
        "contribution différentielle (CDHR), annoncée à l'automne 2024 et votée début 2025 pour les revenus de 2025 ; "
        "l'Insee y voit une possible anticipation.")


# ---------------------------------------------------------------------------------------------------------- n06
def n06_naif():
    n = J["naif"]
    b = J["bareme"]
    p25, p33 = n["PFU 25 % 2024"], n["PFU 33 % 2024"]
    groupes = [("PFU ramené à 25 %", p25["meca"], p25["prem"][1], (min(p25["prem"]), max(p25["prem"])),
                (min(p25["perm_077"]), max(p25["perm_077"]))),
               ("PFU porté à 33 %", p33["meca"], p33["prem"][1], (min(p33["prem"]), max(p33["prem"])),
                (min(p33["perm_077"]), max(p33["perm_077"]))),
               ("Retour au barème", b["statique"], b["0.77"], (b["1.0"], b["0.65"]), None)]
    fig, ax = plt.subplots(figsize=(9.0, 3.6))
    x = np.arange(len(groupes))
    w = 0.34
    for i, (lab, meca, net, fr_net, fr_perm) in enumerate(groupes):
        ax.bar(x[i] - w / 2 - 0.02, meca, width=w, color=SEC, zorder=3)
        ax.bar(x[i] + w / 2 + 0.02, net, width=w, color=NAIF, zorder=3)
        ax.errorbar(x[i] + w / 2 + 0.02, net, yerr=[[net - fr_net[0]], [fr_net[1] - net]], fmt="none",
                    ecolor=ENCRE, elinewidth=0.9, capsize=3, zorder=4)
        off = 6 if meca >= 0 else -8
        ax.annotate(_fr(meca, 1), (x[i] - w / 2 - 0.02, meca), xytext=(0, off), textcoords="offset points",
                    ha="center", va="bottom" if meca >= 0 else "top", fontsize=TXT, color=ENCRE2)
        ax.annotate(_fr(net, 1), (x[i] + w / 2 + 0.02, fr_net[1] if net >= 0 else fr_net[0]), xytext=(0, off),
                    textcoords="offset points", ha="center", va="bottom" if net >= 0 else "top", fontsize=TXT,
                    color=ENCRE, fontweight="bold")
    ax.axhline(0, color=ENCRE2, lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([g[0] for g in groupes])
    ax.set_ylim(-7.5, 15.5)
    ax.set_ylabel("Md€ par an (+ recette, − coût)", fontsize=TXT, color=ENCRE2)
    axes_propres(ax)
    ax.tick_params(axis="x", length=0)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=SEC, label="À comportements inchangés"),
                       Patch(color=NAIF, label="Après réaction des revenus déclarés (premières années)")],
              loc="upper left", frameon=False, fontsize=TXT * ECH_TXT)
    fin(fig, "pfu_n06_reforme_naive",
        "Sources : DGFiP, déclarations 2042 des revenus de 2024 (assiette de 79,6 Md€) ; Lefebvre, Lehmann et Sicsic "
        "(2025) et CAE (2025) pour l'élasticité ; " + SRC_CALC,
        "Note : traits : élasticité des revenus du capital au taux net de 0,65 à 1 (0,77 au centre). Les chiffres "
        "portent sur les premières années, où toute la réaction compte comme recette. En régime permanent, si la "
        "réaction n'est qu'un décalage dans le temps, un PFU à 25 % coûte jusqu'à 5,1 Md€ et un PFU à 33 % rapporte "
        "jusqu'à 1,3 Md€. Retour au barème : ordre de grandeur sous hypothèses fortes (annexe) ; sur la base de 2025, "
        "tous les montants baissent d'environ 9 %.")


# ---------------------------------------------------------------------------------------------------------- n07
def n07_holding():
    h = J["holding"]
    cats = ["Distribué tout de suite", "Gardé 25 ans dans la holding,\npuis distribué",
            "Gardé dans la holding,\npuis transmis"]
    auj = [h["A"], h["B"], h["C"]]
    prop = [h["A"], h["B"], h["C_prop"]]
    fig, ax = plt.subplots(figsize=(9.0, 3.4))
    x = np.arange(3)
    w = 0.36
    ax.bar(x - w / 2 - 0.02, auj, width=w, color=AUJ, zorder=3, label="Aujourd'hui")
    ax.bar(x + w / 2 + 0.02, prop, width=w, color=PROP, zorder=3, label="Avec la reprise du prix d'acquisition")
    for xi, v in zip(x, auj):
        ax.annotate(_fr(v, 0) + " %", (xi - w / 2 - 0.02, v), xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=TXT, color=ENCRE)
    for xi, v in zip(x, prop):
        ax.annotate(_fr(v, 0) + " %", (xi + w / 2 + 0.02, v), xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=TXT, color=ENCRE, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    ax.set_ylim(0, 65)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _fr(v, 0) + " %"))
    axes_propres(ax)
    ax.tick_params(axis="x", length=0)
    ax.legend(loc="upper left", frameon=False, ncol=2, fontsize=TXT * ECH_TXT)
    fin(fig, "pfu_n07_holding",
        "Source : " + SRC_CALC[0].upper() + SRC_CALC[1:],
        "Note : impôt total, en valeur actualisée, sur 100 € de bénéfice d'une filiale avant IS (IS de 25,8 %, "
        "quote-part de 1,25 % sur les dividendes remontés, PFU de 31,4 %). La holding place à 5 % par an en "
        "participations ; actualisation au même taux. « Transmis » : les héritiers reprennent la holding ; "
        "aujourd'hui ils peuvent en sortir la valeur sans impôt sur la plus-value (prix d'acquisition réévalué au "
        "décès) ; avec la proposition, ils paient le PFU quand ils la sortent, ici dix ans après.")


# ---------------------------------------------------------------------------------------------------------- n08
def n08_recette():
    pr = J["profil"]
    ans = np.arange(1, 31)
    c, lo, hi = (np.array(pr[k]["prop"][:30]) for k in ("central", "bas", "haut"))
    da = np.array(pr["central"]["droits_acquis"][:30])
    a5 = np.array(pr["central"]["art5"][:30])
    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    ax.fill_between(ans, lo, hi, color=NUANCES_BLEU[5], zorder=1, lw=0)
    ax.plot(ans, c, color=PROP, lw=2.2, zorder=3)
    ax.plot(ans, da, color=VAR, lw=1.8, zorder=3, ls=(0, (5, 2)))
    ax.plot(ans, a5, color=AUJ, lw=1.3, zorder=2, ls=(0, (1.5, 1.5)))
    ax.annotate("Proposition, hypothèses centrales", (30, c[-1]), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=TXT, color=ENCRE, annotation_clip=False)
    ax.annotate("Fourchette basse-haute", (30, hi[-1] * 0.82), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=TXT, color=ENCRE2, annotation_clip=False)
    ax.annotate("Variante : droits acquis\n(gains futurs seulement)", (30, da[-1]), xytext=(6, -2),
                textcoords="offset points", va="center", fontsize=TXT, color=ENCRE, annotation_clip=False)
    ax.annotate("PLF 2027, art. 5 : reports\nimposés à la transmission", (30, a5[-1]), xytext=(6, -6),
                textcoords="offset points", va="center", fontsize=TXT, color=ENCRE, annotation_clip=False)
    ax.set_xlim(1, 30)
    ax.set_ylim(0, 14)
    ax.set_xticks([1, 5, 10, 15, 20, 25, 30])
    ax.set_xlabel("Années après l'entrée en vigueur", fontsize=TXT, color=ENCRE2)
    ax.set_ylabel("Md€ par an", fontsize=TXT, color=ENCRE2)
    axes_propres(ax)
    fin(fig, "pfu_n08_recette",
        "Sources : Banque de France (titres détenus par les ménages, fin 2025) ; CAE, note n° 69 (2021) ; Assemblée "
        "nationale, rapport n° 3056, et évaluation préalable du PLF 2027 (stock de reports) ; " + SRC_CALC,
        "Note : recette de la reprise du prix d'acquisition à la donation et au décès, y compris le report "
        "d'apport-cession transmis sans effacement. L'impôt n'est payé que lorsque l'héritier vend ; hypothèses "
        "centrales : 2,3 % des titres transmis chaque année, 55 % de plus-value latente, 30 % vendus dans l'année, "
        "4 % par an ensuite. Valeur des titres supposée constante (prudent). Ordre de grandeur : aucune statistique "
        "publique ne mesure les plus-values effacées.")


# ---------------------------------------------------------------------------------------------------------- n09
def n09_entrepreneur():
    e = J["entrepreneur"]["0.035_20"]
    lignes = [("Cession directe, sans holding", e["directe"], AUJ),
              ("Apport-cession, droit actuel (effacé au décès)", e["actuel"], AUJ),
              ("Report expiré au décès (PLF 2027, art. 5)", e["art5"], VAR),
              ("Report transmis sans effacement (proposition)", e["transmis"], PROP),
              ("Report transmis avec intérêt sur l'impôt différé", e["interet"], VAR)]
    fig, ax = plt.subplots(figsize=(9.0, 3.0))
    y = np.arange(len(lignes))[::-1]
    for yi, (lab, v, col) in zip(y, lignes):
        ax.barh(yi, max(v / 1e6, 0.02), color=col, height=0.62, zorder=3)
        valeur(ax, max(v / 1e6, 0.02), yi, _fr(v / 1e6, 2) + " M€")
    ax.set_yticks(y)
    ax.set_yticklabels([l[0] for l in lignes])
    ax.set_xlim(0, 2.9)
    ax.set_xticks([])
    sans_cadre(ax, ("left",))
    ax.spines["left"].set_color("#8a8984")
    fin(fig, "pfu_n09_entrepreneur",
        "Source : " + SRC_CALC[0].upper() + SRC_CALC[1:],
        "Note : valeur actualisée (taux de 3,5 %) de l'impôt sur une plus-value de 7,5 M€ au PFU de 31,4 %. "
        "L'entrepreneur meurt vingt ans après la cession ; ses héritiers vendent les titres de la holding avec une "
        "probabilité de 4 % par an ; l'intérêt court depuis le décès, au taux d'actualisation. Variantes en annexe.")


# ---------------------------------------------------------------------------------------------------------- n10
def n10_sensibilite():
    s = J["sensibilite"]
    ref = s["ref"][0]
    par = sorted(s["par"].values(), key=lambda d: abs(d["haut"][0] - d["bas"][0]))
    fig, ax = plt.subplots(figsize=(9.0, 3.4))
    y = np.arange(len(par))
    for yi, d in zip(y, par):
        lo, hi = d["bas"][0], d["haut"][0]
        ax.barh(yi, lo - ref, left=ref, color=NUANCES_BLEU[4], height=0.6, zorder=3)
        ax.barh(yi, hi - ref, left=ref, color=NUANCES_BLEU[1], height=0.6, zorder=3)
        valeur(ax, min(lo, hi), yi, _fr(min(lo, hi), 1), ha="right", dx=3, col=ENCRE2)
        valeur(ax, max(lo, hi), yi, _fr(max(lo, hi), 1), dx=3, col=ENCRE2)
    ax.axvline(ref, color=ENCRE, lw=0.9, zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels([d["nom"] for d in par])
    ax.set_xlim(2.2, 5.2)
    ax.set_xticks([2.5, 3, 3.5, 4, 4.5, 5])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _fr(v, 1)))
    ax.set_xlabel("Recette la dixième année (Md€)", fontsize=TXT, color=ENCRE2)
    axes_propres(ax, grille="x")
    fin(fig, "pfu_n10_sensibilite",
        "Source : " + SRC_CALC[0].upper() + SRC_CALC[1:],
        "Note : chaque barre fait varier un seul paramètre entre ses valeurs basse (bleu clair) et haute (bleu "
        "foncé), les autres restant au centre (" + _fr(ref, 1) + " Md€, trait vertical). Valeurs : titres couverts "
        "1 200 / 1 450 / 1 700 Md€ ; part transmise 1,7 / 2,3 / 3 % par an ; plus-value latente 40 / 55 / 70 % ; "
        "ventes la première année 15 / 30 / 45 % ; ventes ensuite 2 / 4 / 6 % par an ; stock de reports 127 / 144 / "
        "173 Md€ ; délai avant transmission 35 / 25 / 15 ans.")


if __name__ == "__main__":
    for f in (n01_assiette, n02_concentration, n03_taux, n04_europe, n05_serie, n06_naif, n07_holding,
              n08_recette, n09_entrepreneur, n10_sensibilite):
        f()
