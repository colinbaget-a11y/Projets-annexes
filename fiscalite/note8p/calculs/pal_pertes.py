"""« Pour aller plus loin », piste 2 : traitement fiscal des pertes des sociétés (IS à 25 %).

Droit de référence (vérifié sur le BOFiP, novembre 2026) : report en avant illimité, imputation plafonnée à 1 M€ plus
50 % du bénéfice au-delà (CGI art. 209 I ; BOI-IS-DEF-10-30) ; report en arrière optionnel du seul déficit de l'exercice
sur le bénéfice de l'exercice précédent, dans la limite de 1 M€ ; la créance s'impute sur l'IS des cinq années suivantes,
le solde est remboursé au terme de ce délai (CGI art. 220 quinquies ; BOI-IS-DEF-20 et 20-10).

Simulation [S] : valeur actualisée (taux d'actualisation de l'entreprise r = 5 %, variante 8 %) de l'impôt payé sur un
projet, sous cinq régimes, rapportée à la valeur actualisée du résultat imposable (taux effectif) et comparée à la
symétrie complète (l'État rembourse 25 % de la perte l'année même) :
  0. droit actuel ;
  1. indexation des nouveaux déficits reportables sur le taux de l'OAT à 10 ans (moyenne 2025, BCE) ;
  2. suppression du plafond d'imputation (1 M€ + 50 %) ;
  3. report en arrière sur trois exercices, sans plafond, créance remboursée l'année suivant le déficit ;
  4. report en arrière actuel (un exercice, 1 M€), créance remboursée l'année suivante (remboursement accéléré seul).
Ordres de grandeur nationaux [S/H] : coût de l'indexation = τ × C × ((1+i)^a − 1), C = déficits imputés chaque année,
a = âge moyen des déficits au moment de leur imputation (non publié : fourchette).
Lancer : python3 note8p/calculs/pal_pertes.py
"""
import csv
from pathlib import Path

TAU, PLANCHER, FRAC = 0.25, 1.0, 0.5         # M€ ; imputation ≤ 1 M€ + 50 % du bénéfice au-delà
ICI = Path(__file__).resolve().parent


def oat():
    rows = [r for r in csv.reader(open(ICI / "donnees_oat10_bce.csv", encoding="utf-8")) if r and not r[0].startswith("#")]
    rows = [r for r in rows if r[0].isdigit()]
    return int(rows[-1][0]), float(rows[-1][1]) / 100


AN_OAT, I_OAT = oat()

# Profils de résultat fiscal (M€). Les années ≤ 0 sont passées (déjà imposées) ; le projet commence en année 1.
PROFILS = {
    "jeune_pme": {"libelle": "Jeune PME : −0,4 M€ par an pendant 3 ans, puis +0,5 M€ par an (années 4 à 12)",
                  "passe": [], "projet": [-0.4] * 3 + [0.5] * 9},
    "eti_crise": {"libelle": "Entreprise établie (+3 M€ par an avant la crise) : −2 M€ par an pendant 3 ans,"
                             " puis +2,5 M€ par an (années 4 à 12)",
                  "passe": [3.0] * 3, "projet": [-2.0] * 3 + [2.5] * 9},
    "echec": {"libelle": "Même entreprise établie, qui disparaît après 3 ans de pertes",
              "passe": [3.0] * 3, "projet": [-2.0] * 3},
}


def simule(passe, projet, regime, i=I_OAT):
    """Impôt net payé chaque année du projet (M€ ; négatif = remboursement)."""
    n = len(projet)
    imp = [0.0] * (n + 1)                    # une année de plus pour un remboursement l'année suivant la dernière perte
    stock, creances = 0.0, []                # créances de report en arrière : [montant, année d'échéance]
    hist = list(passe)                       # bénéfices imposés des exercices antérieurs (base d'imputation en arrière)
    for t, y in enumerate(projet):
        if regime == "symetrie":
            imp[t] += TAU * y
            hist.append(max(y, 0.0))
            continue
        if regime == "indexation" and stock > 0:
            stock *= 1 + i
        if y >= 0:
            plafond = y if regime == "sans_plafond" else min(y, PLANCHER + FRAC * max(y - PLANCHER, 0.0))
            imput = min(stock, plafond)
            stock -= imput
            du = TAU * (y - imput)
            for c in creances:                # la créance paie l'IS des années suivantes
                u = min(c[0], du)
                c[0] -= u
                du -= u
            imp[t] += du
            hist.append(y - imput)
        else:
            perte = -y
            if regime in ("carry_back_3", "carry_back_rapide", "actuel", "indexation", "sans_plafond"):
                if regime == "carry_back_3":
                    porte = 3
                    lim = float("inf")
                else:
                    porte, lim = 1, PLANCHER
                rec = 0.0
                for k in range(1, porte + 1):
                    if len(hist) >= k and perte > 0 and lim > 0:
                        u = min(hist[-k], perte, lim)
                        hist[-k] -= u
                        perte -= u
                        lim -= u
                        rec += TAU * u
                if rec > 0:
                    if regime in ("carry_back_3", "carry_back_rapide"):
                        imp[t + 1] -= rec            # remboursée l'année suivante
                    else:
                        creances.append([rec, t + 5])   # imputée sur l'IS 5 ans, solde remboursé au terme
            stock += perte
            hist.append(0.0)
        for c in creances:                        # remboursement du solde au terme des cinq ans
            if c[1] == t and c[0] > 0:
                imp[t] -= c[0]
                c[0] = 0.0
    # créances encore vivantes à la fin de l'horizon : remboursées à l'échéance (actualisées comme telles)
    reste = [(c[0], c[1]) for c in creances if c[0] > 0]
    return imp, reste, stock


def va(flux, r, debut=1):
    return sum(f / (1 + r) ** (k + debut) for k, f in enumerate(flux))


def resultats(r=0.05):
    out = {}
    regs = ["symetrie", "actuel", "indexation", "sans_plafond", "carry_back_3", "carry_back_rapide"]
    for nom, p in PROFILS.items():
        d = {"libelle": p["libelle"], "regimes": {}}
        base = va(p["projet"], r)
        for reg in regs:
            imp, reste, stock = simule(p["passe"], p["projet"], reg)
            v = va(imp, r) - sum(m / (1 + r) ** (e + 1) for m, e in reste)
            d["regimes"][reg] = {"impot_par_annee": [round(x, 4) for x in imp], "va_impot": v,
                                 "taux_effectif_pct": 100 * v / base if abs(base) > 1e-9 else None,
                                 "deficit_perdu_fin_horizon": stock}
        sym = d["regimes"]["symetrie"]["va_impot"]
        for reg in regs:
            d["regimes"][reg]["surcout_vs_symetrie"] = d["regimes"][reg]["va_impot"] - sym
        d["va_resultat"] = base
        out[nom] = d
    return out


def national():
    """Ordres de grandeur [E] et coût de l'indexation [S/H]."""
    E = {
        "deficits_nouveaux_Md": {"2018": 65.0, "2021": 83.0, "2022": 113.0,
                                 "source": "DGFiP Statistiques n° 21, avril 2024 (exercice 2022)"},
        "report_arriere_Md": {"2021": {"montant_octroye": 1.2, "entreprises": 22000},
                              "2022": {"montant_octroye": 0.2, "genere_2022": 0.1, "entreprises_milliers": 7.8},
                              "source": "DGFiP Statistiques n° 21, tableau 3 et texte"},
        "stock_2010": {"stock_Md": 315.0, "dont_imputable_Md": 160.0, "droits_theoriques_Md": 53.0,
                       "consommation_annuelle_Md": 25.0, "flux_annee_normale_Md": 30.0,
                       "source": "Compte général de l'État 2010, cité par le rapport Carrez n° 3718 (AN, 2011)"},
        "plafonnement_2011_rendement_Md": {"2011": 0.5, "2012": 1.5,
                                           "source": "évaluation préalable de l'art. 2 LFR 2011-2, citée par le"
                                                     " rapport Marini n° 787 (Sénat, 2011)"},
        "carry_back_2021_cout_Md": {"montant": 0.4,
                                    "source": "commission des finances du Sénat, présentation du PLFR 2021 (23/06/2021)"},
    }
    grille = {}
    for C in (25.0, 32.0, 40.0):
        for a in (2, 4, 6):
            grille[f"C{C:g}_a{a}"] = TAU * C * ((1 + I_OAT) ** a - 1)
    central = TAU * 32.0 * ((1 + I_OAT) ** 4 - 1)
    montee = {str(2028 + k): TAU * 32.0 * ((1 + I_OAT) ** min(k, 4) - 1) * min(k / 4, 1.0) for k in range(0, 9)}
    return {"empirique": E, "oat10": {"annee": AN_OAT, "taux": I_OAT},
            "indexation_cout_regime_Md": {"grille": grille, "central": central,
                                          "hypotheses": "C = déficits imputés par an (25 Md€ en 2007-2010, portés à"
                                                        " 32 Md€ au centre, 40 en haut) ; a = âge moyen à l'imputation"
                                                        " (2 à 6 ans) [H] ; τ = 25 % ; nouveaux déficits seulement",
                                          "montee_en_charge_indicative": montee}}


if __name__ == "__main__":
    print(f"OAT 10 ans {AN_OAT} : {100*I_OAT:.2f} %")
    for r in (0.05, 0.08):
        R = resultats(r)
        print(f"--- r = {100*r:.0f} %")
        for nom, d in R.items():
            print(nom, f"VA résultat {d['va_resultat']:.2f} M€")
            for reg, x in d["regimes"].items():
                te = f"{x['taux_effectif_pct']:.1f} %" if x["taux_effectif_pct"] is not None else "-"
                print(f"   {reg:18s} VA impôt {x['va_impot']:7.3f}  taux {te:>8s}  surcoût {x['surcout_vs_symetrie']:+.3f}"
                      f"  déficit perdu {x['deficit_perdu_fin_horizon']:.2f}")
    N = national()
    print("indexation, coût en régime (Md€) :", {k: round(v, 2) for k, v in N["indexation_cout_regime_Md"]["grille"].items()},
          "central", round(N["indexation_cout_regime_Md"]["central"], 2))
