# IR + CSG fusionnés : rendement et barèmes à rendement constant

Chiffrage « à la louche » de la mesure 3 de la partie III du rapport Sorbon. Il s'agit d'un impôt unique
qui remplace l'IR et la CSG sur les revenus d'activité et de remplacement. Le barème est progressif
mais reste largement proportionnel. Le PFU est conservé sur les revenus du capital.

Lancer depuis `fiscalite/` :

```
SPLIT=prorata python3 ir_csg/ir_csg.py   # variante (sorties_prorata/)
python3 ir_csg/ir_csg.py                 # variante centrale, à lancer en dernier (elle produit les figures)
```

## Données

- Comptes nationaux (`donnees/ntl_france.csv`, D51M : C07 IR, C04 CSG, C03 CRDS) et PIB Eurostat
  (`donnees/pib_france.json`), 2000-2024.
- IRCOM DGFiP, revenus 2024 (`donnees/ircom_national_revenus2024.csv`). La table donne 25 tranches de
  RFR et, pour chacune, le nombre de foyers, le RFR, l'impôt net, les salaires et les pensions.
  Total : 41,6 M foyers, 1 375 Md€ de RFR, 91,7 Md€ d'impôt net.

## Chiffres clés

Séries 2000 → 2024 :

- IR : 49,5 → 96,2 Md€ (3,36 → 3,28 % du PIB) ;
- CSG : 58,3 → 153,1 Md€ (3,96 → 5,22 % du PIB, avec le saut de 2018) ;
- CRDS : 4,5 → 9,1 Md€.

Élasticités apparentes au PIB (`sorties/elasticites_pib.csv`) :

- CSG à taux légaux inchangés : 1,27 (2006-11), 0,85 (2012-17), 0,98 (2019-24) ;
- IR, médiane des années sans réforme : 1,08 ;
- pentes log-log 2000-2024, réformes comprises : 1,23 pour l'IR, 1,51 pour la CSG.

Barèmes à rendement constant (assiette brute travail + pensions de 1 539 Md€) :

| Barème | Cible | Taux et seuils |
|---|---|---|
| A, taux unique | 192,2 Md€ (fourchette 189-192) | 12,5 % (12,3 % en variante prorata) |
| B, largement proportionnel | idem | 5 % jusqu'à 10 k€, 13,9 % jusqu'à 100 k€, 30 % jusqu'à 250 k€, 40 % au-delà |
| C, huit tranches de 5 à 40 % | idem | seuils 14 / 29 / 43 / 64 / 100 / 171 / 357 k€ |
| D, bas protégé, haut à 49 % | idem | 4 % jusqu'à 12 k€, 9 % jusqu'à 30 k€, 20,2 % jusqu'à 120 k€, 40 % jusqu'à 250 k€, 49 % au-delà |

Les détails par tranche de RFR (taux moyen actuel et taux sous chaque barème, gain ou perte par foyer)
sont dans `sorties/par_tranche.csv`. Les figures sont `figures/ircsg_series` et
`figures/ircsg_taux_moyens`.

## Méthode et hypothèses (à dire dans le texte)

1. Cible. La cible est la somme de deux termes :
   - l'IR net IRCOM, diminué de la part imputable aux autres revenus ;
   - une CSG reconstituée sur les salaires et les pensions.
2. Assiette brute. Les salaires IRCOM sont multipliés par 1,20 et les pensions par 1,075, pour revenir
   à une assiette de type CSG. Ces coefficients sont des hypothèses, non calibrées sur les textes.
3. CSG sur les pensions. Le taux dépend du RFR (0 / 3,8 / 6,6 / 8,3 %). Les seuils pour une part
   (12 817 / 16 755 / 26 004 €) sont multipliés par 1,5 part en moyenne.
4. Autres revenus. Ils sont définis comme RFR − 0,9 × (salaires + pensions) et restent hors barème.
   L'IR qui leur est imputé admet deux bornes :
   - au plus 12,8 % de ces revenus, ce qui correspond au PFU (variante centrale) ;
   - au prorata (variante `sorties_prorata`).
   L'écart entre les deux bornes donne la bande grise de la figure.
5. Distribution intra-tranche. Dans chaque tranche, 60 foyers représentatifs sont tirés selon une
   densité puissance monotone qui reproduit la moyenne de la tranche.
6. Réaction comportementale. Elle est calculée comme ΔB/B = e · Δln(1 − τ), avec τ le taux marginal.
   Les élasticités viennent de Sicsic (2022) : 0,22 pour les 50 % du bas, 0,33 pour les 40 % du milieu,
   0,51 pour les 10 % du haut. Le taux marginal actuel est approché par la pente de la charge moyenne
   entre tranches. L'effet va de −11 à +11 Md€ selon le barème, ce qui reste un ordre de grandeur.

## Limites

- Unité. Le calcul est fait par foyer fiscal, alors que la CSG est individuelle. Le quotient
  conjugal et le quotient familial ne sont pas modélisés.
- Impôt net. L'impôt net IRCOM inclut les crédits d'impôt.
- CSG non reconstituée. Environ 10 Md€ de la CSG des comptes nationaux ne sont pas reconstitués
  (chômage, revenus non déclarés, etc.).
- Constitutionnalité. Dans la décision 2000-437 DC (considérant 9), le Conseil constitutionnel a
  censuré une ristourne dégressive de CSG parce qu'elle ne tenait compte ni des autres revenus du
  contribuable, ni de ceux de son foyer, ni des personnes à charge. Un barème progressif appliqué à
  l'ensemble des revenus et qui tient compte du foyer est donc plus sûr. La décision 2015-725 DC
  (article 77) censure pour un autre motif.

## Littérature utile (lue dans les textes)

- CPO, *Impôt sur le revenu, CSG : quelles réformes ?* (2015), p. 132-140 : transposer tel quel le
  quotient conjugal dans un impôt fusionné coûterait environ 11,8 Md€, et le quotient familial
  environ 10 Md€ ; le CPO cite le rapport inter-administratif de 2012. Le CPO voit la fusion comme un
  projet de moyen terme.
  https://www.vie-publique.fr/files/rapport/pdf/154000100.pdf
- Landais, Piketty et Saez (2011). Leur impôt est individuel, assis sur la base CSG (capital
  compris), avec un barème en taux effectifs (2 % à 1 100 €/mois, 10 % à 2 200 €, 13 % à 5 000 €,
  25 % à 10 000 €) ; rendement environ 147 Md€ (2010). Le simulateur travaille sur des fichiers
  synthétiques ; selon le CPO, sa vocation est « plus pédagogique que pratique ».
- Saez, Slemrod et Giertz (2012, *JEL*) donnent la correction d'une hausse de taux en haut de
  barème : dR = dM · [1 − e · a · τ/(1 − τ)].
- Cabannes, Houdré et Landais (2014, *Économie et Statistique*) estiment l'élasticité française :
  environ 0,02 sur l'ensemble des foyers et 0,31 pour le top 10 %, avec un paramètre de Pareto
  a ≈ 2,1.
- Mourre, Poissonnier et Lausegger (2019, DP 098 de la Commission) donnent, pour la France, une
  élasticité de l'impôt sur le revenu à l'output gap de 1,86 et une élasticité des cotisations de
  0,63. On ne sait pas avec certitude si cet agrégat inclut la CSG.
- Aucune note de l'IPP consacrée à une fusion IR-CSG n'a été trouvée. Allègre, Cornilleau et
  Sterdyniak (2007, *Revue de l'OFCE* n° 101) n'ont pas été lus.
