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
- `donnees_2025.py BRUT` (base 2025, décision 5 du 17/11/2026 de `../synthese/DECISIONS.md`) : à partir du REI 2025,
  de DVF 2025, des comptes de patrimoine 2020-2025 et du PIB de l'Insee (millésime des comptes de la Nation 2025, juin
  2026 ; URL en tête du script), écrit `donnees/tfpb2025_communes.csv` (taxe foncière bâtie 2025 par commune),
  `donnees/ventes_logements_2025.csv` (ventes de logements anciens de 2025 par commune, même filtre que
  `donnees_foncier.py`), `donnees/terrains_secteurs_2025.csv` (terrains par secteur, fin 2025),
  `donnees/patrimoine_2025.csv` (terrains bâtis, logements et PIB 1978-2025) et ajoute `tfpb_2025` à
  `donnees/croissance_tf.json`.
- `donnees/croissance_tf.json` : TFPB 2017 (REI 2017, parts communale, intercommunale et départementale
  comprises), 2024 et 2025 en métropole ; logements des particuliers (recensement 2022).
- `simulation.py` : scénarios → `sorties/simulation.txt` (base 2025 ; `BASE_FONCIER=2024 python3 simulation.py` redonne
  le millésime précédent : part du sol de 2024, taxe foncière de 2024, ventes 2023-2024).
- `donnees/terrains_secteurs_2025.csv` (base 2025) et `terrains_secteurs_2024.csv` (millésime précédent) : valeur des
  terrains par secteur (Insee, comptes de patrimoine, tableau 8.200, URL en tête du fichier) ; sert à l'assiette « tous
  les terrains privés ».
- `../synthese/calculs_foncier.py` (importe `simulation.py`) : tous les chiffres de la partie Immobilier de la note
  fusionnée (refonte du 16/11/2026) → `../synthese/sorties/calculs_foncier.txt` et `.json`.
- `figures_note.py` : figures `foncier_n01` à `foncier_n14` de la note fusionnée (lit le `.json` ; lancer
  `python3 foncier/figures_note.py && FIG_NU=1 python3 foncier/figures_note.py` depuis `fiscalite/`, après
  `calculs_foncier.py`). `figures_foncier.py` (figures `fon_*`) ne sert plus qu'à `note-foncier.tex`.

## Hypothèses du modèle (à rappeler dans la note) ; base 2025

- Champ : logements des particuliers (parc moins les HLM, partagés entre maisons et appartements au prorata),
  30,5 M logements, valeur 6 760 Md€ (prix 2023-2024, non recalés : prix de 2025 inférieurs de 1,5 %).
- Valeur : prix médian au m² des ventes 2023-2024 (commune si au moins 10 ventes, sinon intercommunalité, sinon
  département) × surface médiane des logements vendus.
- Part du terrain : maisons, prix au m² des terrains à bâtir (commune si au moins 5 ventes ; sinon prix du
  département ajusté par l'écart de prix des maisons, élasticité estimée 1,54) × parcelle médiane (plafonnée à
  1 500 m²) ; appartements, résidu (1 − coût de reconstruction / prix), coût calé (1 464 €/m²) pour que la part du
  terrain de l'ensemble égale celle des comptes de patrimoine des ménages (46,2 % fin 2025 ; 45,4 % fin 2024 dans
  le millésime 2025). Bornes 10-90 %.
- Taxe foncière actuelle : ratio TF / valeur de l'Insee (2017, par commune) × valeur × croissance de la TFPB de la
  commune 2017-2025, calée sur 19,2 Md€ (2017, ménages) × croissance de la TFPB 2017-2025 (1,333) × part du champ :
  24,2 Md€ (23,6 en base 2024).
- DMTO : taux permanent de 5,81 % (4,5 % département, 1,2 % commune, frais d'assiette) × ventes de logements anciens
  de 2025 (hors VEFA ; 212 Md€) : 12,3 Md€ (11,4 sur les ventes 2023-2024). Le relèvement temporaire à 6,32 % n'est pas
  compté ; il a rapporté de l'ordre de 0,4 Md€ en 2025 (calcul non vérifié).

## Premiers résultats (note-foncier.tex, ventes 2023-2024 et taxe foncière 2024 ; chiffres périmés, voir la section suivante)

- TF / valeur aujourd'hui : 0,55 % dans le décile de communes le moins cher, 0,16 % dans le plus cher.
- Report simple (DMTO −50 %, TF +24 % partout) : +110 à +230 € par logement et par an ; en ajoutant la baisse
  des DMTO rapportée au parc, presque neutre par décile.
- Assiette nationale en valeur de marché, deux taux (terrain = 4 × bâti) : décile le plus cher +238 %,
  25 % des logements voient leur TF augmenter de plus de moitié : trop brutal sans transition.
- Deux taux avec recette constante par commune et taux départemental sur le terrain pour remplacer les DMTO :
  +9 à +55 % selon le décile ; taux départemental de 0,11 % (Paris : 0,12 %) à 0,85 % (Creuse) de la valeur
  du terrain, d'où la question de la péréquation.

## Proposition retenue (note fusionnée, refonte du 16/11/2026, base 2025 : `../synthese/parties/foncier.tex`)

Droits divisés par deux sur toutes les ventes d'immeubles dès l'annonce (6,2 Md€ sur les logements, ventes de 2025 au
taux permanent ; environ 1,4 Md€ sur les autres biens, ce second chiffre non vérifié) ; taux national d'environ 0,12 %
(valeurs Insee ; 0,151 % sur les valeurs du modèle) sur la valeur de **tous les terrains privés**, bâtis ou non, hors
terres agricoles et terrains publics (6 656 Md€ fin 2025) ; les logements des particuliers en paient 4,7 Md€ ; part
communale à deux taux (sol = 4 × bâti), recette constante par commune ; montée linéaire sur cinq ans (déficit
transitoire de 15 Md€) ; report de paiement par défaut dès 65 ans. Résultats (sans reprise des ventes) : taxe foncière
+2 à +55 % selon le dixième (+10 à +456 €), taxe moins droits de −92 à −4 € ; 19,0 % des logements à plus de +300 € ;
Paris +99 % (+88 % si l'on corrige le double vieillissement) ; perte sèche évitée 2,1 Md€ (logements), 2,4 avec les
autres immeubles. L'ancienne proposition (taux national de 0,197 % sur le seul sol des logements, +4 à +72 %, 25 %,
Paris +129 %) devient une variante. Base 2024 (version précédente) : 5,7 Md€, 0,119 %, +10 à +438 €, −87 à +11 €,
17,6 %, Paris +96 %, 1,9 / 2,3 Md€ (tableau `tab:fon_base` de l'annexe).
Hypothèses et corrections : `../revue/hypotheses_foncier.md` ; annexe : `../synthese/parties/annexe_foncier.tex`.

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
