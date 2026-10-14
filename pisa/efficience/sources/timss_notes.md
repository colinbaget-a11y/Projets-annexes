# TIMSS 4e année (CM1) : notes de construction

Base produite par `timss.py` → `timss.csv` (format long : `pays, indicateur, annee, valeur, source, note`).
Vérifié le 14 octobre 2026. 678 lignes : 25 pays de l'UE, 113 couples pays × cycle, 6 indicateurs chacun.

## 1. Indicateurs

| identifiant | définition | unité |
|---|---|---|
| `timss4_maths`, `timss4_sciences` | score moyen sur l'échelle TIMSS (centre 500, écart-type 100 fixés en 1995) | points |
| `timss4_avance_maths`, `timss4_avance_sciences` | % d'élèves atteignant le niveau international avancé (≥ 625) | % |
| `timss4_bas_maths`, `timss4_bas_sciences` | % d'élèves sous le niveau bas (< 400), calculé comme 100 − % atteignant 400 | % |

- Les pourcentages publiés sont des entiers. Le niveau « bas » hérite de cet arrondi (± 0,5 point).
- La colonne `note` donne l'erreur type publiée (« e.-t. ») pour les moyennes et le % avancé, la
  population effectivement couverte et les renvois TIMSS tels qu'imprimés dans le tableau source.
- Population cible : la 4e année de scolarité formelle (CITE 1), soit le CM1 en France. Âge moyen
  d'environ 10 ans.

## 2. Sources par cycle

Les fichiers sont téléchargés par `telecharger()` dans
`/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/efficience/timss_raw/`.
Le fichier `manifeste.csv` y donne l'URL, la taille et le SHA-256 de chaque fichier. Aucune inscription
n'a été nécessaire. Les microdonnées n'ont pas été utilisées : les tableaux publiés suffisent.

| Cycle | Moyennes | Niveaux (625 / 400) | Format |
|---|---|---|---|
| 2023 | Exhibits 1.1.1 et 2.1.1 : `https://timss2023.org/wp-content/uploads/2024/11/1-1-1_ach-g4m-dist.xlsx`, `…/2-1-1_ach-g4s-dist.xlsx` | Exhibits 1.1.4 et 2.1.4 : `…/1-1-4_ach-g4m-bmk-dist.xlsx`, `…/2-1-4_ach-g4s-bmk-dist.xlsx` | Excel |
| 2019 | Exhibits 1.1 et 2.1 : `https://timss2019.org/reports/wp-content/uploads/download/achievement/1_1-2_achievement-results-M4.xlsx`, `…/2_1-2_achievement-results-S4.xlsx` | Exhibits 1.8 et 2.8 : `…/1-8_benchmarks-results-M4.xlsx`, `…/2-8_benchmarks-results-S4.xlsx` | Excel |
| 2015 | Exhibit 1.1 (maths et sciences) : `https://timssandpirls.bc.edu/timss2015/international-results/wp-content/uploads/filebase/mathematics/1.-student-achievement/1_1_math-distribution-of-mathematics-achievement-grade-4.xls` (idem `science/…`) | Exhibit 2.2 : `…/2.-performance-at-international-benchmarks/2_2_math-performance-at-the-international-benchmarks-of-mathematics-achievement-grade-4.xls` (idem sciences) | Excel 97 |
| 2011 | Exhibit 1.1, p. 6 : `https://timssandpirls.bc.edu/timss2011/downloads/T11_IR_M_Chapter1.pdf`, `…/T11_IR_S_Chapter1.pdf` | Exhibit 2.2, p. 6 : `…/T11_IR_M_Chapter2.pdf`, `…/T11_IR_S_Chapter2.pdf` | PDF |
| 2007 | Exhibit 1.1, p. 4 : `https://timssandpirls.bc.edu/TIMSS2007/PDF/T07_M_IR_Chapter1.pdf`, `…/T07_S_IR_Chapter1.pdf` | Exhibit 2.2, p. 6 : `…/T07_M_IR_Chapter2.pdf`, `…/T07_S_IR_Chapter2.pdf` | PDF |
| 2003 | Exhibit 1.1 : `https://timssandpirls.bc.edu/PDF/t03_download/T03_M_Chap1.pdf` (p. 6), `…/T03_S_Chap1.pdf` (p. 5) | Exhibit 2.2, p. 11 : `…/T03_M_Chap2.pdf`, `…/T03_S_Chap2.pdf` | PDF |
| 1995 | Tableaux de tendance : TIMSS 2023, Exhibits 1.1.10 et 2.1.10 (`…/1-1-10_ach-g4m-trend-table.xlsx`, `…/2-1-10_ach-g4s-trend-table.xlsx`) ; à défaut TIMSS 2019, Exhibits 1.4 et 2.4 (Autriche) ; à défaut TIMSS 2003, Exhibit 1.3 (Lettonie) | TIMSS 2023, Exhibits 1.1.12 et 2.1.12 ; à défaut TIMSS 2019, Exhibits 1.9 et 2.9 ; à défaut TIMSS 2003, Exhibit 2.4 (p. 14) | Excel, PDF |
| 1995 (Grèce) | Banque mondiale, EdStats : `https://api.worldbank.org/v2/indicator/LO.TIMSS.MAT4` (et `SCI4`, `MAT4.ADV`, `SCI4.ADV`, `MAT4.BL`, `SCI4.BL`) | idem | API JSON |

Les numéros de page sont ceux du lecteur PDF (1 = première page). Pour chaque PDF, le code vérifie qu'une
valeur témoin (première ligne du tableau de 4e année) figure sur la page avant de la lire. Sinon,
il s'arrête.

Documents consultés pour les notes de couverture (téléchargés, mais pas lus par le code) :
- annexe A de TIMSS 2007 ;
- annexe C de TIMSS 2011 ;
- annexe A de TIMSS 2003 ;
- annexe B de TIMSS 2019 ;
- chapitre 1 du rapport « primaire » de TIMSS 1995 (`https://timssandpirls.bc.edu/timss1995i/TIMSSPDF/am1chap.pdf`).

## 3. Couverture (pays × cycle)

| | 1995 | 2003 | 2007 | 2011 | 2015 | 2019 | 2023 |
|---|---|---|---|---|---|---|---|
| AT | x | | x | x | | x | |
| BE (fl.) | | x | | x | x | x | x |
| BG | | | | | x | x | x |
| CY | x | x | | | x | x | x |
| CZ | x | | x | x | x | x | x |
| DE | | | x | x | x | x | x |
| DK | | | x | x | x | x | x |
| EL | BM | | | | | | |
| ES | | | | x | x | x | x |
| FI | | | | x | x | x | x |
| FR | | | | | x | x | x |
| HR | | | | x | x | x | |
| HU | x | x | x | x | x | x | x |
| IE | x | | | x | x | x | x |
| IT | | x | x | x | x | x | x |
| LT | | x | x | x | x | x | x |
| LV | x (LSS) | x | x | | | x | x |
| MT | | | | x | | x | |
| NL | x | x | x | x | x | x | x |
| PL | | | | x | x | x | x |
| PT | x | | | x | x | x | x |
| RO | | | | x | | | x |
| SE | | | x | x | x | x | x |
| SI | x | x | x | x | x | | x |
| SK | | | x | x | x | x | x |

BM = Banque mondiale. **Estonie et Luxembourg** n'ont jamais participé à TIMSS en 4e année : ils sont
absents de la base. Une case vide signifie que le pays n'a pas participé à ce cycle en 4e année, sauf pour
l'Italie en 1995 (voir §6).

## 4. Ruptures et populations couvertes

- **Belgique.** Seule la Communauté flamande est couverte (2003, 2011, 2015, 2019, 2023). La ligne `BE` porte
  donc sur la Flandre, ce que dit la colonne `note`. En 2023, la Communauté française a aussi participé :
  maths 489, sciences 481, avancé 3 % et 2 %, sous le niveau bas 12 % et 15 %. Ces valeurs ne sont pas dans
  `timss.csv`, faute de code UE27. On les obtient avec `extraire(..., sous_nationaux=True)` (code `BE_FR`).
  Aucune valeur nationale n'est calculée.
- **Royaume-Uni.** L'Angleterre, l'Écosse et l'Irlande du Nord sont publiées séparément. Elles sont hors UE
  et donc ignorées.
- **Lettonie.**
  - 1995 : seules les écoles de langue lettone (LSS) sont couvertes. La valeur provient du tableau de
    tendance du rapport 2003.
  - 2003 : toutes les écoles (536 en maths). La série de tendance 1995-2003 du rapport 2003 donne 533
    pour les seules écoles LSS.
  - 2007 : seuls les élèves scolarisés en letton sont couverts (72 % de la population, renvoi 1). Ce point
    n'est pas repris dans les tendances ultérieures.
- **Lituanie, 2003-2011.** Seuls les élèves scolarisés en lituanien sont couverts (93 %, renvoi 1).
- **Pologne 2011.** La classe testée est la classe nationale « Grade 3 », qui correspond à la 4e année de
  scolarité formelle (âge moyen 9,9 ans). Ce point est absent des tableaux de tendance de 2019 et 2023 : la
  comparaison avec les cycles suivants est à éviter.
- **Slovénie.**
  - 2003 : les élèves avaient 3 ou 4 ans de scolarité, pendant la transition vers une école primaire en
    9 ans (âge moyen 9,8 ans).
  - 1995 : la valeur de tendance (462 en maths) correspond à la **classe inférieure** de 1995, c'est-à-dire
    la 3e année. Elle vaut 488 sur l'échelle d'origine, contre 552 pour la 4e année. C'est une rupture de
    population cible, à garder en tête pour toute évolution 1995 → 2003.
- **Échelle de 1995.** Le rapport de 1995 publie des scores de 4e année sur une métrique propre à la
  population 1, qui couvre ensemble la 3e et la 4e année. Pour les tendances, les rapports suivants ont
  réétalonné ces scores.
  - Écart vérifié pour la Population 1, 4e année (échelle d'origine → échelle de tendance) : Pays-Bas 577 →
    549, Hongrie 548 → 521, Irlande 550 → 523, Tchéquie 567 → 541, Autriche 559 → 531, Chypre 502 → 475,
    Portugal 475 → 442, Lettonie LSS 525 → 499.
  - La base ne retient que les valeurs **réétalonnées**, publiées dans les tableaux de tendance. Les niveaux
    de 625 et 400 de 1995 sont eux aussi calculés après coup sur l'échelle de tendance. Le rapport de 1995
    utilisait des repères en percentiles.
- **Grèce 1995.** La Grèce n'a participé qu'en 1995 et ne figure dans aucun tableau de tendance de l'ISC.
  Les valeurs viennent de la Banque mondiale (EdStats), qui les calcule à partir des microdonnées IEA.
  Deux éléments indiquent que ces valeurs sont sur l'échelle de tendance :
  - pour les neuf autres pays de 1995, EdStats reproduit les valeurs de tendance de l'ISC à 0,5 point près ;
  - pour la Grèce, l'écart de 492 (échelle d'origine) à 462,8 (EdStats) est du même ordre que pour les
    autres pays (−27 à −33).

  Ces valeurs sont à utiliser avec prudence. On peut les écarter en filtrant `source` sur « Banque mondiale ».
- **Passage au numérique.**
  - 2019 : environ la moitié des pays ont passé eTIMSS (sur ordinateur) ; les autres sont restés sur papier.
  - 2023 : la grande majorité des pays sont passés au numérique.

  L'ISC relie les modes par des échantillons de transition et publie les résultats sur la même échelle.
  Les écarts liés au mode restent une source possible de rupture.
- **Renvois TIMSS** (colonne `note`) :
  - 1 : la population nationale ne couvre pas toute la population internationale ;
  - 2 : la population couverte représente 90 à 95 % de la population nationale ;
  - 3 : elle en représente moins de 90 % ;
  - † : taux de participation atteints seulement avec les écoles de remplacement ;
  - ‡ : taux presque atteints avec les remplacements ;
  - ≡ : taux de participation non atteints (Pays-Bas 2019, Roumanie 2023, Autriche et Pays-Bas 1995).

  Pour 2003-2011, les renvois sont lus dans les PDF. Ils peuvent manquer quand le symbole est imprimé sur
  une autre ligne que le pays. Les annexes des rapports font foi.
- Aucun pays de l'UE n'a testé la 5e année. Aucun n'a de réserve de fiabilité (ψ, Ж).

## 5. Contrôles effectués (sortie de `python3 -I timss.py`)

1. **Valeurs de la commande.** France :
   - TIMSS 2019 maths : 485 ✔ ;
   - TIMSS 2019 sciences : 488 ✔ ;
   - TIMSS 2023 maths : 484 ✔.

   Valeurs complémentaires lues dans la base : sciences 2023 = 488 ; maths et sciences 2015 = 488 et 487.
2. **Valeurs de chaque cycle et tableaux de tendance de 2019 et 2023.** Ces tableaux republient les cycles
   antérieurs. Résultat : 600 comparaisons avec 2023 et 492 avec 2019, **aucun écart**. La comparaison
   porte sur les moyennes, le % avancé et le % sous le niveau bas, de 1995 à 2023. Elle valide l'extraction
   des PDF de 2003, 2007 et 2011.
3. **Banque mondiale (EdStats, dernière mise à jour du 25 juin 2024, sans 2023).** 522 comparaisons :
   - 484 concordent à moins de 0,5 point ;
   - les 38 écarts s'expliquent tous ainsi :
     - **36 sur le % sous le niveau bas en 2015** : les valeurs d'EdStats (1 à 5 %) sont incompatibles avec
       les tableaux officiels (France 4 % contre 13 % dans l'Exhibit 2.2 de 2015). C'est une erreur
       d'EdStats ;
     - **Lituanie 2015** : EdStats donne 536 et 530 contre 535 et 528 dans le rapport 2015 et dans les
       tableaux de tendance de 2019 et 2023.

   Pour la Grèce 1995, il n'y a pas d'auto-contrôle (la valeur vient d'EdStats).
4. **Valeurs sans tableau de tendance.** Trois couples pays-année (18 valeurs) ne figurent dans aucun tableau
   de tendance : Lettonie 1995 (LSS), Lettonie 2007, Pologne 2011. Ils sont contrôlés contre EdStats : écart
   inférieur à 0,5. Toutes les autres valeurs de la base sont couvertes par au moins un contrôle.
5. **Reproductibilité.** Un téléchargement complet dans un répertoire vide, suivi de l'extraction, redonne un
   `timss.csv` identique octet pour octet.

## 6. Lacunes

- **Estonie, Luxembourg** : jamais présents en 4e année.
- **Italie 1995** : l'Italie a participé, mais les rapports excluent ses données de 1995 des tendances, pour
  des différences de couverture de population. Il n'y a ni valeur réétalonnée, ni valeur EdStats.
- **Grèce** : 1995 seulement (EdStats). **Autriche, Croatie, Malte** : absentes de TIMSS 2023 en 4e année.
  **Slovénie** : absente en 2019. **Roumanie** : absente en 2015 et 2019. **France** : présente seulement
  depuis 2015.
- **Année 1999** : TIMSS 1999 ne portait que sur la 8e année. Il n'y a donc pas de point de 4e année.
- **Niveau bas** : il vient d'un pourcentage publié arrondi à l'entier. Pour une précision au dixième, il
  faudrait recalculer à partir des microdonnées. Celles de 2023 sont téléchargeables sans inscription sur
  `https://timss2023.org/data`.
- **Erreurs types** : elles sont données en note pour les moyennes et le % avancé, mais pas pour le niveau bas.

## 7. Reproduction

```bash
python3 -I sources/timss.py [dossier_brut]   # télécharge (si absent), extrait, contrôle, écrit sources/timss.csv
```

- Dépendances : `pandas`, `openpyxl`, `pymupdf` et `xlrd` (pour les `.xls` de 2015).
- Sous `python -I`, `xlrd` doit être importable depuis le site-packages système.
- Dans cette session, il a été installé dans `scratchpad/efficience/pylib`. Le lanceur
  `scratchpad/efficience/tools/run_timss.py` l'ajoute au chemin de recherche avant d'exécuter le module.
- Le téléchargement passe par `urllib` (proxy HTTPS de l'environnement, vérification TLS active).
- Aucun code n'est exécuté depuis le dossier des données brutes.
