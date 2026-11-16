"""Figures de la synthèse d'ensemble (ensemble_n01 à ensemble_n04), d'après sorties/synthese_ensemble.json.

Couleurs de la note (style_note.py) : proposition en bleu, variante en ocre, élément secondaire en gris clair,
composantes d'une décomposition en nuances de bleu. Titres : dans le document (\\figbloc) ; sources et notes de
lecture : figures/nu/<nom>_note.tex.

Lancer depuis fiscalite/, après synthese/synthese_ensemble.py :
python3 synthese/figures_ensemble.py && FIG_NU=1 python3 synthese/figures_ensemble.py
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
from graphiques import ECH_TXT, fin, plt  # noqa: E402
from style_note import AUJ, NUANCES_BLEU, PROP, SEC, VAR, ENCRE, ENCRE2, axes_propres, _fr  # noqa: E402

D = json.loads((HERE / "sorties/synthese_ensemble.json").read_text(encoding="utf-8"))
FS = 9 * ECH_TXT
SRC = "Calculs de l'auteur (synthese/synthese_ensemble.py), d'après les sorties des quatre parties"


def md(v, d=1):
    return _fr(v, d) + " Md€"


def sg(v, d=1):
    """Nombre signé à la française (+1,1 ; −0,4 ; 0,0 quand l'arrondi est nul)."""
    if abs(v) < 0.5 * 10 ** -d:
        return _fr(0.0, d)
    return ("+" if v > 0 else "") + _fr(v, d)


H_ = D["haut"]
V2_ = H_["v2"]
CRDS_PTS = _fr(-D["crds"]["points"], 2)


# ------------------------------------------------------------------ 1. gain d'efficacité
def n01():
    G = D["gains"]
    lignes = [("Fusion IR-CSG", G["ircsg"]), ("Immobilier", G["foncier"]), ("Impôt sur les sociétés", G["is"]),
              ("Revenus du capital", G["pfu"]), ("Ensemble", G["total"])]
    fig, ax = plt.subplots(figsize=(9, 3.4))
    y = np.arange(len(lignes))[::-1]
    for yy, (nom, g) in zip(y, lignes):
        tot = nom == "Ensemble"
        ax.plot([g["bas"], g["haut"]], [yy, yy], color=SEC, lw=2.2, solid_capstyle="round", zorder=2)
        ax.barh(yy, g["central"], height=0.5, color=AUJ if tot else PROP, zorder=3)
        lab = "non chiffré" if nom == "Revenus du capital" else md(g["central"])
        ax.text(max(g["central"], g["haut"]) + 0.25, yy, lab, va="center", fontsize=9.5, color=ENCRE,
                fontweight="bold" if tot else "normal")
        if "long" in g:
            ax.plot(g["long"], yy, marker="D", ms=6.5, color=VAR, mec="white", mew=1.2, zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels([n for n, _ in lignes], fontsize=FS * 1.05)
    ax.set_xlim(0, 17.5)
    ax.set_xlabel("Baisse de la perte sèche, Md€ par an")
    axes_propres(ax, grille="x")
    ax.plot([], [], color=SEC, lw=2.2, label="fourchette (élasticités basses à hautes)")
    ax.plot([], [], marker="D", ls="none", color=VAR, mec="white", label="jeu de long terme")
    ax.legend(frameon=False, fontsize=8.5, loc="center right")
    fin(fig, "ensemble_n01_gain", SRC + " : sorties/proposition_ircsg.json, transition_ircsg.json, calculs_foncier.json, "
        "perte_seche_autres.txt.",
        "Note : perte sèche statique évitée, à recette constante, par rapport à aujourd'hui ; elle mesure des "
        "renoncements (heures, emplois, ventes de logements, machines) et non un effet sur la croissance. Fusion : jeu "
        "central d'élasticités, fourchette des jeux bas et haut ; immobilier : 6 % de ventes en plus par point de "
        "droits en moins, de 0 à 15 % ; IS : déduction immédiate des équipements, élasticité du capital de 0,5 à 1,6. "
        "La fin de l'effacement des plus-values à la transmission n'est pas chiffrée (l'épargne ne réagit pas dans "
        "la note). Le jeu de long terme ne change que la fusion (réaction des heures et de la carrière de 0,10 à 0,25).")


# ------------------------------------------------------------------ 2. trajectoire
def n02():
    T = D["trajectoire"]
    ans = [t["an"] for t in T]
    comp = [("Fin de l'effacement", "pfu", NUANCES_BLEU[1]), ("Fin de la CEHR", "haut", NUANCES_BLEU[4]),
            ("Immobilier", "foncier", NUANCES_BLEU[3]), ("Impôt sur les sociétés", "is_", NUANCES_BLEU[0])]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.9), gridspec_kw=dict(width_ratios=[1.25, 1], wspace=0.32))
    x = np.arange(len(ans))
    pos, neg = np.zeros(len(ans)), np.zeros(len(ans))
    for nom, cle, col in comp:
        v = np.array([t[cle] for t in T])
        base = np.where(v >= 0, pos, neg)
        a1.bar(x, v, bottom=base, width=0.68, color=col, label=nom, zorder=2, edgecolor="white", linewidth=0.6)
        pos += np.where(v >= 0, v, 0)
        neg += np.where(v < 0, v, 0)
    tot = np.array([t["total"] for t in T])
    a1.plot(x, tot, marker="o", ms=4.5, color=ENCRE, lw=0, zorder=4, label="Solde")
    a1.axhline(0, color=ENCRE2, lw=0.7, zorder=3)
    a1.set_xticks(x[::1])
    a1.set_xticklabels([str(a) if i == 0 else str(a)[2:] for i, a in enumerate(ans)], fontsize=FS)
    a1.set_ylabel("Md€ par an")
    a1.set_title("Solde annuel des réformes", loc="left", fontsize=10, color=ENCRE)
    axes_propres(a1)
    a1.legend(frameon=False, fontsize=7.6, ncol=2, loc="lower right", handlelength=1.2, columnspacing=0.8)
    a1.set_ylim(-19, 9.5)
    for cle, nom, col, ls in (("dette", "proposition (avec fin de la CEHR)", PROP, "-"),
                              ("dette_sans", "sans fin de la CEHR", SEC, "-")):
        v = [t[cle] for t in T]
        a2.plot(ans, v, color=col, lw=2.1, ls=ls, label=nom, zorder=3)
        a2.text(ans[-1] + 0.25, v[-1], _fr(v[-1], 0), va="center", fontsize=8.5, color=ENCRE)
    i = int(np.argmax([t["dette"] for t in T]))
    a2.annotate(f"pic : {_fr(T[i]['dette'], 0)} Md€", (ans[i], T[i]["dette"]), xytext=(0, -16),
                textcoords="offset points", ha="center", fontsize=8.5, color=ENCRE)
    a2.set_ylim(0, 56)
    a2.set_xlim(ans[0] - 0.3, ans[-1] + 1.1)
    a2.set_xticks(ans[::3])
    a2.set_ylabel("Md€, intérêts compris")
    a2.set_title("Dette cumulée de transition", loc="left", fontsize=10, color=ENCRE)
    axes_propres(a2)
    a2.legend(frameon=False, fontsize=7.6, loc="upper left")
    fin(fig, "ensemble_n02_trajectoire", SRC + " : is/sorties/calculs_note_is.json (transition, cas central), "
        "sorties/calculs_foncier.json (calendrier sur cinq ans), pfu/sorties/calculs_pfu.json (recette, jeu central).",
        "Note : solde par rapport au droit en vigueur (+ : recette en plus). La fusion IR-CSG est à recette constante "
        "chaque année et n'apparaît pas. Fin de la CEHR : suppression de la majoration du PFU et disparition de la CEHR "
        f"sur les revenus du barème ({md(H_['cehr']['total'])}, CEHR des revenus de 2025). Barème adouci : 50 % atteint à "
        f"{_fr(V2_['z2b'] / 1e6, 2)} M€ au lieu de {_fr(H_['z2_prop'] / 1e3, 0)} 000 € au-delà de 150 000 € "
        f"({md(V2_['cout'])}). Dette : intérêts au taux d'emprunt de l'État de la partie IS (3,25 %). Ne sont pas comptés : "
        "la fin de la contribution exceptionnelle sur l'IS (7 Md€ par an de moins qu'en 2026), l'extinction de la CRDS "
        f"en 2034 (à recette constante si le taux fusionné baisse de {CRDS_PTS} point), les avances du report de taxe "
        "foncière (prêts, hors solde). Montants de 2025 pour l'essentiel (IS : bénéfices de 2025 portés en 2027), "
        "additionnés sans indexation.")


# ------------------------------------------------------------------ 3. le haut
def n03():
    H = D["haut"]
    eff = H["effacement"]["central"]
    pas = [("Fusion\nIR-CSG", H["top_ircsg"]["mixte"]), ("CEHR sur\nle barème", -H["cehr"]["bar"][0] / 2 - H["cehr"]["bar"][1] / 2),
           ("Fin de\nl'effacement", eff)]
    bil = H["bilan"]["central"]
    maj = -H["compensation"]["cehr_cap"]
    apres = H["bilan_majoration"]["central"]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    cum, xs = 0.0, []
    for i, (nom, v) in enumerate(pas):
        ax.bar(i, v if abs(v) > 0.02 else 0.04, bottom=cum, width=0.6,
               color=PROP if v >= 0 else NUANCES_BLEU[4], zorder=2)
        ax.text(i, max(cum, cum + v) + 0.15, sg(v, 1), ha="center", fontsize=9.5, color=ENCRE)
        cum += v
        xs.append(nom)
    ax.bar(3, bil, width=0.6, color=AUJ, zorder=2)
    ax.text(3, bil + 0.15, sg(bil, 1), ha="center", fontsize=9.5, color=ENCRE, fontweight="bold")
    ax.bar(4, maj, bottom=bil, width=0.6, color=NUANCES_BLEU[4], zorder=2)
    ax.text(4, bil + 0.15, _fr(maj, 1), ha="center", fontsize=9.5, color=ENCRE)
    ax.bar(5, apres, width=0.6, color=AUJ, zorder=2)
    ax.text(5.33, apres, sg(apres, 1), va="center", fontsize=9.5, color=ENCRE, fontweight="bold")
    for v, lab in ((H["bilan_majoration"]["imput"], "IR du capital corrigé"),
                   (H["bilan_majoration"]["conv_haut"], "revenus du capital logés tout en haut")):
        ax.plot(5, v, marker="D", ms=7, color=VAR, mec="white", mew=1.2, zorder=4)
        yt = v + 0.17 if abs(v) < 0.2 else v          # au-dessus de l'axe quand le losange est sur le zéro
        ax.text(5.33, yt, f"{sg(v, 1)} : {lab}", va="center", fontsize=8.5, color=ENCRE2,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.5))
    ax.axhline(0, color=ENCRE2, lw=0.7)
    ax.set_xticks(range(6))
    ax.set_xticklabels(xs + ["Bilan", "Fin de la\nmajoration", "Après\ncompensation"], fontsize=FS * 0.9)
    ax.set_xlim(-0.5, 8.4)
    ax.set_ylim(-2.2, 3.3)
    ax.set_ylabel("Md€ par an (+ : paie davantage)")
    axes_propres(ax)
    fin(fig, "ensemble_n03_haut", SRC + " : sorties/proposition_ircsg.json, controle_hauts_purs.txt, "
        "pfu/sorties/calculs_pfu.json.",
        "Note : 1 % des foyers au revenu le plus élevé ; convention centrale du modèle IR-CSG pour la répartition des "
        "revenus du capital entre tranches. Fin de l'effacement : moyenne des dix premières années "
        f"({_fr(H_['effacement']['bas'], 1)} à {md(H_['effacement']['haut'])}), en supposant que le 1 % en paie 90 %. "
        f"CEHR : {md(H_['cehr']['total'])} (revenus de 2025), dont 50 à 80 % payés sur les revenus du capital "
        "(hypothèse). L'immobilier (au plus quelques centaines de millions) et l'IS ne sont pas comptés. Losanges : "
        f"même bilan avec {_fr(H_['imput'], 1)} Md€ d'IR imputés aux revenus du capital au lieu de 11,5 (revenus de "
        "2024), ou dans la convention « haut ».")


# ------------------------------------------------------------------ 4. cas-types cumulés
_CAS = {c["cle"]: c for c in D["cas_types"]["cas"]}


def n04():
    C = D["cas_types"]["cas"]
    noms = {"retraite_province": "Retraité modeste,\nmaison à Limoges", "retraites_paris": "Couple de retraités,\nParis",
            "primo_lyon": "Jeune couple, 2 enfants,\nachète à Lyon", "monoactif_3enf": "Un seul revenu, 3 enfants,\nlocataire",
            "cadre_paris": "Cadre, achète\nà Paris", "dirigeant": "Dirigeant de PME\navec holding",
            "rentier": "Rentier"}
    comp = [("Fusion IR-CSG", lambda c: c["ircsg"], NUANCES_BLEU[0]),
            ("Logement (taxe foncière, droits annualisés)", lambda c: c["tf"] + c["droits_an"], NUANCES_BLEU[2]),
            ("Impôt de la société", lambda c: c["is_"], NUANCES_BLEU[4])]
    fig, ax = plt.subplots(figsize=(9, 4.25))
    y = np.arange(len(C))[::-1]
    pos, neg = np.zeros(len(C)), np.zeros(len(C))
    for nom, f, col in comp:
        v = np.array([f(c) for c in C])
        base = np.where(v >= 0, pos, neg)
        ax.barh(y, v, left=base, height=0.6, color=col, label=nom, zorder=2, edgecolor="white", linewidth=0.6)
        pos += np.where(v >= 0, v, 0)
        neg += np.where(v < 0, v, 0)
    for yy, c, pp, nn in zip(y, C, pos, neg):
        t = c["total_an"]
        x0 = pp + 250 if t >= 0 else nn - 250
        ax.text(x0, yy, ("+" if t > 0 else "") + _fr(t, 0) + " €", va="center", ha="left" if t >= 0 else "right",
                fontsize=9, color=ENCRE, fontweight="bold")
        if c["transm"] > 0:
            m = c["transm"]
            lab = (_fr(m / 1e6, 1) + " M€" if m >= 1e6 else _fr(m, 0) + " €")
            ax.text(8300, yy, "héritiers : " + lab, va="center", ha="left", fontsize=8.2, color=ENCRE2, style="italic")
    ax.axvline(0, color=ENCRE2, lw=0.7, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels([noms[c["cle"]] for c in C], fontsize=FS * 0.98)
    ax.set_xlim(-16500, 13000)
    ax.set_xticks(range(-12000, 8000, 4000))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: ("+" if v > 0 else "") + _fr(v, 0)))
    ax.set_xlabel("€ par an (+ : paie davantage)")
    axes_propres(ax, grille="x")
    ax.legend(frameon=False, fontsize=8, loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=3, handlelength=1.2)
    fin(fig, "ensemble_n04_cas_types", SRC + " : cas-types OpenFisca de la partie IR-CSG (sorties/proposition_ircsg.json), "
        "logements médians de la partie Immobilier, société type de la partie IS, cas de la partie PFU.",
        f"Note : variation annuelle au terme des transitions (fusion après cinq ans, avant la baisse de {CRDS_PTS} point "
        "liée à la fin de la CRDS en 2034). Droits de mutation économisés à l'achat ramenés à un montant annuel sur dix "
        f"ans de détention, à 3 % (Lyon : {_fr(-_CAS['primo_lyon']['droits'], 0)} €, Paris : "
        f"{_fr(-_CAS['cadre_paris']['droits'], 0)} € une fois). Taxe foncière sans effet sur les prix ; hausse "
        "reportable pour les retraités. En italique : impôt sur la plus-value latente que les héritiers paieront en "
        "vendant (rien aujourd'hui). Hypothèses de chaque ménage : tableau de la section et sortie du programme.")


if __name__ == "__main__":
    for f in (n01, n02, n03, n04):
        f()
