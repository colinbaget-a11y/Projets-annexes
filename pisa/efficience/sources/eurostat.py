"""
Indicateurs Eurostat de la base « efficience de la dépense publique » (éducation et santé), UE-27,
toutes les années disponibles.

    python sources/eurostat.py        écrit sources/eurostat.csv

Format de sortie (commun à toutes les sources) : pays, indicateur, annee, valeur, source, note.
"""
import json
import time
import urllib.request
from pathlib import Path

import pandas as pd

ICI = Path(__file__).resolve().parent
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
UE27 = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU", "IE", "IT",
        "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"]

# identifiant : (jeu, filtres, note). Toutes les autres dimensions doivent être fixées par les filtres.
SERIES = {
    # ------------------------------------------------------------ éducation : insertion
    "edu_chomage_15_24": ("une_rt_a", {"age": "Y15-24", "sex": "T", "unit": "PC_ACT"},
                          "Taux de chômage des 15-24 ans, % de la population active"),
    "edu_neet_15_29": ("edat_lfse_20", {"age": "Y15-29", "sex": "T", "wstatus": "NEMP",
                                        "training": "NO_FE_NO_NFE", "unit": "PC"},
                       "Jeunes de 15-29 ans ni en emploi, ni en études, ni en formation, %"),
    "edu_decrochage_18_24": ("edat_lfse_14", {"age": "Y18-24", "sex": "T", "wstatus": "POP",
                                              "unit": "PC"},
                             "Sortants précoces de l'éducation et de la formation, 18-24 ans, %"),
    "edu_emploi_diplomes_recents": ("edat_lfse_24", {"age": "Y20-34", "sex": "T", "duration": "Y1-3",
                                                     "isced11": "ED3-8", "unit": "PC"},
                                    "Taux d'emploi des 20-34 ans diplômés depuis 1 à 3 ans (CITE 3-8), "
                                    "hors études et formation, %"),
    "edu_emploi_25_64_cite5_8": ("lfsa_ergaed", {"age": "Y25-64", "sex": "T", "isced11": "ED5-8",
                                                 "unit": "PC"}, "Taux d'emploi des 25-64 ans diplômés du supérieur, %"),
    "edu_emploi_25_64_cite0_2": ("lfsa_ergaed", {"age": "Y25-64", "sex": "T", "isced11": "ED0-2",
                                                 "unit": "PC"}, "Taux d'emploi des 25-64 ans peu diplômés (CITE 0-2), %"),
    # ------------------------------------------------------------ éducation : excellence
    "edu_chercheurs": ("rd_p_perslf", {"prof_pos": "RSE", "sectperf": "TOTAL", "sex": "T",
                                       "unit": "PC_ACT_FTE"},
                       "Chercheurs en équivalent temps plein, % de la population active"),
    "edu_langues_3plus": ("edat_aes_l22", {"n_lang": "GE3", "age": "Y25-64", "unit": "PC"},
                          "Adultes de 25-64 ans déclarant connaître 3 langues étrangères ou plus, % "
                          "(enquête sur l'éducation des adultes)"),
    # ------------------------------------------------------------ éducation : dépense et effectifs
    "edu_dep_eleve_cite1_2_pub_eur": ("educ_uoe_fini04", {"unit": "EUR", "sector": "PUB", "isced11": "ED1_2"},
                                      "Dépense annuelle par élève (ETP) des établissements publics, "
                                      "primaire et premier cycle du secondaire, EUR (UOE)"),
    "edu_dep_eleve_cite1_2_pub_spa": ("educ_uoe_fini04", {"unit": "PPS", "sector": "PUB", "isced11": "ED1_2"},
                                      "Idem, en standard de pouvoir d'achat (SPA)"),
    "edu_dep_eleve_cite1_2_tot_eur": ("educ_uoe_fini04", {"unit": "EUR", "sector": "TOT_SEC", "isced11": "ED1_2"},
                                      "Dépense annuelle par élève (ETP), tous établissements, CITE 1-2, EUR (UOE)"),
    **{f"edu_dep_pub_pib_{nom}": ("educ_uoe_fine06", {"unit": "PC_GDP", "isced11": code},
                                  f"Dépense publique d'éducation, {lib}, % du PIB (UOE)")
       for nom, code, lib in (("cite02_8", "ED02-8", "pré-primaire au supérieur"),
                              ("cite1_2", "ED1_2", "primaire et premier cycle du secondaire"),
                              ("cite3_4", "ED3_4", "second cycle du secondaire et post-secondaire"))},
    "edu_dep_pub_pib_cite97": ("educ_figdp", {"unit": "PC", "indic_ed": "FP01_1"},
                               "Dépense publique totale d'éducation, % du PIB, tous niveaux (CITE 1997, "
                               "série arrêtée 1991-2011)"),
    "edu_eleves_cite1": ("educ_uoe_enra02", {"unit": "NR", "age": "TOTAL", "sex": "T", "isced11": "ED1"},
                         "Élèves inscrits dans le primaire (CITE 1), nombre"),
    "edu_eleves_cite2": ("educ_uoe_enra02", {"unit": "NR", "age": "TOTAL", "sex": "T", "isced11": "ED2"},
                         "Élèves inscrits dans le premier cycle du secondaire (CITE 2), nombre"),
    "edu_eleves_cite3": ("educ_uoe_enra02", {"unit": "NR", "age": "TOTAL", "sex": "T", "isced11": "ED3"},
                         "Élèves inscrits dans le second cycle du secondaire (CITE 3), nombre"),
    "edu_eleves_cite0": ("educ_uoe_enra02", {"unit": "NR", "age": "TOTAL", "sex": "T", "isced11": "ED0"},
                         "Enfants inscrits dans l'éducation de la petite enfance (CITE 0), nombre"),
    # ------------------------------------------------------------ santé : résultats finaux
    "sante_ev_naissance": ("demo_mlexpec", {"unit": "YR", "sex": "T", "age": "Y_LT1"},
                           "Espérance de vie à la naissance, années"),
    "sante_ev_65": ("demo_mlexpec", {"unit": "YR", "sex": "T", "age": "Y65"}, "Espérance de vie à 65 ans, années"),
    "sante_evbs_naissance": ("hlth_hlye", {"unit": "YR", "sex": "T", "hlth_hle": "HLY_Y0"},
                             "Espérance de vie en bonne santé (années de vie en bonne santé) à la naissance"),
    "sante_evbs_65": ("hlth_hlye", {"unit": "YR", "sex": "T", "hlth_hle": "HLY_Y65"},
                      "Espérance de vie en bonne santé à 65 ans"),
    "sante_depression": ("hlth_ehis_cd1e", {"unit": "PC", "hlth_pb": "DPR_CHR", "isced11": "TOTAL",
                                            "sex": "T", "age": "TOTAL"},
                         "Personnes déclarant une dépression chronique, % (EHIS, 15 ans et plus)"),
    # ------------------------------------------------------------ santé : qualité clinique
    "sante_mort_traitable": ("hlth_cd_apr", {"mortalit": "TRT", "icd10": "TOTAL", "sex": "T", "unit": "RT"},
                             "Mortalité traitable, taux standardisé pour 100 000 habitants"),
    "sante_mort_evitable_prev": ("hlth_cd_apr", {"mortalit": "PRVT", "icd10": "TOTAL", "sex": "T", "unit": "RT"},
                                 "Mortalité évitable par la prévention, taux standardisé pour 100 000 habitants"),
    **{f"sante_{nom}": ("hlth_rs_medim", {"unit": "P_HTHAB", "facility": code, "icha_hp": "HP1_3"},
                        f"{lib} pour 100 000 habitants (hôpitaux et soins ambulatoires)")
       for nom, code, lib in (("scanners", "CT_SCAN", "Scanners (tomodensitomètres)"),
                              ("irm", "MRI", "Appareils d'IRM"), ("tep", "PET_SCAN", "Caméras TEP"),
                              ("gamma", "GAMMA", "Gamma-caméras"), ("mammographes", "MAMMO", "Mammographes"),
                              ("radiotherapie", "RAD", "Équipements de radiothérapie"))},
    # ------------------------------------------------------------ santé : accès et protection financière
    "sante_besoins_non_satisfaits": ("hlth_silc_08", {"unit": "PC", "quant_inc": "TOTAL",
                                                      "reason": "TXP_TFAR_WLIST", "age": "Y_GE16", "sex": "T"},
                                     "Besoins d'examen médical non satisfaits (trop cher, trop loin ou "
                                     "liste d'attente), % des 16 ans et plus"),
    "sante_besoins_non_satisfaits_q1": ("hlth_silc_08", {"unit": "PC", "quant_inc": "QU1",
                                                         "reason": "TXP_TFAR_WLIST", "age": "Y_GE16", "sex": "T"},
                                        "Idem, premier quintile de revenu"),
    "sante_reste_a_charge": ("hlth_sha11_hf", {"unit": "PC_CHE", "icha11_hf": "HF3"},
                             "Paiements directs des ménages, % de la dépense courante de santé"),
    "sante_densite_medicale": ("hlth_rs_prs2", {"unit": "P_HTHAB", "med_spec": "PHYS", "wstatus": "PRACT"},
                               "Médecins en exercice pour 100 000 habitants"),
    "sante_densite_medicale_actifs": ("hlth_rs_prs2", {"unit": "P_HTHAB", "med_spec": "PHYS", "wstatus": "PACT"},
                                      "Médecins professionnellement actifs pour 100 000 habitants "
                                      "(substitut quand les médecins en exercice manquent)"),
    # ------------------------------------------------------------ santé : prévention, innovation
    "sante_vaccin_grippe_65": ("hlth_ps_immu", {"unit": "PC"},
                               "Vaccination contre la grippe des 65 ans et plus, %"),
    "sante_prod_pharma_indice": ("sts_inpr_a", {"indic_bt": "PRD", "nace_r2": "C21", "s_adj": "CA", "unit": "I21"},
                                 "Indice de production de l'industrie pharmaceutique (NACE C21), 2021 = 100"),
    # ------------------------------------------------------------ santé : dépense
    "sante_dep_hab_eur": ("hlth_sha11_hf", {"unit": "EUR_HAB", "icha11_hf": "TOT_HF"},
                          "Dépense courante de santé par habitant, tous financeurs, EUR"),
    "sante_dep_hab_spa": ("hlth_sha11_hf", {"unit": "PPS_HAB", "icha11_hf": "TOT_HF"},
                          "Dépense courante de santé par habitant, tous financeurs, SPA"),
    "sante_dep_pub_hab_eur": ("hlth_sha11_hf", {"unit": "EUR_HAB", "icha11_hf": "HF1"},
                              "Dépense courante de santé par habitant, régimes publics et obligatoires "
                              "(HF1, convention OCDE-Eurostat-OMS), EUR"),
    "sante_dep_pub_hab_spa": ("hlth_sha11_hf", {"unit": "PPS_HAB", "icha11_hf": "HF1"},
                              "Dépense courante de santé par habitant, régimes publics et obligatoires, SPA"),
    "sante_dep_pib": ("hlth_sha11_hf", {"unit": "PC_GDP", "icha11_hf": "TOT_HF"},
                      "Dépense courante de santé, % du PIB"),
    # ------------------------------------------------------------ pondérations
    "pop_totale": ("demo_pjan", {"unit": "NR", "age": "TOTAL", "sex": "T"}, "Population au 1er janvier"),
}

# Dépense publique d'éducation par fonction (COFOG), administrations publiques, en millions d'euros
COFOG_EDU = {"GF09": "Enseignement (total)", "GF0901": "Pré-primaire et primaire",
             "GF0902": "Secondaire", "GF0903": "Post-secondaire non supérieur", "GF0904": "Supérieur",
             "GF0905": "Non défini par niveau", "GF0906": "Services annexes", "GF0907": "R&D",
             "GF0908": "Enseignement n.c.a."}


def jsonstat(jeu, **filtres):
    q = "&".join(f"{k}={v}" for k, vs in filtres.items() for v in (vs if isinstance(vs, list) else [vs]))
    for essai in range(4):
        try:
            with urllib.request.urlopen(f"{API}{jeu}?{q}", timeout=300) as r:
                d = json.load(r)
            break
        except OSError:
            if essai == 3:
                raise
            time.sleep(5 * (essai + 1))
    dims, tailles = d["id"], d["size"]
    codes = [sorted(d["dimension"][x]["category"]["index"], key=d["dimension"][x]["category"]["index"].get)
             for x in dims]
    lignes = []
    for cle, val in d["value"].items():
        k, pos = int(cle), []
        for t in reversed(tailles):
            pos.append(k % t)
            k //= t
        pos.reverse()
        lignes.append({**{x: codes[i][p] for i, (x, p) in enumerate(zip(dims, pos))}, "valeur": val})
    return pd.DataFrame(lignes)


def extraire():
    sorties = []
    for ind, (jeu, filtres, note) in SERIES.items():
        t = jsonstat(jeu, geo=UE27, **filtres)
        if t.empty:
            print(f"  {ind:34s} AUCUNE DONNÉE ({jeu} {filtres})")
            continue
        autres = [c for c in t.columns if c not in ("geo", "time", "valeur", "freq", *filtres)]
        if any(t[c].nunique() > 1 for c in autres):
            raise ValueError(f"{ind} : dimensions non fixées {autres}")
        sorties.append(pd.DataFrame({"pays": t.geo, "indicateur": ind, "annee": t.time.astype(int),
                                     "valeur": t.valeur, "source": f"Eurostat {jeu}", "note": note}))
        print(f"  {ind:34s} {len(t):5d} valeurs, {t.time.min()}-{t.time.max()}")
    # COFOG : dépense d'éducation par sous-fonction (total et rémunérations)
    for na, suffixe, lib in (("TE", "", "dépense totale"), ("D1", "_d1", "rémunération des salariés")):
        t = jsonstat("gov_10a_exp", geo=UE27, unit="MIO_EUR", sector="S13", na_item=na,
                     cofog99=list(COFOG_EDU))
        for code, nom in COFOG_EDU.items():
            s = t[t.cofog99 == code]
            sorties.append(pd.DataFrame({
                "pays": s.geo, "indicateur": f"edu_cofog_{code.lower()}{suffixe}", "annee": s.time.astype(int),
                "valeur": s.valeur, "source": "Eurostat gov_10a_exp",
                "note": f"COFOG {code} {nom}, {lib}, administrations publiques, millions d'euros"}))
    t = jsonstat("gov_10a_exp", geo=UE27, unit="PC_GDP", sector="S13", na_item="TE", cofog99=["GF09", "GF07"])
    for code, ind in (("GF09", "edu_cofog_gf09_pib"), ("GF07", "sante_cofog_gf07_pib")):
        s = t[t.cofog99 == code]
        sorties.append(pd.DataFrame({"pays": s.geo, "indicateur": ind, "annee": s.time.astype(int),
                                     "valeur": s.valeur, "source": "Eurostat gov_10a_exp",
                                     "note": f"Dépense publique COFOG {code}, % du PIB"}))
    base = pd.concat(sorties, ignore_index=True)
    return pd.concat([base, derives(base)], ignore_index=True)


def derives(b):
    """Indicateurs calculés à partir des séries brutes."""
    w = b.pivot_table(index=["pays", "annee"], columns="indicateur", values="valeur")
    out = []

    def ajoute(ind, serie, note):
        s = serie.dropna()
        out.append(pd.DataFrame({"pays": s.index.get_level_values(0), "indicateur": ind,
                                 "annee": s.index.get_level_values(1), "valeur": s.values,
                                 "source": "calcul (Eurostat)", "note": note}))

    ajoute("edu_emploi_relatif", w.edu_emploi_25_64_cite5_8 / w.edu_emploi_25_64_cite0_2,
           "Rapport des taux d'emploi des 25-64 ans diplômés du supérieur et peu diplômés (CITE 5-8 / 0-2)")
    ajoute("edu_part_annexes", 100 * w.edu_cofog_gf0906 / w.edu_cofog_gf09,
           "Services annexes (GF0906 : transport, restauration, internat), % de la dépense publique d'éducation")
    ajoute("edu_part_preprimaire_primaire", 100 * w.edu_cofog_gf0901 / w.edu_cofog_gf09,
           "Pré-primaire et primaire (GF0901), % de la dépense publique d'éducation")
    ajoute("edu_part_remunerations", 100 * w.edu_cofog_gf09_d1 / w.edu_cofog_gf09,
           "Rémunération des salariés (D1), % de la dépense publique d'éducation")
    ajoute("edu_cofog_hors_superieur_pib", (1 - w.edu_cofog_gf0904 / w.edu_cofog_gf09) * w.edu_cofog_gf09_pib,
           "Dépense publique d'éducation hors enseignement supérieur (GF09 moins GF0904), % du PIB")
    eleves = w[["edu_eleves_cite0", "edu_eleves_cite1", "edu_eleves_cite2", "edu_eleves_cite3"]].sum(
        axis=1, min_count=4)
    ajoute("edu_dep_eleve_cofog_cite0_3", 1e6 * (w.edu_cofog_gf0901 + w.edu_cofog_gf0902) / eleves,
           "Dépense publique COFOG pré-primaire, primaire et secondaire (GF0901+GF0902) par élève inscrit "
           "en CITE 0 à 3, EUR (calcul ; les effectifs incluent le privé)")
    # croissance de la production pharmaceutique sur 10 ans
    ind = w.sante_prod_pharma_indice.unstack(0)
    ajoute("sante_prod_pharma_croissance_10a", (100 * (ind / ind.shift(10) - 1)).stack().swaplevel(),
           "Croissance de l'indice de production pharmaceutique (NACE C21) sur 10 ans, %")
    return pd.concat(out, ignore_index=True)


if __name__ == "__main__":
    b = extraire()
    b.sort_values(["indicateur", "pays", "annee"]).to_csv(ICI / "eurostat.csv", index=False)
    print(f"eurostat.csv : {len(b)} lignes, {b.indicateur.nunique()} indicateurs")
