"""Bloc IR-CSG v4 (révision finale, 19/11/2026) : données sur les niches de l'IR et tableau de travail par dispositif.

Sources lues pour cette révision (tout est recopié des documents, rien de mémoire) :
- CPO, « L'impôt sur le revenu, ses réductions et crédits d'impôt depuis 2017 », étude à la demande de la commission des
  finances de l'Assemblée nationale, septembre 2026 (PDF de 418 p., vie-publique.fr/files/rapport/pdf/304837.pdf) :
  synthèse (p. 15-19), tableaux 13 à 22 (chap. II), annexe 4 (fiches par dispositif : coût 2024, bénéficiaires,
  répartition par âge, répartition du coût par groupe de RFR par part : C01-C40, C41-C80, C81-C90, C91-C99, C100 ; les
  graphiques ont été lus sur les pages rendues en image). Champ : POTE 2024 (revenus 2024), montants effectivement
  imputés ou restitués.
- DGFiP Statistiques n° 41, « L'impôt sur le revenu 2024 a été plus dynamique que les revenus », novembre 2025 (PDF et
  classeur xlsx sur impots.gouv.fr) : tableaux 3 et 4, texte p. 5.
- Voies et moyens, tome II, PLF 2026 (coût 2025 ; fichier ir_csg/sorties/depenses_fiscales_ir_plf2026.csv, copie
  assemblee-nationale.fr). Le tome II du PLF 2027 n'a pas été trouvé sur les sites accessibles : non utilisé.
Statuts : [E] donnée publiée ; [H] hypothèse des auteurs ; [C] choix de politique.
"""
import numpy as np

GROUPES_C = ["C01-C40", "C41-C80", "C81-C90", "C91-C99", "C100"]   # groupes de RFR par part (CPO)
BORNES_C = [(0.0, 0.40), (0.40, 0.80), (0.80, 0.90), (0.90, 0.99), (0.99, 1.0)]
AGES = ["18-29", "30-49", "50-64", "65-79", "80+"]

# ------------------------------------------------------------------ chiffres d'ensemble [E]
ENSEMBLE = dict(
    foyers_M=41.5,                      # DGFiP n° 41, p. 1 (déclarations 2025, revenus 2024)
    beneficiaires_M=12.83,              # DGFiP n° 41, tableau 3 (au moins une RICI imputée ou restituée)
    part_foyers_pct=30.9,               # DGFiP n° 41, p. 5
    rici_Md=19.53,                      # DGFiP n° 41, tableau 3, y compris RI revenus de source étrangère (3,83)
    moyen_eur=1522.0,                   # DGFiP n° 41, tableau 3 (texte : « 1 500 € »)
    credits_Md=9.77, reductions_Md=9.75,
    credits_non_imposes_Md=4.0, credits_non_imposes_pct=45.0, restitutions_Md=2.0,   # DGFiP n° 41, p. 5
    imposes_beneficiaires_M=8.7, part_montant_imposes_pct=64.1,
    cpo_cout_2024_hors_double_imposition_Md=15.0, cpo_ri_Md=6.1, cpo_ci_Md=8.9,      # CPO, synthèse p. 17
    cpo_utilisateurs_M=14.26, cpo_utilisateurs_pct=34.3,                               # CPO, tableau 20
    cpo_beneficiaires_M=12.5, cpo_moins_1000_M=8.46,                                   # CPO, p. 105 et tableau 17
    cpo_plafonnement_global_M=45.0,
)
# CPO, tableau 17 : foyers selon le montant total de RICI (2024) : (borne basse, borne haute, foyers, montant moyen)
CPO_T17 = [(0, 1000, 8460800, 300), (1000, 2500, 2430700, 1600), (2500, 5000, 1005300, 3500), (5000, 7500, 362000, 6100),
           (7500, 10000, 124300, 8700), (10000, 25000, 78800, 14000), (25000, 50000, 15000, 33900),
           (50000, 100000, 1200, 61000), (100000, np.inf, 200, 219600)]
# CPO, tableau 21 : profils d'utilisation (millions de foyers) [E]
CPO_T21 = dict(un_seul=9.32, dons_seul=2.55, cisap_seul=2.28, scolarite_seul=2.20, garde_seul=1.09, autre_seul=1.20,
               deux=3.65, dons_cisap=1.19, dons_scolarite=0.46, cisap_scolarite=0.33, cisap_garde=0.18, trois_plus=1.29)
# CPO, tableau 15 : répartition (%) par groupe de RFR par part, 2024 [E]
CPO_T15 = {"impot_avant_rici": [0.3, 14.2, 14.9, 40.1, 30.6], "reductions": [0.1, 22.1, 18.9, 44.0, 14.9],
           "credits": [19.1, 33.5, 14.2, 25.7, 7.4], "double_imposition": [0.7, 3.7, 6.2, 41.7, 47.6],
           "impot_du": [-1.6, 12.2, 15.1, 41.2, 33.1], "rfr": [14.4, 38.3, 14.6, 21.3, 11.4]}
# DGFiP n° 41, tableau 4 : RICI moyenne par foyer (€) par décile de RFR par part, hors RICI PFU [E]
DGFIP_T4_RICI_DECILE = [48.8, 93.2, 126.5, 154.9, 182.4, 223.0, 286.3, 396.7, 647.2, 2538.3]

# ------------------------------------------------------------------ dispositifs : fiches CPO (annexe 4) et DGFiP [E]
# cout : coût 2024 (Md€, CPO) ; benef : bénéficiaires 2024 ; repC : % du coût par groupe C (2024, lu sur les graphiques) ;
# age : (% de foyers de la classe d'âge bénéficiaires, montant moyen €) ; vm : coût 2025 Voies et moyens PLF 2026 (Md€)
FICHES = {
    "emploi_domicile": dict(cout=6.507, benef=5146000, repC=[16, 30, 15, 30, 9], vm=7.029, tot_pct=12.36,
                            age=[(1.04, 674), (8.62, 1328), (10.42, 1250), (17.82, 1036), (40.95, 1468)]),
    "dons": dict(cout=2.212, benef=4948000, repC=[0, 29, 21, 37, 13], vm=2.204, tot_pct=11.88,
                 age=[(3.70, 299), (9.35, 420), (13.69, 458), (19.31, 458), (15.33, 519)]),
    "garde": dict(cout=1.796, benef=1946000, repC=[26, 49, 12, 12, 1], vm=1.799, tot_pct=4.67,
                  age=[(3.38, 830), (12.46, 937), (0.19, 727), (0.0, 756), (0.0, 0)]),
    "locatif": dict(cout=1.562, benef=385000, repC=[0, 11, 22, 57, 10], vm=1.459 + 0.169 + 0.030, tot_pct=0.925,
                    age=[(0.047, 3046), (1.127, 4019), (1.910, 4176), (0.440, 3657), (0.062, 3402)]),
    "outre_mer": dict(cout=0.781, benef=59000, repC=[0, 1, 5, 52, 41], vm=0.825, tot_pct=0.14,
                      age=[(0.03, 9297), (0.20, 12213), (0.21, 15013), (0.09, 13057), (0.02, 13116)]),
    "scolarite": dict(cout=0.468, benef=2591000, repC=[0, 61, 17, 18, 3], vm=0.229 + 0.225, tot_pct=6.22,
                      age=[(0.01, 100), (10.47, 156), (11.34, 212), (0.25, 182), (0.01, 174)]),
    "dependance": dict(cout=0.307, benef=242000, repC=[0, 42, 29, 27, 2], vm=0.312, tot_pct=0.582,
                       age=[(0.002, 391), (0.024, 571), (0.155, 784), (0.537, 1173), (5.077, 1344)]),
    "pme": dict(cout=0.100, benef=47000, repC=None, vm=0.052 + 0.029 + 0.010 + 0.009 + 0.009, tot_pct=0.11,
                age=[(0.05, 916), (0.16, 1808), (0.14, 2672), (0.09, 2523), (0.03, 2613)]),
}


def population_par_age():
    """Nombre de foyers par classe d'âge, déduit des fiches CPO : pour chaque dispositif, la part de bénéficiaires de
    l'ensemble (tot_pct) est la moyenne des parts par âge pondérée par la population de chaque classe ; on résout par
    moindres carrés non négatifs (8 dispositifs, 5 inconnues, somme = 41,5 M). [S] à partir de [E]."""
    A, b = [], []
    for f in FICHES.values():
        A.append([p / 100 for p, _ in f["age"]])
        b.append(f["tot_pct"] / 100)
    A, b = np.array(A), np.array(b)
    # normalisation : parts de population s_a, somme 1 (contrainte forte ajoutée comme équation pondérée)
    A2 = np.vstack([A * 10, 1000 * np.ones(5)])
    b2 = np.r_[b * 10, 1000.0]
    s = np.linalg.lstsq(A2, b2, rcond=None)[0]
    for _ in range(50):                      # moindres carrés non négatifs (projection simple)
        neg = s < 0
        if not neg.any():
            break
        s = np.where(neg, 0.0, s)
        k = ~neg
        s[k] = np.linalg.lstsq(A2[:, k], b2, rcond=None)[0]
    return dict(zip(AGES, s * ENSEMBLE["foyers_M"]))


def part_retraites(cle, pop=None):
    """Part du coût d'un dispositif qui va aux foyers de 65 ans et plus (fiche CPO, âge moyen des déclarants)."""
    pop = pop or population_par_age()
    f = FICHES[cle]
    c = [p / 100 * pop[a] * m for (p, m), a in zip(f["age"], AGES)]
    return float(sum(c[3:]) / sum(c)) if sum(c) else 0.0


# ------------------------------------------------------------------ tableau de travail par dispositif
# classement : V = vraie niche ; R = mesure du revenu ; X = externalité ou bien public ; N = neutralisation d'une double
# imposition ; S = non supprimable (conventions) ; G = gardé (invalidité, dépendance) ; H = hors périmètre de l'assiette
# modele : "residu" = l'avantage est dans l'écart droit simulé − impôt observé (27,1 Md€) ; "hors" = le revenu exonéré
# n'est pas dans l'assiette du modèle (sa taxation est une recette en plus du modèle) ; "etape" = traité par une autre
# étape de la cascade ; "nul" = ni l'un ni l'autre
# part : part supprimable en régime de croisière [C/H] ; ramp : profil de la recette 2027… (fraction du régime de croisière,
# avant la montée en charge λ de la fusion) ; recette = coût 2025 (Voies et moyens) × part [S statique]
TABLEAU = [
    # clé, libellé, coût VM 2025 (Md€), bénéficiaires, classement, modèle, part, profil, commentaire
    ("emploi_domicile", "Crédit emploi d'un salarié à domicile", 7.029, "5,1 M", "V/X", "residu", 1.0, "immediat",
     "Crédit remboursable ; 32 % des dépenses « contraintes » (CPO) ; 16 % du coût aux 40 % les plus modestes, 39 % au "
     "dixième le plus aisé. Le motif « emploi déclaré » relève d'une aide sociale ciblée (APA, CMG), pas de l'impôt."),
    ("garde", "Crédit frais de garde des enfants de moins de 6 ans", 1.799, "1,9 M", "R/V", "residu", 1.0, "immediat",
     "Coût de l'activité des parents (argument de mesure du revenu) ; remboursable ; 75 % du coût sous le 8e dixième. "
     "Remplacement possible par le CMG ou les crèches : une dépense, qui n'est pas gratuite."),
    ("dons", "Réduction pour dons (66 % et 75 %)", 2.204, "4,9 M", "X", "residu", 1.0, "immediat",
     "Externalité (biens publics) ; 50 % du coût au dixième le plus aisé, 13 % au centième ; un abondement budgétaire "
     "des dons reste possible (dépense)."),
    ("locatif_stock", "Pinel, Duflot, Scellier, Denormandie (engagements en cours)", 1.658, "0,39 M", "V", "residu", 0.0,
     "stock", "Pinel fermé fin 2024 ; les réductions engagées courent jusqu'en 2036 (CPO). Le droit actuel les éteint "
     "déjà : les supprimer ne rapporte rien par rapport au droit actuel, sauf à revenir sur des engagements (confiance "
     "légitime). Gardées jusqu'à extinction."),
    ("outre_mer", "Girardin (investissements productifs et logement outre-mer)", 0.825 + 0.037 + 0.020 + 0.012, "59 000",
     "V", "residu", 1.0, "reports",
     "Avantage moyen 13 200 € ; 93 % du coût au dixième le plus aisé ; IGF 2023 : pratiques abusives. Plus de nouveaux "
     "investissements ; les reports des réductions déjà acquises s'imputent encore quelques années [H : 60 % la première "
     "année, 100 % la 4e]."),
    ("dom", "Réduction de 30 % ou 40 % de l'impôt dans les DOM", 0.426, "0,6 M", "V", "residu", 1.0, "immediat",
     "Réduction territoriale ; à remplacer, si on veut aider, par une dépense ciblée sur la vie chère."),
    ("scolarite", "Frais de scolarité (collège, lycée, supérieur)", 0.454, "2,6 M", "V", "residu", 1.0, "immediat",
     "Forfaitaire (61 à 183 €) ; redondant avec la franchise par enfant ; le CPO (2024) recommande sa suppression."),
    ("pme", "Souscriptions PME, FCPI, FIP, SOFICA, JEI, foncières solidaires", 0.052 + 0.029 + 0.010 + 0.009 + 0.009
     + 0.035 + 0.017, "0,05 M", "V", "residu", 1.0, "reports",
     "Avantage concentré au dixième supérieur ; reports possibles sur 4 ans."),
    ("syndicales", "Crédit cotisations syndicales", 0.156, "1,3 M", "R", "residu", 1.0, "immediat",
     "Frais professionnels : restent déductibles au titre des frais réels."),
    ("prestation_comp", "Prestation compensatoire en capital", 0.056, "18 000", "V", "residu", 1.0, "immediat", ""),
    ("autres_rici", "Autres réductions et crédits (Malraux, bornes, forêts, agriculture bio, comptabilité…)",
     0.044 + 0.036 + 0.023 + 0.022 + 0.015 + 0.010 + 0.143, "", "V", "residu", 0.55, "immediat",
     "Réduction pour frais de comptabilité supprimée en 2025 par le droit actuel (0,14) : pas de recette ; le reste supprimé."),
    ("dependance", "Frais de dépendance et d'hébergement en établissement", 0.312, "0,24 M", "G", "residu", 0.0, "garde",
     "Gardée (charge contrainte liée à la dépendance) ; coût compté dans la recette à tenir."),
    ("source_etrangere", "Réduction pour revenus de source étrangère", 3.833, "0,49 M", "N/S", "residu", 0.0, "garde",
     "Élimine une double imposition, découle des conventions : non supprimable. Moitié supposée sur des revenus du "
     "barème [H], dans l'écart du modèle."),
    ("heures_sup", "Exonération des heures supplémentaires (7 500 €)", 2.212, "≈ 10 M de foyers", "V", "residu", 1.0,
     "immediat", "Les heures supplémentaires restent soumises à la CSG ; l'exonération d'IR tombe ; la réduction de "
     "cotisations salariales (hors périmètre) est inchangée."),
    ("epargne_salariale", "Exonération de l'intéressement et de la participation placés, PPV", 2.890, "n.d.", "V", "hors",
     0.85, "immediat", "Assujettis à la CSG, donc dans l'assiette du nouvel impôt ; 15 % supposés se reporter vers "
     "l'épargne retraite déductible [H]. Revenu absent de l'assiette du modèle : recette ajoutée."),
    ("ij_ald", "Exonération des indemnités journalières (ALD, AT-MP)", 0.621 + 0.015, "n.d.", "V", "hors", 1.0, "immediat",
     "Revenu de remplacement : imposé comme le revenu qu'il remplace (déjà soumis à la CSG)."),
    ("impatries", "Régime des impatriés, salariés détachés", 0.394 + 0.369, "87 000", "V/S", "hors", 0.25, "immediat",
     "Détachés : en partie conventions ; impatriés : mobiles ; recette prudente [H]."),
    ("etudiants_apprentis", "Salaires des apprentis et jobs d'étudiants", 0.533 + 0.314, "n.d.", "H", "nul", 0.0, "immediat",
     "Apprentis : hors assiette de la CSG ; avec le taux d'entrée bas, enjeu faible ; non chiffré."),
    ("titres_restaurant", "Titres-restaurant, transports, chèques-vacances (part employeur)", 0.555 + 0.239 + 0.088,
     "≈ 6 M", "H", "nul", 0.0, "immediat",
     "Hors assiette de la CSG : relèvent d'une réforme de l'assiette sociale, pas de ce bloc."),
    ("demi_parts", "Demi-parts : vivant seul ayant élevé un enfant, anciens combattants, veufs avec enfants",
     0.684 + 0.475 + 0.115, "2,3 M", "V", "residu", 1.0, "immediat",
     "Avantages sans rapport avec la capacité contributive actuelle ; surtout des retraités."),
    ("demi_part_invalides", "Demi-parts des invalides et des personnes à charge invalides", 0.538 + 0.177, "1,8 M", "G",
     "residu", 0.0, "garde", "Gardées (compensation d'un handicap) ; coût compté dans la recette à tenir."),
    ("abat_pensions", "Abattement de 10 % sur les pensions", 5.322, "15,1 M", "V", "etape", 1.0, "immediat",
     "Étape « alignement des pensions » de la cascade."),
    ("abat_ages", "Abattement des personnes âgées ou invalides modestes", 0.419, "7,2 M", "V", "etape", 1.0, "immediat",
     "Étape « alignement des pensions »."),
    ("foncier_reparations", "Déduction des travaux de réparation et d'amélioration", 1.990, "1,9 M", "R", "nul", 0.0,
     "immediat", "Charge de l'activité de location : mesure du revenu, gardée."),
    ("foncier_autres", "Déductions spécifiques (Cosse, Borloo…), déficits fonciers", 0.180, "0,2 M", "V", "nul", 0.0,
     "stock", "Engagements en cours, à éteindre ; non chiffré."),
    ("independants", "Abattements et exonérations des indépendants (BA, BNC, BIC)", 0.563, "n.d.", "V/R", "nul", 0.0,
     "immediat", "Hétérogènes ; à expertiser ; non chiffré."),
    ("prestations", "Prestations familiales, AAH, APL, APA exonérées", 2.625, "n.d.", "H", "nul", 0.0, "immediat",
     "Prestations sous condition de ressources, hors assiette : gardées hors assiette."),
]
PROFILS = {  # fraction de la recette de croisière perçue l'année n de la réforme (n = 1 en 2027) [H]
    "immediat": [1.0] * 14, "reports": [0.6, 0.8, 0.9] + [1.0] * 11, "stock": [0.0] * 14, "garde": [0.0] * 14}


def tableau():
    rows = []
    for cle, lib, cout, ben, cls, mod, part, prof, com in TABLEAU:
        rows.append(dict(cle=cle, libelle=lib, cout_vm_2025_Md=round(cout, 3), beneficiaires=ben, classement=cls,
                         modele=mod, part_supprimable=part, profil=prof, recette_croisiere_Md=round(cout * part, 3),
                         commentaire=com))
    return rows


def recette_par_profil(rows, annees=range(2027, 2041)):
    """Recette annuelle (Md€, niveau 2025) des niches supprimées, avant la montée en charge λ de la fusion."""
    out = {}
    for k, an in enumerate(annees):
        out[str(an)] = sum(r["recette_croisiere_Md"] * PROFILS[r["profil"]][k] for r in rows
                           if r["modele"] in ("residu", "hors"))
    return out


if __name__ == "__main__":
    pop = population_par_age()
    print("population par âge (M) :", {k: round(v, 2) for k, v in pop.items()})
    for c in FICHES:
        print(c, "part du coût aux 65 ans et plus :", round(part_retraites(c, pop), 3))
    for r in tableau():
        print(f"{r['cle']:22s} {r['cout_vm_2025_Md']:6.2f} {r['classement']:4s} {r['modele']:6s} {r['part_supprimable']:4.2f}"
              f" -> {r['recette_croisiere_Md']:5.2f}")
