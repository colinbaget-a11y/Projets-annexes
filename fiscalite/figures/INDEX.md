# Figures de l'état des lieux

Produites par `graphiques.py`. Palette catégorielle validée par le script de contrôle
(bande de clarté, plancher de chroma, séparation en vision déficiente, contraste) ; les
séries sont toujours identifiées par une étiquette directe, jamais par la couleur seule.

| Fichier | Ce qu'il montre |
|---|---|
| `g1_blocs_pib.png` | Les six blocs de prélèvements en % du PIB, 1995-2024. Le total bouge peu, la composition bascule. |
| `g2_csg_contre_ir.png` | CSG contre impôt sur le revenu. Le plus gros des deux impôts sur le revenu est proportionnel. |
| `g3_classement_2024.png` | Les vingt premiers impôts de 2024, en milliards. |
| `g4_concentration.png` | Part cumulée du produit fiscal : 3 impôts font 50 %, 21 en font 90 %. |
| `g5_comparaison_structure.png` | France et Danemark prélèvent autant, par des moyens opposés. Les 27 États membres. |
| `g6_impots_production.png` | Les autres impôts sur la production en % du PIB. France deuxième derrière la Suède, dont la classification diffère. |
| `g7_fonction_economique.png` | Ce que l'on taxe : consommation, travail, capital, et la part non répartie. |
| `g8_depenses_fiscales.png` | Les quatorze dépenses fiscales les plus coûteuses du PLF 2026. |
| `g9_longue_traine.png` | Les 99 impôts à rendement non nul, échelle logarithmique. |
| `g10_detention_transaction.png` | Taxe foncière, DMTG et DMTO : détenir, transmettre, échanger. |
| `g11_taux_global_pays.png` | Le taux de prélèvement de 1995 à 2024, chaque État membre en gris. |
| `g12_fiscalite_energie.png` | La fiscalité de l'énergie : niveau depuis 1995 et composition en 2024. |

## Découpages analytiques (chapitre 3)

Produites par `graphiques_decoupages.py`, à partir de la classification de
`donnees/classification_prelevements.csv`.

| Fichier | Ce qu'il montre |
|---|---|
| `h1_ce_que_l_on_taxe.png` | Les 1 274,9 Md€ reclassés selon ce qu'ils atteignent en dernier ressort, et non selon leur étiquette comptable. |
| `h2_efficience_productive.png` | La part des prélèvements qui distord les décisions de production, et celle qui le fait sans corriger de dommage. |
| `h3_prelevements_sur_intrants.png` | Le détail des 77 Md€ assis sur un facteur de production sans justification correctrice. |
| `h4_lecture_par_principe.png` | Ce que les principes du chapitre 2 impliqueraient, prélèvement par prélèvement. |

## Mirrlees Review appliquée à la France (chapitre 4)

Produites par `graphiques_mirrlees.py`, à partir des données OCDE extraites par `extract_mirrlees.py`.

| Fichier | Ce qu'il montre | Équivalent dans Tax by Design |
|---|---|---|
| `m1_prix_carbone_secteurs.png` | La dispersion du prix implicite du carbone entre secteurs français. | chapitre 11 |
| `m2_carbone_comparaison.png` | Part des émissions tarifées au-dessus de 60 € la tonne, France et comparaisons. | chapitre 11 |
| `m3_taux_marginaux_effectifs.png` | Taux effectif de prélèvement sur une hausse du temps de travail, par ménage et par pays. | figures 4.6 et 4.8 |
| `m4_taux_participation.png` | Ce que rapporte une reprise d'emploi depuis le revenu minimum. | figures 4.5 et 4.7 |

## Les trois chapitres pédagogiques (partie III)

Produites par `graphiques_pedagogie.py`, à partir des données extraites par
`extract_pedagogie.py`.

| Fichier | Ce qu'il montre |
|---|---|
| `p1_retraites_niveau_vie.png` | Le niveau de vie relatif des 65 ans et plus en Europe, et le taux de pauvreté par âge : la France est le pays où la vieillesse protège le mieux de la pauvreté et où l'enfance en protège le moins. |
| `p2_salaire_pension.png` | Les prélèvements sociaux sur 100 € de salaire et sur 100 € de pension, en distinguant la part qui ouvre des droits : l'écart vaut 11,7 points ou 0,4 point selon la convention comptable retenue. |
| `p4_impot_sur_l_attente.png` | Le taux d'imposition implicite de la consommation différée, qui croît avec la durée de détention : trente ans d'épargne au prélèvement forfaitaire unique reviennent à taxer la consommation à 23 %. |
| `p3_stock_contre_flux.png` | Ce qu'un impôt annuel sur le patrimoine représente en taux sur le rendement : à 2 % du stock et 3 % de rendement réel, l'impôt dépasse la totalité du rendement. |

Deux avertissements de lecture. Les listes nationales d'impôts sont libellées en monnaie
nationale : les comparaisons entre pays passent donc par `gov_10a_taxag`, déjà exprimé en
points de PIB. Et la Suède classe les cotisations patronales en impôts sur la production,
ce qui explique son niveau dans `g6` et son profil dans `g5`.
