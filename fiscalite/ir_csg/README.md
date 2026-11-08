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
- Constitutionnalité. La contrainte constitutionnelle d'une CSG progressive reste à documenter
  (décision 2000-437 DC).
