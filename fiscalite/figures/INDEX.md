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

Deux avertissements de lecture. Les listes nationales d'impôts sont libellées en monnaie
nationale : les comparaisons entre pays passent donc par `gov_10a_taxag`, déjà exprimé en
points de PIB. Et la Suède classe les cotisations patronales en impôts sur la production,
ce qui explique son niveau dans `g6` et son profil dans `g5`.
