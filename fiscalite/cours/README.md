# Le cours

`refaire-l-impot.tex` est la version de référence : 62 pages, treize chapitres en trois parties,
quarante et une figures, deux tableaux et dix rapports publics français cités là où ils servent.

## Organisation

Le cours est construit pour qu'on puisse réexpliquer chaque impôt à quelqu'un d'autre.

| partie | chapitres |
|---|---|
| Avant de commencer | ce que la théorie peut dire ; les trois textes et ce qu'on peut leur demander |
| I. Trois questions à poser à n'importe quel impôt | 1 Que détruit-il ? · 2 Qui le paie vraiment ? · 3 Comment le juger ? |
| II. Impôt par impôt | 4 Production · 5 Sociétés · 6 Travail · 7 TVA · 8 Épargne · 9 Immobilier et transmissions · 10 Carbone |
| III. Le système d'ensemble | 11 Niveau, structure, classement de l'OCDE · 12 Autres pays · 13 Ce qu'il faudrait changer |

Chaque chapitre de la deuxième partie suit le même ordre : l'argument en une phrase (encadré en
tête), un exemple chiffré qu'on peut refaire de tête, ce que montrent les données
internationales, la situation française, ce qu'il faudrait faire, l'objection la plus forte. Le
tableau 2, au chapitre 13, rassemble l'ensemble.

Les trois textes — Mankiw, Weinzierl et Yagan (2009), *Tax by Design* (2011), OCDE WP 620 (2008)
— ne font plus l'objet de chapitres séparés : chacun est cité là où il éclaire un impôt
particulier. Les PDF de travail sont dans `sources/` (non versionné).

## Rapports publics français

Dix rapports appliquent les raisonnements du cours aux impôts français. Chaque chiffre repris a
été relu dans le rapport lui-même, pas dans un résumé de presse.

| rapport | chapitre | ce qu'il apporte |
|---|---|---|
| CAE n° 53, Martin et Trannoy, *Les impôts sur (ou contre) la production*, juin 2019 | 4 | pyramidage mesuré de la C3S (effet-prix ≈ 2 × le taux effectif), effet sur les exportations, comparaison hors taxes sur les salaires (3,6 % de la VA contre 0,5 % en Allemagne) |
| CPO, *Tracer un cadre fiscal et social pluriannuel pour l'industrie française*, septembre 2025 | 4, 5, 6 | supprimer la C3S avant d'achever celle de la CVAE ; taux implicite de l'IS ; IS stable à 25 % ; heures supplémentaires sans effet sur les heures travaillées |
| CAE n° 49, L'Horty, Martin et Mayer, *Baisses de charges : stop ou encore ?*, janvier 2019 | 6 | effets des allègements selon le niveau de salaire ; aucun effet détectable au-delà de 1,6 Smic sur les exportations |
| Cour des comptes, *La sécurité sociale* (RALFSS), mai 2025, chapitre III | 6 | 77,3 Md€ d'allègements en 2024 ; taux patronal de 4,3 % au Smic à 43,4 % à 3,5 Smic ; pas d'amas aux seuils |
| CPO, *La TVA, un impôt à recentrer sur son objectif de rendement*, février 2023 | 7 | 47 Md€ de dérogations ; régressivité réduite de moitié sur le cycle de vie ; chèque contre baisse de TVA à coût égal |
| CPO, *Pour une fiscalité du logement plus cohérente*, décembre 2023 | 9 | taxe foncière régressive entre propriétaires à cause de l'assiette ; ordre de réforme : assiette, puis bascule des droits de mutation vers la détention |
| CAE n° 69, Dherbécourt, Fack, Landais et Stantcheva, *Repenser l'héritage*, décembre 2021 | 9 | taux effectifs réels des transmissions (≈ 10 % pour le millième le plus aisé) ; coût des trois grandes exceptions |
| Cour des comptes, *Le pacte Dutreil*, novembre 2025 | 3, 9 | coût de 5,5 Md€ en 2024 contre 0,5 Md€ inscrit ; effets mesurés avec l'IPP |
| CAE n° 50, Bureau, Henriet et Schubert, *Pour le climat : une taxe juste, pas juste une taxe*, mars 2019 | 10 | effets distributifs de la taxe carbone et du reversement ; coût des exonérations |
| Cour des comptes, *Le budget de l'État en 2025 : résultats et gestion*, avril 2026 | 3 | 474 dépenses fiscales, 91,8 Md€ en 2025, coûts inconnus et sous-estimés |

Le site de la Cour des comptes refusait les connexions depuis l'environnement de travail ; les
rapports de la Cour et du CPO ont été lus dans leurs copies officielles sur vie-publique.fr.

## Données et figures

| préfixe | script | contenu |
|---|---|---|
| `r1`–`r12` | `graphiques_reels.py` | données réelles OCDE et Tax Foundation, produites par `extract_reelles.py` |
| `c*` | `graphiques_cours.py` | mécanismes chiffrés et données françaises |
| `m*`, `p*`, `s*`, `g*` | `graphiques_mirrlees.py`, `graphiques_pedagogie.py`, `graphiques_situation.py`, `graphiques.py` | figures des documents de travail reprises dans le cours |

```sh
cd fiscalite
python extract_reelles.py                       # OCDE Revenue Statistics, Tax Foundation (GitHub)
FIG_NU=1 python graphiques_reels.py             # etc. pour chaque script de figures
cd cours && pdflatex refaire-l-impot.tex && pdflatex refaire-l-impot.tex
```

Les figures incluses sont les versions « nues » de `figures/nu/*.pdf` : le titre principal devient
la légende LaTeX, le sous-titre, les sources et la note de lecture restent dans l'image.

`refaire-l-impot.html` est une ancienne version, conservée pour la lecture en ligne ; elle n'est
plus tenue à jour.

## Ce que les données réelles ont corrigé

- **Détention contre transaction immobilière.** Une version antérieure disait le partage
  français « à l'envers ». Sur les catégories de l'OCDE (2023), la France est à 1,9 % du PIB pour
  la détention et 0,7 % pour les transactions, le double de la moyenne dans les deux cas : le
  partage est celui de la moyenne. Ce qui distingue la France est le niveau des droits sur les
  transactions et l'assiette de 1970.
- **Assiette de la TVA.** Une version antérieure la disait « déjà large par comparaison
  internationale ». Le ratio de recettes de l'OCDE est de 51 % en France contre 55 % en moyenne.
- **Classement de l'OCDE appliqué à la France.** L'ancienne figure c10 reposait sur des montants
  saisis à la main (dont 90 Md€ d'impôt sur les sociétés, contre 68 Md€ dans la National Tax
  List) ; elle est remplacée par r12, construite sur les catégories de recettes de l'OCDE.
- **Amortissements.** Le mécanisme reste exposé, mais les données de la Tax Foundation placent la
  France au-dessus de la moyenne pour les trois catégories d'actifs : ce n'est pas un problème
  français.
- **Taux supérieur de l'impôt sur le revenu.** Élevé (55,4 %), mais appliqué à partir de treize
  fois le salaire moyen, contre environ une fois en Belgique et au Danemark.

- **Benzarti et Carloni (2019).** Une version antérieure attribuait « plus de la moitié » de la
  baisse de TVA sur la restauration aux propriétaires. Le papier donne 41 % aux propriétaires,
  25 % aux salariés, 16 % aux fournisseurs et 18 % aux consommateurs.

## Ce que les rapports publics ont nuancé

- **Cotisation foncière des entreprises.** Le cours la plaçait juste après la C3S ; le CAE n'y
  trouve pas de distorsion majeure et place la CVAE avant elle. Le chapitre 4 suit désormais cet
  ordre.
- **Régressivité de la TVA.** Rapportée à la dépense, elle est à peu près proportionnelle ; sur le
  cycle de vie, le CPO la trouve réduite de près de moitié, pas annulée.
- **Trappe à bas salaires.** Le mécanisme est dans le barème, mais la Cour des comptes ne trouve
  pas d'amas de salariés sous les seuils d'allègement.

## Points de méthode à ne pas perdre

- La valeur publiée par l'OCDE pour le taux supérieur français en 2013 (122,8 %) est écartée du
  tracé de la figure c21 et signalée en note : point isolé, cause non documentée par la source.
- Les magnitudes du document de l'OCDE ne sont pas reprises comme chiffrage : ses auteurs écrivent
  eux-mêmes qu'elles sont « plus élevées que ce à quoi on pourrait raisonnablement s'attendre ».
- Le poste SEC D29 et la catégorie OCDE 3000 ne contiennent pas la même chose partout : la Suède y
  classe une large part de ses prélèvements patronaux.
- Deux mesures du niveau de prélèvement coexistent : Eurostat (43,5 % en 2024, hors cotisations
  imputées) et OCDE (43,9 % en 2023). Le texte dit laquelle il utilise.
- La valeur actuelle des amortissements (r4) suit l'hypothèse d'actualisation de la Tax
  Foundation, 7,5 % par an ; l'illustration c8 utilise 5 %.
