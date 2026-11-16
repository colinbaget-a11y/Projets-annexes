"""Figures de la partie IR-CSG réécrite (ircsg_n01 à ircsg_n18, sans n06), d'après les sorties des programmes de la partie.

Base 2025 (décision 5 du 17/11/2026) ; taux marginaux par 1 000 € de revenu après cotisations, grille de 100 €, chaque
point calculé (aucun lissage, aucune interpolation de l'impôt ; décision 6) ; pas de figure sur les cotisations
sociales (décision 7 : l'ancienne figure n06 du coin au Smic est retirée).

Couleurs de la note (style_note.py) : aujourd'hui en encre grise, réforme naïve en brique, proposition en bleu,
variantes en ocre ; composantes d'une décomposition en nuances de bleu. Titres : dans le document (\\figbloc) ;
sources et notes de lecture : figures/nu/<nom>_note.tex.

Lancer depuis fiscalite/, après situation_ircsg, naive_ircsg, proposition_ircsg, arbitrages_prop_ircsg et
transition_ircsg : python3 synthese/figures_ircsg_n.py && FIG_NU=1 python3 synthese/figures_ircsg_n.py
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import outils_ircsg as U  # noqa: E402
from graphiques import ECH_TXT, fin, plt  # noqa: E402
from style_note import AUJ, NAIF, NUANCES_BLEU, PROP, SEC, VAR, ENCRE, ENCRE2, axes_propres, pct, euros, _fr  # noqa: E402

S = HERE / "sorties"
SIT = json.loads((S / "situation_ircsg.json").read_text(encoding="utf-8"))
NV = json.loads((S / "naive_ircsg.json").read_text(encoding="utf-8"))
PJ = json.loads((S / "proposition_ircsg.json").read_text(encoding="utf-8"))
ARB = json.loads((S / "arbitrages_prop_ircsg.json").read_text(encoding="utf-8"))
TR = json.loads((S / "transition_ircsg.json").read_text(encoding="utf-8"))
C = PJ["choix"]
PR = PJ["evaluations"]["proposition"]
NQ = NV["quotient"]
O_P = U.options(F=C["F"], **PJ["base"])
S_P = U.bareme(C["t0"], C["tb"], C["z1"], C["t1"], C["z2"])
O_N = U.options(fam="quotient")
S_N = U.empile(NQ["tau"])
SRC_OF = "OpenFisca-France 176.1 (législation des revenus 2025), cas-types sans niche ; calculs de l'auteur"
SRC_M = ("DGFiP, IRCOM et totaux des déclarations 2042 des revenus 2024 (répartition) ; Insee, comptes nationaux 2025, "
         "et rapport d'évaluation « Financement » annexé au projet de loi d'approbation des comptes de la Sécurité "
         "sociale 2025 (agrégats de 2025) ; OpenFisca-France ; calculs de l'auteur (synthese/modele_purs.py, "
         "proposition_ircsg.py)")
CIB = U.M.CIBLE
NOTE_MG = ("chaque point est le supplément d'IR, de CSG et de CRDS dû pour 1 000 € de revenu après cotisations en plus "
           "(salaire net de cotisations, ou pension brute), calculé tous les 100 € sans lissage")
FS = 9 * ECH_TXT


def k_euros(ax, axe="x"):
    f = plt.FuncFormatter(lambda v, _: _fr(v / 1e3) + " k€")
    (ax.xaxis if axe == "x" else ax.yaxis).set_major_formatter(f)


def legende(ax, **k):
    ax.legend(frameon=False, fontsize=9, **k)


# ------------------------------------------------------------------ 1. situation
def n01():
    r = SIT["recettes"]
    fig, ax = plt.subplots(figsize=(9, 3.2))
    y = [2, 1, 0]
    ax.barh(2, r["ir"], color=NUANCES_BLEU[0], height=0.6, zorder=2)
    g = 0
    for (v, lab), col in zip(((r["csg_activite"], "revenus d'activité"), (r["csg_pensions"], "pensions"),
                              (r["csg_chomage"], "chômage")), (NUANCES_BLEU[1], NUANCES_BLEU[3], NUANCES_BLEU[5])):
        ax.barh(1, v, left=g, color=col, height=0.6, zorder=2)
        if v > 10:
            ax.text(g + v / 2, 1, f"{lab}\n{_fr(v)} Md€", ha="center", va="center", fontsize=8.5,
                    color="white" if col != NUANCES_BLEU[5] else ENCRE)
        g += v
    ax.barh(0, r["crds"], color=NUANCES_BLEU[2], height=0.6, zorder=2)
    for yy, v in zip(y, (r["ir"], r["csg"], r["crds"])):
        ax.text(v + 2, yy, f"{_fr(v)} Md€", va="center", fontsize=9.5, color=ENCRE, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(["Impôt sur le revenu", "CSG", "CRDS"], fontsize=FS * 1.05)
    ax.set_xlim(0, 155)
    ax.set_xlabel("Md€ en 2025, revenus imposés au barème")
    axes_propres(ax, grille="x")
    f = r["facteurs"]
    fin(fig, "ircsg_n01_recettes", "DGFiP, IRCOM des revenus 2024 (répartition) ; Insee, comptes nationaux 2025 (IR, CSG, "
        "CRDS) ; rapport d'évaluation « Financement » annexé au projet de loi d'approbation des comptes de la Sécurité "
        "sociale 2025 (CSG par assiette) ; calculs de l'auteur (synthese/modele_purs.py, situation_ircsg.py).",
        f"Note : champ de la fusion, c'est-à-dire les revenus imposés au barème (salaires, pensions, revenus des "
        f"indépendants, loyers, allocations chômage) ; l'IR des revenus du capital au prélèvement forfaitaire unique "
        f"(environ {_fr(r['ir_pfu'], 1)} Md€) n'y est pas. Montants de 2024 (IRCOM, Sécurité sociale) portés en 2025 avec "
        f"la croissance de l'IR des comptes nationaux (+{_fr(100 * (f['ir'] - 1), 1)} %, impôt encaissé en 2025), de la CSG "
        f"sur les revenus d'activité (+{_fr(100 * (f['csg_activite'] - 1), 1)} %) et de remplacement "
        f"(+{_fr(100 * (f['csg_remplacement'] - 1), 1)} %) et de la CRDS (+{_fr(100 * (f['crds'] - 1), 1)} %). Au niveau "
        f"national (comptes nationaux 2025) : IR {_fr(r['nat_ir'], 1)} Md€, CSG {_fr(r['nat_csg'], 1)} Md€, CRDS "
        f"{_fr(r['nat_crds'], 1)} Md€. La CSG des pensions de 2024 ({_fr(r['base_2024']['csg_pensions'], 1)} Md€) est un "
        f"chiffre de la CCSS repris par le modèle, non relu à la source.")


def n02():
    o = SIT["ocde_1100"]
    v = o["valeurs"]
    pays = sorted(v, key=lambda k: v[k])
    fig, ax = plt.subplots(figsize=(9, 3.9))
    for i, k in enumerate(pays):
        if k == "France":
            a, b = o["france_ir_pct"], o["france_csg_crds_pct"]
            ax.barh(i, a, color=NUANCES_BLEU[0], height=0.65, zorder=2, label="France : impôt sur le revenu")
            ax.barh(i, b, left=a, color=NUANCES_BLEU[3], height=0.65, zorder=2, label="France : CSG et CRDS")
            ax.barh(i, v[k] - a - b, left=a + b, color=NUANCES_BLEU[5], height=0.65, zorder=2,
                    label="France : autres impôts sur le revenu des personnes")
        else:
            ax.barh(i, v[k], color=AUJ if k == "Moyenne OCDE" else SEC, height=0.65, zorder=2)
        ax.text(v[k] + 0.3, i, _fr(v[k], 1), va="center", fontsize=8.5, color=ENCRE)
    ax.set_yticks(range(len(pays)))
    ax.set_yticklabels(pays, fontsize=FS)
    ax.set_xlabel(f"Impôts sur le revenu des personnes, % du PIB, {o['annee']}")
    ax.xaxis.set_major_formatter(pct)
    axes_propres(ax, grille="x")
    legende(ax, loc="lower right")
    fin(fig, "ircsg_n02_ocde", "OCDE, Revenue Statistics (catégorie 1100) ; Insee, comptes nationaux (IR, CSG, CRDS) ; "
        "calculs de l'auteur (synthese/situation_ircsg.py).",
        "Note : l'OCDE range la CSG et la CRDS parmi les impôts sur le revenu des personnes. La partie « autres » de la "
        "France est l'écart entre le total de l'OCDE et les trois impôts des comptes nationaux (prélèvements sur les revenus "
        "du capital notamment, non détaillés ici). Les autres pays ne sont pas décomposés.")


REPERES_RET = [(17_600, "CSG : exonération\n→ 3,8 %"), (20_600, "3,8 → 6,6 %"), (31_900, "6,6 → 8,3 %"),
               (33_100, "abattement\ndes plus de 65 ans")]


def panneaux(series, titre_note, nom, src, reperes=True, xmax_s=120e3, xmax_r=60e3):
    """Deux panneaux de taux marginaux (salarié seul, retraité seul) ; series : [(sched, o, couleur, épaisseur,
    libellé)], sched None pour aujourd'hui."""
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.8), sharey=True)
    for ax, prof, xmax, t, xl in ((axs[0], "seul", xmax_s, "Salarié seul", "Salaire net de cotisations, par an"),
                                  (axs[1], "retraite_seul", xmax_r, "Retraité seul", "Pension brute, par an")):
        for sched, o, col, lw, lab in series:
            xs, ys = U.courbe_marginale(sched, o, prof, bmin=2000.0, bmax=xmax)
            ax.plot(xs, ys, color=col, lw=lw, label=lab, drawstyle="steps-post")
        ax.set_title(t, fontsize=10, loc="left", color=ENCRE)
        ax.set_xlabel(xl)
        ax.set_xlim(0, xmax)
        k_euros(ax)
        ax.yaxis.set_major_formatter(pct)
        axes_propres(ax)
    if reperes:
        xs, ys = U.courbe_marginale(None, None, "retraite_seul", bmin=2000.0, bmax=xmax_r)
        for xr, lab in REPERES_RET:
            yr = float(ys[np.argmin(np.abs(xs - xr))])
            axs[1].annotate(lab, (xr, yr), xytext=(4, -2), textcoords="offset points", fontsize=7.2, color=ENCRE2,
                            va="top", ha="left")
    axs[0].set_ylabel("Prélèvement sur 1 000 € de plus")
    axs[0].set_ylim(0, 90)
    if len(series) > 1:
        legende(axs[0], loc="upper left")
    fig.subplots_adjust(wspace=0.15)
    fin(fig, nom, src, titre_note)


def n03():
    panneaux([(None, None, AUJ, 1.4, "Aujourd'hui")],
             f"Note : droit des revenus 2025 ; {NOTE_MG}. Retraité de plus de 65 ans, dont le taux de CSG dépend du revenu "
             "fiscal de l'avant-dernière année, pris en régime stable. Les pics sont de vrais sauts du droit, larges de "
             "1 000 € parce que c'est l'écart mesuré : quand le revenu fiscal du retraité franchit un seuil de CSG, le "
             "nouveau taux s'applique à toute sa pension ; quand il franchit l'un des deux seuils de l'abattement des plus "
             "de 65 ans, cet abattement baisse d'un coup de 1 411 € ; le petit pic du salarié à l'entrée dans l'impôt vient "
             "de ce que l'IR n'est pas recouvré sous 61 €.",
             "ircsg_n03_marches", SRC_OF + " (synthese/openfisca_cas_ircsg.py, outils_ircsg.py).")


def n04():
    m = SIT["meme_revenu_courbe"]
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(m["base"], m["seul"], color=AUJ, lw=1.8, label="Salarié seul")
    ax.plot(m["base"], m["retraite"], color=AUJ, lw=1.8, ls=(0, (4, 2)), label="Retraité seul")
    k_euros(ax)
    ax.yaxis.set_major_formatter(pct)
    ax.set_xlabel("Revenu après cotisations sociales (salaire net de cotisations ou pension brute)")
    ax.set_ylabel("IR + CSG + CRDS, % du revenu")
    axes_propres(ax)
    legende(ax, loc="upper left")
    fin(fig, "ircsg_n04_meme_revenu", SRC_OF + " (synthese/situation_ircsg.py).",
        "Note : à revenu après cotisations égal, c'est-à-dire avec la même assiette que l'impôt fusionné. Le retraité a plus "
        "de 65 ans (abattement des personnes âgées) et bénéficie de l'abattement de 10 % sur les pensions et des taux "
        "réduits de CSG. Les deux ménages n'ont aucune niche.")


def n05():
    q = SIT["qf_courbe"]
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(q["brut"], q["deux"], color=AUJ, lw=1.8, label="Couple avec deux enfants")
    ax.plot(q["brut"], q["trois"], color=AUJ, lw=1.8, ls=(0, (4, 2)), label="Couple avec trois enfants")
    k_euros(ax)
    ax.yaxis.set_major_formatter(euros)
    ax.set_xlabel("Revenu brut du couple (partagé 60/40)")
    ax.set_ylabel("Baisse d'impôt due aux enfants")
    axes_propres(ax)
    legende(ax, loc="upper left")
    fin(fig, "ircsg_n05_quotient", SRC_OF + " (synthese/situation_ircsg.py).",
        "Note : écart d'IR entre le couple avec enfants et le même couple sans enfant, au même revenu ; salariés mariés ou "
        "pacsés, enfants à charge nés en 2015. Plafond : 1 807 € par demi-part (revenus 2025). Au total, le quotient familial "
        f"des enfants réduit l'IR d'environ {_fr(SIT['qf_agregat']['cout'], 1)} Md€ dans le modèle.")


# ------------------------------------------------------------------ 3. réforme naïve
def n07():
    panneaux([(None, None, AUJ, 1.0, "Aujourd'hui"), (S_N, O_N, NAIF, 2.0, "Réforme naïve")],
             f"Note : réforme naïve : barème de l'IR des revenus 2025 avec quotient conjugal et familial, appliqué au revenu "
             f"après cotisations sans abattement ni décote, plus un taux proportionnel de {_fr(100 * NQ['tau'], 2)} % qui "
             f"remplace la CSG et la CRDS ; {NOTE_MG}. Les marches de la réforme naïve sont celles des tranches de l'IR "
             f"(11, 30 et 41 %).",
             "ircsg_n07_naive_marges", SRC_OF + " (synthese/naive_ircsg.py, outils_ircsg.py).", reperes=False)


def n08():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    d = NQ["dec_eur"]
    x = np.arange(1, 11)
    ax.bar(x, d, color=NAIF, width=0.6, zorder=2)
    for i, v in zip(x, d):
        ax.text(i, v + (60 if v >= 0 else -60), _fr(v), ha="center", va="bottom" if v >= 0 else "top", fontsize=9, color=ENCRE)
    ax.axhline(0, color=ENCRE2, lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([f"D{i}" for i in x], fontsize=FS)
    ax.yaxis.set_major_formatter(euros)
    ax.set_ylim(-900, 2500)
    ax.set_ylabel("Variation de l'impôt par foyer et par an")
    ax.set_xlabel("Déciles de revenu fiscal de référence")
    axes_propres(ax)
    fin(fig, "ircsg_n08_naive_deciles", SRC_M + " (naive_ircsg.py).",
        f"Note : réforme naïve (barème de l'IR du foyer et taux proportionnel de {_fr(100 * NQ['tau'], 2)} %), à recette égale "
        f"({_fr(CIB)} Md€, base 2025) avant réaction des contribuables. Le 1 % le plus aisé paierait {_fr(NQ['top1_Md'], 1)} Md€ de plus, le "
        f"dixième le plus aisé {_fr(NQ['top10_Md'], 1)} Md€.")


# ------------------------------------------------------------------ 4. proposition
_xr, _yr = U.courbe_marginale(S_P, O_P, "retraite_seul", bmin=12500.0, bmax=25000.0)
MAX_RET, X_MAX_RET = float(_yr.max()), float(_xr[_yr.argmax()] + 500)    # milieu de la fenêtre de 1 000 €


def n09():
    panneaux([(None, None, AUJ, 1.0, "Aujourd'hui"), (S_P, O_P, PROP, 2.0, "Proposition")],
             f"Note : proposition : franchise de {_fr(C['F'])} € par adulte sur les revenus d'activité, puis taux marginal de "
             f"{_fr(100 * C['t0'])} % au premier euro imposé, {_fr(100 * C['tb'])} % à 20 000 €, {_fr(100 * C['t1'], 1)} % à "
             f"{_fr(C['z1'] / 1e3, 1 if C['z1'] % 1000 else 0)} 000 €, 50 % à {_fr(C['z2'] / 1e3)} 000 €, en ligne droite "
             f"entre ces points ; pensions exonérées jusqu'à 12 500 €, puis de moins en moins jusqu'à 25 000 € ; {NOTE_MG}. "
             "Le seul saut qui reste est un vrai effet de la règle : entre 12 500 et 25 000 € de pension, chaque euro de "
             "pension en plus retire un euro d'exonération, si bien que le retraité paie deux fois le taux marginal du "
             f"barème, jusqu'à {_fr(MAX_RET)} % vers {_fr(X_MAX_RET / 1e3)} 000 € ; à 25 000 €, l'exonération est épuisée et "
             "le taux retombe à celui du barème.",
             "ircsg_n09_prop_marges", SRC_OF + " (synthese/proposition_ircsg.py, outils_ircsg.py).", reperes=False)


def n10():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    x = np.arange(1, 11)
    ax.bar(x, PR["dec_eur"], width=0.6, color=PROP, label="Proposition", zorder=2)
    for i, v in zip(x, PR["dec_eur"]):
        ax.text(i, v + (25 if v >= 0 else -25), _fr(v), ha="center", va="bottom" if v >= 0 else "top", fontsize=9, color=ENCRE)
    ax.set_ylim(-700, 700)
    ax.axhline(0, color=ENCRE2, lw=0.8)
    for yv in (500, -500):
        ax.axhline(yv, color=PROP, lw=0.7, ls=":")
    ax.set_xticks(x)
    ax.set_xticklabels([f"D{i}" for i in x], fontsize=FS)
    ax.yaxis.set_major_formatter(euros)
    ax.set_ylabel("Variation de l'impôt par foyer et par an")
    ax.set_xlabel("Déciles de revenu fiscal de référence")
    axes_propres(ax)
    fin(fig, "ircsg_n10_deciles", SRC_M + ".",
        "Note : moyenne par décile de foyers fiscaux, à recette égale avant réaction. Pointillés : la contrainte que s'impose la "
        f"proposition (plus ou moins 500 € par décile). Le 1 % le plus aisé : {_fr(PR['top1_Md'], 1)} Md€ (convention centrale de "
        "répartition des revenus au PFU).")


def n11():
    types = [("seuls_actifs", "Personne seule active"), ("parents_isoles", "Parent isolé"),
             ("couples0_actifs", "Couple actif sans enfant"), ("couples2", "Couple actif avec enfants"),
             ("seuls_retraites", "Retraité seul"), ("couples0_retraites", "Couple de retraités")]
    fig, ax = plt.subplots(figsize=(9, 3.7))
    y = np.arange(len(types))[::-1]
    h = 0.36
    ax.barh(y + h / 2, [NQ["groupes"][t]["eur"] for t, _ in types], height=h, color=NAIF, label="Réforme naïve", zorder=2)
    ax.barh(y - h / 2, [PR["groupes"][t]["eur"] for t, _ in types], height=h, color=PROP, label="Proposition", zorder=2)
    for yy, (t, _) in zip(y, types):
        v = PR["groupes"][t]["eur"]
        ax.text(v + (60 if v >= 0 else -60), yy - h / 2, _fr(v), va="center", ha="left" if v >= 0 else "right", fontsize=8.5,
                color=PROP, fontweight="bold")
    ax.axvline(0, color=ENCRE2, lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels([lab for _, lab in types], fontsize=FS)
    ax.xaxis.set_major_formatter(euros)
    ax.set_xlim(-2300, 3200)
    ax.set_xlabel("Variation moyenne de l'impôt par foyer et par an (positif : paie plus)")
    axes_propres(ax, grille="x")
    legende(ax, loc="upper right")
    fin(fig, "ircsg_n11_qui_paie", SRC_M + ".",
        f"Note : moyenne par type de foyer, à recette égale. Au total, les retraités paient {_fr(PR['groupes']['retraites']['Md'], 1)} "
        f"Md€ de plus avec la proposition ({_fr(NQ['groupes']['retraites']['Md'], 1)} Md€ avec la réforme naïve) et les actifs "
        f"autant de moins. Les retraités sont des foyers qui n'ont que des pensions ; les enfants ne sont que chez les actifs.")


def n12():
    pa, pn, pp = SIT["ptr_auj"], NQ["ptr"], PR["ptr"]
    cles = [("seul_mi", "Personne seule,\nmi-temps au Smic"), ("seul_smic", "Personne seule,\nSmic à temps plein"),
            ("conjoint_mi", "Conjoint d'un salarié,\nmi-temps au Smic"), ("conjoint_smic", "Conjoint d'un salarié,\nSmic à temps plein")]
    fig, ax = plt.subplots(figsize=(9, 3.6))
    x = np.arange(len(cles))
    w = 0.26
    for k, (d, col, lab) in enumerate(((pa, AUJ, "Aujourd'hui"), (pn, NAIF, "Réforme naïve"), (pp, PROP, "Proposition"))):
        v = [d[c] for c, _ in cles]
        ax.bar(x + (k - 1) * w, v, width=w, color=col, label=lab, zorder=2)
        for i, vv in enumerate(v):
            ax.text(i + (k - 1) * w, vv + 0.3, _fr(vv, 1), ha="center", fontsize=8, color=ENCRE)
    ax.set_xticks(x)
    ax.set_xticklabels([lab for _, lab in cles], fontsize=FS)
    ax.yaxis.set_major_formatter(pct)
    ax.set_ylim(0, 17)
    ax.yaxis.set_major_locator(plt.MultipleLocator(5))
    ax.set_ylabel("IR + CSG + CRDS prélevés sur ce salaire")
    axes_propres(ax)
    legende(ax, loc="upper left", ncol=3)
    fin(fig, "ircsg_n12_premier_salaire", SRC_OF + " (synthese/outils_ircsg.py).",
        "Note : impôt du ménage avec ce salaire moins impôt sans ce salaire, rapporté au salaire brut ; Smic 2025 de 21 622 € "
        "brut par an. Conjoint : marié ou pacsé à un salarié qui gagne 30 000 € brut, sans enfant. Hors prime d'activité, "
        "que la réforme ne change pas.")


# ------------------------------------------------------------------ 5. arbitrages
def n13():
    pf = PJ["par_franchise"]
    Fs = sorted(float(k) for k in pf)
    part = [pf[str(int(F))]["part"] for F in Fs]
    ret = [pf[str(int(F))]["retraites"] for F in Fs]
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.4))
    for ax, v, yl in ((axs[0], part, "Gain sur la participation (Md€)"), (axs[1], ret, "Hausse pour les retraités (Md€)")):
        ax.plot(Fs, v, color=VAR, lw=1.6, marker="o", ms=4, zorder=2)
        i = Fs.index(C["F"])
        ax.plot([Fs[i]], [v[i]], marker="o", ms=8, color=PROP, zorder=3)
        ax.annotate("Proposition", (Fs[i], v[i]), xytext=(-8, 8), textcoords="offset points", ha="right", fontsize=9, color=PROP)
        ax.set_xlabel("Franchise d'activité par adulte")
        ax.set_title(yl, fontsize=10, loc="left", color=ENCRE)
        ax.xaxis.set_major_formatter(euros)
        ax.set_ylim(0, max(v) * 1.2)
        axes_propres(ax)
    fig.subplots_adjust(wspace=0.25)
    fin(fig, "ircsg_n13_franchise", SRC_M + ".",
        "Note : pour chaque franchise, le barème qui maximise le gain sur la participation (marge extensive) sous les "
        f"contraintes de la proposition : recette de {_fr(CIB)} Md€ (base 2025), aucun décile au-delà de plus ou moins 500 €, "
        "charge du 1 % le plus aisé inchangée. Participation : hypothèse centrale (élasticité de 0,25 sous 2 Smic).")


def n14():
    vs = [("proposition", "Proposition", PROP), ("quotient_c", "Quotient conjugal et familial", VAR),
          ("abat5_c", "Abattement de 5 % sur les pensions", VAR), ("abat10_c", "Abattement de 10 % sur les pensions", VAR),
          ("sortie_etalee_c", "Sortie de l'exonération étalée", VAR), ("cheque_egal_c", "Chèque par enfant (même coût)", VAR),
          ("franchise_4000", "Franchise de 4 000 €", VAR), ("franchise_0", "Sans franchise", VAR),
          ("haut_baisse", "Le 1 % peut payer moins", VAR)]
    vs = [v for v in vs if ARB.get(v[0])]
    fig, ax = plt.subplots(figsize=(9, 4.1))
    y = np.arange(len(vs))[::-1]
    for yy, (k, lab, col) in zip(y, vs):
        r = ARB[k]
        ax.barh(yy, r["gain_central"], color=col, height=0.6, zorder=2)
        ax.text(r["gain_central"] + 0.08, yy, f"{_fr(r['gain_central'], 1)} Md€ ; retraités {_fr(r['groupes']['retraites']['Md'], 1)} Md€",
                va="center", fontsize=8.5, color=ENCRE)
    ax.set_yticks(y)
    ax.set_yticklabels([lab for _, lab, _ in vs], fontsize=FS)
    ax.set_xlim(0, 8.5)
    ax.set_xlabel("Gain d'efficacité, Md€ par an (hypothèses centrales)")
    axes_propres(ax, grille="x")
    fin(fig, "ircsg_n14_arbitrages", SRC_M + " (arbitrages_prop_ircsg.py).",
        "Note : chaque variante change un paramètre de la proposition ; son barème est recherché de nouveau sous les mêmes "
        "contraintes (recette, déciles à plus ou moins 500 €, charge du 1 % inchangée, sauf la dernière ligne, où le 1 % peut payer moins). "
        "Retraités : variation de leur charge totale.")


def n15():
    cles = ["smic_mi", "smic", "cadre60", "cadre100", "pi_smic", "c2_50", "c3_60", "c0m_80", "c2m_50", "ret16", "ret20",
            "ret25", "rc45"]
    fig, ax = plt.subplots(figsize=(9, 4.3))
    y = np.arange(len(cles))[::-1]
    h = 0.38
    ax.barh(y + h / 2, [NQ["cas"][k]["delta"] for k in cles], height=h, color=NAIF, label="Réforme naïve", zorder=2)
    ax.barh(y - h / 2, [PR["cas"][k]["delta"] for k in cles], height=h, color=PROP, label="Proposition", zorder=2)
    ax.axvline(0, color=ENCRE2, lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels([PR["cas"][k]["libelle"].replace(" (60/40)", "") for k in cles], fontsize=FS * 0.92)
    ax.xaxis.set_major_formatter(euros)
    ax.set_xlabel("Variation de l'IR + CSG + CRDS, € par an (positif : paie plus)")
    axes_propres(ax, grille="x")
    legende(ax, loc="upper right")
    fin(fig, "ircsg_n15_cas_types", SRC_OF + " (outils_ircsg.py).",
        "Note : revenus bruts ; couples mariés ou pacsés, revenus partagés 60/40 sauf « un seul revenu » ; retraités de "
        "plus de 65 ans ; aucune niche. Les montants d'aujourd'hui figurent au tableau des ménages types.")


# ------------------------------------------------------------------ 6. transition
def n16():
    H = TR["hausses"]
    cles = ["Retraité seul, pension de 20 000 €", "Retraité seul, pension de 25 000 €",
            "Couple de retraités, 45 000 € de pensions (60/40)", "Retraités, 90e centile", "Couples de retraités, 90e centile"]
    lib = ["Retraité seul,\n20 000 €", "Retraité seul,\n25 000 €", "Couple de retraités,\n45 000 €", "Retraités,\n90e centile",
           "Couples de retraités,\n90e centile"]
    fig, ax = plt.subplots(figsize=(9, 3.6))
    x = np.arange(len(cles))
    w = 0.26
    for k, (an, col, lab) in enumerate((("an3", SEC, "Sur 3 ans"), ("an5", PROP, "Sur 5 ans"), ("an10", VAR, "Sur 10 ans"))):
        v = [H[c][an] for c in cles]
        ax.bar(x + (k - 1) * w, v, width=w, color=col, label=lab, zorder=2)
        for i, vv in enumerate(v):
            ax.text(i + (k - 1) * w, vv + 20, _fr(vv), ha="center", fontsize=7.8, color=ENCRE)
    ax.set_xticks(x)
    ax.set_xticklabels(lib, fontsize=FS * 0.95)
    ax.yaxis.set_major_formatter(euros)
    ax.set_ylabel("Hausse d'impôt chaque année")
    axes_propres(ax)
    legende(ax, loc="upper left")
    fin(fig, "ircsg_n16_transition", SRC_M + " (transition_ircsg.py).",
        "Note : convergence linéaire de l'ancien impôt vers le nouveau ; hausse supplémentaire chaque année jusqu'à la "
        "hausse finale. Centiles : foyers représentatifs du modèle, dont la dispersion est plus faible que la réalité.")


# ------------------------------------------------------------------ annexe
def n17():
    ok = PJ["admissibles"]
    Fs = sorted({r["F"] for r in ok})
    fig, ax = plt.subplots(figsize=(9, 3.9))
    for F, col in zip(Fs, NUANCES_BLEU[::-1]):
        rr = [r for r in ok if r["F"] == F]
        ax.scatter([r["part"] for r in rr], [r["gain"] for r in rr], s=10, color=col, label=f"Franchise {_fr(F)} €", zorder=2)
    ax.scatter([C["part"]], [C["gain"]], s=60, facecolor="none", edgecolor=VAR, lw=1.6, zorder=3)
    ax.annotate("Proposition", (C["part"], C["gain"]), xytext=(-10, 10), textcoords="offset points", ha="right", fontsize=9,
                color=ENCRE)
    ax.set_xlabel("Gain sur la participation (Md€)")
    ax.set_ylabel("Gain d'efficacité total (Md€)")
    dec = plt.FuncFormatter(lambda v, _: _fr(v, 2).rstrip("0").rstrip(","))
    ax.xaxis.set_major_formatter(dec)
    ax.yaxis.set_major_formatter(dec)
    axes_propres(ax)
    legende(ax, loc="upper left", ncol=2, markerscale=1.5)
    fin(fig, "ircsg_n17_designs", SRC_M + ".",
        f"Note : chaque point est un barème qui respecte les contraintes de la proposition ({PJ['n_ok']} sur {PJ['n_essais']} "
        "essayés) ; hypothèses centrales. Le gain total comprend la participation et la marge intensive.")


def n18():
    r4 = PJ["par_franchise"]["4000"]
    s4 = U.bareme(r4["t0"], r4["tb"], r4["z1"], r4["t1"], r4["z2"])
    o4 = dict(O_P, F=4000.0)
    se = ARB["sortie_etalee_c"]
    s_e = U.bareme(*se["bareme"])
    o_e = dict(O_P, Fp_pente=0.5)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.8), sharey=True)
    for ax, prof, xmax, t, xl, var in ((axs[0], "seul", 120e3, "Salarié seul", "Salaire net de cotisations, par an",
                                        (s4, o4, "Franchise de 4 000 €")),
                                       (axs[1], "retraite_seul", 60e3, "Retraité seul", "Pension brute, par an",
                                        (s_e, o_e, "Sortie de l'exonération étalée"))):
        for sched, o, col, lw, lab in ((None, None, AUJ, 1.0, "Aujourd'hui"), (S_P, O_P, PROP, 2.0, "Proposition"),
                                       (var[0], var[1], VAR, 1.6, var[2])):
            xs, ys = U.courbe_marginale(sched, o, prof, bmin=2000.0, bmax=xmax)
            ax.plot(xs, ys, color=col, lw=lw, label=lab, drawstyle="steps-post")
        ax.set_title(t, fontsize=10, loc="left", color=ENCRE)
        ax.set_xlabel(xl)
        ax.set_xlim(0, xmax)
        k_euros(ax)
        ax.yaxis.set_major_formatter(pct)
        axes_propres(ax)
        legende(ax, loc="upper left" if prof == "seul" else "upper right")
    axs[0].set_ylabel("Prélèvement sur 1 000 € de plus")
    axs[0].set_ylim(0, 90)
    fig.subplots_adjust(wspace=0.15)
    fin(fig, "ircsg_n18_variantes_marges", SRC_OF + " (synthese/arbitrages_prop_ircsg.py, outils_ircsg.py).",
        f"Note : {NOTE_MG}. Chaque variante a son propre barème, recherché sous les mêmes contraintes que la proposition. "
        "Franchise de 4 000 € : barème qui maximise le gain sur la participation à cette franchise. Sortie étalée : "
        "l'exonération des pensions baisse d'un demi-euro, et non d'un euro, par euro de pension au-delà de 12 500 €, et "
        "s'éteint à 37 500 € ; le taux marginal est alors 1,5 fois celui du barème, mais sur une bande deux fois plus "
        "large.")


if __name__ == "__main__":
    for f in (n01, n02, n03, n04, n05, n07, n08, n09, n10, n11, n12, n13, n14, n15, n16, n17, n18):
        f()
