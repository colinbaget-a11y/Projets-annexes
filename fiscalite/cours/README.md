# Le cours

`refaire-l-impot.tex` est la version de référence : 74 pages, treize chapitres en trois parties,
quarante-cinq figures, trois tableaux et dix rapports publics français cités là où ils servent.

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
la légende LaTeX, et les sources et la note de lecture sont écrites dans `figures/nu/<figure>_note.tex`,
que la macro `\figbloc` compose en texte sous l'image. La largeur des figures est plafonnée à celle
de la ligne (`LARG_MAX` dans `graphiques.py`) et leur hauteur à 42 % de la page.

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

## Ce que la relecture d'octobre 2026 a changé

Les commentaires portaient sur le style (structures « A, et A' » répétées, phrases d'annonce,
paragraphes de méthode), sur la lisibilité des figures et sur une vingtaine de points de fond.
Chaque réponse de fond a été vérifiée dans les textes eux-mêmes (droit en vigueur, articles,
rapports), avec quatre recherches documentaires menées en parallèle.

- **Mobilité des revenus.** Le tableau britannique de *Tax by Design* (BHPS 1991-2008, revenu
  hebdomadaire des ménages, tous âges) est remplacé par les données françaises de l'Insee (POTE
  2003-2019, 25-49 ans) : 63 % des 20 % les plus aisés le sont encore seize ans plus tard, 3,5 %
  sont tombés parmi les 20 % les plus modestes. Les deux séries ne se comparent pas ; les passages
  du haut vers le bas du tableau britannique tiennent probablement à la retraite, ce que ni
  l'IFS ni le DWP ne documentent.
- **Impôt sur les sociétés.** Le taux de 36,1 % ne vaut que pour les groupes dont le chiffre
  d'affaires réalisé en France dépasse 3 Md€ (contribution exceptionnelle 2025, reconduite en 2026
  avec un seuil relevé à 1,5 Md€ ; environ 450 redevables prévus en 2025). Le cas courant est
  25 % puis 30 % de prélèvement forfaitaire, 47,5 % au total (48,6 % en 2026 avec le PFU à 31,4 %).
  La CEHR s'applique bien aux dividendes, puisque son assiette est le revenu fiscal de référence ;
  la CDHR porte le prélèvement sur le dividende à 37,2 % pour les foyers qui en vivent.
- **Carey et Rabesona.** La hausse moyenne du taux implicite sur le capital (+6,4 points, 16 pays)
  est reprise ; pour la France (+14 points), elle tombe à moins de 2 points si l'on attribue au
  travail une partie du revenu des indépendants (tableau 5 de l'article) : le texte le dit.
- **Poll tax.** Elle n'était forfaitaire que dans son principe : montants fixés localement,
  réductions jusqu'à 80 % dégressives avec le revenu, registre auquel on pouvait se soustraire,
  non-paiement massif.
- **Règle du carré.** Origine (Dupuit, 1844), statut d'approximation, et ce qui s'estime
  réellement (l'élasticité) sont désormais dits.
- **Douze dépenses fiscales à moins de 100 € par bénéficiaire.** La Cour ne publie pas la liste
  dans son rapport ; celle du cours est reconstituée en appliquant son critère au PLF 2025
  (12 dépenses, 2,2 Md€), ce que le texte précise.
- **C3S.** L'abattement de 19 M€ s'applique société par société, sans consolidation ; la
  contribution est plafonnée à 3,08 % de la marge brute pour quelques activités de négoce à faible
  marge, pas pour les autres. Aucun pays européen n'a d'équivalent (CAE) ; l'Allemagne a remplacé
  en 1968 une taxe en cascade dont elle reconnaissait qu'elle favorisait l'intégration verticale.
- **Déduction pour fonds propres.** Effet robuste sur l'endettement (2 à 5 points, 9 chez les
  bénéficiaires italiens), effet faible et contradictoire sur l'investissement ; coût belge
  multiplié par plus de dix par rapport à la prévision, sur une base de stock et avec des montages
  intragroupe ; suppressions belge (2023) et italienne (2024). Le chapitre 5 le dit dans
  l'objection.
- **Droits de mutation et mobilité.** L'effet sur les déménagements est établi (Hilber et
  Lyytikäinen ; Best et Kleven), l'effet sur la mobilité professionnelle ne l'est pas : la chaîne
  « mutation → mobilité professionnelle → appariement » du chapitre 9 a été corrigée.
- **Graphiques nouveaux.** c23 (taux et recettes de l'IS, 18 pays, 1981-2023), c24 (taux implicite
  de Carey et Rabesona) ; c6 refait sur le cas courant, c14 sur données françaises, s1 lisible à
  la taille d'impression.
- **Hypothèses de l'auteur.** Cinq intuitions de la relecture sont gardées dans le texte comme
  hypothèses explicitement non démontrées (C3S et agglomération, ch. 4 ; montée en gamme, ch. 4 ;
  propriété du logement et croissance, ch. 3 ; imposition commune et formation des couples, ch. 3 ;
  baisse des taux, élargissement des assiettes et recettes, ch. 5), et rappelées au chapitre 13.
- **Principes.** Le chapitre 13 contient une section « Les principes qui guident ces
  propositions » : séparer le démontré du supposé, juger sur le cas courant et l'ordre de
  grandeur, vérifier les hypothèses d'un résultat avant de l'appliquer, regarder comment on échappe
  à l'impôt, chiffrer coût et financement, juger la progressivité sur l'ensemble du système.

## Vérification en fiscaliste (octobre 2026)

Chaque explication du fonctionnement d'un impôt a été relue sur les textes (CGI, code de la
sécurité sociale, BOFiP, brochure IR 2026, lois de finances 2025 et 2026). Principales corrections :
retenue à la source sur les dividendes versés aux non-résidents (12,8 % ou 25 %, réduite par les
conventions, nulle pour une mère européenne) ; plafonnement des charges financières (3 M€ ou 30 %
de l'EBITDA) ; régime mère-fille et option pour le barème ; taux de 2026 (PFU 31,4 %, PEA 18,6 %,
barème IR, plafond du quotient familial) ; revenu foncier recalculé (l'inflation ne frappe pas le
loyer : 55 % et non 97 %) ; biscuits à 5,5 % ; lissage des revenus irréguliers (quotient, moyenne
triennale agricole, artistes) ; universalité budgétaire et affectations autorisées par la LOLF ;
CVAE déjà perçue par l'État ; réduction générale unique de 2026 ; prestations sous condition de
ressources ; valeurs locatives (révision des logements repoussée à 2031) ; Dutreil (seuils de
l'engagement) ; droits de mutation (option à 5 % depuis 2025) ; carbone (composante figée à
44,6 €/t, biomasse, enchères, ETS2 en 2028, MACF depuis 2026).
