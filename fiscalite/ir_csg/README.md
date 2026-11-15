# IR + CSG fusionnés : rendement, barème « le plus proportionnel » et vérifications

Ce dossier chiffre la mesure 3 de la partie III du rapport Sorbon.

**Livrable (version 4, novembre 2026).** `note-ir-csg.pdf` (et `.docx` par `tex2docx.py`), 9 pages :
« Fusionner les impôts sur le revenu : une fausse bonne idée ? », et `annexe-ir-csg.pdf` (niches, inventaire des
impôts sur le revenu, vérifications), sortie de la note. Introduction de l'auteur raccourcie d'un tiers. Un seul
programme pour tous les chiffres : `proposition.py` (sortie `sorties/proposition.txt`, étiquettes P0 à P7 ; barèmes
dans `sorties/proposition_baremes.json`, lus par `figures_exercices.py` pour `ircsg_x01` à `ircsg_x05`).
`exercices.py` reste la version 3 (représentation des enfants par une fraction d'enfant par couple), conservée.
Représentation des foyers : personnes seules avec ou sans enfant, couples sans enfant ou avec deux enfants,
partages de l'Insee. Étapes à recette égale (220 Md€), assiette commune, impôt individuel :
1. harmonisation : tranches de l'IR 2024 par adulte + 2,99 % ; perte sèche 18,5 Md€ ; perdants > 500 € 14 % ;
2. aplanissement (écart minimal à la charge actuelle) : 5 % → 13 % à 20 k€ → 25,5 % à 30 k€ → 50 % à 250 k€ ; 13,3 Md€ ; 13 % ;
3. perte sèche minimale : 14 % → 16 % → 18 % à 120 k€ → 50 % à 600 k€ ; 5,2 Md€ ; 57 % de perdants ;
4. proposition (étape 3 corrigée, décidée avec l'auteur) : franchise de 8 000 € par adulte sur les revenus
   d'activité (correction des déciles 2 à 4 ; tableau du prix de 0 à 10 000 €) et franchise de 6 000 € par enfant
   (la plus favorable aux familles des quatre variantes) : 17 % → 22 % à 20 k€ → 24,2 % à 45 k€ → 50 % à 600 k€ ;
   perte sèche 9,3 Md€ (3,9 à 15,9) ; 33 % de perdants ; pensions +13,0 Md€, chômage +3,0, salaires −13,3.
Famille, quatre variantes (franchise d'activité 8 000 €) : rien (perte 7,8) ; franchise 6 000 €/enfant (aide 20,6 Md€,
9,3) ; chèque de 772 €/enfant = coût du QF des enfants 13,9 Md€ (8,2) ; quotient conjugal et familial plafonné sur
l'impôt fusionné (aide 3,6 Md€, 8,1). Coût du QF des enfants : 13,9 Md€ (modèle, revenus 2024), à comparer à
13,3 Md€ pour les familles avec enfants en 2017 (André et Sireyjol, Économie et Statistique 526-527, 2021).
Choix de l'auteur : les retraités financent la réforme (pas de dispositif pour les épargner).

**Note courte (novembre 2026).** `note-efficace.pdf` (et `.docx` par `python3 tex2docx.py note-efficace`),
3 pages : « L'impôt sur le revenu le plus efficace possible ». Objectif : perte sèche minimale, travail et
familles favorisés, redistribution indifférente, même recette (220 Md€). Programme `systeme_efficace.py`
(chiffres dans `sorties/systeme_efficace.txt`, étiquettes S0 à S9), figure `figures_efficace.py`
(`ircsg_e01_systeme`). Système proposé (B) : 21,4 % sur les revenus d'activité et fonciers au-delà de 10 000 €
par adulte, 26,4 % sur les pensions et le chômage dès le premier euro, crédit de 1 500 € par enfant (27 Md€).
Perte sèche 6 Md€ (2 à 10) contre 18 (8 à 31) ; 11 des 12 Md€ de gain viennent des 10 % du haut. Payé par les
retraités (+15,5 Md€) et les chômeurs (+3) ; retraité seul à 17 000 € : +4 490 €. Variantes : A sans
franchise (15,2 / 20,2 %, perte 3 Md€, SMIC +850 €) ; C franchise sur tout revenu, taux unique 24,4 % (perte
9 Md€, retraité à 17 000 € +1 710 €). Ne modifie rien des exercices.

**Livrable (version 3, relecture v2 de l'auteur).** `note-ir-csg.pdf`, 13 pages. Impôt unique remplaçant
l'IR, la CSG et la CRDS sur les revenus au barème (`bareme_v3.py`, `figures_v3.py`, chiffres recalculés par
`controles_v3.py` dans `sorties/controles_v3.txt`) :
- assiette : revenu après cotisations sociales, la même pour salariés, indépendants, retraités, chômeurs ;
- taux marginal en ligne droite par part : 7 % au premier euro, 14 % à 20 000 €, 19,9 % à 30 000 €, 50 % à
  120 000 € ; quotient conjugal (deux parts) ; crédit non remboursable de 750 € par enfant ; toutes les
  réductions, abattements et demi-parts de l'IR supprimés ;
- recette 220,1 Md€ (IR 80,2 + CSG 132,4 + CRDS 7,4) ; 96 % des foyers paient ;
- coût d'efficacité 18 → 15 Md€ (jeu central ; 8 → 7 et 31 → 26 selon les élasticités) ;
- déciles : au plus +450 € (D3) parmi D1-D9, D10 +640 € ; salaires −13,7 Md€, pensions +10,9,
  chômage +3,0, indépendants −0,2 ; taux du haut 50 % (contre 54-55 % aujourd'hui au très haut) ; retraité seul jusqu'à +1 700 € vers 17 000 € de pension.
- La charge actuelle est répartie entre personnes seules et couples d'une même tranche selon les rapports
  OpenFisca (`CUR_S`, `CUR_C`), car le barème distingue désormais les types de foyers.
- Littérature et données vérifiées : `sorties/lit_haut_elasticites.md`, `sorties/lit_chomage_natalite.md`,
  `sorties/niches_crds.md` (et CSV associés).
- `openfisca_courbes.py` exporte aussi la CRDS, la CASA et l'assiette après cotisations de chaque adulte,
  pour cinq profils.

**Version 2 (barème-fonction familial).** Toujours reproductible : `bareme_lisse.py`, `figures_lisse.py`,
`controles.py`.

Figures : `figures_lisse.py` (`ircsg_l01` à `ircsg_l08`) et `ircsg_f10` (taux maximisant la recette).
La version précédente (barème E à franchise et taux unique, critère de Lorenz) reste reproductible
avec `ir_csg.py`, `robustesse.py`, `optimal.py` et `figures_note.py`.

## Programmes

- **`bareme_lisse.py`** cherche la famille de barèmes « fonction » (taux marginal linéaire par morceaux,
  sans marche) qui minimise le coût d'efficacité approché, sous trois contraintes : même recette,
  écart d'au plus 800 € par décile, et au plus +0,3 point pour les déciles 7 à 10. Il chiffre les
  versions familles (par l'impôt / par la dépense) et la décomposition par type de revenu. Le résultat
  va dans `sorties/bareme_lisse.txt` et `sorties/bareme_lisse_balayage.csv`.
- **`figures_lisse.py`** produit les figures de la note.

Tous se lancent depuis `fiscalite/`.

- **`ir_csg.py`** produit les séries 2000-2024, les élasticités au PIB, la reconstitution par
  tranche de RFR et les barèmes A à E. Il écrit dans `sorties/` ; avec `SPLIT=prorata`, il écrit
  dans `sorties_prorata/`. Il produit aussi les figures `ircsg_series` et `ircsg_taux_moyens`. Les
  variables d'environnement suivantes choisissent les hypothèses :
  - `SPLIT=prorata` répartit l'IR au prorata du RFR entre les revenus au barème et les revenus au
    PFU (borne alternative) ;
  - `CAPITAL=prorata`, `CAPITAL=haut` ou `CAPITAL=mixte` (scénario central) fixe la répartition des
    revenus au PFU entre les tranches ;
  - `FIG_NU=1` produit les figures sans habillage, pour la note.
- **`robustesse.py`** produit `sorties/robustesse.txt`. Il contient trois choses :
  - la validation de la reconstitution sur des agrégats indépendants ;
  - la sensibilité aux hypothèses ;
  - le balayage des barèmes « franchise + taux unique + 40 ou 45 % + 49 % », avec le critère de
    dominance de Lorenz et une hausse d'au plus 2 points par tranche.
- **`optimal.py`** produit `sorties/optimal.txt` et la figure `ircsg_optimal`. Il calcule :
  - le paramètre de Pareto ;
  - les taux supérieurs de Saez ;
  - l'inverse optimum, c'est-à-dire les poids sociaux implicites ;
  - les indices d'Atkinson.
- **`figures_note.py`** produit les figures complémentaires `ircsg_f01` à `ircsg_f11` :
  composition de l'assiette et de la recette, élasticités annuelles, courbes de concentration,
  cas-types OpenFisca, gains par tranche, écart de Lorenz, balayage des barèmes, sensibilité du
  taux unique, paramètre de Pareto, taux maximisant la recette, comparaison avec les Pays-Bas.
- **`openfisca_courbes.py`** calcule l'IR et la CSG actuels sur une grille fine de revenus pour trois
  profils (personne seule, couple avec deux enfants, retraité seul). Le résultat va dans
  `sorties/courbes_openfisca.csv` ; il sert à la figure finale.
- **`openfisca_cas.py`** et **`openfisca_marges.py`** calculent, sur des cas-types OpenFisca-France
  (revenus 2024), le passage du net imposable au brut, la CSG et les taux marginaux. Le résultat va
  dans `sorties/marges_openfisca.csv`, qui est versionné. Ces deux scripts demandent un environnement
  où `openfisca-france` est installé (`pip install openfisca-france`, version 176.1.10).

## Données

- **IRCOM DGFiP, revenus 2024** (`donnees/ircom_national_revenus2024.csv`) : 25 tranches de RFR.
- **Totaux par case des déclarations 2042, revenus 2024** (`donnees/ir_2042_cases_revenus2024.csv`).
  Source : data.economie.gouv.fr, jeu `ir-declarations-2042-nat`. Ces totaux servent à décomposer
  les salaires, les pensions et les autres revenus.
- **CCSS mai 2026, fiche 1.3** : CSG 2024 par assiette. Les montants sont recopiés dans le code et
  dans la note.
- **Eurostat** : salaires bruts D11 reçus par les ménages et pensions ESSPROS. Ils servent de
  contrôle uniquement.
- **Comptes nationaux** (`donnees/ntl_france.csv`) et **PIB** (`donnees/pib_france.json`), pour
  les séries.

## Chiffres clés (scénario central)

| Grandeur | Valeur |
|---|---|
| Cible à remplacer | 212,6 Md€ (209,1 en variante prorata) |
| Assiette brute | 1 598 Md€ |
| Revenus au PFU hors champ | 90 Md€, soit 11,5 Md€ d'IR |
| Taux unique (barème A) | 13,3 % |
| Kakwani actuel | 0,170 |

**Barème E retenu** : 0 % jusqu'à 14 k€, 17,2 % jusqu'à 120 k€ (76 % des foyers), 40 % jusqu'à
250 k€, 49 % au-delà. Ses propriétés :
- Kakwani de 0,199 ;
- le revenu après impôt domine celui d'aujourd'hui au sens de Lorenz ;
- la hausse maximale dans une tranche est de 0,25 point ;
- l'effet des réactions comportementales est de +3 Md€.

Selon la répartition du PFU entre tranches, le taux unique va de 16,6 à 17,7 %. La dominance de
Lorenz est vérifiée dans 3 scénarios sur 4. Elle échoue si l'on loge le PFU tout en haut de la
distribution.

**Optimal.** Le poids implicite de la bande centrale est ḡ ≈ 0,95 pour e = 0,25. Le taux qui
maximise la recette au-dessus de 250 k€ est de 70 % pour e = 0,25 et de 53 % pour e = 0,51
(a = 2,1). Aucun poids implicite n'est négatif.

## Corrections par rapport à la version 1 (vérifications, novembre 2026)

1. **Composition de la rubrique « salaires » IRCOM.** Les salaires de source étrangère (33 Md€,
   sans CSG française), le chômage (37 Md€) et les gérants (31 Md€) sont désormais traités à part.
2. **Facteur de passage au brut des pensions.** Il est de 1,055 et non plus de 1,075 (OpenFisca).
   La CSG des pensions est calée sur la CCSS.
3. **Périmètre.** Les indépendants et le foncier, imposés au barème, entrent dans l'impôt
   fusionné. La v1 leur imputait 12,8 % d'IR comme s'ils relevaient du PFU.
4. **Taux marginaux actuels.** Ils viennent maintenant d'OpenFisca. La pente entre tranches les
   sous-estimait de 10 à 20 points au-dessus de 200 k€.
5. **Réactions.** Seule la part de l'assiette qui vient du travail réagit ; les pensions sont fixes.
6. **Critère de choix du barème.** La dominance de Lorenz remplace l'égalité des indices de
   Kakwani, que l'on peut tenir en déplaçant la charge.

## Limites

- **Famille.** Avec une franchise par foyer et sans quotient, la réforme avantage les personnes
  seules et fait payer davantage les couples avec enfants. Une seconde franchise pour les couples
  coûterait environ 21 Md€ ; le taux unique monterait alors à 19,5-21,5 %. C'est un ordre de
  grandeur : la part de couples par tranche n'est pas publiée, et 31 % des foyers sont des couples.

- **Unité.** Le calcul est fait par foyer, sans quotient. Une franchise par adulte n'est pas
  chiffrable avec l'IRCOM.
- **Répartition intra-tranche.** Les foyers d'une même tranche reçoivent la même composition de
  revenus. Au-delà de 150 k€, cela comprime la distribution de l'assiette, et α y est remplacé par
  a = 2,1 (Cabannes, Houdré et Landais, 2014).
- **Critère de Lorenz.** Il est vérifié sur les 25 tranches, pas sur des foyers individuels.
- **Réductions et crédits d'impôt.** Le barème-fonction les suppose supprimés (environ 11 Md€) ; les garder porte le taux à 30 000 € à 18,9 % (barème E : supposés maintenus).
- **Microsimulation.** Il faudra une microsimulation sur fichiers individuels avant d'aller plus loin.
