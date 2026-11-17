"""« Pour aller plus loin », piste 1 : ce que rapporte un logement neuf à sa commune, aujourd'hui et après la réforme
foncière (scénario central B_E10 : part communale à double taux, sol taxé 4 fois plus que le bâti, à recette communale
constante ; taxe nationale de 10 Md€ sur le seul sol, qui ne va pas à la commune).

Taux moyens (taxe / valeur vénale) lus dans sorties/foncier3.json : aujourd'hui, taxe foncière du bloc communal sur
les logements ≈ 0,358 % de la valeur, sol et bâti confondus ; après réforme, part communale 0,569 % du sol et 0,142 % du
bâti [S]. Terrain nu avant construction : 0,08 % [H, convention du bloc foncier].
Autres recettes : taxe d'aménagement (part communale, unique) = surface × valeur forfaitaire 2026 (892 €/m², 1 011 en
Île-de-France ; service-public.fr, Institut Paris Région) × 50 % (abattement sur les 100 premiers m² d'une résidence
principale) × taux communal (1 à 5 % ; 3 % retenu [H]) ; DGF : variation de population × 64,46 à 128,93 € par habitant
(dotation forfaitaire, CGCT art. L. 2334-7, réponse ministérielle au Sénat du 29/09/2021), 2 habitants par logement [H].
Actualisation : 4 % réel sur 30 ans [H]. Exonération de deux ans de la taxe foncière (CGI art. 1383) dans le droit
actuel ; supprimée dans notre architecture.
Lancer : python3 note8p/calculs/pal_maires.py
"""
import json
from pathlib import Path

N8 = Path(__file__).resolve().parents[1]
F3 = json.loads((N8 / "sorties" / "foncier3.json").read_text(encoding="utf-8"))
TX = F3["scenarios"]["B_E10"]["taux"]
T0 = F3["g6"]["aujourdhui"]["t_sol"] / 100            # 0,358 %
TC_SOL, TC_BATI, TN_SOL = TX["tc_sol"] / 100, TX["tc_bati"] / 100, TX["tn_sol"] / 100
T_NU = 0.0008
R, H = 0.04, 30
VF_TA = {"hors_idf": 892.0, "idf": 1011.0}
TX_TA = 0.03
DGF_HAB = (64.46, 128.93)
HAB = 2.0

CAS = {
    "appartement_densification": {"libelle": "Appartement neuf de 65 m² à 290 000 € (sol 25 %), sur une parcelle déjà"
                                             " bâtie (densification)", "v": 290_000, "sol": 0.25, "m2": 65,
                                  "terrain_nu_avant": False},
    "appartement_friche": {"libelle": "Même appartement, sur un terrain auparavant nu", "v": 290_000, "sol": 0.25,
                           "m2": 65, "terrain_nu_avant": True},
    "maison_periurbaine": {"libelle": "Maison neuve de 100 m² à 250 000 € (sol 35 %), sur un terrain nu",
                           "v": 250_000, "sol": 0.35, "m2": 100, "terrain_nu_avant": True},
}


def ann(x, r=R, n=H, debut=0):
    return sum(x / (1 + r) ** k for k in range(debut, n))


def cas(c):
    S, B = c["v"] * c["sol"], c["v"] * (1 - c["sol"])
    avant = T_NU * S if c["terrain_nu_avant"] else 0.0
    # supplément annuel de taxe foncière communale dû à la construction (sol déjà taxé s'il portait un bâtiment)
    auj = T0 * (S + B) - (avant if c["terrain_nu_avant"] else T0 * S)
    if not c["terrain_nu_avant"]:
        auj = T0 * B          # densification : la valeur du sol était déjà taxée (approximation : sol inchangé)
    apres = TC_BATI * B       # la part communale sur le sol est la même avant et après la construction
    ta = c["m2"] * VF_TA["hors_idf"] * 0.5 * TX_TA
    dgf = tuple(HAB * d for d in DGF_HAB)
    va_auj = ann(auj, debut=2)          # exonération de deux ans (droit commun)
    va_apres = ann(apres)
    return {"libelle": c["libelle"], "sol": S, "bati": B,
            "tf_annuelle_aujourdhui": auj, "tf_annuelle_apres": apres, "baisse_pct": 100 * (1 - apres / auj),
            "perte_annuelle": auj - apres, "va_tf_aujourdhui": va_auj, "va_tf_apres": va_apres,
            "va_perte": va_auj - va_apres, "ta_communale_unique": ta, "dgf_annuelle_min_max": dgf,
            "va_dgf_min_max": tuple(ann(d, debut=1) for d in dgf),
            "taxe_nationale_sol_annuelle_pour_info": TN_SOL * S}


def ouverture(c=CAS["appartement_friche"], part_avant=0.2):
    """Ouverture à l'urbanisation : la valeur du sol (par logement) passe de part_avant × S à S [H]. Le gain communal
    annuel sur le sol après réforme, comparé à la taxe sur le bâti, dit où se loge désormais l'incitation."""
    S = c["v"] * c["sol"]
    return {"part_valeur_avant": part_avant, "gain_sol_communal_apres": TC_SOL * S * (1 - part_avant),
            "gain_sol_aujourdhui": 0.0,
            "note": "aujourd'hui, la taxe sur un terrain nu suit une valeur cadastrale de 1970 qui ne réagit pas à"
                    " l'ouverture à l'urbanisation ; gain ≈ 0 avant construction [H]",
            "part_nationale_si_territorialisee_25pct": 0.25 * TN_SOL * S * (1 - part_avant)}


def couts():
    dgf, bloc = 27.4, 19.1                 # Md€, LFI 2026 (DGF totale ; bloc communal)
    g = {}
    for m in (2000, 3000, 5000):
        for n in (150_000, 280_000, 300_000):
            c = m * n / 1e9
            g[f"{m}_eur_x_{n}"] = {"Md": c, "pct_dgf": 100 * c / dgf, "pct_dgf_bloc_communal": 100 * c / bloc}
    return {"dgf_2026_Md": dgf, "dgf_bloc_communal_2026_Md": bloc, "grille": g,
            "logements_commences_2025": 279_700,
            "sources": "DGF : 27,4 Md€ dont 19,1 bloc communal (Sénat, avis PLF 2026 ; préfectures) ; logements"
                       " commencés 2025 : SDES (Sit@del2), repris par les DREAL Grand Est et PACA"}


def calcule():
    return {"taux": {"aujourdhui": T0, "communal_sol_apres": TC_SOL, "communal_bati_apres": TC_BATI,
                     "national_sol": TN_SOL, "terrain_nu": T_NU},
            "hypotheses": {"r": R, "horizon": H, "taux_ta": TX_TA, "valeur_forfaitaire_ta": VF_TA,
                           "habitants_par_logement": HAB, "dgf_par_habitant": DGF_HAB},
            "cas": {k: cas(c) for k, c in CAS.items()}, "ouverture_urbanisation": ouverture(),
            "couts_dotation": couts()}


if __name__ == "__main__":
    R_ = calcule()
    print("taux :", {k: f"{100*v:.3f} %" for k, v in R_["taux"].items()})
    for k, d in R_["cas"].items():
        print(f"{k}: TF/an {d['tf_annuelle_aujourdhui']:.0f} → {d['tf_annuelle_apres']:.0f} € (−{d['baisse_pct']:.0f} %),"
              f" VA {d['va_tf_aujourdhui']:.0f} → {d['va_tf_apres']:.0f} (perte VA {d['va_perte']:.0f}) ; TA {d['ta_communale_unique']:.0f} ;"
              f" DGF/an {d['dgf_annuelle_min_max'][0]:.0f}-{d['dgf_annuelle_min_max'][1]:.0f}")
    o = R_["ouverture_urbanisation"]
    print(f"ouverture : gain communal sur le sol {o['gain_sol_communal_apres']:.0f} €/an par logement ; 25 % de la part"
          f" nationale : {o['part_nationale_si_territorialisee_25pct']:.0f} €/an")
    for k, v in R_["couts_dotation"]["grille"].items():
        print(k, f"{v['Md']:.2f} Md€ = {v['pct_dgf_bloc_communal']:.1f} % de la DGF du bloc communal")
