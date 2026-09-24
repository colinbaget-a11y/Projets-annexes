# Part de l'industrie : d'où vient l'écart 12 % / 10 %

Réponse courte : **oui, l'essentiel vient de C contre B-E**, mais c'est en partie une
coïncidence. Le passage du manufacturier (C) à l'industrie hors construction (B-E) vaut
**+2,3 points** sur un écart net de 2,5 points, soit 93 % en 2024. Les deux autres choix
pèsent chacun plus d'un point et se compensent presque : le dénominateur (VA totale au
lieu du PIB) ajoute +1,2 point, le passage en volume en retire −1,1.

## Les trois choix qui séparent les deux graphiques

| | calcul du collègue | calcul de la note |
|---|---|---|
| numérateur | industrie manufacturière, NACE C | industrie hors construction, NACE B-E |
| dénominateur | PIB | valeur ajoutée totale des branches |
| valorisation | prix courants | volumes chaînés, prix de 2020 |

B-E ajoute à C les industries extractives, l'énergie, l'eau et les déchets : environ un
quart de la VA industrielle française. Le PIB dépasse la VA totale de 11,8 % en 2024
(impôts nets de subventions sur les produits), ce qui gonfle mécaniquement tout ratio
rapporté à la VA.

## Décomposition de l'écart (AMECO, printemps 2026, France)

Contributions calculées en valeur de Shapley, c'est-à-dire en moyennant sur les six ordres
possibles de substitution, pour que l'ordre des étapes ne décide pas du partage.

| | 2019 | 2024 | 2025 |
|---|---|---|---|
| C / PIB en valeur | 9,91 % | 9,57 % | 9,49 % |
| B-E / VA en volume | 12,90 % | 12,05 % | 11,92 % |
| **écart** | **+2,99 pt** | **+2,48 pt** | **+2,43 pt** |
| dont numérateur C → B-E | +2,11 | +2,32 | +2,12 |
| dont dénominateur PIB → VA | +1,38 | +1,22 | +1,24 |
| dont valeur → volume | −0,51 | −1,06 | −0,93 |

Les huit combinaisons en 2024 : C/PIB 9,57 (valeur) et 9,02 (volume) ; C/VA 10,70 et
10,09 ; B-E/PIB 12,21 et 10,77 ; B-E/VA 13,65 et **12,05**.

Deux remarques sur le terme valeur / volume. Il a triplé entre 2019 et 2024 à cause du
choc énergétique : la VA nominale de la branche énergie a bondi en 2023 (ratio B-E/VA en
valeur : 12,1 % en 2022, 14,5 % en 2023), sans contrepartie en volume. Et un ratio de deux
volumes chaînés ne dépend de l'année de référence qu'à un facteur d'échelle près : changer
2020 en 2015 déplace le niveau, jamais la pente.

## Les comptes n'ont pas été révisés dans AMECO

Entre le millésime d'automne 2025 et celui de printemps 2026, **aucune des séries
françaises utilisées n'a bougé sur 1960-2024** : VA par branche et PIB, en valeur comme en
volume, emploi en équivalents temps plein, 0 année révisée sur 65 pour chacune. La seule
nouveauté du millésime de printemps est l'année 2025, absente de la version précédente.
La révision des comptes annuels de mai n'est donc pas en cause dans l'écart.

Attention cependant : elle existe bien, mais elle n'est pas encore dans AMECO. Eurostat
(nama_10_a10, consulté le 24 septembre 2026) donne pour 2024 une part B-E/VA en volume de
12,40 % contre 12,05 % dans AMECO, et une part C/PIB en valeur de 10,16 % contre 9,57 %.
Les deux sources coïncident exactement jusqu'en 2022 et divergent à partir de 2023. AMECO
de printemps 2026 a donc été arrêté avant la publication de l'INSEE de fin mai. Si le
collègue calcule sur les fichiers INSEE ou Eurostat à jour, il obtient 10,2 % là où AMECO
donne 9,6 % — cela déplace les deux chiffres dans le même sens et laisse l'écart à
2,2 points.

## Fichiers

- `extract_ameco.py` : télécharge les deux millésimes et extrait les 21 séries françaises.
  Le millésime courant vient du site de la Commission ; la Commission n'archivant pas ses
  versions, le millésime d'automne 2025 est repris du dépôt miroir de DBnomics, qui
  conserve les fichiers bruts `AMECO*.TXT` commit par commit
  (`git.nomics.world/dbnomics-source-data/ameco-source-data`, projet 36, commit `1b7562a4`
  du 13 décembre 2025).
- `donnees/ameco_france_s2026.csv`, `donnees/ameco_france_a2025.csv` : les extraits.
- `part_industrie.py` : les huit ratios, la décomposition et le test de révision.
- `resultats.json` : les chiffres ci-dessus.

Codes AMECO utiles : `UVGM` / `OVGM` manufacturier, `UVG2` / `OVG2` industrie B-E,
`UVG0` / `OVG0` VA totale, `UVGD` / `OVGD` PIB, `FETM` / `FET2` / `FETD` emploi en ETP.
Préfixe `U` pour les prix courants, `O` pour les volumes aux prix de 2020.
