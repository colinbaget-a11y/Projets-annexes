"""
Reclassement des 121 prélèvements français selon des critères de taxation optimale.

La nomenclature SEC répond à une question comptable : à quel moment du circuit l'argent est
prélevé. Elle ne dit rien de ce qui est réellement taxé, ni de la distorsion produite. On
reclasse donc chaque prélèvement sur quatre dimensions, chacune adossée à une proposition
précise de la théorie (voir 02_cadre_theorique.md).

  assiette   ce que le prélèvement atteint en dernier ressort
  intrant    frappe-t-il un facteur ou une consommation intermédiaire ? (Diamond-Mirrlees 1971 :
             à l'optimum, aucun prélèvement ne doit distordre les décisions de production)
  correctif  corrige-t-il une externalité ou une internalité ? (Pigou : seul cas où taxer un
             intrant est justifié, puisque le dommage est le même quel que soit l'émetteur)
  verdict    lecture de l'auteur, au regard des principes retenus ; discutable par construction

Les affectations sont faites à la main pour tout prélèvement supérieur à 50 M€, par règle sur
la fonction économique Eurostat en dessous. Chaque choix discutable est commenté.

    python classification.py
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOUBLONS = {"D51M", "D51O"}

# nom exact dans la liste Eurostat -> (assiette, intrant, correctif, verdict, commentaire)
# intrant : oui / partiel / non      correctif : oui / partiel / non
C = {
    # ---------------------------------------------------------------- consommation
    "TVA": ("conso_menages", "partiel", "non", "conserver_base_large",
            "Neutre par construction tant que la chaîne de déduction est complète. Elle ne l'est pas : "
            "les secteurs exonérés ne déduisent pas la TVA de leurs intrants, qui reste incorporée dans leurs prix. "
            "Cette rémanence n'est pas isolable dans la liste Eurostat."),
    "Taxes sur les tabacs": ("conso_menages", "non", "oui", "conserver_correctif",
                             "Internalité et externalité ; le taux doit viser le dommage, pas le rendement."),
    "Taxes sur les boissons": ("conso_menages", "non", "oui", "conserver_correctif", ""),
    "Produits de la loterie nationale et du loto": ("conso_menages", "non", "partiel", "conserver_correctif",
                                                    "Mêle correction d'une internalité et prélèvement sur une rente de monopole."),
    "Taxes sur les paris hippiques": ("conso_menages", "non", "partiel", "conserver_correctif", ""),
    "Taxes sur les jeux des casinos": ("conso_menages", "non", "partiel", "conserver_correctif", ""),
    "Octroi de mer": ("conso_menages", "partiel", "non", "supprimer",
                      "Taxe sur les entrées de biens outre-mer : protège la production locale au prix d'une distorsion de production."),
    "Droits d'importation": ("conso_menages", "partiel", "non", "contrainte_europeenne",
                             "Ressource propre de l'Union ; un droit de douane distord la production, mais la décision n'est pas nationale."),
    "Part sur la consommation": ("conso_menages", "non", "non", "a_identifier",
                                 "Ligne sans nom dans la source, base déclarée : consommation."),
    "Taxes sur les spectacles": ("conso_menages", "non", "non", "fusionner_tva", ""),
    "Redevance cynégétique (permis de chasse)": ("conso_menages", "non", "non", "conserver_redevance", ""),

    # ---------------------------------------------------------------- assurance
    "Taxe spéciale sur les conventions d'assurance": ("conso_menages", "partiel", "non", "refondre",
        "L'assurance étant exonérée de TVA, on taxe la prime. Or la prime n'est pas une consommation : "
        "elle achète un transfert de risque. Taxer le partage du risque réduit la couverture, ce que rien ne justifie."),
    "Taxe de solidarité additionnelle": ("conso_menages", "partiel", "non", "refondre", "Même logique, sur les complémentaires santé."),
    "Cotisations sur primes d'assurance": ("conso_menages", "partiel", "non", "refondre", ""),
    "Taxe sur primes d'assurance automobile": ("conso_menages", "non", "partiel", "refondre", ""),

    # ---------------------------------------------------------------- énergie et environnement
    "Taxe intérieure de consommation des produits énergétiques": ("energie", "oui", "oui", "refondre_prix_carbone",
        "Frappe les ménages et les entreprises, à des tarifs très différents selon l'usage. "
        "Taxer un intrant est ici légitime : le dommage est le même quel que soit l'émetteur. "
        "Ce qui ne l'est pas, c'est que le prix implicite de la tonne varie d'un usage à l'autre."),
    "Accise sur l'électricité": ("energie", "oui", "partiel", "refondre_prix_carbone",
        "L'électricité française est peu carbonée : la taxer décourage l'électrification, c'est-à-dire l'inverse de l'objectif."),
    "Taxe intérieure sur la consommation de gaz naturel": ("energie", "oui", "oui", "refondre_prix_carbone", ""),
    "Taxe sur les émissions de CO2": ("intrant_entreprises", "oui", "oui", "conserver_correctif",
                                      "Produit des enchères de quotas : la seule assiette directement proportionnelle au dommage."),
    "Autres taxes sur l'énergie": ("energie", "oui", "partiel", "refondre_prix_carbone", ""),
    "Taxe sur les mises à disposition de produits pétroliers pour le stockage stratégique": ("intrant_entreprises", "oui", "non", "refondre_prix_carbone", ""),
    "Contribution des distributeurs d'énergie électrique basse tension": ("intrant_entreprises", "oui", "non", "supprimer", ""),
    "Imposition sur les pylônes": ("intrant_entreprises", "oui", "non", "supprimer", ""),
    "Impositions forfaitaires sur les entreprises de réseaux": ("intrant_entreprises", "oui", "non", "refondre",
        "Assise sur les équipements de réseau : taxe directement un facteur de production."),
    "Autres taxes sur la pollution": ("energie", "partiel", "oui", "conserver_correctif", ""),
    "Redevances sur les prélèvements de l'eau": ("energie", "oui", "oui", "conserver_correctif", ""),
    "Contribution sur les rentes infra marginales (électricité)": ("rente", "non", "non", "conserver_rente",
        "Porte sur une rente infra-marginale : la base la moins distorsive qui soit."),

    # ---------------------------------------------------------------- transport
    "Taxe sur les certificats d'immatriculation des véhicules": ("conso_menages", "partiel", "partiel", "refondre", ""),
    "Taxes sur les transports": ("energie", "partiel", "partiel", "refondre", ""),
    "Taxe sur les véhicules de tourisme des sociétés": ("intrant_entreprises", "oui", "partiel", "refondre", ""),
    "Taxe spéciale sur les véhicules routiers (taxe à l'essieu)": ("intrant_entreprises", "oui", "oui", "conserver_correctif",
        "Approxime l'usure de la voirie : correctif, donc légitimement assis sur un intrant."),

    # ---------------------------------------------------------------- revenus
    "Contribution sociale généralisée": ("revenu_global", "non", "non", "fusionner_impot_revenu",
        "Assiette large, taux proportionnel, unité individuelle. Avec l'impôt sur le revenu, la France entretient "
        "deux impôts sur le revenu dont ni l'assiette ni l'unité ne coïncident."),
    "Impôt sur le revenu": ("revenu_global", "non", "non", "fusionner_impot_revenu",
        "Assiette étroite, barème progressif, unité familiale, rendement 1,6 fois plus faible que la CSG."),
    "Contribution au remboursement de la dette sociale": ("revenu_global", "non", "non", "fusionner_impot_revenu", ""),
    "Autres prélèvements sociaux": ("revenu_capital", "non", "non", "refondre_rendement_normal",
        "Prélèvements sociaux sur les revenus du capital : frappent le rendement normal comme les rentes."),
    "Prélèvements sur les revenus des capitaux mobiliers": ("revenu_capital", "non", "non", "refondre_rendement_normal", ""),
    "Autres taxes sur le revenu": ("revenu_global", "non", "non", "fusionner_impot_revenu", ""),

    # ---------------------------------------------------------------- travail
    "Taxes sur les salaires": ("travail", "oui", "non", "supprimer_avec_tva",
        "Payée par les secteurs exonérés de TVA : substitut grossier à la TVA qu'ils n'acquittent pas, "
        "mais assis sur le seul facteur travail, donc il distord le choix capital-travail de ces secteurs."),
    "Versement mobilité": ("travail", "oui", "non", "supprimer",
        "Finance les transports urbains par une taxe sur la masse salariale : aucun lien entre l'assiette et le service rendu."),
    "Contributions des entreprises à la formation professionnelle et à l'apprentissage": ("travail", "oui", "non", "refondre", ""),
    "Forfait social": ("travail", "non", "non", "fusionner_impot_revenu", ""),
    "Cotisation patronale pour le FNAL (Fonds national d'aide au logement)": ("travail", "oui", "non", "supprimer", ""),
    "Contribution de solidarité pour l'autonomie": ("travail", "oui", "non", "fusionner_cotisations", ""),
    "Participation des employeurs à l'effort de construction": ("travail", "oui", "non", "supprimer", ""),
    "Taxes au profit de l'Association sur la garantie des salaires": ("travail", "oui", "non", "conserver_assurance", ""),
    "Contribution patronale sur stock-options": ("travail", "non", "non", "fusionner_impot_revenu", ""),
    "Part sur les salaires": ("travail", "oui", "non", "a_identifier",
                              "Ligne sans nom dans la source, base déclarée : salaires."),

    # ---------------------------------------------------------------- bénéfices
    "Impôts sur les sociétés y compris majoration et frais de poursuite": ("profit", "non", "non", "refondre_rendement_normal",
        "Sans déduction d'un rendement normal des fonds propres, l'impôt frappe aussi la rémunération "
        "de l'attente, et favorise la dette sur les fonds propres puisque l'intérêt est déductible et pas le dividende."),
    "Autres taxes": ("profit", "non", "non", "a_identifier", "Poste non nommé de 13,4 Md€ sur les bénéfices."),
    "Contribution sociale sur les bénéfices des sociétés": ("profit", "non", "non", "fusionner_is", ""),
    "Retenue sur les bénéfices non commerciaux": ("profit", "non", "non", "fusionner_is", ""),
    "Taxe sur infrastructures de transport longues distances": ("rente", "non", "non", "conserver_rente",
        "Vise les concessions d'infrastructure : rente de monopole concédé."),

    # ---------------------------------------------------------------- production et chiffre d'affaires
    "Contribution sociale de solidarité des sociétés": ("intrant_entreprises", "oui", "non", "supprimer",
        "Assise sur le chiffre d'affaires : chaque stade de la chaîne paie sur un montant qui inclut déjà la taxe "
        "payée en amont. Plus la chaîne compte d'étapes, plus le prélèvement total est élevé, à production identique."),
    "Cotisation foncière des entreprises": ("intrant_entreprises", "oui", "non", "refondre_fonciere",
        "Assise sur la valeur locative des locaux : taxe le capital productif, et le foncier d'activité."),
    "Taxe sur les surfaces commerciales": ("intrant_entreprises", "oui", "non", "supprimer", ""),
    "Taxe sur construction de bureaux et sur les locaux à usage de bureaux": ("intrant_entreprises", "oui", "non", "supprimer", ""),
    "Taxes sur la construction": ("intrant_entreprises", "oui", "non", "supprimer", ""),
    "Taxes sur les services professionnels hors droits de mutations": ("intrant_entreprises", "oui", "non", "supprimer", ""),
    "Taxe sur les services numériques": ("intrant_entreprises", "oui", "non", "contrainte_internationale",
        "Taxe sur le chiffre d'affaires, donc en cascade ; sa justification est l'impuissance à taxer le bénéfice là où il est créé."),
    "Taxes pharmaceutiques (contribution grossistes répartiteurs, taxe sur les ventes en gros)": ("intrant_entreprises", "oui", "non", "refondre", ""),
    "Cotisation des entreprises cinématographiques au profit du CNC (Centre national du cinéma)": ("intrant_entreprises", "oui", "non", "refondre", ""),
    "Taxe due par les opérateurs de communications électroniques": ("intrant_entreprises", "oui", "non", "supprimer", ""),
    "Contributions sur les loyers immobiliers": ("intrant_entreprises", "oui", "non", "supprimer", ""),
    "Taxe GEMAPI": ("intrant_entreprises", "oui", "non", "refondre_fonciere", ""),
    "Produit de l'imposition chambre de commerce": ("intrant_entreprises", "oui", "non", "supprimer", ""),
    "Chambre d'agriculture": ("intrant_entreprises", "oui", "non", "supprimer", ""),
    "Taxe chambre métier": ("intrant_entreprises", "oui", "non", "supprimer", ""),

    # ---------------------------------------------------------------- patrimoine
    "Foncier bâti": ("stock_capital", "partiel", "non", "refondre_fonciere",
        "Deux impôts en un : sur le terrain, c'est une taxe sur une rente, la meilleure assiette possible, "
        "l'offre de sol ne répondant pas au prix ; sur la construction, c'est une taxe sur le capital, qui décourage de bâtir. "
        "L'assiette reste celle des valeurs locatives de 1970."),
    "Foncier non-bâti (partie)": ("rente", "non", "non", "conserver_rente", "Assiette foncière pure, la plus proche d'une rente."),
    "Impôt de solidarité sur la fortune (jusque 2017) / Impôt sur la fortune immobilière (à partir de 2018)":
        ("stock_capital", "non", "non", "refondre",
         "Restreint à l'immobilier depuis 2018 : deux patrimoines de même valeur sont imposés différemment selon leur composition."),
    "Part sur le capital": ("stock_capital", "partiel", "non", "a_identifier",
                            "Lignes sans nom dans la source, base déclarée : capital."),
    "Contribution de sécurité immobilière": ("transaction", "non", "non", "supprimer", ""),

    # ---------------------------------------------------------------- transactions et transmissions
    "Droits d'enregistrement (y compris taxe additionnelle)": ("transaction", "non", "non", "supprimer",
        "Taxe la mutation et non la détention : bloque les échanges dont le gain est inférieur au droit. "
        "Le ménage qui déménage pour un meilleur emploi paie ; celui qui reste ne paie rien."),
    "Taxe sur les transactions financières": ("transaction", "non", "non", "supprimer", ""),
    "Mutations à titre gratuit": ("transmission", "non", "non", "refondre_assiette",
        "Taux faciaux élevés sur une assiette très réduite par les abattements, l'assurance-vie, "
        "l'exonération Dutreil et l'effacement des plus-values latentes au décès."),

    # ---------------------------------------------------------------- divers
    "Recettes diverses et pénalités": ("autre", "non", "non", "autre", ""),
}

# Règle de repli, à partir de la fonction économique Eurostat, pour les lignes non listées.
REPLI = {"C": ("conso_menages", "non"), "KS": ("stock_capital", "partiel"), "KIC": ("profit", "non"),
         "KIH": ("revenu_capital", "non"), "LEYRS": ("travail", "oui"), "LEES": ("travail", "non"),
         "SPLIT1": ("revenu_global", "non"), "_Z": ("autre", "non")}


def charger():
    rows = list(csv.DictReader(open(HERE / "donnees" / "ntl_france.csv", encoding="utf-8")))
    return [r for r in rows if r["details"] not in ("_T", "") and r["sto"] not in DOUBLONS and r["2024"] != ""]


def classer(r):
    nom = r["nom_fr"].strip()
    if nom in C:
        a, i, co, v, cm = C[nom]
        return dict(assiette=a, intrant=i, correctif=co, verdict=v, commentaire=cm, methode="manuelle")
    a, i = REPLI.get(r["fonction"], ("autre", "non"))
    return dict(assiette=a, intrant=i, correctif="non", verdict="non_examine", commentaire="", methode="repli")


COTISATIONS = [
    ("Cotisations sociales effectives à la charge des employeurs", "D611C", "travail", "partiel",
     "Prélèvement sur la masse salariale. Sa distorsion dépend du lien perçu entre la cotisation et le droit "
     "qu'elle ouvre : à la marge, une cotisation qui achète un point de retraite n'est pas un impôt, "
     "une cotisation qui finance une prestation universelle en est un."),
    ("Cotisations sociales effectives à la charge des ménages", "D613", "travail", "non",
     "Même question de contributivité, du côté du salarié et des indépendants."),
]


def main():
    det = charger()
    pib = {int(k): v for k, v in json.loads((HERE / "donnees" / "pib_france_cp_meur.json").read_text()).items()}
    G = pib[2024]
    lignes = []
    for r in det:
        c = classer(r)
        c.update(nom=r["nom_fr"].strip(), sto=r["sto"], fonction=r["fonction"], meur=float(r["2024"]))
        lignes.append(c)

    agg = {r["sto"]: float(r["2024"]) for r in csv.DictReader(open(HERE / "donnees" / "ntl_france.csv", encoding="utf-8"))
           if r["details"] == "_T" and r["2024"] != ""}
    for nom, sto, a, i, cm in COTISATIONS:
        lignes.append(dict(nom=nom, sto=sto, fonction="COTIS", meur=agg[sto], assiette=a, intrant=i,
                           correctif="non", verdict="fusionner_cotisations", methode="manuelle", commentaire=cm))

    with open(HERE / "donnees" / "classification_prelevements.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["nom", "sto", "fonction", "meur", "assiette", "intrant",
                                          "correctif", "verdict", "methode", "commentaire"])
        w.writeheader()
        w.writerows(lignes)

    tot = sum(l["meur"] for l in lignes)
    manuel = sum(l["meur"] for l in lignes if l["methode"] == "manuelle")
    print(f"{len(lignes)} prélèvements, {tot:,.0f} M€".replace(",", " "))
    print(f"classés à la main : {sum(1 for l in lignes if l['methode']=='manuelle')} lignes, "
          f"{manuel:,.0f} M€, soit {100*manuel/tot:.1f} % du produit\n".replace(",", " "))

    def table(cle, titre):
        d = defaultdict(float)
        n = defaultdict(int)
        for l in lignes:
            d[l[cle]] += l["meur"]; n[l[cle]] += 1
        print(f"=== {titre} ===")
        for k, v in sorted(d.items(), key=lambda t: -t[1]):
            print(f"  {k:26s} {v:9,.0f} M€   {100*v/G:5.2f} % du PIB   {100*v/tot:5.1f} %   ({n[k]} prélèvements)".replace(",", " "))
        print()
        return dict(d), dict(n)

    res = {"total_meur": tot, "pib_meur": G}
    for cle, t in [("assiette", "Ce qui est réellement taxé"),
                   ("intrant", "Prélèvements frappant un facteur ou une consommation intermédiaire"),
                   ("correctif", "Prélèvements correctifs"),
                   ("verdict", "Lecture au regard des principes retenus")]:
        d, n = table(cle, t)
        res[cle] = {"meur": d, "nombre": n}

    # agrégats parlants
    intr = sum(l["meur"] for l in lignes if l["intrant"] == "oui")
    intr_p = sum(l["meur"] for l in lignes if l["intrant"] == "partiel")
    non_corr = sum(l["meur"] for l in lignes if l["intrant"] == "oui" and l["correctif"] == "non")
    trans = sum(l["meur"] for l in lignes if l["assiette"] == "transaction")
    res["agregats"] = {
        "intrant_oui_meur": intr, "intrant_partiel_meur": intr_p,
        "intrant_oui_non_correctif_meur": non_corr, "transaction_meur": trans,
        "intrant_oui_pct_pib": 100 * intr / G, "intrant_oui_non_correctif_pct_pib": 100 * non_corr / G,
    }
    print("=== Synthèse ===")
    print(f"  prélèvements assis sur un intrant : {intr:,.0f} M€ ({100*intr/G:.2f} % du PIB), "
          f"plus {intr_p:,.0f} M€ partiellement".replace(",", " "))
    print(f"  dont sans justification correctrice : {non_corr:,.0f} M€ ({100*non_corr/G:.2f} % du PIB)".replace(",", " "))
    print(f"  prélèvements sur les transactions : {trans:,.0f} M€ ({100*trans/G:.2f} % du PIB)".replace(",", " "))
    (HERE / "decoupages.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
