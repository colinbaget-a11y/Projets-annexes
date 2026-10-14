# Base de données du bulletin « Efficience des dépenses publiques » (C26-096)

Bulletin de C. Baget et C. Deredec (juillet 2026). Il porte sur 24 pays de l'UE, avec 27 indicateurs
pour l'éducation et 26 pour la santé, et compare un score composite à la dépense (frontière
d'efficience). La note elle-même n'est pas versionnée ici.

Cette base rassemble toutes les séries qui ont servi au bulletin. Elle couvre les 27 pays de l'UE et,
pour chaque série, toutes les années disponibles : des plus anciennes (PISA 2000, TIMSS 1995,
Eurostat depuis 1960 pour certaines séries) aux plus récentes (PISA 2025, TIMSS 2023, Eurostat 2025).

## Utilisation

```bash
python base_efficience.py                 # assemble la base à partir de sources/*.csv
python base_efficience.py --telecharger   # relance chaque extraction (PISA : plusieurs Go)
python sources/eurostat.py                # ne relance que la source Eurostat
```

Sorties :

- `base_efficience.csv` : données en format long, colonnes `pays, indicateur, annee, valeur,
  source, note`. Les pays sont en codes ISO2 Eurostat (EL pour la Grèce).
- `base_efficience.sqlite` : la même base, avec les tables `donnees` et `indicateurs`.
- `indicateurs.csv` : dictionnaire des 53 indicateurs du bulletin, avec pour chacun :
  - objectif, polarité, année retenue dans le bulletin ;
  - source et définition ;
  - années disponibles et couverture ;
  - remarque sur la correspondance avec la note.

  Il documente aussi la dépense, les pondérations et les séries de l'encadré.
- `couverture.csv` : nombre de pays couverts par indicateur et par année.

## Sources (`sources/`)

Chaque source a un module `<nom>.py` (fonctions `extraire` et `telecharger`), un fichier `<nom>.csv`
et, pour les sources complexes, des notes `<nom>_notes.md`.

| Module | Contenu |
|---|---|
| `eurostat` | Insertion, chercheurs, langues, dépense d'éducation (UOE, COFOG), effectifs, espérance de vie, mortalité, imagerie, accès, reste à charge, médecins, vaccination, production pharmaceutique, dépense de santé, population |
| `pisa` | Indicateurs calculés sur les microdonnées PISA 2000-2025 |
| `timss` | TIMSS 4e année (CM1), 1995-2023 |
| `sante_ext` | Infarctus (OCDE), antibiotiques (ECDC), dépenses catastrophiques (OMS), attente, R&D pharmaceutique, surmortalité, inégalité territoriale des médecins |
| `ocde_sha` | Dépense de santé par habitant (EUR à PPA, prix courants et constants) et part du reste à charge, OCDE Health Statistics, 2000-2025 |

## Correspondance avec les chiffres de la note

| Chiffre de la note | Retrouvé dans la base |
|---|---|
| Dépense par élève, France, environ 9 360 EUR (moyenne 2022-2024) | UOE, établissements publics, CITE 1-2 : 9 061 (2022) et 9 663 (2023), moyenne 9 362 ; 2024 pas encore publié |
| Primaire et secondaire, en % du PIB : FR 4,5, BE 5,3, EE 4,8, SI 4,6 | COFOG GF09 moins le supérieur (GF0904), 2022 : identique |
| Services annexes 14 %, pré-primaire et primaire 27,5 %, rémunérations 71 % (2024) | COFOG 2024 : 13,5 %, 28,4 %, 69,8 %. Écarts dus aux révisions des données |
| Dépense de santé par habitant (figure 3), source : dépense publique de santé harmonisée par l'OCDE | La convention harmonisée OCDE-Eurostat-OMS range l'assurance privée obligatoire (Allemagne, Pays-Bas) avec le public : ce sont les « régimes publics et obligatoires » (HF1). Série retenue : HF1 en euros, 2022. Elle reproduit l'allure de la figure (Bulgarie et Roumanie autour de 650 €) mais pas tous les points : France 3 783 contre 4 250, Luxembourg 5 675 contre 8 900, Irlande 4 612 contre 3 950. Écart médian d'environ 12 %. Testées sans meilleur résultat, 2015-2025 : dépense totale (EUR, SPA, PPA OCDE), COFOG santé, part du PIB × PIB par habitant |
| Reste à charge 9,3 % (France) contre 14,9 % (moyenne UE), source OCDE Health at a Glance | Non retrouvé. OCDE et Eurostat (HF3) : 10,2-10,7 % pour la France entre 2020 et 2024. La valeur la plus proche est 9,2-9,5 %, mais pour la Croatie |
| Part d'élèves peu performants | Élèves sous le niveau 2 dans les trois domaines à la fois (`pisa_faibles_3domaines`) : France 16,8 % en 2022 |

## État de la base

- 53 indicateurs du bulletin sur 53, plus la dépense, les pondérations et les séries de l'encadré :
  107 séries et 50 481 valeurs au total.
- Couverture par indicateur dans `indicateurs.csv`, colonnes `annees_disponibles` et `n_pays`.

## Points à connaître

- **PISA, cycles 2000-2012.** Les valeurs publiées (Banque mondiale EdStats) remplacent les
  calculs sur microdonnées, car l'Internet Archive refusait les connexions.
  - Le lecteur des fichiers texte est prêt. Relancer `python sources/pisa.py` substitue
    automatiquement les calculs aux valeurs publiées.
  - Pour Chypre (absente des fichiers publics), les valeurs viennent aussi des tableaux OCDE et
    d'EdStats.
- **Élèves résilients.** La définition OCDE 2022 est appliquée à tous les cycles. L'OCDE utilise
  la lecture en 2018 et les sciences en 2025.
- **TIMSS.** Pour la Belgique, `BE` correspond à la seule Communauté flamande. Les valeurs de
  1995 sont réétalonnées, prises dans les tableaux de tendance.
- **Infarctus.** La série est chaînée dans 20 pays et non chaînée dans 4. Une variante homogène
  existe : `sante_ima30_nonchaine`.
- **Antibiotiques.** Les données viennent de l'OCDE, car l'ECDC n'est pas téléchargeable.
- **Temps d'attente.** Le délai OCDE pour une prothèse de hanche ne couvre que 11 pays, sans la
  France.
- **R&D pharmaceutique.** La série française présente une rupture probable en 2021.
- **Notes détaillées** : `sources/*_notes.md`.

## Reproduction des figures du bulletin (`bulletin.py`)

`python bulletin.py` recalcule les scores, les contributions, les frontières et la sensibilité
(20 000 tirages), puis écrit :

- `resultats_bulletin.csv` ;
- dans `figures/` :
  - `figure1_education.png`, `figure2_decomposition_education.png` ;
  - `figure3_sante.png` (dépense HF1 en euros courants), `figure3_sante_ppa.png` (même dépense en
    parité de pouvoir d'achat), `figure4_decomposition_sante.png` ;
  - `encadre_depense_education.png`, `figureA_sensibilite.png`.

Le schéma de la chaîne méthodologique n'est pas reproduit : il ne repose sur aucune donnée.

Les années retenues sont la dernière valeur disponible entre 2019 et 2024 ; pour TIMSS, la dernière
valeur entre 2019 et 2023 ; pour PISA, 2022. Avec cette convention, on retrouve les chiffres de la
note pour l'éducation :

| | Note | Base |
|---|---|---|
| Score de la France | 0,39 | 0,393 |
| Rang | 21ᵉ | 21ᵉ |
| Écart à la moyenne UE | −9,8 | −9,4 |
| Contributions des quatre objectifs | −3,3 / −1,2 / −3,6 / −1,7 | −3,4 / −1,3 / −3,2 / −1,6 |
| Ratio d'efficience | 55 % | 55,2 % |
| Gain à dépense constante | 32 points | 32 points |
| Rang sous les 20 000 pondérations | 19ᵉ-23ᵉ, médiane 21ᵉ | identique |

La tête du classement (Irlande, Estonie, Finlande, Pologne, Danemark) et la queue (Roumanie,
Bulgarie, Grèce, France, Slovaquie) sont les mêmes.

En santé, avec la dépense publique et obligatoire (HF1, euros, 2022) :

| | Note | Base |
|---|---|---|
| Score de la France | 0,60 | 0,601 |
| Rang | 11ᵉ | 11ᵉ |
| Écart à la moyenne UE | +3,5 | +2,8 |
| Ratio d'efficience | 83 % | 86 % |
| Pays sur la frontière | BG, PL, EL, PT, SI, IT, SE | BG, PL, EL, SI, ES, IT, SE, DK |

En parité de pouvoir d'achat (`figure3_sante_ppa.png`, colonne `ratio_efficience_ppa`) :
- le ratio de la France passe de 86 % à 83 % ;
- les pays d'Europe centrale et orientale perdent beaucoup : Pologne de 100 % à 73 %, Roumanie de 75 %
  à 55 %, Hongrie de 83 % à 62 %, Tchéquie de 85 % à 73 %.

Variante intermédiaire, où les biens médicaux sont comptés au prix de marché et le reste en PPA :
la France est à 83 %, la Pologne à 73 %, la Roumanie à 63 %. Les biens médicaux ne pèsent que
5 à 26 % de la dépense HF1, le personnel et les services le reste.

Écarts restants :

- **Santé.** Le score de la France est retrouvé (0,601 contre 0,604). Pour la moitié des pays,
  l'écart est de moins de 0,03. Il est plus grand pour le Portugal (−0,08), la Hongrie, la Finlande,
  la Suède, la Slovénie, l'Estonie (environ −0,05) et l'Allemagne (+0,05). Ces écarts viennent
  probablement des indicateurs dont la définition n'est pas précisée dans la note : temps
  d'attente, reste à charge.
- **Équivalent dépense : 71 Md€ dans la note, 48 Md€ dans la base.** La frontière atteint le score
  de la France pour 3 062 € par élève, contre 9 362 € dépensés. L'écart de 6 300 € par élève,
  multiplié par 7,67 millions d'élèves des CITE 1 et 2, donne 48 Md€. Or 9 362 € × 7,67 millions
  = 71,8 Md€. Le chiffre de la note correspond donc probablement à la dépense totale, et non à la
  distance horizontale à la frontière. Aucun autre périmètre d'effectifs ne retombe sur 71 : CITE
  0-2 donne 63 Md€, CITE 1-3 66 Md€, CITE 0-3 81 Md€.

## Indice d'évolution (`evolution.py`)

Le score du bulletin est relatif : ses bornes min-max sont celles de l'année étudiée. L'indice
d'évolution fixe les bornes de chaque indicateur une fois pour toutes, sur l'ensemble des couples
pays-année de la période. Chaque variation est exprimée en part de l'écart européen observé sur la
période et ne dépend pas de ce que font les autres pays.

**Indice chaîné, 2000-2025 en éducation, 2000-2023 en santé.**

- **Calcul des variations.** La variation entre deux années consécutives est calculée, pays par
  pays, sur les indicateurs disponibles les deux années, avec l'agrégation du bulletin.
- **Niveau.** Il est ancré sur le score à bornes fixes de 2022 ; on cumule ensuite les variations
  vers l'avant et vers l'arrière.
- **Intérêt.** Un indicateur qui n'existe qu'à partir de 2015 (élèves faibles dans les trois
  domaines, résilients, écart social) ou de 2011 (mortalité évitable) compte à partir de cette date,
  sans créer de saut.

Règles :

- **Comparabilité PISA.** Les échelles OCDE sont reliées depuis 2000 pour la lecture, 2003 pour les
  mathématiques et 2006 pour les sciences ; les valeurs antérieures sont écartées.
- **Interpolation.** Linéaire entre deux valeurs observées, prolongation de 3 ans au plus. Chaque
  variation est décomposée par indicateur, en part observée (indicateur mesuré les deux années) et
  part interpolée : `evolution_contributions.csv`, en points de score.
- **Ruptures de série.** Elles sont signalées par la source (statut Eurostat « b », conservé dans
  la colonne `statut` de la base) ou connues. Quand le saut est anormal (plus de 3 écarts-types
  robustes), la série est raccordée. Liste dans `evolution_ruptures.csv`.
- **Indicateurs exclus.**
  - Indices PISA d'appartenance, de sécurité et de harcèlement, recentrés sur la moyenne OCDE à
    chaque cycle.
  - Indicateurs couvrant moins de 75 % des pays, quelle que soit l'année.
- **Panier réduit.** Avant 2005, le panier compte moins des deux tiers des indicateurs : 11 en
  éducation en 2000 (lecture PISA et indicateurs Eurostat), 8 en santé. Un seul indicateur peut
  alors peser lourd, par exemple la vaccination antigrippale en santé en 2001. Ces années sont
  grisées sur les figures.
- **Contrôle.** La colonne `score_panier_constant` donne un indice à panier constant (2015-2025 en
  éducation, 2013-2023 en santé). Pour la France, en éducation, 2015-2025 : −0,5 point en chaîné,
  −0,6 à panier constant.

Sorties : `evolution_scores.csv` (score, objectifs, nombre d'indicateurs, variante à panier
constant), `evolution_contributions.csv`, `evolution_ruptures.csv`,
`figures/evolution_education.png`, `figures/evolution_sante.png`.

Points à vérifier :

- **Hausse de l'objectif équité en 2025.** L'écart de score entre élèves favorisés et défavorisés
  baisse dans presque tous les pays en 2025 (médiane de l'échantillon : de 98 à 81 points). Il faut
  vérifier que l'indice socio-économique ESCS de 2025 est comparable avant d'interpréter cette
  hausse.
- **Hausse de l'objectif équité en 2018.** Elle vient en partie de la dispersion D9-D1 en lecture,
  qui baisse en 2018, année du nouveau cadre et du test adaptatif.
- **Tendance santé.** Elle intègre la hausse générale des équipements d'imagerie, que le bulletin
  compte comme une amélioration.

## Performance éducative 2006-2025 (`performance_education.py`)

Méthode retenue pour comparer l'évolution des pays entre eux.

1. **Panier commun.** Seuls les indicateurs observés pour les 24 pays en 2006 et en fin de période
   sont retenus. Tous les pays sont mesurés sur le même panier chaque année : pas de chaînage, pas
   de poids propre à un pays. Le panier compte 17 indicateurs :
   - scores PISA et élèves faibles par domaine ;
   - élèves forts et chercheurs ;
   - dispersion D9-D1 ;
   - NEET, décrochage, emploi relatif et emploi des jeunes diplômés.

   Sont exclus faute de recul : TIMSS, l'indicateur « faibles dans les trois domaines », les
   résilients, l'écart social, les langues et le chômage des 15-24 ans (2009). 2006 est la première
   année où les trois domaines PISA sont reliés dans le temps et où les 24 pays participent.
2. **Standardisation fixe.** z = signe × (x − moyenne des pays en 2006) / écart-type moyen entre
   pays. C'est une fonction linéaire de x, comme le min-max à bornes fixes, mais l'unité ne dépend
   pas des deux pays extrêmes.
3. **Agrégation du bulletin.** Quatre objectifs à 25 %. L'indice est exprimé en écarts-types
   entre pays ; 0 = pays européen moyen en 2006.

Sorties :

- `performance_education.csv` : indice, objectifs et variante sans insertion.
- Dans `figures/` :
  - `performance_petits_multiples.png` : un panneau par pays, même échelle ;
  - `performance_haltere.png` : niveaux 2006, 2015 et 2025 ;
  - `performance_contributions.png` : contribution de chaque objectif à la variation.

Contrôles :

- Les variations 2015-2025 sont corrélées à 0,91 avec celles de l'indice chaîné (`evolution.py`).
- La variante sans insertion, qui retire le cycle du marché du travail, a des variations
  2006-2025 corrélées à 0,97 avec l'indice complet.

Limite : les erreurs d'échantillonnage et de liaison de PISA ne sont pas encore propagées. Elles
pourraient l'être sur 2015-2025 avec les poids répliqués des microdonnées.
