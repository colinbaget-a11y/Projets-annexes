# Niches de l'IR, CRDS et paramètres vérifiés (revenus 2024)

Note de travail pour la fusion IR + CSG + CRDS. Elle a été écrite en novembre 2026.
- Les montants viennent des textes et publications cités.
- Les estimations faites ici sont signalées comme telles.
- Tableaux joints dans `sorties/` :
  - `depenses_fiscales_ir_plf2026.csv` : les 170 dépenses fiscales d'IR du PLF 2026, avec leur classement et leur sort dans la réforme ;
  - `rici_deciles_revenus2024.csv` : réductions et crédits par décile ;
  - `crds_2024_assiette.csv` ;
  - `ecart_retraite_salarie_openfisca.csv`.

## 0. Ce que mesure aujourd'hui la colonne « IR » du modèle

`ir_csg.py` prend la colonne `impot_net_keur` de l'IRCOM (`x["ir"] = x.impot_net_keur / 1e6`).
- **Total : 91,72 Md€ pour 41,6 millions de foyers.** C'est l'impôt net de la DGFiP : 92 Md€ pour les revenus 2024, « après réductions et crédits d'impôt (RICI) » (DGFiP Statistiques n° 41, novembre 2025).
- Il inclut l'impôt hors barème (10 Md€) et la CEHR (moins de 2 Md€). Le code retire ensuite 12,8 % des revenus au PFU.
- Les tranches basses ont un impôt net négatif (−0,73 Md€ sous 20 000 € de RFR) : ce sont les restitutions de crédits.

**Conséquence.** La charge actuelle du modèle est déjà nette de toutes les niches. Cela vaut pour :
- les RICI ;
- les éléments qui passent par l'assiette : quotient, 10 %, abattements, exonérations.

Le calcul « à recette égale » sur une assiette brute sans déduction finance donc déjà, par construction, la suppression de toutes ces niches.

Tranche par tranche, la comparaison « nouvel impôt sur le brut moins impôt net IRCOM » impute donc déjà à chaque tranche de RFR la perte moyenne de ses niches. Ce que le calcul ne voit pas :
1. **La dispersion à l'intérieur d'une tranche.** Les gros utilisateurs de niches perdent plus que la moyenne de leur tranche, les autres moins. C'est un effet de répartition, pas de recette.
2. **L'allègement des revenus de source étrangère.** Cette « RI » vaut 3,8 Md€ et va surtout au haut de la distribution. Elle neutralise une double imposition et découle des conventions fiscales. La réforme ne peut pas la supprimer.
3. **Les comportements.** L'investissement défiscalisé (Pinel, Girardin) s'arrêterait. S'y ajoute une question juridique, non instruite ici : supprimer des réductions déjà engagées sur 6 à 12 ans.

## 1. Les niches de l'IR que la réforme supprime implicitement

### 1.1 Dépenses fiscales au sens officiel (Voies et moyens, tome II, PLF 2026)

Source : *Évaluation des voies et moyens, tome II, dépenses fiscales*, annexe au PLF 2026. Copie sur assemblee-nationale.fr :
https://www.assemblee-nationale.fr/dyn/dyn/contenu/visualisation/1087933/file/Voies_et_moyens_Tome_2_2026.pdf

**Quelle colonne retenir pour les revenus 2024.** Le coût de l'année N est l'impôt émis en N, donc l'impôt sur les revenus N−1. La méthodologie de l'annexe ne le dit pas, mais les chiffres le confirment :

| Dispositif | VM « 2024 » | DGFiP, revenus 2023 | VM « 2025 » | DGFiP, revenus 2024 |
|---|---|---|---|---|
| Frais de garde (Md€) | 1,737 | 1,742 | 1,799 | 1,791 |
| Cotisations syndicales (M€) | 149 | 149 | 156 | 155 |

On retient donc la colonne **2025** (prévision du PLF 2026) pour les revenus 2024.

Le total des dépenses fiscales d'IR est de **43 980 M€** en 2025, dont **15 076 M€** de réductions et crédits d'impôt (tableau « Dépenses fiscales par impôt »). Selon la norme de l'annexe, **ne sont pas** des dépenses fiscales :
- le quotient conjugal et le quotient familial (hors demi-parts spéciales) ;
- l'abattement de 10 % pour frais professionnels des salariés, regardé comme une « modalité de détermination du revenu net catégoriel » ;
- la décote ;
- le seuil de mise en recouvrement ;
- les reports et sursis d'imposition.

La déduction pour épargne retraite (PER) n'apparaît pas non plus dans la liste.

Classement des 170 dépenses fiscales d'IR selon leur sort dans la réforme (coût 2025, en M€) :
- La réforme taxe les salaires (×0,9825), les pensions, les bénéfices des indépendants, le foncier et le chômage.
- Elle n'admet ni déduction, ni réduction, ni crédit.
- Les dépenses non chiffrées sont comptées pour leur dernier montant chiffré, selon la convention de l'annexe.

| Catégorie | Nombre de dépenses | Coût 2025 (M€) | Sort |
|---|---|---|---|
| A. Réductions et crédits d'impôt (1102xx, 1103xx) | 42 | **15 502** | supprimées |
| B1. Déductions et abattements du revenu global, dont l'abattement personnes âgées ou invalides (100201 : 419) | 6 | 482 | supprimées |
| B2. Demi-parts spéciales : parents isolés, vivant seuls ayant élevé un enfant, invalides, anciens combattants, veufs | 6 | 2 854 | supprimées ou remplacées par la règle familiale |
| B3. Abattement de 10 % sur les pensions (120401) | 1 | **5 322** | supprimé |
| B4. Exonérations et régimes salariaux | 26 | 9 270 | supprimées si l'assiette suit celle de la CSG |
| G. Bénéfices des indépendants (BNC, BA, BIC) | 21 | 563 | supprimées si le bénéfice est taxé avant ces déductions |
| E. Revenus fonciers, dont la déduction des réparations et améliorations (130201 : 1 990, dernier chiffrage 2024) | 13 | 2 170 | dépend de la définition du revenu foncier taxé |
| C. Prestations exonérées : prestations familiales et AAH (1 558), APA, PCH, APL, rentes AT-MP | 10 | 2 625 | maintenues de fait (hors assiette) |
| D. Taux forfaitaires : actions gratuites, capital PER (365) | 7 | 681 | hors champ |
| F. Capitaux mobiliers et plus-values : livrets (1 045 pour le livret A), PEA, assurance-vie | 38 | 4 513 | hors champ |
| **Total IR** | 170 | **43 982** | |

La catégorie B4 comprend :
- intéressement, participation et PPV placés (120108 : 2 890) ;
- heures supplémentaires (120146 : 2 212) ;
- titres-restaurant (555) ;
- apprentis (533) ;
- IJ ALD (621) ;
- assistants maternels (427) ;
- impatriés (394) ;
- jobs d'étudiants (314) ;
- ruptures conventionnelles (285) ;
- etc.

**Supprimé à coup sûr (A + B1 + B2 + B3) : environ 24,2 Md€.** On peut ajouter jusqu'à 9,8 Md€ selon la définition des assiettes salariale et indépendante (B4 + G), et 2,2 Md€ pour le foncier.

L'annexe prévient que « la somme des coûts des dépenses fiscales est […] dépourvue de réelle signification » : les dispositifs interagissent, et ils sont chiffrés sans effet de comportement.

Principales réductions et crédits (coût 2025 en M€, bénéficiaires) :

| Dispositif | Coût 2025 (M€) | Bénéficiaires |
|---|---|---|
| Emploi d'un salarié à domicile (110246) | 7 029 | 4,9 M |
| Dons (110201) | 2 204 | 5,6 M |
| Frais de garde des enfants de moins de 6 ans (110203) | 1 799 | 1,9 M |
| Duflot et Pinel (110261) | 1 459 | 384 000 |
| Investissements productifs outre-mer (110224) | 825 | 55 900 |
| DOM : réduction de 30 ou 40 % de l'impôt au barème (110302) | 426 | — |
| Dépendance et EHPAD (110213) | 312 | — |
| Scolarité secondaire (110215) | 229 | — |
| Scolarité supérieure (110242) | 225 | — |
| Scellier majoré (110252) | 169 | — |
| Cotisations syndicales (110202) | 156 | — |
| Frais de comptabilité des centres de gestion agréés (110211) | 143 | — |
| IR-PME (110216) | 52 | — |
| FCPI (110218) | 29 | — |
| Malraux, sites patrimoniaux remarquables (110249) | 44 | — |
| Monuments historiques : déduction des charges (100102) | 29 | — |
| Monuments historiques : déficit foncier (130302) | 55 | — |
| Censi-Bouvard (110250) | 35 | — |
| Denormandie (110265) | 5 | — |
| Loc'Avantages (110269) | 10 | — |

### 1.2 Éléments structurels, hors dépenses fiscales

Ils ne sont pas chiffrés dans les Voies et moyens. Montants d'assiette tirés des totaux des cases 2042 (revenus 2024, `donnees/ir_2042_cases_revenus2024.csv`) :
- **Déduction de 10 % pour frais professionnels** (CGI 83, 3°) : de 504 € à 14 426 € par personne pour les rémunérations de 2024 ; elle s'applique aussi au chômage. Frais réels déclarés (1AK à 1DK) : **35,3 Md€**, pour 5,9 millions de déclarants.
  - Le forfait n'est pas publié. Estimation faite ici : 10 % d'environ 600 à 650 Md€ de salaires et d'allocations non soumis aux frais réels, soit **environ 60 à 65 Md€**.
  - Coût en impôt : ordre de grandeur de 10 Md€ ou plus. C'est une hypothèse faite ici, à un taux marginal moyen de 10 à 15 %, sans microsimulation.
- **Quotient conjugal et quotient familial.** Pas de chiffre officiel récent dans les sources consultées. Chiffres déjà présents dans le dossier, non revérifiés ici :
  - CPO : 11,8 Md€ pour le quotient conjugal et 10 Md€ pour le quotient familial, dans un impôt fusionné (`note-ir-csg.tex`) ;
  - André et Sireyjol (2021, Ines, IR 2017) : 27,7 Md€ pour la conjugalisation et la familialisation ensemble, dont 40 % pour la conjugalisation ; les 15 % les plus aisés captent 48 % du gain de la conjugalisation (`lit_chomage_natalite.md`).
  - Plafond de l'avantage par demi-part, revenus 2024 : **1 791 €** ; 4 224 € pour la part du premier enfant d'un parent isolé (CGI 197, I, 2).
- **Épargne retraite.** Déductions déclarées : 6NS à 6NU 7,10 Md€ ; 6RS à 6RU (PERP) 1,00 ; 6QS à 6QU 1,55 ; soit **environ 9,6 Md€**, plus 0,94 Md€ en 6OS et 6OT pour les indépendants. Ces sommes sont réintégrées dans le RFR (CGI 1417, IV, 1° a), donc l'IRCOM par RFR les « voit ».
- **Pensions alimentaires versées** (6EL, 6EM, 6GI, 6GJ, 6GP, 6GU) : **9,1 Md€** déduits. Elles sont imposables chez le bénéficiaire (1AO : 5,0 Md€). Les supprimer des deux côtés est presque neutre en assiette, mais pas en impôt.
- **CSG déductible.** Fractions déductibles (CGI 154 quinquies) :
  - 6,8 points sur 9,2 pour les revenus d'activité ;
  - 5,9 points sur 8,3 pour les pensions ;
  - 4,2 points sur 6,6 ;
  - 3,8 points sur 3,8 et sur 6,2.
  - Hors salaires et pensions, la case 6DE représente 3,15 Md€.
  - Dans un impôt fusionné, ce mécanisme disparaît sans perte : il n'était qu'un transfert interne entre CSG et IR.
- **Heures supplémentaires.** Elles sont exonérées d'IR mais restent soumises à la CSG et à la CRDS :
  - aucune exclusion n'apparaît dans la liste du III de CSS L136-1-1 consultée ;
  - `ir_csg.py` les compte d'ailleurs dans les salaires soumis à la CSG (21,8 Md€ en 1GH à 1JH).
  - Le plafond d'exonération d'IR n'a pas été revérifié.
- **Prime de partage de la valeur** exonérée : 2,29 Md€ déclarés (1AD à 1DD). Son assujettissement à la CSG n'a pas été vérifié sur le texte.
- **Décote** (structurelle) et **seuil de recouvrement** de 61 € : non chiffrés dans les sources consultées.

### 1.3 À qui vont les réductions et crédits

Source : DGFiP Statistiques n° 41, novembre 2025, tableaux 3 et 4. Les données sont tirées de POTE 2024, 3e émission. Les déciles sont des déciles de RFR par part.
https://www.impots.gouv.fr/sites/default/files/media/9_statistiques/0_etudes_et_stats/0_publications/dgfip_statistiques/2025/num41_11/dgfip_stat_41.xlsx

**Total des RICI pour les revenus 2024 : 19,53 Md€**, pour 12,8 millions de foyers :
- crédits d'impôt 9,77 Md€, dont emploi à domicile 6,52 et garde 1,79 ;
- réductions d'impôt 9,75 Md€, dont dons 1,64 + 0,51, revenus de source étrangère **3,83**, Pinel, Scellier et apparentés 1,73, Girardin productif 0,76.

45 % des crédits (4 Md€) vont à des foyers non imposés, dont 2 Md€ restitués. Hors revenus de source étrangère, les RICI (≈ 15,7 Md€) recoupent les 15,1 Md€ des Voies et moyens.

| Groupe (RFR par part) | RICI moyen | Part des RICI | Part de l'IR net | RICI en % de l'IR avant RICI | Taux moyen sur le RFR, avant puis après RICI |
|---|---|---|---|---|---|
| D1 à D5 | 49 à 182 € | 12,9 % | < 0 | — | ≈ 0 → < 0 |
| D6 à D9 | 223 à 647 € | 33,0 % | 27,6 % | 16 à 44 % | 8,2 → 6,9 % (D9) |
| **D10** | **2 538 €** | **54,0 %** | **74,3 %** | **13,4 %** | 18,0 → 15,6 % |
| dont 1 % | 8 999 € | 19,2 % | 33,1 % | 11,0 % | 22,2 → 19,7 % |
| dont 0,1 % | 33 214 € | 7,1 % | 14,1 % | 9,6 % | 20,7 → 18,7 % |

Au dernier millième, un tiers de la hausse des RICI de 2024 vient de la RI sur les revenus de source étrangère (texte de la publication).

**RFR supérieur à 100 000 € et à 200 000 €.**
- Ces foyers représentent 3,4 % et 0,72 % des foyers (IRCOM 2024).
- Ils paient 49,0 Md€ (53,4 %) et 28,5 Md€ (31,1 %) de l'IR net.
- Leur part des RICI n'est pas publiée. En interpolant en log entre les points 0,1 %, 1 % et 10 % (estimation faite ici, avec le classement par part comme approximation), on obtient :
  - **environ 35 à 40 % des RICI (≈ 7 à 8 Md€) au-dessus de 100 000 €** ;
  - **environ 15 à 18 % (≈ 3 à 3,5 Md€) au-dessus de 200 000 €**.
- Une part notable correspond aux revenus de source étrangère, qui ne peuvent pas être supprimés.

**Lecture.** En euros par foyer, le haut de la distribution perd beaucoup plus de niches : 2 538 € au dernier décile contre 49 € au premier. Mais les RICI sont **moins concentrés que l'impôt lui-même** :
- elles valent 13 % de l'IR avant RICI du dernier décile ;
- 10 % de celui du dernier millième ;
- 17,5 % de celui de l'ensemble des foyers.

L'hypothèse selon laquelle le haut paierait plus que ne l'indique le calcul mécanique n'est donc **pas confirmée** :
- la perte des RICI est déjà dans l'IR net par tranche ;
- elle pèse relativement moins en haut qu'au milieu ;
- en haut, les montants moyens par bénéficiaire sont élevés pour le Girardin (14 293 €), le Pinel et apparentés (3 923 €) et l'IR-PME (2 148 €), mais ces dispositifs concernent peu de foyers.

Aucune répartition par décile publiée n'a été trouvée pour les éléments structurels (10 %, quotients, épargne retraite).

## 2. CRDS 2024

### Règles

- **Taux de 0,5 % sur toutes les assiettes** (ordonnance n° 96-50, art. 19, version en vigueur depuis le 1er janvier 2020). Exceptions : jeux, 2,2 % ou 3 % selon art. 18.
- **Revenus d'activité et de remplacement** (art. 14, I). La CRDS est « soumise aux conditions prévues aux articles L. 136-1-1 à L. 136-4 » du CSS, ce qui emporte trois choses :
  - **même assiette que la CSG** ;
  - **abattement de 1,75 % jusqu'à 4 PASS**, soit une assiette de 98,25 %, pour les revenus d'activité salariés et pour les allocations chômage (CSS L136-2, I, 3°, qui renvoie au a du 1° du II de L136-8) ;
  - **mêmes exonérations** pour les revenus de remplacement des personnes sous le seuil de RFR.
- **Pensions soumises à la CSG.** Un retraité soumis à la CSG à 3,8 %, 6,6 % ou 8,3 % paie la CRDS à 0,5 % plein. Un retraité exonéré de CSG est exonéré de CRDS (annexe 2 de l'instruction DSS du 4 décembre 2024 ; CADES).
- **Chômage.** Il est aussi soumis à l'écrêtement : le prélèvement ne peut porter l'allocation nette sous le SMIC (CSS L136-1-2, II, 4°, dernier alinéa).
- **Assiette plus large que la CSG** (art. 14, II) : CRDS sans CSG sur les prestations familiales (sauf l'AEEH), les aides au logement et la prime d'activité. Elle est aussi due sur les ventes de métaux précieux et de bijoux.
- **Patrimoine et placements** : art. 15 et 16, même assiette que la CSG.

### Rendement 2024

Source : CADES, rapport financier annuel 2024, p. 26 à 28 (https://www.cades.fr/pdf/rapportactivite/CADES%20RA%202024.pdf).

| Assiette | M€ (net comptable) |
|---|---|
| Revenus d'activité | 5 833 |
| Revenus de remplacement | 2 216 |
| Patrimoine | 370 |
| Placements | 580 |
| Jeux | 204 |
| Bijoux et métaux | 7,5 |
| **Total** | **9 212** (encaissements notifiés : 9 169) |

Détail des produits :

| Poste | M€ |
|---|---|
| Activité : secteur privé | 3 825 |
| Activité : public | 1 158 |
| Activité : « ETI », lu comme travailleurs indépendants | 649 |
| Activité : agricole | 197 |
| Activité : autres | 34 |
| Remplacement : retraites de base | 1 097 |
| Remplacement : retraites complémentaires | 512 (pensions : 1 609) |
| Remplacement : prestations familiales (sans CSG) | 273 |
| Remplacement : indemnités journalières | 105 |
| Remplacement : chômage | 45 |
| Remplacement : autres | 124 |

La CRDS rapporte 445 M€ de plus que 0,5 point de CSG : prestations familiales 273, jeux 186, bijoux 7.

**Repères pour la réforme.**
- La CRDS assise sur des revenus du champ de la réforme vaut **environ 7,7 Md€** : activité, pensions, chômage, IJ, autres.
- Restent hors champ :
  - prestations familiales (0,27 Md€) ;
  - placements (0,58 Md€) ;
  - jeux et bijoux (0,21 Md€) ;
  - patrimoine (0,37 Md€), en partie hors champ seulement, car le foncier relève de la réforme.

La CRDS sur le chômage (45 M€, soit une assiette d'environ 9 Md€) est faible au regard des allocations versées. C'est cohérent avec la CSG chômage de 0,56 Md€ retenue dans `ir_csg.py` (42 M€ pour 0,45 point, soit environ 0,58 Md€ à 6,2 %). L'explication la plus probable, non chiffrée ici, est l'effet combiné des exonérations sous seuil de RFR et de l'écrêtement au SMIC.

## 3. Paramètres vérifiés sur les textes

### CSG sur les revenus de remplacement (CSS L136-8)

Version en vigueur du 16 décembre 2020 au 1er juillet 2025.
- **Taux.** 8,3 % pour les pensions de retraite et d'invalidité ; 6,2 % pour les allocations chômage (II). Taux réduits de 3,8 % (III) et 6,6 % (III bis), pensions seulement pour ce dernier. Exonération sous le seuil du III.
- **Seuils légaux de base**, revalorisés chaque 1er janvier comme les prix hors tabac de l'avant-dernière année (III ter) : 11 128, 14 548 et 22 580 € pour la première part.
- **Seuils effectifs pour une part, en métropole :**

| Année d'application (RFR retenu) | Exonération si RFR ≤ | 3,8 % jusqu'à | 6,6 % jusqu'à | 8,3 % à partir de | Demi-part supplémentaire |
|---|---|---|---|---|---|
| **2024** (RFR 2022 ; DSS, 23 novembre 2023) | 12 230 € | 15 988 € | 24 812 € | 24 813 € | 3 265, 4 269 et 6 623 € |
| **2025** (RFR 2023 ; DSS, 4 décembre 2024) | 12 817 € | 16 755 € | 26 003 € | 26 004 € | 3 422, 4 474 et 6 941 € |
| 2026 (RFR 2024 ; DSS, 11 décembre 2025) | 13 048 € | 17 057 € | 26 471 € | 26 472 € | 3 484, 4 555 et 7 066 € |

- **Règle des deux années.** Elle ne vise que la **sortie du taux de 3,8 %**, vers 6,6 % ou 8,3 %. On reste à 3,8 % si le RFR de l'avant-dernière année **ou celui de l'antépénultième année** ne dépasse pas le plafond du 3,8 % (L136-8, III, 2° : « perçus l'avant-dernière ou l'antépénultième année sont inférieurs ou égaux à 14 548 € »). Cette règle date de la LFSS 2019.
- **Pas de lissage entre 6,6 % et 8,3 %.** Selon l'annexe 3 des instructions DSS, un RFR N−3 dans la bande du 6,6 % et un RFR N−2 au-dessus du seuil donnent 8,3 % dès l'année N.
- **Les seuils sont appliqués au RFR de l'année N−2.** `ir_csg.py` (`SEUILS_1P`) utilise les seuils 2025 avec le RFR 2024. Les seuils qui correspondent logiquement au RFR 2024 sont ceux de 2026, qui sont 1,8 % plus hauts. L'effet est faible, car le nombre de parts est calé sur la recette CCSS.
- **CASA de 0,3 %** et cotisation maladie de 1 % sur les pensions complémentaires : seulement aux taux de 6,6 % et 8,3 %, pas à 3,8 % (annexe 2 des instructions DSS). Le texte de CASF L14-10-4 n'a pas été relu.
- **Chômage.** CSG à 6,2 %, ou 3,8 %, ou exonération selon les mêmes seuils (L136-1-2, II, 4°). L'assiette est de 98,25 % (L136-2, I, 3°). Écrêtement : « ne peut avoir pour effet de porter leur montant net […] en deçà du montant du salaire minimum de croissance » (L136-1-2, II, 4°, version du 1er juillet 2023 au 28 février 2025).

### IR, revenus 2024

Textes : LF 2025, loi n° 2025-127 du 14 février 2025, art. 2 (+1,8 %), puis décret n° 2025-547 du 17 juin 2025.
- **Barème** (CGI 197) : 0 % jusqu'à 11 497 € ; 11 % jusqu'à 29 315 € ; 30 % jusqu'à 83 823 € ; 41 % jusqu'à 180 294 € ; 45 % au-delà.
- **Plafond du quotient familial** : 1 791 € par demi-part.
- **Décote** : 889 € − 45,25 % de l'impôt pour une personne seule ; 1 470 € − 45,25 % pour un couple.
- **Abattement de 10 % sur les pensions** (CGI 158, 5 a) : au moins **450 € par pensionné**, au plus **4 399 € par foyer**.
- **Déduction de 10 % des salariés** (CGI 83, 3°) : au moins 504 €, au plus **14 426 € par personne**.
- **Abattement des plus de 65 ans et des invalides** (CGI 157 bis, version du 19 juin 2025) : **2 796 €** si le revenu net global ne dépasse pas **17 510 €** ; **1 398 €** entre 17 510 et **28 170 €**. Il est doublé si les deux conjoints remplissent la condition. Pour mémoire, revenus 2023 : 2 746 et 1 373 €, seuils de 17 200 et 27 670 €.
- **Seuil de recouvrement** (CGI 1657, 1 bis) : l'impôt n'est pas mis en recouvrement s'il est « inférieur à 61 € », montant apprécié « avant imputation de tout crédit d'impôt ».

### Non vérifié sur le texte

- PASS 2024, pris à 46 368 € dans les calculs ;
- plafond d'exonération d'IR des heures supplémentaires ;
- CSG sur la PPV ;
- CASF L14-10-4 ;
- coûts du quotient familial et du quotient conjugal (repris du dossier).

## 4. Pourquoi le retraité seul d'OpenFisca paie plus que le salarié seul au même « brut »

Données : `courbes_openfisca.csv`, profils `seul` et `retraite_seul` ; décomposition dans `ecart_retraite_salarie_openfisca.csv`. Le barème recalculé ici reproduit l'IR d'OpenFisca à l'euro près jusqu'à 200 000 €. Au-delà, l'écart vient de la CEHR.

**Où l'écart apparaît.** (IR + CSG) / brut est plus élevé pour le retraité **à partir de 31 000 € de brut** (439 points de grille sur 491).
- Écart à 32 000 € : +0,3 point.
- Écart à 50 000 € : +2,7 points.
- Écart à 100 000 € : +4,5 points.
- Écart entre 150 000 et 300 000 € : +6 points.
- Avec la CASA (0,3 %, hors colonne `csg`), il faut ajouter 0,3 point.

En dessous de 31 000 €, le retraité paie moins. Il bénéficie de :
- l'exonération de CSG, puis des taux de 3,8 % et 6,6 % (seuils 2024 appliqués à son RFR) ;
- l'abattement des plus de 65 ans ;
- la décote.

**Décomposition à 100 000 € de brut.** Écart total de +4 540 €, soit +4,5 points :

| Composante | Effet sur l'écart |
|---|---|
| Cotisations sociales salariales, environ 10,8 % du brut | **+2 937 € d'IR** |
| Plafond de l'abattement de 10 % des pensions (4 399 € par foyer contre 14 426 € par salarié) | **+2 055 € d'IR** |
| CSG déductible plus faible (5,9 % de 100 % contre 6,8 % de 98,25 %) | +288 € d'IR |
| CSG elle-même, moindre (8,3 % sur 100 % = 8,3 % du brut, contre 9,2 % × 98,25 % = 9,04 %) | **−739 €** |
| CASA | +300 € |

Les cotisations salariales sont déduites de l'assiette de l'IR du salarié et ne figurent pas au numérateur IR + CSG. Le retraité n'en a pas, donc son revenu imposable est plus haut : 89 701 € contre 74 258 €.

L'effet du plafond de 4 399 € joue dès que la pension dépasse environ 47 000 €. Il atteint +4 000 à +4 500 € d'IR au-delà de 150 000 €.

**Le facteur principal est donc le dénominateur.** Le « brut » du salarié contient environ 11 % de cotisations salariales contributives, qui ne sont pas un impôt. Le « brut » du retraité n'en contient pas. À revenu égal après cotisations (pension brute = salaire brut − cotisations salariales), l'écart change de sens :

| Revenu après cotisations | Retraité | Salarié |
|---|---|---|
| 26 600 € | 9,3 % | 13,2 % |
| 44 300 € | 18,3 % | 19,7 % |
| 89 200 € | 27,4 % | 27,5 % |
| 134 000 € | 33,6 % | 32,3 % |
| 268 700 € | 41,3 % | 40,7 % |

Le retraité paie donc moins jusqu'à environ 90 000 €, puis un peu plus (+0,5 à +1,3 point) au-delà. Ce reste vient du plafond de l'abattement de 10 %, en partie compensé par la CSG plus faible.

Pour la note, la bonne comparaison se fait sur l'assiette de la réforme : revenu après cotisations, avant CSG, soit `base_a`.
