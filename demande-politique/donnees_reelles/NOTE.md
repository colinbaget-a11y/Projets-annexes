# Nuages d'électeurs sur données réelles

Ce dossier refait, sur des enquêtes réelles, les graphiques du prototype simulé que l'on
voulait vraiment : le plan idéologique en deux dimensions (économie × culture), **un point par
répondant, coloré par son vote**, la superposition faisant apparaître les zones denses.

Tout ce qui suit a été vérifié sur les fichiers eux-mêmes (codebooks et données) le 11 septembre 2026.

## 1. Fichiers

| Fichier | Rôle |
|---|---|
| `extract_cses.py` | extrait les vagues France 2017 et 2012 des fichiers CSES complets (cses.org, libre) |
| `nuages_cses.py` | figures `r1` à `r4` (CSES) et `resultats_cses.json` |
| `extract_barometre.py` | télécharge et extrait, pour la France, quatre vagues du Baromètre de la confiance politique (Dataverse Sciences Po, CC-BY) |
| `nuages_barometre.py` | figures `b1` à `b6` (Baromètre) et `resultats_barometre.json` |
| `data/barometre/*.csv` | extraits France du Baromètre (versionnés : licence CC-BY 4.0, source citée ci-dessous) |
| `data/fr2017_cses5.csv`, `data/fr2012_cses4.csv` | extraits CSES, non versionnés (à régénérer avec `extract_cses.py`) |

Reproduction : `python extract_cses.py cses5.csv cses4.csv && python nuages_cses.py`, puis
`python extract_barometre.py && python nuages_barometre.py`.

## 2. Sources et accès

**Ce qui est utilisable sans compte ni demande d'accès.**

- **CSES** (Comparative Study of Electoral Systems), téléchargement libre sur cses.org.
  Module 5 (`doi:10.7804/cses.module5.2023-07-25`), vague française 2017 : enquête post-électorale
  Kantar Public, face-à-face, 9-23 mai 2017, quotas stratifiés, N = 1 830. Module 4
  (`doi:10.7804/cses.module4.2018-05-29`), vague française 2012, N = 2 014. Le questionnaire commun
  CSES est court : en 2017, neuf items culturels mais un seul item économique ; en 2012, huit items
  de dépenses publiques plus un item de redistribution mais aucun item culturel.
- **Baromètre de la confiance politique** (CEVIPOF / Sciences Po, terrain OpinionWay), déposé au
  CDSP sous licence CC-BY 4.0 : `doi:10.21410/7E4/9K3VGR`. Panel en ligne (CAWI) avec quotas, inscrits
  sur les listes électorales. Les fichiers de données sont ouverts et accessibles par l'API
  (`https://data.sciencespo.fr/api/access/datafile/<id>`). Vagues utilisées : 9 (13-26 décembre 2017,
  N = 2 084), 13 (23 décembre 2021 - 10 janvier 2022, N = 10 566), 15 (22-29 janvier 2024, N France =
  3 514), 16 (17 janvier - 5 février 2025, N France = 3 561). Chaque vague contient le vote déclaré
  au premier tour précédent (2017 dans les vagues 9 et 13, 2022 dans les vagues 15 et 16), une
  intention de vote 2022 dans la vague 13, l'auto-positionnement gauche-droite et une batterie
  d'opinions dont la composition change d'une vague à l'autre.

**Ce qui existe mais demande un compte et une demande d'accès.** Sur le Dataverse de Sciences Po,
les fichiers de données de toutes les enquêtes électorales du CDSP sont marqués « restricted »,
même quand la licence affichée est CC BY-SA : ENEF 2017 (vagues 1 à 18 et jeu apparié), ENEF 2019,
ENEF 2024 (7 vagues), enquêtes post-électorales 1962, 1978, 1988, 1995, 1997, 2007 et 2012, panel
électoral 2002. Seuls la documentation, les dictionnaires et les fichiers DDI sont ouverts ; l'API
répond 403 sur les données. Les fiches ENEF 2022 (vagues 1, 2, 4, 5, 6 bis, 7) ont été publiées en
juillet-août 2026 mais n'exposent encore aucun fichier. Ces enquêtes, en particulier ENEF 2017
(294 variables dans la seule vague 1, avec des batteries économiques et culturelles complètes),
restent la meilleure base pour une version plus fine : il faut créer un compte sur
data.sciencespo.fr et demander l'accès aux fichiers, ce que je n'ai pas fait à votre place.

## 3. Construction des axes

Pour chaque enquête, chaque item est standardisé, orienté (fermeture > 0 pour la culture,
libéralisme > 0 pour l'économie), puis les items sont moyennés (au moins 70 % d'items renseignés)
et l'indice est centré-réduit. Les points sont non pondérés ; les barycentres par candidat et
les parts de voix affichées utilisent le poids « politique » de l'enquête (calé sur les résultats
officiels du premier tour). Les positions sont donc **relatives au répondant moyen de la vague** :
« libéral » signifie plus libéral que la moyenne des répondants, pas libéral dans l'absolu. La
figure `r1` (CSES) est la seule à garder l'échelle absolue de l'item économique.

| Enquête | Axe économique (items, α) | Axe culturel (items, α) | r(E, C) |
|---|---|---|---|
| CSES 2017 | 1 item : « l'État devrait réduire les écarts de revenus » | 9 items : minorités, immigration (5), « être vraiment français » (4) ; α = 0,83 | −0,02 |
| CSES 2012 | 6 items : dépenses de santé, d'éducation, de chômage, de retraites, de prestations sociales, écarts de revenus ; α = 0,66 | aucun (axe vertical = gauche-droite déclaré) | — |
| Baromètre déc. 2017 | 7 items : fonctionnaires, économie profite aux patrons, chômeurs, prendre aux riches, réformer le capitalisme, licencier plus facilement, compétitivité vs salariés ; α = 0,73 | 10 items : peine de mort, trop d'immigrés, mariage homosexuel, PMA, autorité des parents, islam menace, enfants d'immigrés, immigration enrichissement, priorité nationale à l'emploi, hommes prioritaires ; α = 0,86 | +0,29 |
| Baromètre janv. 2022 | 5 items ; α = 0,48 | 6 items ; α = 0,78 | +0,26 |
| Baromètre janv. 2024 | 4 items (dont « société où il y a trop d'inégalités ») ; α = 0,49 | 4 items ; α = 0,74 | +0,35 |
| Baromètre janv.-févr. 2025 | 4 items (dont l'échelle compétitivité / salariés, orientée par sa corrélation avec « prendre aux riches ») ; α = 0,44 | 5 items ; α = 0,73 | +0,38 |

La liste exacte des items, leur orientation et les codes manquants sont dans les dictionnaires
`CULT17`, `ECO12` (`nuages_cses.py`) et `ITEMS` (`nuages_barometre.py`). L'échelle culturelle est
toujours bien unidimensionnelle (première valeur propre 44 à 57 % de la variance). L'échelle
économique ne l'est vraiment qu'en 2017 (Baromètre, 7 items) ; dans les vagues 2022-2025 elle
mélange peu d'items et son alpha tombe sous 0,5, ce qui atténue mécaniquement tout ce qui se lit
sur l'axe horizontal de ces vagues.

## 4. Ce que montrent les figures

**`b1_nuage_2017.png` (Baromètre, décembre 2017, vote 2017)** est la figure la plus proche de ce
que l'on cherchait : deux indices continus, N = 1 998, un point par personne. Le nuage n'occupe
pas le carré : il est allongé le long de la diagonale interventionnisme-ouverture /
libéralisme-fermeture (r = +0,29) et vide dans le coin libéral-ouvert extrême. Barycentres
pondérés (économie, culture, en écarts-types) : Mélenchon (−0,78 ; −0,55), Hamon (−0,68 ; −0,79),
Macron (+0,20 ; −0,39), Dupont-Aignan (+0,02 ; +0,27), Le Pen (−0,07 ; +0,93), Fillon (+1,02 ;
+0,49). L'électorat Le Pen est au centre de l'axe économique et tout en haut de l'axe culturel ;
l'électorat Fillon est le plus libéral ; l'électorat Macron est légèrement libéral et nettement
ouvert. La part de variance des positions individuelles expliquée par le vote est de 0,34 sur
l'axe économique et 0,36 sur l'axe culturel (0,49 pour l'auto-positionnement gauche-droite) :
deux tiers de la dispersion sont à l'intérieur des électorats, ce que `b2_par_candidat_2017.png`
montre panneau par panneau.

**`b3_nuage_2022_intentions.png` et `b4_par_candidat_2022_intentions.png` (janvier 2022,
N = 9 753, intentions)** : l'électorat Zemmour se place à droite de l'électorat Le Pen sur l'axe
économique (+0,31 contre −0,07) et un peu plus haut sur l'axe culturel (+0,93 contre +0,64) ;
Pécresse est libérale et modérément fermée (+0,58 ; +0,39) ; Macron libéral et ouvert (+0,36 ;
−0,27) ; Mélenchon, Hidalgo et Jadot occupent le même coin interventionniste-ouvert. Le panneau
« abstention » (n = 391) est diffus, centré près de l'origine.

**`b5_nuage_2025_vote2022.png` (janvier-février 2025, vote 2022 déclaré, N = 3 411)** : même
géométrie avec trois ans de recul, Zemmour encore plus excentré (+0,81 ; +1,13).

**`b6_quatre_dates.png`** met les quatre nuages côte à côte. La forme diagonale est stable
(r de +0,26 à +0,38) mais les items diffèrent d'une vague à l'autre : ne pas lire les
différences de forme comme une évolution.

**`r1` à `r4` (CSES)** sont les versions « enquête académique face-à-face » : `r1` garde les cinq
modalités de l'item économique en abscisse, ce qui montre l'asymétrie absolue perdue par le
centrage (70 % des répondants pondérés sont d'accord pour que l'État réduise les écarts de
revenus ; 15 % seulement sont en désaccord) et fait apparaître les bandes verticales que produit
un item unique. Dans CSES 2017, l'item économique est presque orthogonal à l'indice culturel
(r = −0,02) et le vote est bien plus lié à la culture (R² = 0,29) qu'à cet item (0,10). `r4`
(CSES 2012, 6 items économiques × gauche-droite) montre ce qu'apporte un axe multi-items :
l'électorat Sarkozy (+0,64) se sépare nettement de l'électorat Hollande (−0,34), et l'électorat
Le Pen 2012 (+0,37) est du côté libéral, entre Bayrou et Sarkozy.

## 5. Limites à garder en tête

- Le Baromètre est un panel en ligne à quotas ; les enquêtes CSES/ENEF sont en face-à-face avec
  tirage stratifié. Les deux calent le vote déclaré sur les résultats officiels, mais rien ne
  garantit que la distribution des opinions soit représentative à vote donné.
- Le vote 2022 dans les vagues 15 et 16 est un souvenir à deux ou trois ans de distance.
- Les indices sont centrés-réduits par vague : on ne peut pas lire un déplacement de l'ensemble
  de l'électorat sur ces figures, seulement la géométrie relative des électorats.
- Les items sont des échelles à quatre ou cinq modalités : les nuages sont en réalité des
  treillis ; un léger jitter les dé-superpose, il ne crée pas d'information.
- L'axe culturel du Baromètre mélange immigration, islam, ordre (peine de mort, autorité) et
  mœurs (mariage homosexuel, PMA). Dans CSES il ne contient que immigration et identité nationale.

## 6. Suite possible

1. Demander l'accès à ENEF 2017 (et ENEF 2022 dès que les fichiers seront exposés) : ce sont les
   seules bases avec des batteries économiques et culturelles complètes, un vote effectif et un
   plan de sondage documenté.
2. Sur ces bases, remplacer la moyenne d'items par une analyse factorielle ou une MCA, comme
   Chiche, Le Roux, Perrineau et Rouanet (2000), pour ne pas imposer l'orientation des items.
3. Estimer ensuite les objets du prototype (densité D, noyaux de parti, valences) sur ces
   coordonnées, en gardant les positions absolues plutôt que centrées.
