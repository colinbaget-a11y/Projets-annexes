"""
Graphiques de l'état des lieux des prélèvements obligatoires français.

Toutes les séries viennent de donnees/ (voir extract_donnees.py). Unité : millions d'euros
courants, rapportés au PIB à prix courants. Sorties dans figures/.

    python graphiques.py
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- charte
INK, INK2, MUTED, GRID, SURFACE = "#1F2328", "#4B5158", "#8A9099", "#E6E8EA", "#FCFCFB"
# palette catégorielle validée (validate_palette.js, mode light : tous les tests passent,
# avertissement de contraste levé par les étiquettes directes)
PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
BLEU, SEQ = PAL[0], ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
HALO = [pe.withStroke(linewidth=2.8, foreground=SURFACE)]

plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 10,
    "axes.edgecolor": MUTED, "axes.linewidth": 0.6,
    "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "figure.dpi": 200, "savefig.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.3,
})
PCT = FuncFormatter(lambda v, _: f"{v:g} %".replace(".", ","))
MDS = FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " "))


def grille(ax, axe="y"):
    ax.grid(axis=axe, color=GRID, lw=0.7, zorder=0)
    ax.set_axisbelow(True)


def titre(ax, t, st=None):
    n = st.count("\n") + 1 if st else 0
    ax.set_title(t, loc="left", fontsize=12, pad=10 + 14 * n, color=INK)
    if st:
        ax.text(0, 1.012, st, transform=ax.transAxes, fontsize=9.5, color=INK2, va="bottom")


def fin(fig, nom, src):
    fig.text(0.005, -0.01, src, fontsize=7.5, color=MUTED, ha="left")
    fig.savefig(OUT / nom)
    plt.close(fig)
    print("  ", nom)


def etiquette(ax, x, y, texte, couleur, dx=6, va="center", ha="left", gras=True):
    ax.annotate(texte, (x, y), xytext=(dx, 0), textcoords="offset points", color=couleur,
                fontsize=10, fontweight="bold" if gras else "normal", va=va, ha=ha, path_effects=HALO)


# ---------------------------------------------------------------- données
DOUBLONS = {"D51M", "D51O"}
SRC_FR = "Source : Eurostat, National Tax List France (table 0900 SEC 2010), mise à jour du 21 juillet 2026 ; PIB Eurostat nama_10_gdp."
SRC_PAYS = "Source : Eurostat, gov_10a_taxag, recettes fiscales par catégorie SEC en % du PIB, secteur S13 et institutions européennes."

rows = list(csv.DictReader(open(HERE / "donnees" / "ntl_france.csv", encoding="utf-8")))
PIB = {int(k): v for k, v in json.loads((HERE / "donnees" / "pib_france_cp_meur.json").read_text()).items()}
ANS = sorted(y for y in PIB if 1995 <= y <= 2024)
DET = [r for r in rows if r["details"] not in ("_T", "") and r["sto"] not in DOUBLONS]
AGG = {r["sto"]: {int(y): float(r[y]) for y in r if y.isdigit() and r[y] != ""} for r in rows if r["details"] == "_T"}

PIBP = {k: {int(a): v for a, v in d.items()} for k, d in json.loads((HERE / "donnees" / "pib_pays_cp_meur.json").read_text()).items()}
# Les listes nationales sont libellées en monnaie nationale : inutilisables telles quelles pour
# comparer les pays hors zone euro. Les comparaisons passent donc par gov_10a_taxag, déjà en % du PIB.
TAX = json.loads((HERE / "donnees" / "taxag_pays_pcgdp.json").read_text())
TOTAL = "D2_D5_D91_D61_M_D612_M_D614_M_D995"


def pc(p, code, annee=2024):
    return TAX.get(f"{p}|{code}|{annee}")
PAYSAGG = defaultdict(dict)
for r in csv.DictReader(open(HERE / "donnees" / "ntl_agregats_pays.csv", encoding="utf-8")):
    PAYSAGG[(r["pays"], r["sto"])][int(r["annee"])] = float(r["meur"])

NOMS = {"BE": "Belgique", "BG": "Bulgarie", "CZ": "Tchéquie", "DK": "Danemark", "DE": "Allemagne",
        "EE": "Estonie", "IE": "Irlande", "EL": "Grèce", "ES": "Espagne", "FR": "France",
        "HR": "Croatie", "IT": "Italie", "CY": "Chypre", "LV": "Lettonie", "LT": "Lituanie",
        "LU": "Luxembourg", "HU": "Hongrie", "MT": "Malte", "NL": "Pays-Bas", "AT": "Autriche",
        "PL": "Pologne", "PT": "Portugal", "RO": "Roumanie", "SI": "Slovénie", "SK": "Slovaquie",
        "FI": "Finlande", "SE": "Suède", "IS": "Islande", "NO": "Norvège", "CH": "Suisse"}
UE = [p for p in NOMS if p not in ("IS", "NO", "CH")]


def serie(code, ans=None):
    return [100 * AGG[code][y] / PIB[y] for y in (ans or ANS)]


def impot(motif, ans=None):
    r = [x for x in DET if x["nom_fr"].strip().lower() == motif.lower()][0]
    return [100 * float(r[str(y)]) / PIB[y] for y in (ans or ANS)]


def pays_pct(p, code, annee=2024):
    v = PAYSAGG.get((p, code), {}).get(annee)
    g = PIBP.get(p, {}).get(annee)
    return 100 * v / g if v is not None and g else None


# ================================================================ 1. les quatre blocs
def g1():
    fig, ax = plt.subplots(figsize=(9.2, 5.8))
    series = [("Cotisations sociales", "D61", PAL[0]), ("Impôts sur les produits", "D21", PAL[1]),
              ("Impôts sur le revenu des ménages", "D51A", PAL[2]), ("Autres impôts sur la production", "D29", PAL[3]),
              ("Impôts sur les sociétés", "D51B", PAL[4]), ("Impôts en capital", "D91", PAL[6])]
    for lib, code, col in series:
        v = serie(code)
        ax.plot(ANS, v, color=col, lw=2, solid_capstyle="round", zorder=3)
        etiquette(ax, ANS[-1], v[-1], f"{lib}  {v[-1]:.1f} %".replace(".", ","), col)
    grille(ax)
    ax.set_xlim(1995, 2024 + 13.5); ax.set_ylim(0, 21)
    ax.set_xticks([1995, 2000, 2005, 2010, 2015, 2020, 2024]); ax.yaxis.set_major_formatter(PCT)
    titre(ax, "Le taux global a peu bougé, sa composition a basculé",
          "Prélèvements obligatoires par bloc, en % du PIB. Les cotisations perdent 3,4 points depuis 1995,\nles impôts sur le revenu des ménages en gagnent 4,2.")
    fin(fig, "g1_blocs_pib.png", SRC_FR)


# ================================================================ 2. CSG contre IR
def g2():
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    for lib, nom, col in [("Contribution sociale généralisée", "Contribution sociale généralisée", PAL[0]),
                          ("Impôt sur le revenu", "Impôt sur le revenu", PAL[1])]:
        v = impot(nom)
        ax.plot(ANS, v, color=col, lw=2.4, solid_capstyle="round", zorder=3)
        ax.scatter([ANS[0], ANS[-1]], [v[0], v[-1]], s=30, color=col, zorder=4)
        etiquette(ax, ANS[-1], v[-1], f"{lib}\n{v[-1]:.2f} % du PIB".replace(".", ","), col)
    grille(ax)
    ax.set_xlim(1995, 2024 + 11); ax.set_ylim(0, 6)
    ax.set_xticks([1995, 2000, 2005, 2010, 2015, 2020, 2024]); ax.yaxis.set_major_formatter(PCT)
    titre(ax, "La France a deux impôts sur le revenu, et le plus gros est proportionnel",
          "Rendement en % du PIB. La CSG passe de 1,18 % à 5,22 % ; l'impôt sur le revenu recule de 3,49 % à 3,28 %.")
    fin(fig, "g2_csg_contre_ir.png", SRC_FR)


# ================================================================ 3. classement 2024
def g3(n=20):
    s = sorted([r for r in DET if r["2024"] != ""], key=lambda r: -float(r["2024"]))[:n]
    noms = [r["nom_fr"].replace("Impôts sur les sociétés y compris majoration et frais de poursuite", "Impôt sur les sociétés")
            .replace("Taxe intérieure de consommation des produits énergétiques", "TICPE, accise sur les produits énergétiques")
            .replace("Droits d'enregistrement (y compris taxe additionnelle)", "Droits d'enregistrement (DMTO)")
            .replace("Mutations à titre gratuit", "Mutations à titre gratuit (DMTG)")
            .replace("Autres taxes", "Autres impôts sur les bénéfices")
            .replace("Contributions des entreprises à la formation professionnelle et à l'apprentissage", "Formation professionnelle et apprentissage")[:58]
            for r in s]
    vals = [float(r["2024"]) / 1000 for r in s]
    fig, ax = plt.subplots(figsize=(9.6, 7.4))
    y = range(len(s))
    ax.barh(list(y), vals, height=0.74, color=[BLEU if i < 3 else SEQ[3] for i in y], zorder=3)
    for i, v in enumerate(vals):
        ax.text(v + 2.5, i, f"{v:,.1f}".replace(",", " ").replace(".", ","), va="center", fontsize=9,
                color=INK if i < 3 else INK2, fontweight="bold" if i < 3 else "normal")
    ax.set_yticks(list(y)); ax.set_yticklabels(noms, fontsize=9.5)
    ax.invert_yaxis(); grille(ax, "x")
    ax.set_xlim(0, max(vals) * 1.14); ax.set_xlabel("milliards d'euros, 2024")
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    titre(ax, "Trois prélèvements font la moitié du produit fiscal",
          "Les vingt premiers impôts de 2024, hors cotisations sociales. Ensemble ils représentent 90 % des recettes fiscales.")
    fin(fig, "g3_classement_2024.png", SRC_FR)


# ================================================================ 4. concentration
def g4():
    s = sorted([float(r["2024"]) for r in DET if r["2024"] != ""], reverse=True)
    tot = sum(s)
    cum = [0.0]
    for v in s:
        cum.append(cum[-1] + 100 * v / tot)
    x = list(range(len(cum)))
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    ax.plot(x, cum, color=BLEU, lw=2.4, zorder=3)
    ax.fill_between(x, cum, color=BLEU, alpha=0.08, zorder=2)
    for n, lib in [(3, "3 impôts\n50 %"), (8, "8 impôts\n75 %"), (21, "21 impôts\n90 %")]:
        ax.plot([n, n], [0, cum[n]], color=MUTED, lw=0.8, ls=(0, (2, 3)), zorder=2)
        ax.scatter([n], [cum[n]], s=34, color=BLEU, zorder=4)
        ax.annotate(lib, (n, cum[n]), xytext=(9, -20 if n > 3 else -34), textcoords="offset points",
                    fontsize=9.5, color=INK2, path_effects=HALO)
    grille(ax)
    ax.set_xlim(0, len(s)); ax.set_ylim(0, 103)
    ax.set_xlabel("nombre d'impôts, classés du plus au moins productif")
    ax.yaxis.set_major_formatter(PCT)
    titre(ax, "Les cent derniers impôts rapportent moins que le vingt-et-unième",
          "Part cumulée du produit fiscal 2024, hors cotisations sociales. 121 prélèvements recensés,\ndont 34 rapportent moins de 150 M€ chacun.")
    fin(fig, "g4_concentration.png", SRC_FR)


# ================================================================ 5. comparaison de structure
def g5():
    blocs = [("Cotisations sociales", "D61", PAL[0]), ("Production et importations", "D2", PAL[1]),
             ("Revenu et patrimoine", "D5", PAL[2]), ("Capital", "D91", PAL[3])]
    data = []
    for p in UE:
        v = [pc(p, c) or 0.0 for _, c, _ in blocs]
        if pc(p, "D2") and pc(p, "D5"):
            data.append((p, v, sum(v)))
    data.sort(key=lambda t: t[2])
    fig, ax = plt.subplots(figsize=(10.6, 6.4))
    xs = list(range(len(data)))
    bas = [0.0] * len(data)
    for k, (lib, _, col) in enumerate(blocs):
        h = [d[1][k] for d in data]
        ax.bar(xs, h, bottom=bas, width=0.74, color=col, label=lib, edgecolor=SURFACE, linewidth=1.2, zorder=3)
        bas = [b + v for b, v in zip(bas, h)]
    noms = [d[0] for d in data]
    ax.set_xticks(xs)
    ax.set_xticklabels([NOMS[p] for p in noms], rotation=60, ha="right", fontsize=8.5)
    for t in ax.get_xticklabels():
        if t.get_text() in ("France", "Danemark"):
            t.set_fontweight("bold"); t.set_color(INK)
    for p, dx, ha in (("FR", -4, "right"), ("DK", 4, "left")):
        i = noms.index(p)
        ax.annotate(f"{NOMS[p]}  {data[i][2]:.1f} %".replace(".", ","), (i, data[i][2]), xytext=(dx, 9),
                    textcoords="offset points", ha=ha, fontsize=10, fontweight="bold", color=INK)
    grille(ax)
    ax.yaxis.set_major_formatter(PCT); ax.set_ylim(0, 52)
    ax.legend(frameon=False, fontsize=9, ncol=4, loc="upper left", bbox_to_anchor=(0, 1.005))
    titre(ax, "Même niveau de prélèvement que le Danemark, structure opposée",
          "Impôts et cotisations sociales 2024 en % du PIB, cotisations imputées comprises. Le Danemark lève 31 points\nde PIB en impôts sur le revenu et le patrimoine et presque rien en cotisations ; la France fait l'inverse.")
    fin(fig, "g5_comparaison_structure.png", SRC_PAYS)


# ================================================================ 6. impôts de production
def g6():
    data = sorted([(p, pc(p, "D29")) for p in UE if pc(p, "D29") is not None], key=lambda t: -t[1])
    fig, ax = plt.subplots(figsize=(9.8, 6.0))
    cols = [PAL[1] if p == "FR" else (PAL[4] if p == "SE" else SEQ[2]) for p, _ in data]
    ax.bar(range(len(data)), [v for _, v in data], width=0.74, color=cols, zorder=3)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels([NOMS[p] for p, _ in data], rotation=60, ha="right", fontsize=8.5)
    for t in ax.get_xticklabels():
        if t.get_text() == "France":
            t.set_fontweight("bold"); t.set_color(INK)
    i = [p for p, _ in data].index("FR")
    ax.annotate(f"France  {data[i][1]:.1f} % du PIB".replace(".", ","), (i, data[i][1]), xytext=(6, 4),
                textcoords="offset points", ha="left", fontsize=10.5, fontweight="bold", color=PAL[1])
    j = [p for p, _ in data].index("SE")
    ax.annotate("Suède : les cotisations patronales\ny sont classées en impôts\nsur la production, pas en cotisations",
                (j, data[j][1]), xytext=(14, -6), textcoords="offset points", ha="left", va="top",
                fontsize=9, color=PAL[4], path_effects=HALO)
    grille(ax); ax.yaxis.set_major_formatter(PCT); ax.set_ylim(0, 11.2)
    titre(ax, "Hors cas suédois, les impôts de production sont une singularité française",
          "Autres impôts sur la production (D29) en % du PIB, 2024 : prélèvements assis sur la masse salariale,\nla valeur locative ou le chiffre d'affaires, donc dus même en l'absence de bénéfice.")
    fin(fig, "g6_impots_production.png", SRC_PAYS)


# ================================================================ 7. que taxe-t-on ?
def g7():
    groupes = [("Cotisations sociales effectives", None, PAL[0]),
               ("Consommation", {"C"}, PAL[1]),
               ("Travail, hors cotisations", {"LEYRS", "LEES"}, PAL[2]),
               ("Capital et patrimoine", {"KIC", "KIH", "KS"}, PAL[3]),
               ("Non réparti (IR, CSG, CRDS)", {"SPLIT1"}, "#B6BAC0")]
    def bande(fcts, y):
        return sum(float(r[str(y)]) for r in DET if r["fonction"] in fcts and r[str(y)] != "")
    series = []
    for lib, f, col in groupes:
        if f is None:
            v = [100 * (AGG["D611C"][y] + AGG["D613"][y]) / PIB[y] for y in ANS]
        else:
            v = [100 * bande(f, y) / PIB[y] for y in ANS]
        series.append((lib, v, col))
    fig, ax = plt.subplots(figsize=(9.2, 5.8))
    ax.stackplot(ANS, [s[1] for s in series], colors=[s[2] for s in series],
                 labels=[s[0] for s in series], edgecolor=SURFACE, linewidth=0.8, zorder=3)
    bas = [0.0] * len(ANS)
    for lib, v, col in series:
        milieu = bas[-1] + v[-1] / 2
        etiquette(ax, 2024.3, milieu, f"{lib}  {v[-1]:.1f} %".replace(".", ","),
                  INK if col == "#B6BAC0" else col)
        bas = [b + x for b, x in zip(bas, v)]
    grille(ax)
    ax.set_xlim(1995, 2024 + 15); ax.set_ylim(0, 46)
    ax.set_xticks([1995, 2000, 2005, 2010, 2015, 2020, 2024]); ax.yaxis.set_major_formatter(PCT)
    titre(ax, "Ce que l'on taxe, en % du PIB",
          "Les 121 impôts répartis par fonction économique, plus les cotisations effectives. L'impôt sur le revenu\net la CSG sont déclarés à cheval sur plusieurs fonctions et restent non répartis.")
    fin(fig, "g7_fonction_economique.png", SRC_FR)


# ================================================================ 8. dépenses fiscales
def g8():
    d = json.loads((HERE / "donnees" / "depenses_fiscales_top.json").read_text())
    court = {1: "Crédit d'impôt recherche", 2: "Crédit d'impôt emploi d'un salarié à domicile",
             3: "Abattement de 10 % sur les pensions", 4: "Transmission d'entreprises (pacte Dutreil)",
             5: "Participation, intéressement, épargne salariale", 6: "TVA à 10 % sur les travaux dans le logement",
             7: "TVA à 10 % sur la restauration", 8: "Exonération des heures supplémentaires",
             9: "Réduction d'impôt au titre des dons", 10: "Déduction des dépenses de réparation (foncier)",
             11: "Crédit d'impôt frais de garde des jeunes enfants", 12: "Dons des entreprises",
             13: "Tarif réduit d'accise sur les gazoles", 14: "Exonération des prestations familiales et AAH"}
    d = sorted(d, key=lambda r: -r["meur"])
    fig, ax = plt.subplots(figsize=(9.4, 5.8))
    y = range(len(d))
    ax.barh(list(y), [r["meur"] / 1000 for r in d], height=0.74,
            color=[PAL[1] if r["rang"] == 4 else SEQ[3] for r in d], zorder=3)
    for i, r in enumerate(d):
        ax.text(r["meur"] / 1000 + 0.11, i, f"{r['meur']/1000:.1f}".replace(".", ","),
                va="center", fontsize=9, color=INK2)
    ax.set_yticks(list(y)); ax.set_yticklabels([court[r["rang"]] for r in d], fontsize=9.5)
    ax.invert_yaxis(); grille(ax, "x")
    ax.set_xlim(0, 9.3); ax.set_xlabel("coût pour 2026, en milliards d'euros")
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    titre(ax, "Les niches : 88,3 milliards en 2026, dont la moitié dans quatorze dispositifs",
          "Mesures les plus coûteuses. Le chiffrage du pacte Dutreil a été relevé de 4,2 Md€ d'une année sur l'autre.")
    fin(fig, "g8_depenses_fiscales.png",
        "Source : Évaluation des voies et moyens, tome II, annexe au projet de loi de finances pour 2026.")


# ================================================================ 9. la longue traîne
def g9():
    s = sorted([float(r["2024"]) for r in DET if r["2024"] not in ("",) and float(r["2024"]) > 0], reverse=True)
    fig, ax = plt.subplots(figsize=(9.0, 5.4))
    ax.bar(range(len(s)), s, width=0.9, color=[BLEU if v >= 1000 else PAL[1] for v in s], zorder=3)
    ax.set_yscale("log"); grille(ax)
    ax.set_ylim(0.5, 400000)
    ax.set_xlabel("les 99 impôts à rendement non nul, classés par rendement décroissant")
    ax.set_ylabel("rendement 2024, M€, échelle logarithmique")
    n_petits = sum(1 for v in s if v < 150)
    ax.axhline(150, color=MUTED, lw=1, ls=(0, (3, 3)), zorder=5)
    ax.annotate(f"sous la ligne des 150 M€ :\n{n_petits} prélèvements à rendement non nul,\n643 M€ en tout, soit 0,08 % du produit fiscal",
                (57, 4.5e4), ha="left", va="top", fontsize=9.5, color=INK2)
    ax.annotate("150 M€", (len(s) - 1, 150), xytext=(6, 4), textcoords="offset points",
                fontsize=9, color=MUTED)
    titre(ax, "Une longue traîne de prélèvements sans rendement",
          "Chaque barre est un impôt. Vingt-deux autres, non représentés ici, ont un rendement nul :\nils existent juridiquement sans produire de recette.")
    fin(fig, "g9_longue_traine.png", SRC_FR)


# ================================================================ 10. détenir ou transmettre
def g10():
    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    for lib, nom, col in [("Taxe foncière sur le bâti", "Foncier bâti", PAL[0]),
                          ("Mutations à titre gratuit (DMTG)", "Mutations à titre gratuit", PAL[2]),
                          ("Droits d'enregistrement (DMTO)", "Droits d'enregistrement (y compris taxe additionnelle)", PAL[1])]:
        v = impot(nom)
        ax.plot(ANS, v, color=col, lw=2.2, solid_capstyle="round", zorder=3)
        etiquette(ax, ANS[-1], v[-1], f"{lib}\n{v[-1]:.2f} %".replace(".", ","), col)
    grille(ax)
    ax.set_xlim(1995, 2024 + 12); ax.set_ylim(0, 1.7)
    ax.set_xticks([1995, 2000, 2005, 2010, 2015, 2020, 2024]); ax.yaxis.set_major_formatter(PCT)
    titre(ax, "Taxer la détention, la transmission ou la transaction",
          "En % du PIB. Les droits de mutation à titre onéreux suivent le marché immobilier : ils s'effondrent\nde 0,74 % à 0,50 % du PIB entre 2022 et 2024, alors que la taxe foncière ne bouge pas.")
    fin(fig, "g10_detention_transaction.png", SRC_FR)


# ================================================================ 11. taux global, comparaison
def g11():
    def serie_pays(p):
        return [(y, TAX[f"{p}|{TOTAL}|{y}"]) for y in ANS if f"{p}|{TOTAL}|{y}" in TAX]
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    med = []
    for y in ANS:
        v = sorted(TAX[f"{p}|{TOTAL}|{y}"] for p in UE if f"{p}|{TOTAL}|{y}" in TAX)
        med.append(v[len(v) // 2] if v else float("nan"))
    for p in UE:
        if p in ("FR", "DK", "DE", "IT"):
            continue
        v = serie_pays(p)
        if v:
            ax.plot([a for a, _ in v], [b for _, b in v], color=GRID, lw=1, zorder=2)
    ax.plot(ANS, med, color=MUTED, lw=1.6, ls=(0, (4, 3)), zorder=3)
    etiquette(ax, ANS[-1], med[-1], f"médiane de l'Union  {med[-1]:.1f} %".replace(".", ","), MUTED)
    for p, col in [("FR", PAL[0]), ("DK", PAL[2]), ("DE", PAL[3]), ("IT", PAL[1])]:
        v = serie_pays(p)
        ax.plot([a for a, _ in v], [b for _, b in v], color=col, lw=2.4 if p == "FR" else 1.8, zorder=4)
        etiquette(ax, v[-1][0], v[-1][1], f"{NOMS[p]}  {v[-1][1]:.1f} %".replace(".", ","), col)
    grille(ax)
    ax.set_xlim(1995, 2024 + 13); ax.set_ylim(18, 52)
    ax.set_xticks([1995, 2000, 2005, 2010, 2015, 2020, 2024]); ax.yaxis.set_major_formatter(PCT)
    titre(ax, "Un niveau stable, au sommet de l'Union sans en être le record",
          "Impôts et cotisations sociales en % du PIB, hors cotisations imputées. Chaque ligne grise est un État membre.")
    fin(fig, "g11_taux_global_pays.png", SRC_PAYS)


# ================================================================ 12. fiscalité de l'énergie
def g12():
    env = [r for r in DET if r["tag"].startswith("E")]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13.2, 5.2), gridspec_kw={"width_ratios": [1, 1.25], "wspace": 0.52})
    v = [100 * sum(float(r[str(y)]) for r in env if r[str(y)] != "") / PIB[y] for y in ANS]
    a1.plot(ANS, v, color=PAL[2], lw=2.4, zorder=3)
    a1.fill_between(ANS, v, color=PAL[2], alpha=0.1, zorder=2)
    a1.scatter([ANS[-1]], [v[-1]], s=34, color=PAL[2], zorder=4)
    etiquette(a1, ANS[-1], v[-1], f"{v[-1]:.2f} %".replace(".", ","), PAL[2], dx=-6, ha="right")
    grille(a1); a1.set_xlim(1995, 2026); a1.set_ylim(0, 2.4)
    a1.set_xticks([1995, 2005, 2015, 2024]); a1.yaxis.set_major_formatter(PCT)
    a1.set_title("France, en % du PIB", loc="left", fontsize=10.5, color=INK2)
    s = sorted(env, key=lambda r: -float(r["2024"]))[:6]
    noms = [r["nom_fr"].replace("Taxe intérieure de consommation des produits énergétiques", "TICPE (produits énergétiques)")
            .replace("Taxe intérieure sur la consommation de gaz naturel", "Accise sur le gaz naturel")
            .replace("Impositions forfaitaires sur les entreprises de réseaux", "IFER (entreprises de réseaux)")
            .replace("Taxe sur les émissions de CO2", "Quotas et émissions de CO₂")[:40] for r in s]
    vals = [float(r["2024"]) / 1000 for r in s]
    a2.barh(range(len(s)), vals, height=0.7, color=SEQ[3], zorder=3)
    for i, x in enumerate(vals):
        a2.text(x + 0.4, i, f"{x:.1f}".replace(".", ","), va="center", fontsize=9, color=INK2)
    a2.set_yticks(range(len(s))); a2.set_yticklabels(noms, fontsize=9.5); a2.invert_yaxis()
    grille(a2, "x"); a2.set_xlim(0, 34); a2.set_xlabel("milliards d'euros, 2024")
    a2.spines["left"].set_visible(False); a2.tick_params(axis="y", length=0)
    a2.set_title("Composition, 2024", loc="left", fontsize=10.5, color=INK2)
    fig.suptitle("La fiscalité de l'énergie pèse 43,6 Md€, soit 1,5 % du PIB", x=0.005, ha="left",
                 fontsize=12, color=INK, y=1.03)
    fig.text(0.005, 0.975, "Douze prélèvements identifiés comme environnementaux. Les deux tiers viennent de la seule TICPE.",
             fontsize=9.5, color=INK2, ha="left")
    fin(fig, "g12_fiscalite_energie.png", SRC_FR)


if __name__ == "__main__":
    print("figures :")
    for f in (g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12):
        f()
