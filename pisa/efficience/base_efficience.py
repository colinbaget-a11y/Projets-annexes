"""
Base de données du bulletin « Efficience des dépenses publiques en zone euro : que vaut un euro dépensé
en éducation et en santé ? » (C26-096). Toutes les séries qui ont servi à la note, pour l'UE-27, sur
toutes les années disponibles (des plus anciennes aux plus récentes : PISA 2000-2025, TIMSS 1995-2023,
Eurostat jusqu'en 2025).

    python base_efficience.py                  assemble la base depuis les fichiers sources/*.csv
    python base_efficience.py --telecharger    relance d'abord chaque extraction (Eurostat rapide ;
                                               PISA long : plusieurs Go de microdonnées)

Sources (un module par source dans sources/, chacun avec extraire() et un fichier .csv) :
  eurostat   indicateurs Eurostat (insertion, chercheurs, langues, dépense d'éducation, espérance de vie,
             mortalité, équipements, accès, reste à charge, médecins, vaccination, production pharmaceutique)
  pisa       indicateurs calculés sur les microdonnées PISA (scores, faibles et forts, dispersion, équité,
             climat scolaire, pensée créative, effectifs de 15 ans)
  timss      TIMSS 4e année (CM1) : scores et niveau avancé
  sante_ext  indicateurs de santé hors Eurostat (OCDE, ECDC, OMS) et calculs (surmortalité, inégalité
             territoriale des médecins, R&D pharmaceutique)
  ocde_sha   dépense de santé par habitant et reste à charge, OCDE Health Statistics

Sorties :
  base_efficience.csv     format long : pays, indicateur, annee, valeur, source, note
  base_efficience.sqlite  tables « donnees » et « indicateurs »
  indicateurs.csv         dictionnaire : les 53 indicateurs du bulletin (objectif, polarité, définition
                          retenue, année du bulletin), les dépenses, les pondérations et l'encadré
  couverture.csv          nombre de pays couverts par indicateur et par année
"""
import sqlite3
import sys
from pathlib import Path

import pandas as pd

ICI = Path(__file__).resolve().parent
SOURCES = ICI / "sources"
BRUT = Path("/tmp") / "efficience_brut"          # téléchargements volumineux, hors dépôt
MODULES = ["eurostat", "pisa", "timss", "sante_ext", "ocde_sha"]
UE27 = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU", "IE", "IT",
        "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"]
ECHANTILLON_EDU = [p for p in UE27 if p not in ("MT", "LU", "CY")]          # 24 pays du bulletin
ECHANTILLON_SANTE = [p for p in UE27 if p not in ("CY", "MT", "SK")]

# ----------------------------------------------------------------------------------------------
# Dictionnaire des indicateurs. Colonnes : identifiant de la base, domaine, objectif du bulletin,
# libellé du bulletin, polarité (+ : plus est mieux), année ou période retenue dans le bulletin
# (d'après le texte), remarque sur la correspondance avec la note.
# ----------------------------------------------------------------------------------------------
E, S = "education", "sante"
O = {"E1": "O1 Maîtrise des savoirs fondamentaux", "E2": "O2 Excellence et dynamisme académique",
     "E3": "O3 Équité et climat scolaire", "E4": "O4 Insertion dans la vie active",
     "S1": "O1 Résultats finaux de santé", "S2": "O2 Qualité et efficience clinique",
     "S3": "O3 Accès effectif et protection financière", "S4": "O4 Prévention, innovation et résilience"}
DICO = [
    # éducation, O1
    ("pisa_maths", E, "E1", "PISA mathématiques", "+", "2022", ""),
    ("pisa_lecture", E, "E1", "PISA lecture", "+", "2022", ""),
    ("pisa_sciences", E, "E1", "PISA sciences", "+", "2022", ""),
    ("timss4_maths", E, "E1", "TIMSS mathématiques (CM1)", "+", "2019 et 2023", ""),
    ("timss4_sciences", E, "E1", "TIMSS sciences (CM1)", "+", "2019 et 2023", ""),
    ("pisa_faibles_3domaines", E, "E1", "Part d'élèves peu performants", "-", "2022",
     "Élèves sous le niveau 2 dans les trois domaines à la fois (choix confirmé par l'auteur) ; "
     "microdonnées 2015-2025 ; par domaine : pisa_faibles_*"),
    # éducation, O2
    ("pisa_forts_maths", E, "E2", "Top performers en mathématiques", "+", "2022", ""),
    ("pisa_forts_lecture", E, "E2", "Top performers en lecture", "+", "2022", ""),
    ("pisa_forts_sciences", E, "E2", "Top performers en sciences", "+", "2022", ""),
    ("pisa_pensee_creative", E, "E2", "PISA pensée créative", "+", "2022",
     "Évaluée seulement en 2022 ; AT, IE et SE n'y ont pas participé"),
    ("edu_chercheurs", E, "E2", "Nombre de chercheurs (% population active)", "+", "2019-2024", ""),
    ("edu_langues_3plus", E, "E2", "Part de la population parlant 3 langues étrangères ou plus", "+",
     "2022", "Enquête sur l'éducation des adultes (2007, 2011, 2016, 2022), 25-64 ans"),
    ("timss4_avance_maths", E, "E2", "Part d'élèves au niveau avancé, TIMSS mathématiques", "+",
     "2019 et 2023", ""),
    ("timss4_avance_sciences", E, "E2", "Part d'élèves au niveau avancé, TIMSS sciences", "+",
     "2019 et 2023", ""),
    # éducation, O3
    ("pisa_resilients", E, "E3", "Part d'élèves résilients", "+", "2022",
     "Définition OCDE 2022 (quart inférieur ESCS national, quart supérieur national en maths) appliquée à "
     "tous les cycles ; l'OCDE retient la lecture en 2018 et les sciences en 2025"),
    ("pisa_ecart_escs_maths", E, "E3", "Écart favorisés / défavorisés", "-", "2022",
     "Écart de score en maths entre quartiles ESCS extrêmes"),
    ("pisa_securite", E, "E3", "Sentiment de sécurité (PISA)", "+", "2022",
     "Indice FEELSAFE, 2022 et 2025 seulement ; absent pour DE et DK (et ES en 2022)"),
    ("pisa_appartenance", E, "E3", "Sentiment d'appartenance (PISA)", "+", "2022", "Indice BELONG"),
    ("pisa_harcelement", E, "E3", "Exposition au harcèlement scolaire (PISA)", "-", "2022",
     "Indice BULLIED, depuis 2018 ; variante pisa_harcelement_freq (% subissant au moins un acte "
     "quelques fois par mois), rupture en 2025 (cyberharcèlement ajouté)"),
    ("pisa_d9d1_maths", E, "E3", "Dispersion des scores en mathématiques (D9-D1)", "-", "2022", ""),
    ("pisa_d9d1_lecture", E, "E3", "Dispersion en lecture (D9-D1)", "-", "2022", ""),
    ("pisa_d9d1_sciences", E, "E3", "Dispersion en sciences (D9-D1)", "-", "2022", ""),
    # éducation, O4
    ("edu_chomage_15_24", E, "E4", "Chômage des 15-24 ans", "-", "2019-2024", ""),
    ("edu_neet_15_29", E, "E4", "Taux de NEET", "-", "2019-2024", "Tranche d'âge 15-29 ans retenue (indicateur phare UE)"),
    ("edu_decrochage_18_24", E, "E4", "Taux de décrochage scolaire précoce (18-24 ans)", "-", "2019-2024", ""),
    ("edu_emploi_relatif", E, "E4", "Taux d'emploi des diplômés (relatif)", "+", "2019-2024",
     "Définition supposée : rapport des taux d'emploi 25-64 ans, supérieur / CITE 0-2 ; à confirmer"),
    ("edu_emploi_diplomes_recents", E, "E4", "Taux d'emploi des diplômés récents", "+", "2019-2024",
     "20-34 ans diplômés depuis 1 à 3 ans (CITE 3-8)"),
    # santé, O1
    ("sante_ev_naissance", S, "S1", "Espérance de vie à la naissance", "+", "2019-2024", ""),
    ("sante_ev_65", S, "S1", "Espérance de vie à 65 ans", "+", "2019-2024", ""),
    ("sante_evbs_naissance", S, "S1", "Espérance de vie en bonne santé à la naissance", "+", "2019-2024", ""),
    ("sante_evbs_65", S, "S1", "Espérance de vie en bonne santé à 65 ans", "+", "2019-2024", ""),
    ("sante_depression", S, "S1", "Prévalence de la dépression chronique", "-", "2019", "EHIS 2014 et 2019"),
    ("sante_surmortalite_12m", S, "S1", "Surmortalité sur 12 mois", "-", "2019-2024",
     "Moyenne annuelle de la surmortalité mensuelle Eurostat (référence 2016-2019)"),
    # santé, O2
    ("sante_mort_traitable", S, "S2", "Mortalité traitable", "-", "2019-2024", ""),
    ("sante_ima30", S, "S2", "Mortalité à 30 jours post-infarctus", "-", "2019-2024",
     "OCDE : série chaînée pour 20 pays, non chaînée pour AT, BE, DE, IE (définitions mêlées) ; "
     "série homogène non chaînée : sante_ima30_nonchaine"),
    ("sante_scanners", S, "S2", "Plateau technique : scanners (CT)", "+", "2019-2024", "Bloc imagerie : 1/18 de l'objectif chacun"),
    ("sante_irm", S, "S2", "Plateau technique : IRM", "+", "2019-2024", "Bloc imagerie"),
    ("sante_tep", S, "S2", "Plateau technique : TEP (PET)", "+", "2019-2024", "Bloc imagerie"),
    ("sante_gamma", S, "S2", "Plateau technique : gamma-caméras", "+", "2019-2024", "Bloc imagerie"),
    ("sante_mammographes", S, "S2", "Plateau technique : mammographes", "+", "2019-2024", "Bloc imagerie"),
    ("sante_radiotherapie", S, "S2", "Plateau technique : radiothérapie", "+", "2019-2024", "Bloc imagerie"),
    # santé, O3
    ("sante_besoins_non_satisfaits", S, "S3", "Besoins de soins non satisfaits (total)", "-", "2019-2024", ""),
    ("sante_besoins_non_satisfaits_q1", S, "S3", "Besoins non satisfaits (quintile le plus pauvre)", "-",
     "2019-2024", ""),
    ("sante_depenses_catastrophiques", S, "S3", "Ménages à dépenses de santé catastrophiques", "-",
     "2019-2024", "OMS Europe (UHCFP_4) : reste à charge > 40 % de la capacité à payer ; années rares"),
    ("sante_reste_a_charge", S, "S3", "Part du reste à charge", "-", "2019-2024",
     "La note donne 9,3 % pour la France et 14,9 % en moyenne UE (source : OCDE, Health at a Glance) ; "
     "Eurostat et l'OCDE (HF3, sante_reste_a_charge_ocde) donnent 10,2-10,4 % pour 2021-2024 : "
     "chiffre de la note non retrouvé"),
    ("sante_attente", S, "S3", "Temps d'attente moyen", "-", "2019-2024",
     "Définition non précisée dans la note ; base : délai moyen OCDE pour une prothèse de hanche "
     "(11 pays, pas la France) ; compléments sante_attente_mediane et sante_attente_silc"),
    ("sante_densite_medicale", S, "S3", "Densité médicale", "+", "2019-2024", "Médecins en exercice"),
    ("sante_inegalite_densite", S, "S3", "Inégalité territoriale de densité médicale", "-", "2019-2024",
     "Dispersion entre régions NUTS 2"),
    # santé, O4
    ("sante_mort_evitable_prev", S, "S4", "Mortalité évitable par la prévention", "-", "2019-2024", ""),
    ("sante_vaccin_grippe_65", S, "S4", "Vaccination antigrippale des 65 ans et plus", "+", "2019-2024", ""),
    ("sante_antibiotiques", S, "S4", "Consommation d'antibiotiques (J01)", "-", "2019-2024",
     "OCDE (ECDC non téléchargeable) ; totaux 2024 identiques à l'ECDC pour NL et EL"),
    ("sante_rd_pharma_ratio", S, "S4", "R&D pharmaceutique / dépense pharmaceutique", "+", "2019-2024",
     "BERD NACE C21 / dépense HC.5.1 ; rupture probable pour la France en 2021 (BERD x 2,9)"),
    ("sante_prod_pharma_croissance_10a", S, "S4", "Croissance de la production pharmaceutique sur 10 ans",
     "+", "2019-2024", ""),
]
AUTRES = [
    ("edu_dep_eleve_cite1_2_pub_eur", E, "dépense", "Dépense publique par élève, primaire et premier cycle "
     "du secondaire (EUR)", "", "moyenne 2022-2024",
     "Retrouvée : moyenne 2022-2023 pour la France = 9 362 EUR (la note : 9 360) ; 2024 pas encore publié"),
    ("sante_dep_hab_ocde_ppa", S, "dépense", "Dépense courante de santé par habitant, publique et privée, "
     "EUR à PPA (OCDE)", "", "2022", "Source indiquée par l'auteur : OCDE Health Statistics. France 4 164 "
     "(2022), 4 319 (2023) ; la note donne 4 250. Les autres pays de la figure 3 de la note (LU 8 900, "
     "IE sous la France) ne correspondent à aucune série OCDE ou Eurostat"),
    ("sante_dep_hab_spa", S, "dépense", "Dépense courante de santé par habitant, SPA (Eurostat)", "",
     "", "Identique à la série OCDE en PPA pour la France (4 164 en 2022)"),
    ("edu_cofog_hors_superieur_pib", E, "encadré", "Dépense publique d'éducation primaire et secondaire, "
     "% du PIB", "", "2022", "Retrouvée : FR 4,5 ; BE 5,3 ; EE 4,8 ; SI 4,6 (COFOG GF09 moins GF0904)"),
    ("edu_part_annexes", E, "encadré", "Services annexes, % de la dépense d'éducation", "", "2024",
     "13,5 % (note : près de 14 %) ; écart dû aux révisions COFOG"),
    ("edu_part_preprimaire_primaire", E, "encadré", "Pré-primaire et primaire, % de la dépense d'éducation",
     "", "2024", "28,4 % en 2024, 27,6-27,8 % en 2022-2023 (note : 27,5 %)"),
    ("edu_part_remunerations", E, "encadré", "Rémunérations (D1), % de la dépense d'éducation", "", "2024",
     "69,8 % (note : 71 %) ; écart dû aux révisions COFOG"),
    ("pisa_effectif_15ans", E, "pondération", "Population de 15 ans représentée dans PISA", "", "2022",
     "Pondération « effectifs scolarisés » (définition exacte non précisée dans la note)"),
    ("pisa_harcelement_freq", E, "complément", "Élèves subissant au moins un acte de harcèlement "
     "quelques fois par mois ou plus, %", "", "", "Mesure publiée par l'OCDE en 2018 et 2025"),
    ("pop_totale", S, "pondération", "Population au 1er janvier", "", "2022", ""),
]


def charger(telecharger=False):
    tables = []
    for nom in MODULES:
        f = SOURCES / f"{nom}.csv"
        if telecharger:
            sys.path.insert(0, str(SOURCES))
            mod = __import__(nom)
            if hasattr(mod, "telecharger"):
                (BRUT / nom).mkdir(parents=True, exist_ok=True)
                mod.telecharger(BRUT / nom)
            t = mod.extraire(BRUT / nom) if mod.extraire.__code__.co_argcount else mod.extraire()
            t.to_csv(f, index=False)
        if not f.exists():
            print(f"  source absente : {f.name}")
            continue
        t = pd.read_csv(f, dtype={"pays": str})
        t["module"] = nom
        tables.append(t)
        print(f"  {nom:10s} {len(t):6d} lignes, {t.indicateur.nunique():3d} indicateurs, "
              f"{int(t.annee.min())}-{int(t.annee.max())}")
    base = pd.concat(tables, ignore_index=True)
    base = base[base.pays.isin(UE27)].dropna(subset=["valeur"])
    return base.sort_values(["indicateur", "pays", "annee"]).reset_index(drop=True)


def dictionnaire(base):
    lignes = []
    for ident, dom, obj, lib, pol, an, rem in DICO + AUTRES:
        s = base[base.indicateur == ident]
        lignes.append({"indicateur": ident, "domaine": dom, "objectif": O.get(obj, obj),
                       "libelle_bulletin": lib, "polarite": pol, "annee_bulletin": an,
                       "source": "; ".join(sorted(s.source.astype(str).unique()))[:200],
                       "definition": s.note.dropna().iloc[0] if s.note.notna().any() else "",
                       "annees_disponibles": f"{int(s.annee.min())}-{int(s.annee.max())}" if len(s) else "",
                       "n_annees": s.annee.nunique(), "n_pays": s.pays.nunique(),
                       "dans_la_base": "oui" if len(s) else "NON", "remarque": rem})
    return pd.DataFrame(lignes)


if __name__ == "__main__":
    base = charger("--telecharger" in sys.argv)
    dico = dictionnaire(base)
    base.drop(columns="module").to_csv(ICI / "base_efficience.csv", index=False)
    dico.to_csv(ICI / "indicateurs.csv", index=False)
    couv = base.groupby(["indicateur", "annee"]).pays.nunique().unstack(fill_value=0)
    couv.to_csv(ICI / "couverture.csv")
    with sqlite3.connect(ICI / "base_efficience.sqlite") as con:
        base.to_sql("donnees", con, if_exists="replace", index=False)
        dico.to_sql("indicateurs", con, if_exists="replace", index=False)
        con.execute("CREATE INDEX IF NOT EXISTS i_donnees ON donnees(indicateur, pays, annee)")
    manque = dico[(dico.dans_la_base == "NON")].indicateur.tolist()
    print(f"\nBase : {len(base)} valeurs, {base.indicateur.nunique()} séries, "
          f"{base.annee.min()}-{base.annee.max()}")
    print(f"Indicateurs du bulletin présents : {53 - len([m for m in manque if m in [d[0] for d in DICO]])}/53")
    if manque:
        print("Absents :", ", ".join(manque))
