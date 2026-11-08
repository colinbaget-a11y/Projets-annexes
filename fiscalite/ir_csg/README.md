# IR + CSG fusionnés : rendement, barème « le plus proportionnel » et vérifications

Ce dossier chiffre la mesure 3 de la partie III du rapport Sorbon.

**Livrable.** `note-ir-csg.pdf`, environ 9 pages avec l'annexe de vérifications. Le source est
`note-ir-csg.tex` ; il se compile depuis `ir_csg/` avec pdflatex, en deux passes.

## Programmes

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

- **Unité.** Le calcul est fait par foyer, sans quotient. Une franchise par adulte n'est pas
  chiffrable avec l'IRCOM.
- **Répartition intra-tranche.** Les foyers d'une même tranche reçoivent la même composition de
  revenus. Au-delà de 150 k€, cela comprime la distribution de l'assiette, et α y est remplacé par
  a = 2,1 (Cabannes, Houdré et Landais, 2014).
- **Critère de Lorenz.** Il est vérifié sur les 25 tranches, pas sur des foyers individuels.
- **Réductions et crédits d'impôt.** Ils sont supposés maintenus.
- **Microsimulation.** Il faudra une microsimulation sur fichiers individuels avant d'aller plus loin.
