# Réforme de la fiscalité immobilière : moins de droits de mutation, plus de taxe foncière, deux taux

Note livrée (novembre 2026) pour le rapport Sorbon : `note-foncier.pdf` (7 pages) et `note-foncier.docx`
(par `python3 ../ir_csg/tex2docx.py ../foncier/note-foncier` depuis `ir_csg/`). Objectif de l'auteur : une fiscalité immobilière
favorable à la croissance et à l'accession à la propriété, en particulier des jeunes. Trois volets :
état des lieux de tous les prélèvements assis sur l'immobilier ; littérature (problèmes de l'impôt foncier,
effets des droits de mutation, en priorité sur la France) ; proposition simulée (baisser les DMTO de 30 à 50 %,
reporter la recette sur la taxe foncière, passer à deux taux, terrain plus taxé que le bâti).

S'appuie sur la note « Taxer le terrain » (`../lvt/`, notes de lecture vérifiées dans `../lvt/notes/`).

## Programmes

- `donnees_foncier.py BRUT` : fichier par commune `donnees/communes.csv.gz` (France métropolitaine hors
  Alsace-Moselle) à partir du REI 2024 (DGFiP), du recensement 2022 (logement), de l'Insee Analyses n° 91
  (taxe foncière / valeur des logements, 2017) et de DVF 2023-2024 ; `donnees/terrains_dep.csv`. Les fichiers
  bruts ne sont pas versionnés (URL en tête du script). Paris, Lyon et Marseille : arrondissements ramenés à la
  commune.
- `donnees/croissance_tf.json` : TFPB 2017 (REI 2017, parts communale, intercommunale et départementale
  comprises) et 2024 en métropole ; logements des particuliers (recensement 2022).
- `simulation.py` : scénarios → `sorties/simulation.txt`.

## Hypothèses du modèle (à rappeler dans la note)

- Champ : logements des particuliers (parc moins les HLM, partagés entre maisons et appartements au prorata),
  30,5 M logements, valeur 6 760 Md€.
- Valeur : prix médian au m² des ventes 2023-2024 (commune si au moins 10 ventes, sinon intercommunalité, sinon
  département) × surface médiane des logements vendus.
- Part du terrain : maisons, prix au m² des terrains à bâtir (commune si au moins 5 ventes ; sinon prix du
  département ajusté par l'écart de prix des maisons, élasticité estimée 1,54) × parcelle médiane (plafonnée à
  1 500 m²) ; appartements, résidu (1 − coût de reconstruction / prix), coût calé (1 560 €/m²) pour que la part du
  terrain de l'ensemble égale celle des comptes de patrimoine des ménages (45,4 % en 2024). Bornes 10-90 %.
- Taxe foncière actuelle : ratio TF / valeur de l'Insee (2017, par commune) × valeur 2024, calée sur 19,2 Md€
  (2017, ménages) × croissance de la TFPB 2017-2024 (1,296) × part du champ : 23,6 Md€.
- DMTO : 5,81 % (4,5 % département, 1,2 % commune, frais d'assiette) × ventes de logements anciens 2023-2024
  (hors VEFA) : 11,4 Md€.

## Premiers résultats (sorties/simulation.txt)

- TF / valeur aujourd'hui : 0,55 % dans le décile de communes le moins cher, 0,16 % dans le plus cher.
- Report simple (DMTO −50 %, TF +24 % partout) : +110 à +230 € par logement et par an ; en ajoutant la baisse
  des DMTO rapportée au parc, presque neutre par décile.
- Assiette nationale en valeur de marché, deux taux (terrain = 4 × bâti) : décile le plus cher +238 %,
  25 % des logements voient leur TF augmenter de plus de moitié : trop brutal sans transition.
- Deux taux avec recette constante par commune et taux départemental sur le terrain pour remplacer les DMTO :
  +9 à +55 % selon le décile ; taux départemental de 0,11 % (Paris : 0,12 %) à 0,85 % (Creuse) de la valeur
  du terrain, d'où la question de la péréquation.

## Proposition retenue

DMTO divisés par deux (5,81 → 2,9 %) ; chaque commune garde sa recette de taxe foncière, répartie sur la
valeur de marché avec un taux sur le terrain égal à 4 fois le taux sur le bâti ; taux national unique sur la
valeur des terrains (0,15 % avec reprise des ventes de +6 % par point, 0,19 % sans) reversé aux départements.
TF +2 % (décile le moins cher) à +60 % (le plus cher) ; total TF + DMTO de −86 à +26 € par logement et par an ;
18 % des logements à plus de 300 € de hausse ; transition sur dix ans, plafond attaché au bien.

## Notes de lecture (`notes/`)

- `inventaire.md` : tous les prélèvements sur l'immobilier, montants vérifiés, comparaison OCDE.
- `droits_mutation.md` : effets des DMTO (transactions, mobilité, primo-accédants).
- `taxe_fonciere_split_rate.md` : problèmes de l'impôt foncier, Pennsylvanie, Bade-Wurtemberg, faisabilité.

## Révision après revue (novembre 2026, `../revue/revue_foncier.md`)

- Taxe foncière actuelle vieillie commune par commune (croissance de la TFPB 2017-2024, REI ;
  `donnees/tfpb2017_communes.csv`) : Paris +36 % par rapport à la croissance nationale.
- Taux national sur le terrain calé sans reprise des ventes (0,19 %) ; la reprise est un gain.
- Contrôles ajoutés à `sorties/simulation.txt` ([CONTROLE], [VARIANTE]) : impôt sur le bâti 14,1 -> 7,3 Md€ ;
  appartement parisien : +660 €/an, −22 000 € en valeur actuelle sans capitalisation des droits, −8 250 € si
  les deux se capitalisent ; variante « résidu pour les maisons » qui inverse le partage maisons/appartements.
- Texte : deux hypothèses d'incidence, calendrier (hausse uniforme temporaire le temps d'établir les valeurs),
  finances locales, références corrigées (Bachelet et Poulhès ; Dolls et al. 2025 ; TSE WP 23-1486).
