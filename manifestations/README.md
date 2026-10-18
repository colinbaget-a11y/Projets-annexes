# Les émeutes profitent-elles à un bord politique ?

On compare l'évolution des intentions de vote dans les semaines qui suivent de grandes émeutes à la
tendance qu'elles suivaient avant. Pays : France, Royaume-Uni, Allemagne, Espagne, Italie ; période
2005-2025.

## Fichiers

| Fichier | Contenu |
|---|---|
| `sondages.py` → `sondages.csv.gz` | Environ 7 000 sondages, par parti, institut et date de fin de terrain. Sources : Wikipédia en anglais (pages « Opinion polling for… »), Wikipédia en français (présidentielles 2007 à 2027) et wahlrecht.de (Allemagne, tous instituts) |
| `blocs.py` | Regroupement des partis en six blocs : droite radicale, droite, centre, gauche, gauche radicale, autres. Bloc du chef de gouvernement à chaque date |
| `episodes_candidats.csv`, `episodes_notes.md` | 38 épisodes documentés et sourcés (dates, morts, interpellations, véhicules, dégâts, déclencheur, profil), avec la règle de sélection |
| `episodes.csv` | Liste retenue (21 épisodes), par échantillon |
| `analyse.py` → `resultats.csv`, `resultats_regroupes.csv`, `figures/` | Estimation, placebos, figures |

```bash
python sondages.py          # collecte (cache local des pages)
python analyse.py           # estimation sur episodes.csv
```

## Sélection des épisodes

La règle a été fixée avant tout calcul d'effet :

- **Destruction (obligatoire).** Au moins 100 véhicules incendiés, ou 20 bâtiments ou commerces
  incendiés ou pillés, ou 1 M€ de dégâts.
- **Plus intensité ou extension.**
  - Intensité : au moins 300 interpellations, ou 100 membres des forces de l'ordre blessés.
  - Extension : au moins 3 communes, sur au moins 2 jours.

Trois échantillons :

- **Principal (10 épisodes)** : les épisodes retenus, en métropole.
- **Robustesse (8 épisodes)** : les cas limites.
- **Hors champ (3 épisodes)** : outre-mer et Irlande du Nord, non couverts par les sondages
  nationaux.

La date de l'événement est le premier jour des émeutes.

## Méthode

1. **Une seule base de sondages par pays.** Toutes les séries de sondages du pays sont gardées, avec
   un effet fixe série × institut. Cet effet absorbe le biais habituel de chaque sondeur et la
   différence de niveau entre questions (présidentielle, européennes…). Les scénarios d'un même
   sondage sont moyennés. Les fenêtres s'arrêtent aux élections.
2. **Tendance d'avant.** Sur les 26 semaines précédentes, part du bloc = effet institut + pente ×
   temps.
3. **Écart.** Les sondages des 0 à 6 semaines (puis 6 à 12) qui suivent, moins le prolongement de
   cette tendance. Variante sans tendance : écart au niveau des 12 dernières semaines.
4. **Placebos.** La même procédure est appliquée à toutes les dates du même pays, à plus ou moins
   4 ans, loin de toute émeute. Ces placebos donnent la distribution des écarts « normaux » et la
   p-valeur.
5. **Estimation regroupée.** C'est la moyenne des écarts sur un échantillon. Sa distribution sous
   l'hypothèse nulle s'obtient en tirant un placebo par épisode, dans la distribution de son propre
   pays.

## Résultats (version du 18 octobre 2026)

Épisodes utilisables : les autres manquent de sondages, voir plus bas.

| Épisode | Droite radicale, avec tendance | Droite radicale, sans tendance | Parti au pouvoir, avec / sans tendance |
|---|---|---|---|
| Angleterre 2011 | +0,1 | +0,2 | −0,1 / −0,1 |
| Blockupy Francfort 2015 | +0,3 | −0,4 | −0,6 / −0,2 |
| G20 Hambourg 2017 | +2,0 | +0,1 | −0,4 / +1,4 |
| Gilets jaunes, déc. 2018 | +5,8 | +2,9 | +4,6 / −2,5 |
| Catalogne 2019 | +2,4 | +3,1 | −0,1 / −1,1 |
| **Moyenne (principal)** | **+2,1 (p = 0,03)** | **+1,2 (p = 0,07)** | +0,7 / −0,5 (n.s.) |
| Moyenne (robustesse, 5 épisodes) | +1,2 (p = 0,60) | +1,1 (p = 0,12) | −2,5 / −0,4 |

Lecture :

- **Les émeutes « sans mouvement politique » ne déplacent rien de mesurable.** C'est le cas de
  l'Angleterre 2011, mais aussi de Blockupy, Rome 2011 et Milan 2015.
- **La hausse de la droite radicale vient de deux épisodes** : les Gilets jaunes et la Catalogne.
  Ce sont deux mouvements politiques en eux-mêmes. Pour la Catalogne, le déclencheur (la sentence
  du procès) et la campagne des législatives de novembre 2019 tombent dans la même fenêtre. On ne
  peut pas attribuer l'écart aux images d'émeutes plutôt qu'à la question catalane.
- **Le G20 (+2,0) dépend entièrement de la tendance.** L'AfD baissait avant ; sans tendance,
  l'écart est nul.
- **Aucun effet systématique sur le parti au pouvoir.**

## Limites

- **France.** Les intentions de vote entre deux élections sont trop rares.
  - Banlieues 2005, Villiers-le-Bel 2007, Nahel 2023, PSG 2025, retraites 2023 et 1er mai 2018
    sont inutilisables : moins de 8 sondages avant ou 4 après.
  - Il n'y a que 10 dates placebo utilisables en France, toutes en 2021 et consécutives. La
    p-valeur des Gilets jaunes n'est donc pas fiable.
  - Les sondages européens de décembre 2018 à février 2019 testent parfois une liste Gilets jaunes
    (« autres »). La moyenne des scénarios change alors de composition.
- **Royaume-Uni 2024 (Southport).** L'élection a eu lieu 4 semaines avant : pas de tendance
  d'avant.
- **Espagne 2021 (Hasél).** Les sondages 2019-2022 ne figurent plus sur la page Wikipédia en
  anglais.
- **Peu d'épisodes.** Cinq épisodes utilisables dans l'échantillon principal : l'estimation
  regroupée est très sensible à un seul cas.
- **Le déclencheur et l'émeute sont confondus.** On mesure l'effet de l'épisode dans son ensemble.
