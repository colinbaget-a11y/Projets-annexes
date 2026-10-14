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

## Correspondance avec les chiffres de la note

| Chiffre de la note | Retrouvé dans la base |
|---|---|
| Dépense par élève, France, environ 9 360 EUR (moyenne 2022-2024) | UOE, établissements publics, CITE 1-2 : 9 061 (2022) et 9 663 (2023), moyenne 9 362 ; 2024 pas encore publié |
| Primaire et secondaire, en % du PIB : FR 4,5, BE 5,3, EE 4,8, SI 4,6 | COFOG GF09 moins le supérieur (GF0904), 2022 : identique |
| Services annexes 14 %, pré-primaire et primaire 27,5 %, rémunérations 71 % (2024) | COFOG 2024 : 13,5 %, 28,4 %, 69,8 %. Écarts dus aux révisions des données |
| Dépense de santé, France, environ 4 250 EUR par habitant (2022) | En SPA : 4 164 (2022) et 4 319 (2023). En EUR : 4 548. Correspondance probable : SPA, moyenne 2022-2023 |
| Reste à charge 9,3 % (France) contre 14,9 % (moyenne UE) | Eurostat HF3 : 10,4 % pour la France en 2022. La source de la note est probablement l'OCDE ou l'OMS |

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
  - `figure3_sante.png`, `figure4_decomposition_sante.png` ;
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

Écarts restants :

- **Santé.** La France est bien 11ᵉ, mais avec un écart de +2,8 points (note : +3,5) et un ratio
  de 86 % (note : 83 %). La série de dépense de santé de la note n'a pas été identifiée : sur sa
  figure 3, l'Irlande dépense moins que la France et le Luxembourg 8 900 €, ce qui ne correspond à
  aucune série d'Eurostat. La base utilise Eurostat en euros, 2022. Quelques rangs diffèrent.
- **Équivalent dépense.** On trouve 48 Md€ contre 71 Md€ dans la note. Ce chiffre dépend des
  effectifs retenus : on prend les élèves des CITE 1 et 2, soit 7,7 millions en 2022.
