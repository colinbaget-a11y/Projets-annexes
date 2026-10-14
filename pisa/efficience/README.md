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
