# Refaire le système fiscal français : architecture du rapport

Projet : un rapport d'environ 150 pages sur ce que serait le système fiscal français s'il
était reconstruit à partir de zéro pour être optimal. L'exercice prend pour modèle la
*Mirrlees Review* (2010-2011), avec deux différences : le terrain est français, et le système
à réformer comporte un bloc de cotisations sociales qui n'a pas d'équivalent britannique.

## La méthode qu'on emprunte à Mirrlees

Trois principes commandent toute la construction. Ils ne sont pas des slogans, chacun a une
conséquence opératoire.

1. **Juger le système comme un tout, pas impôt par impôt.** La progressivité, la neutralité et
   la contrainte de rendement se jugent sur l'ensemble. Il n'y a aucune raison que chaque
   impôt pris isolément soit progressif, ni que chacun soit neutre : il faut que le système le
   soit. Conséquence pratique : on n'évalue jamais un taux réduit de TVA sans dire par quoi on
   compense, et on ne discute pas de la fiscalité du capital sans l'articuler à celle du
   travail.

2. **Neutralité par défaut, écart justifié.** Deux activités économiquement semblables doivent
   être taxées de la même façon, sauf raison explicite : une externalité, un problème
   d'information, ou un gain d'efficience identifié. La charge de la preuve pèse sur l'écart,
   pas sur l'uniformité. Conséquence : chaque dérogation du système actuel doit être confrontée
   à la raison qui la justifierait.

3. **Obtenir la redistribution au moindre coût d'efficience.** La progressivité doit passer par
   l'instrument qui la produit avec le moins de distorsion, c'est-à-dire le barème direct des
   prélèvements et des transferts, plutôt que par la différenciation des taux sur les biens.

## Plan

### Partie I — Cadre (environ 20 pages)

1. **Ce que l'on cherche.** Les trois critères : efficience, équité, administrabilité. Ce que
   la théorie dit vraiment et ce qu'elle ne dit pas. Pourquoi l'exercice « from scratch » est
   utile même si la transition ne l'est pas. → `02_cadre_theorique.md`, rédigé.
2. **Les contraintes du cas français.** Le niveau de dépense à financer. L'ouverture et la
   mobilité des assiettes. La décentralisation et l'autonomie financière des collectivités. Le
   droit européen, le droit constitutionnel, la jurisprudence sur l'égalité devant l'impôt.

### Partie II — État des lieux (environ 45 pages)

3. **Anatomie des 1 270 Md€.** → `01_etat_des_lieux.md`, rédigé.
   **Découper selon ce que font les prélèvements.** → `03_decoupages.md`, rédigé.
4. **La taxation de la consommation.** TVA, accises, taxes sur les services spécifiques.
5. **La taxation du travail.** Les deux impôts sur le revenu, les cotisations, les allègements,
   l'interaction avec les transferts. Le barème effectif.
6. **La taxation du capital des ménages.** Revenus, stock, transmissions, immobilier.
7. **La taxation des entreprises.** Impôt sur les sociétés, impôts de production, fiscalité
   internationale.
8. **La fiscalité environnementale.** Prix implicites du carbone par usage.
9. **La fiscalité locale.**
10. **Le coût de la complexité.** Dépenses fiscales, micro-taxes, coûts de gestion et de
    conformité, contentieux, instabilité des règles.

### Partie III — Le système reconstruit (environ 60 pages)

11. **Consommation.** Base large, taux unique, compensation par le barème direct. Traitement
    des services financiers et du logement.
12. **Travail et transferts.** Fusion des deux impôts sur le revenu. Un barème effectif
    continu et lisible, du RSA au dernier décile. Choix de l'unité d'imposition.
13. **Épargne et capital.** Neutralité entre formes de détention. Les options disponibles :
    exonération du rendement normal, déduction à l'entrée, allocation pour rendement normal.
14. **Entreprises.** Suppression des impôts assis sur une assiette indépendante du résultat.
    Neutralité entre dette et fonds propres. Ce que l'on peut faire seul et ce qui dépend de
    la coordination européenne.
15. **Patrimoine et transmissions.** Détention contre transaction. Une base de taxation de la
    transmission reconstruite.
16. **Environnement.** Un prix unique du carbone et ce qu'il implique pour les autres taxes
    énergétiques.
17. **Fiscalité locale.** Quelle assiette pour quel échelon.

### Partie IV — Transition et économie politique (environ 25 pages)

18. **Les gagnants et les perdants**, mesurés par simulation sur données d'enquête.
19. **Les effets d'annonce et de capitalisation**, en particulier pour l'immobilier.
20. **Les séquences possibles**, et ce que l'on sait des réformes fiscales qui ont tenu.

## Méthode de travail

Chaque chiffre du rapport doit être traçable à un fichier de `donnees/` ou à une source
téléchargée dans `sources/`. Les affirmations qui ne le sont pas encore portent la marque
**[à sourcer]** dans le texte, et sont résolues avant publication du chapitre.

## Fichiers

| Fichier | Contenu |
|---|---|
| `extract_donnees.py` | télécharge et extrait les trois sources de base |
| `panorama.py` | agrégats, classement, concentration, déformation depuis 1995 |
| `donnees/ntl_france.csv` | 121 prélèvements français, rendement 1995-2024, code SEC, fonction économique |
| `donnees/pib_france_cp_meur.json` | PIB à prix courants, pour les ratios |
| `panorama.json` | les chiffres du chapitre 3 |
| `01_etat_des_lieux.md` | chapitre 3 rédigé |
| `02_cadre_theorique.md` | les propositions de taxation optimale retenues, et leurs conditions |
| `03_decoupages.md` | les quatre découpages analytiques et ce qu'ils commandent |
| `04_mirrlees_applique.md` | les diagnostics chiffrés de Tax by Design répliqués sur la France |
| `extract_mirrlees.py` | données OCDE TaxBEN et Effective Carbon Rates |
| `classification.py` | reclassement des 123 prélèvements sur quatre dimensions |
| `donnees/classification_prelevements.csv` | le classement ligne par ligne, avec le motif |
| `graphiques.py`, `graphiques_decoupages.py` | les seize figures |

## Sources déjà mobilisées

- Eurostat, *National Tax Lists*, mise à jour du 21 juillet 2026, onglet FR, données
  1995-2024. Liste détaillée transmise par la France avec la table 0900 du SEC 2010.
- Eurostat, `nama_10_gdp`, PIB à prix courants.
- *Évaluation des voies et moyens*, tome II, annexe au projet de loi de finances pour 2026 :
  dépenses fiscales de l'État.

## Sources à mobiliser ensuite

- *Voies et moyens* tome I, et la liste des taxes affectées, pour nommer les prélèvements que
  la liste Eurostat laisse en « autres taxes ».
- Annexes au PLFSS et données URSSAF, pour le détail des cotisations.
- Rapports du Conseil des prélèvements obligatoires et de la Cour des comptes, par bloc.
- Rapport de l'IGF sur les taxes à faible rendement.
- OCDE, *Revenue Statistics* et *Taxing Wages*, pour les comparaisons internationales.
- Listes Eurostat des 26 autres pays, déjà contenues dans le fichier téléchargé.
