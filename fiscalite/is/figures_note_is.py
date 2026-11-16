"""Figures de la partie IS de la note de synthèse (refonte du 16/11/2026) : is_n01 à is_n09.

Lancer depuis fiscalite/, après is/calculs_note_is.py :
    python3 is/figures_note_is.py ; FIG_NU=1 python3 is/figures_note_is.py
Chiffres : is/sorties/calculs_note_is.json ; couleurs : synthese/style_note.py (aujourd'hui = encre grise, réforme
naïve = brique, proposition = bleu, variante = ocre). Sources et notes de lecture : passées à fin(), écrites dans
figures/nu/<nom>_note.tex en mode nu, jamais dans l'image.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parent / "synthese")]
from graphiques import ECH_TXT, NU, fin, plt  # noqa: E402
from style_note import AUJ, ENCRE, ENCRE2, NAIF, PROP, SEC, VAR, axes_propres  # noqa: E402

J = json.loads((HERE / "sorties" / "calculs_note_is.json").read_text(encoding="utf-8"))
TXT = 10.0          # taille des étiquettes (mise à l'échelle par graphiques en mode nu)
GRIS_M = "#8a8984"
AN1 = 2027


def f(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def taille_ticks(ax, s=9.5):
    ax.tick_params(labelsize=s * ECH_TXT)


SRC_SIM = "calculs de l'auteur (fiscalite/is/calculs_note_is.py, mécanique de fiscalite/is/simulation_is.py)"

# ------------------------------------------------------------------ n01 : recette de l'IS dans l'OCDE
NOMS = {"AUS": "Australie", "AUT": "Autriche", "BEL": "Belgique", "CAN": "Canada", "CHL": "Chili", "COL": "Colombie",
        "CRI": "Costa Rica", "CZE": "Tchéquie", "DNK": "Danemark", "EST": "Estonie", "FIN": "Finlande", "FRA": "France",
        "DEU": "Allemagne", "GRC": "Grèce", "HUN": "Hongrie", "ISL": "Islande", "IRL": "Irlande", "ISR": "Israël",
        "ITA": "Italie", "JPN": "Japon", "KOR": "Corée", "LVA": "Lettonie", "LTU": "Lituanie", "LUX": "Luxembourg",
        "MEX": "Mexique", "NLD": "Pays-Bas", "NZL": "Nouvelle-Zélande", "NOR": "Norvège", "POL": "Pologne",
        "PRT": "Portugal", "SVK": "Slovaquie", "SVN": "Slovénie", "ESP": "Espagne", "SWE": "Suède", "CHE": "Suisse",
        "TUR": "Turquie", "GBR": "Royaume-Uni", "USA": "États-Unis"}
d = J["ocde_2023"]
pays = sorted(d, key=lambda c: -d[c])
v = np.array([d[c] for c in pays])
fig, ax = plt.subplots(figsize=(9.0, 4.2))
cols = [AUJ if c == "FRA" else SEC for c in pays]
ax.bar(range(len(pays)), v, color=cols, width=0.72, zorder=2)
moy = float(np.mean(v))
ax.axhline(moy, color=ENCRE2, lw=0.9, ls=(0, (4, 3)), zorder=3)
ax.text(13.5, moy + 0.15, f"moyenne de l'OCDE : {f(moy, 2)} %", ha="left", va="bottom", fontsize=TXT,
        color=ENCRE)
i_fr = pays.index("FRA")
ax.annotate(f"France : {f(d['FRA'], 2)} %\n{i_fr+1}e sur {len(pays)}", (i_fr, d["FRA"]), xytext=(0, 48),
            textcoords="offset points", ha="center", va="bottom", fontsize=TXT, color=ENCRE,
            arrowprops=dict(arrowstyle="-", color=ENCRE2, lw=0.7))
ax.set_xticks(range(len(pays)))
ax.set_xticklabels([NOMS[c] for c in pays], rotation=90, fontsize=8.0 * ECH_TXT)
ax.set_xlim(-0.6, len(pays) - 0.4)
ax.set_ylabel("% du PIB")
axes_propres(ax)
taille_ticks(ax)
ax.tick_params(axis="x", labelsize=8.0 * ECH_TXT)
fin(fig, "is_n01_ocde_recette",
    "Source : OCDE, Revenue Statistics (jeu DSD_REV_COMP_OECD@DF_RSOECD, rubrique 1200, impôts sur le revenu, les "
    "bénéfices et les gains en capital des sociétés, toutes administrations publiques), téléchargé le 16/11/2026 ; "
    "extraction : fiscalite/is/donnees/extraire_ocde_is_pib.py.",
    f"Note : année 2023, la dernière disponible pour les 38 pays. Médiane de l'OCDE : {f(float(np.median(v)), 2)} %. "
    "Pour la France, 2,85 % en 2022 (année de bénéfices exceptionnels) et 2,25 % en 2024 (31e sur 36). La contribution "
    "exceptionnelle sur les grands groupes, perçue en 2025 et 2026, n'est pas encore dans ces chiffres. Plusieurs pays "
    "du haut du classement doivent leur rang à des ressources naturelles ou à des bénéfices de multinationales "
    "localisés chez eux.")

# ------------------------------------------------------------------ n02 : qui paie
q = J["qui_paie"]
cats = ["Très petites", "PME", "ETI", "Grandes"]
lib = {"Très petites": "Très petites\nentreprises", "PME": "PME", "ETI": "Entreprises de taille\nintermédiaire",
       "Grandes": "Grandes\nentreprises"}
DE = {"Très petites": " d'", "PME": " ", "ETI": " ", "Grandes": " "}
nb = {"Très petites": "2,6 millions", "PME": "220 000", "ETI": "8 700", "Grandes": "370"}
fig, ax = plt.subplots(figsize=(9.0, 3.4))
y = np.arange(len(cats))[::-1]
parts = [100 * q[c]["part"] for c in cats]
ax.barh(y, parts, color=AUJ, height=0.56, zorder=2)
for yi, c, pv in zip(y, cats, parts):
    ax.text(pv + 0.6, yi, f"{f(pv, 0)} % de l'IS ({f(q[c]['is_brut'])} Md€), payés par {nb[c]}{DE[c]}entreprises",
            va="center", ha="left", fontsize=TXT, color=ENCRE)
ax.set_yticks(y)
ax.set_yticklabels([lib[c] for c in cats], fontsize=9.5 * ECH_TXT)
ax.set_xlim(0, 62)
ax.set_xticks([0, 10, 20, 30])
ax.set_xticklabels(["0 %", "10 %", "20 %", "30 %"])
axes_propres(ax, grille="x")
taille_ticks(ax)
rf = [f(100 * q[c]["part_resultat"], 0) for c in cats]
fin(fig, "is_n02_qui_paie",
    "Source : DGFiP, Statistiques n° 51 (septembre 2026), tableau 2, exercice 2025 (données provisoires).",
    f"Note : IS brut, avant crédits et réductions d'impôt ({f(sum(q[c]['is_brut'] for c in cats))} Md€ en 2025). "
    "Catégories d'entreprises du décret n° 2008-1354 (une entreprise peut regrouper plusieurs sociétés). Le résultat "
    f"fiscal (bénéfices moins déficits) se répartit en {rf[0]}, {rf[1]}, {rf[2]} et {rf[3]} %. En 2022, la répartition de "
    "l'IS brut était presque la même (19, 28, 23 et 30 %). La contribution exceptionnelle de 2025 et 2026 (7,5 Md€ en "
    "2025) s'ajoute pour les seuls groupes de plus de 1 Md€ de chiffre d'affaires.")

# ------------------------------------------------------------------ n03 : taux affiché, taux sur le bénéfice, taux sur l'excédent
cat3 = [("Microentreprises", 13.1 / 60.3, 19.0), ("PME", 18.9 / 75.9, 21.4), ("Grandes entreprises", 20.6 / 79.5, 14.3)]
fig, ax = plt.subplots(figsize=(9.0, 3.9))
x = np.arange(len(cat3))
w = 0.34
b1 = ax.bar(x - w / 2 - 0.01, [100 * c[1] for c in cat3], w, color=AUJ, zorder=2, label="IS brut / bénéfice fiscal")
b2 = ax.bar(x + w / 2 + 0.01, [c[2] for c in cat3], w, color=SEC, zorder=2, label="IS brut / excédent net d'exploitation")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5, f"{f(b.get_height())} %", ha="center",
                va="bottom", fontsize=TXT, color=ENCRE)
ax.axhline(25, color=ENCRE2, lw=0.9, ls=(0, (4, 3)), zorder=3)
ax.text(2.62, 25.4, "taux normal : 25 %", ha="right", va="bottom", fontsize=TXT, color=ENCRE)
ax.axhline(36.13, color=ENCRE2, lw=0.9, ls=(0, (1, 2)), zorder=3)
ax.text(2.62, 36.5, "plus grands groupes en 2025-2026 : 36,1 %", ha="right", va="bottom", fontsize=TXT, color=ENCRE)
ax.set_xticks(x)
ax.set_xticklabels([c[0] for c in cat3], fontsize=9.5 * ECH_TXT)
ax.set_ylim(0, 47)
ax.set_yticks([0, 10, 20, 30, 40])
ax.set_yticklabels(["0 %", "10 %", "20 %", "30 %", "40 %"])
ax.set_xlim(-0.55, 2.65)
axes_propres(ax)
taille_ticks(ax)
ax.legend(loc="upper left", frameon=False, fontsize=9.5 * ECH_TXT if NU else 9.5, ncol=2)
fin(fig, "is_n03_taux",
    "Sources : DGFiP, Statistiques n° 21, tableau 2 (IS brut et bénéfices, 2022) ; Insee Analyses n° 112 (septembre "
    "2025), taux implicites 2022.",
    "Note : IS brut avant crédits d'impôt. Bénéfice fiscal : somme des bénéfices des sociétés bénéficiaires, après "
    "imputation des déficits reportés. Excédent net d'exploitation : ce que dégage l'activité, avant intérêts et "
    "impôt, au sens de la comptabilité nationale (Insee). Les deux sources ne mesurent pas exactement le même champ. "
    "Le taux réduit de 15 % (bénéfice jusqu'à 42 500 €) explique l'essentiel du taux plus bas des microentreprises sur "
    "leur bénéfice. Année 2022 : la dernière pour laquelle l'Insee publie ces taux implicites ; en 2024 (DGFiP n° 39), "
    "l'IS brut représente 21,2, 24,5 et 26,1 % du bénéfice fiscal des trois catégories.")

# ------------------------------------------------------------------ n04 : à coût égal (réforme naïve)
T = J["tef"]
k_eq = [k for k in T if "même coût actualisé" in k][0]
barres = [("Aujourd'hui\n(taux de 25 %)", T["Équipement, aujourd'hui (25 %, linéaire 7 ans)"]["temi"], AUJ, ""),
          (f"Taux à {f(25 - J['x_eq'], 0)} %\n2,6 Md€ par an", T[k_eq]["temi"], NAIF, ""),
          (f"Taux à 22 %\n{f(J['naif']['3'][0], 0)} Md€ par an", T["Équipement, baisse à 22 %"]["temi"], NAIF, ""),
          (f"Taux à 20 %\n{f(J['naif']['5'][0], 0)} Md€ par an", T["Équipement, baisse à 20 %"]["temi"], NAIF, ""),
          ("Déduction\nimmédiate\n2,6 Md€ actualisés",
           T["Équipement, déduction immédiate 100 % (25 %)"]["temi"], PROP, "")]
fig, ax = plt.subplots(figsize=(9.0, 3.9))
for i, (nom, val, col, cout) in enumerate(barres):
    ax.bar(i, 100 * val, 0.56, color=col, zorder=2)
    lab = f"{f(100*val)} %" if val > 0.001 else "0 %"
    ax.text(i, 100 * val + 0.5, lab, ha="center", va="bottom", fontsize=TXT, color=ENCRE)
    if cout:
        ax.text(i, -2.2, cout, ha="center", va="top", fontsize=TXT * 0.92, color=ENCRE2, linespacing=1.3)
    if val < 0.001:
        ax.bar(i, 0.35, 0.56, color=col, zorder=2)
ax.set_xticks(range(len(barres)))
ax.set_xticklabels([b[0] for b in barres], fontsize=9.5 * ECH_TXT)
ax.set_ylim(0, 25)
ax.set_yticks([0, 5, 10, 15, 20, 25])
ax.set_yticklabels([f"{t} %" for t in (0, 5, 10, 15, 20, 25)])
ax.set_ylabel("Taux effectif marginal")
axes_propres(ax)
taille_ticks(ax)
ax.tick_params(axis="x", labelsize=9.5 * ECH_TXT)
fin(fig, "is_n04_cout_egal",
    "Source : " + SRC_SIM + ".",
    "Note : taux effectif marginal d'une machine qui rapporte tout juste ce qu'exigent ses financeurs (méthode de "
    "Devereux et Griffith, 2003) : financement par fonds propres, rendement réel exigé de 5 %, inflation de 2 %, usure "
    "de 14 % par an, amortissement linéaire sur sept ans aujourd'hui. Ces conventions ne sont pas celles de l'OCDE "
    "(9,8 % pour les équipements en 2025) : seuls les écarts entre barres comptent. Coûts en 2027 : la baisse du taux "
    f"normal, taux réduit gardé, coûte {f(J['naif']['1'][0], 2)} Md€ par point avant toute réaction des bénéfices déclarés "
    "(bénéfices de 2025 portés en 2027) ; la déduction "
    "immédiate de tous les équipements coûte 1,7 à 2,6 Md€ par année d'achats en valeur actualisée au taux des "
    "entreprises (5 %). Le taux de 24 % est la baisse qui coûte autant.")

# ------------------------------------------------------------------ n05 : avant / après
cas = [("Équipement\nsociété au taux normal", T["Équipement, aujourd'hui (25 %, linéaire 7 ans)"]["temi"], 0.0),
       ("Équipement\npetite société\nsous 42 500 €", T["Équipement, petite société sous 42 500 € aujourd'hui (15 %)"]["temi"], 0.0),
       ("Bâtiment\nsociété au taux normal", T["Bâtiment, aujourd'hui (25 %)"]["temi"], T["Bâtiment, aujourd'hui (25 %)"]["temi"]),
       ("Bâtiment\npetite société\nsous 42 500 €", T["Bâtiment, petite société sous 42 500 € aujourd'hui (15 %)"]["temi"],
        T["Bâtiment, aujourd'hui (25 %)"]["temi"])]
fig, ax = plt.subplots(figsize=(9.0, 3.9))
x = np.arange(len(cas))
w = 0.34
for j, (lab_s, col, k) in enumerate((("Aujourd'hui", AUJ, 1), ("Proposition (2032)", PROP, 2))):
    vals = [100 * c[k] for c in cas]
    bars = ax.bar(x + (j - 0.5) * (w + 0.02), vals, w, color=col, zorder=2, label=lab_s)
    for b, vv in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, vv + 0.5, f"{f(vv)} %" if vv > 0.01 else "0 %", ha="center",
                va="bottom", fontsize=TXT, color=ENCRE)
ax.set_xticks(x)
ax.set_xticklabels([c[0] for c in cas], fontsize=9.3 * ECH_TXT, linespacing=1.05)
ax.set_ylim(0, 27)
ax.set_yticks([0, 5, 10, 15, 20, 25])
ax.set_yticklabels([f"{t} %" for t in (0, 5, 10, 15, 20, 25)])
ax.set_ylabel("Taux effectif marginal")
axes_propres(ax)
taille_ticks(ax)
ax.tick_params(axis="x", labelsize=9.3 * ECH_TXT)
ax.legend(loc="upper left", frameon=False, fontsize=9.5 * ECH_TXT if NU else 9.5, ncol=2)
fin(fig, "is_n05_avant_apres",
    "Source : " + SRC_SIM + ".",
    "Note : mêmes conventions que la figure précédente ; bâtiment amorti sur 25 ans, usure de 3,1 % par an. "
    "« Petite société sous 42 500 € » : bénéfice inférieur au plafond du taux réduit, donc taxé à 15 % à la marge "
    "aujourd'hui, à 25 % avec la proposition. Proposition en 2032, quand la déduction atteint 100 % au-delà du "
    "plafond, avant la baisse finale du taux (0,6 à 1,2 point, qui ramènerait le bâtiment vers 21 %). Pour une "
    "société qui amortit aujourd'hui en dégressif, l'équipement est taxé à 15 % au lieu de 20,7 %. Les stocks et "
    "le besoin en fonds de roulement des petites sociétés suivent le même sort que leurs bâtiments.")

# ------------------------------------------------------------------ n06 : calendriers et coût annuel
S = J["series"]
N = 19
ans = AN1 + np.arange(N)
fig, ax = plt.subplots(figsize=(9.0, 4.1))
res = np.array(J["series_fin"]["central"][:N])
ax.fill_between(ans, J["series_fin"]["bas"][:N], J["series_fin"]["haut"][:N], color=SEC, alpha=0.35, lw=0, zorder=1)
ax.text(ans[-1] - 0.2, J["series_fin"]["haut"][N - 1] + 0.25, "Ressources de l'assiette", ha="right", va="bottom",
        fontsize=TXT, color=ENCRE)
for cle, col, lw, ls, lab, xy in (
        ("falaise", AUJ, 1.4, (0, (4, 2)), "Ancien calendrier : 50 % puis\n100 % en 2033", (2033.25, None)),
        ("cent", VAR, 1.6, "-", "100 % pour tous dès 2027", (2027.2, None)),
        ("plafond_paliers", PROP, 2.4, "-", "Proposition : 100 % sous\nplafond, paliers au-delà", (2029.0, None))):
    yv = np.array(S[cle]["mix"][:N])
    ax.plot(ans, yv, color=col, lw=lw, ls=ls, zorder=4, solid_capstyle="round")
ym = np.array(S["falaise"]["mix"][:N])
ax.annotate("Ancien calendrier : 50 %,\npuis 100 % en 2033", (2033, ym[6]), xytext=(14, 4), textcoords="offset points",
            ha="left", va="center", fontsize=TXT, color=ENCRE, linespacing=1.05)
yc = np.array(S["cent"]["mix"][:N])
ax.annotate("100 % pour tous dès 2027", (2027, yc[0]), xytext=(10, 2), textcoords="offset points", ha="left",
            va="center", fontsize=TXT, color=ENCRE)
yp = np.array(S["plafond_paliers"]["mix"][:N])
ax.text(2039.6, yp[12] + 0.55, "Proposition : 100 % sous le plafond,\n+10 points par an au-delà", ha="left",
        va="bottom", fontsize=TXT, color=ENCRE, linespacing=1.05)
ax.set_xlim(ans[0] - 0.3, ans[-1] + 0.3)
ax.set_ylim(0, 16)
ax.set_xticks(ans[::2])
ax.set_ylabel("Md€ courants par an")
axes_propres(ax)
taille_ticks(ax)
fin(fig, "is_n06_calendriers",
    "Source : Insee, comptes nationaux 2025 (tableau 8.212) ; DGFiP Statistiques n° 51 (bénéfices de 2025) ; CPO (2025) ; " + SRC_SIM + ".",
    "Note : coût annuel pour l'État, hors intérêts, d'une déduction immédiate des machines, équipements et matériels "
    "informatiques neufs des sociétés non financières (84 Md€ en 2025, hors matériels de transport), en hausse de 3 % "
    "par an ; 75 % de cet investissement fait par des sociétés imposables (hypothèse) ; régime actuel supposé pour "
    "moitié linéaire, pour moitié dégressif (cas central). Plafond de 1 M€ par groupe et par an, supposé couvrir 20 % "
    "de l'investissement. Sans investissement supplémentaire suscité. Ressources : fin du taux réduit, CIR apprécié au "
    "niveau du groupe, fin des exonérations zonées d'IR et d'IS hors outre-mer, avantage de la boîte à brevets réduit "
    f"de moitié, {f(J['fin']['bas'])} à {f(J['fin']['haut'])} Md€ en 2027 puis +3 % par an. Les trois calendriers ont le "
    "même coût en régime permanent "
    "(1,3 à 2,0 Md€ en 2034).")

# ------------------------------------------------------------------ n07 : cas types
C = J["cas"]
gg = C["Grand groupe"]
lignes = [("Société qui n'investit pas\n(bénéfice 42 500 €)", 100 * C["Société qui n'investit pas"]["net_pct"], PROP),
          ("PME de services\n(bénéfice 40 000 €, achète 10 000 €/an)", 100 * C["PME de services"]["net_pct"], PROP),
          ("PME industrielle\n(bénéfice 300 000 €, achète 150 000 €/an)", 100 * C["PME industrielle"]["net_pct"], PROP),
          ("Grand groupe : la réforme\n(bénéfice 500 M€, achète 300 M€/an)", 100 * gg["net_pct"], PROP),
          ("Grand groupe : fin de la contribution\nexceptionnelle (par rapport à 2026)", -100 * gg["ce"] / gg["is_2026"], VAR)]
fig, ax = plt.subplots(figsize=(9.0, 4.0))
y = np.arange(len(lignes))[::-1]
for yi, (nom, val, col) in zip(y, lignes):
    ax.barh(yi, val, 0.56, color=col, zorder=2)
    ax.text(val + (1.2 if val >= 0 else -1.2), yi, f"{'+' if val > 0 else ''}{f(val, 0)} %", va="center",
            ha="left" if val >= 0 else "right", fontsize=TXT, color=ENCRE)
ax.axvline(0, color=ENCRE2, lw=0.8, zorder=3)
ax.set_yticks(y)
ax.set_yticklabels([l[0] for l in lignes], fontsize=9.0 * ECH_TXT, linespacing=1.05)
ax.set_xlim(-45, 85)
ax.set_xticks([-40, -20, 0, 20, 40, 60, 80])
ax.set_xticklabels(["−40 %", "−20 %", "0", "+20 %", "+40 %", "+60 %", "+80 %"])
ax.set_xlabel("Variation de l'impôt annuel, en % de l'impôt actuel")
axes_propres(ax, grille="x")
taille_ticks(ax)
ax.tick_params(axis="y", labelsize=9.0 * ECH_TXT)
fin(fig, "is_n07_cas_types",
    "Source : " + SRC_SIM + ".",
    "Note : régime permanent, avant la baisse finale du taux. La déduction immédiate ne change pas le total déduit : sa "
    "valeur est celle de l'avance d'impôt, actualisée à 5 % (taux des entreprises), pour une année d'achats ; elle vaut "
    "chaque année 3,8 % des achats d'équipements. La première année, l'avance en trésorerie est bien plus grande : "
    "34 800 € pour la PME industrielle, 2 300 € pour la PME de services, 35 M€ pour le grand groupe. Les PME achètent "
    "sous le plafond de 1 M€ et déduisent 100 % dès 2027. Grand groupe : chiffre d'affaires d'au moins 3 Md€, sans CIR "
    "fractionné ni boîte à brevets ; impôt actuel 129 M€ (taux de 25,8 %), 181 M€ en 2026 avec la contribution "
    "exceptionnelle.")

# ------------------------------------------------------------------ n08 : dette de transition
db = J["dette_bornes"]
dp = J["dette_part"]
N = 30
ans = AN1 + np.arange(N)
fig, ax = plt.subplots(figsize=(9.0, 4.1))
fav, dfav = np.array(db["deg_haut"][:N]), np.array(db["lin_bas"][:N])
cen = np.array(dp["0.75"][:N])
p90 = np.array(dp["0.9"][:N])
ax.fill_between(ans, np.maximum(fav, 0), np.maximum(dfav, 0), color=PROP, alpha=0.14, lw=0, zorder=1)
ax.plot(ans, np.where(cen > -1e-9, cen, np.nan), color=PROP, lw=2.4, zorder=4)
ax.plot(ans, np.where(p90 > -1e-9, p90, np.nan), color=VAR, lw=1.6, ls=(0, (4, 2)), zorder=4)
ax.axhline(0, color=ENCRE2, lw=0.8, zorder=2)
T_ = J["transition"]
ipk = int(np.argmax(cen))
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
ax.legend(handles=[Line2D([], [], color=PROP, lw=2.4, label=f"Cas central : {f(T_['pic'], 0)} Md€ en {T_['an_pic']},\néteinte en {T_['extinction']}"),
                   Patch(color=PROP, alpha=0.14, lw=0, label="Du cas favorable au cas défavorable"),
                   Line2D([], [], color=VAR, lw=1.6, ls=(0, (4, 2)),
                          label="Cas central, si 90 % de l'investissement\nest fait par des sociétés imposables")],
          loc="upper right", frameon=False, fontsize=9.0 * ECH_TXT if NU else 9.0)
ax.set_xlim(ans[0] - 0.3, ans[-1] + 0.3)
ax.set_ylim(0, 47)
ax.set_xticks(ans[::3])
ax.set_ylabel("Md€ courants")
axes_propres(ax)
taille_ticks(ax)
fin(fig, "is_n08_dette",
    "Source : " + SRC_SIM + ".",
    "Note : dette cumulée de la réforme (coût de la déduction moins ressources de l'assiette, intérêts de 3,25 % "
    "compris), avant la baisse finale du taux, qui n'intervient qu'une fois la dette éteinte. Cas central : régime "
    "actuel pour moitié linéaire, pour moitié dégressif, ressources au milieu de la fourchette, 75 % de l'investissement "
    "éligible fait par des sociétés imposables. Cas favorable : dégressif, ressources hautes ; défavorable : linéaire, "
    "ressources basses. Courbe en tirets : cas central avec une part imposable de 90 %. Hors contribution "
    "exceptionnelle, qui s'éteint dans le droit en vigueur.")

# ------------------------------------------------------------------ n09 (annexe) : dette de tous les calendriers
fig, ax = plt.subplots(figsize=(9.0, 4.1))
N = 30
ans = AN1 + np.arange(N)
G = 0.03


def dette_c(c, fin0, r=0.0325):
    out, dd = [], 0.0
    for t in range(N):
        dd = dd * (1 + r) - (fin0 * (1 + G) ** t - c[t])
        out.append(dd)
    return np.array(out)


fc = J["fin"]["central"]
for cle, col, lw, ls, lab in (("falaise", AUJ, 1.3, (0, (4, 2)), "50 % puis 100 % en 2033"),
                              ("paliers", SEC, 1.6, "-", "paliers seuls (50 → 100 % en 2032)"),
                              ("plafond_paliers", PROP, 2.4, "-", "proposition (plafond + paliers)"),
                              ("cent", VAR, 1.6, "-", "100 % dès 2027"),
                              ("cinquante", GRIS_M, 1.2, (0, (1, 1.5)), "50 % sans montée")):
    dd = dette_c(np.array(S[cle]["mix"]), fc)
    ax.plot(ans, np.where(dd > -1e-9, dd, np.nan), color=col, lw=lw, ls=ls, label=lab, zorder=3)
ax.axhline(0, color=ENCRE2, lw=0.8)
ax.set_xlim(ans[0] - 0.3, ans[-1] + 0.3)
ax.set_ylim(0, 35)
ax.set_xticks(ans[::3])
ax.set_ylabel("Md€ courants")
axes_propres(ax)
taille_ticks(ax)
ax.legend(loc="upper right", frameon=False, fontsize=9.0 * ECH_TXT if NU else 9.0)
fin(fig, "is_n09_dette_calendriers",
    "Source : " + SRC_SIM + ".",
    f"Note : cas central (régime actuel moitié linéaire, moitié dégressif ; ressources de l'assiette de {f(J['fin']['central'])} Md€ en 2027 ; "
    "part imposable 75 % ; plafond couvrant 20 % de l'investissement). Dette cumulée, intérêts de 3,25 % compris, avant "
    "toute baisse du taux. Les calendriers « 100 % sous plafond seul » et « amortissement neutre » ne créent pas de "
    "dette : leur coût reste toujours inférieur aux ressources.")
