# Registre des hypothèses et des chiffres : partie « Revenus du capital » (PFU, holdings, apport-cession, CEHR/CDHR)

Contrôle du 16 novembre 2026, avant la réécriture de `synthese/parties/pfu.tex` selon `synthese/CHARTE_NOTE.md`.
Source du tableau d'annexe « Hypothèses fortes et chiffres non vérifiés » de la partie.

- **Recalcul indépendant** : `/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_pfu/verif_pfu.py`,
  sortie `verif_pfu_sortie.txt` dans le même dossier (écrit sans reprendre le code du dépôt).
- **Sources relues** : rapport AN n° 3056 (texte intégral, copie `scratchpad/pfu_an3056/r.txt`) ; PLF 2027, texte et
  évaluation préalable de l'art. 5 (`scratchpad/is_ep_plf2027/ep.txt`, p. 42-47) et état A (`scratchpad/pfu_plf2027/plf.txt`) ;
  CAE Focus 124 et 147 (`scratchpad/litA/`) ; BOFiP CDHR (`scratchpad/pfu_bofip_cdhr/`) ; totaux DGFiP de la 2042
  (`donnees/ir_2042_cases_revenus2024.csv`) ; Insee Première n° 2105 (mai 2026), téléchargée pour ce contrôle
  (`scratchpad/dl_hyp_pfu/insee_ip2105/`).
- **Statuts** : VÉRIFIÉ (source primaire lue, ici ou dans un contrôle antérieur cité) ; SECONDAIRE (rapporté par une
  autre source) ; NON VÉRIFIÉ ; CALCUL (calcul de l'auteur ou de ce contrôle) ; HYPOTHÈSE.
- **Aucun fichier .tex modifié.** Un seul fichier du dépôt modifié : `synthese/perte_seche_autres.py` (bloc PFU, § 5),
  relancé ; sa sortie `synthese/sorties/perte_seche_autres.txt` change dans le seul bloc PFU.

## 0. Ce qui change pour la réécriture

1. **Perte sèche d'un PFU à 25 % : +0,4 Md€ (0,2 à 0,9), pas +0,3 (0,15 à 0,6).** Le script comptait la recette que
   rapporte la réaction des dividendes alors même qu'il supposait que cette réaction n'est qu'un calendrier. Corrigé (§ 5).
2. **Coût d'un PFU à 25 % : 3,3 à 3,9 Md€ les premières années, 3,7 à 5,1 Md€ en régime permanent**, selon que la
   réaction est une sortie définitive de l'optimisation ou un simple déplacement dans le temps. Sur la base de 2025
   plutôt que 2024, tout baisse d'environ 9 % (coût mécanique 4,6 au lieu de 5,1).
3. **L'assiette de 2024 (79,6 Md€) est gonflée par l'anticipation de la CDHR** : dividendes reçus par les ménages
   +13,9 Md€ en 2024 puis −10,5 Md€ en 2025 (Insee, vérifié). C'est aussi la preuve la plus récente et la plus nette
   que les dividendes réagissent au taux *attendu*.
4. **Apport-cession : le stock de 153 / 173 Md€ est un majorant** (note 462 du rapport n° 3056 : la case 8UT contient
   d'autres reports) ; l'évaluation préalable du PLF 2027 l'évalue à **127 Md€ en 2023**. Le calcul de l'auteur
   (153 / 25 × 31,4 %) donne 1,9 Md€, pas « au moins 2 » ; la fourchette défendable est **de l'ordre de 1,5 à 3 Md€
   par an** dans les dix prochaines années, hors réactions. Le 0,5 Md€ de 2027 est désormais vérifié sur l'évaluation
   préalable, et sa propre méthode implique une année pleine de 2 à 3 Md€.
5. **Un PFU à 25 % obtenu en baissant la part d'impôt sur le revenu ne rapporterait rien aux foyers à la CDHR** :
   la CDHR reprend la baisse euro pour euro (rentier à 600 000 € ou 3 M€ : 38,6 % avant comme après). Le « 44 % du gain
   au 1 % » de 2017 ne vaut plus ; tant que la CDHR existe, le gain irait aux foyers sous ses seuils et aux revenus
   mixtes, et la CDHR reprendrait de l'ordre de 0,7 à 1,2 Md€ du coût (ordre de grandeur, § 3, H8).
6. **Rendement de la CDHR 2025 : 370 M€ d'acompte au lieu de 1,9 Md€ prévus** (rapport n° 3056, d'après la DGFiP,
   provisoire) : vérifié, alors que le CSV le marquait NON VÉRIFIÉ.

---

## 1. La méthode en clair

**Taux cumulés.** On suit 100 € de bénéfice avant impôt. La société paie l'IS (25 %, ou 25,825 % si son IS dépasse
763 000 € et qu'elle doit la contribution sociale de 3,3 %). Le reste est soit distribué au foyer, qui paie le PFU
(31,4 %), éventuellement majoré de la CEHR ou porté au plancher de la CDHR, soit versé à une holding, qui ne paie l'IS
que sur une quote-part de 5 % (1,25 % du dividende). Pur calcul sur les taux légaux.

**Assiette du PFU.** Somme des cases de la déclaration 2042 des revenus de 2024 (dividendes 2DC, intérêts 2TR, autres
distributions 2TS, plus-values 3VG, actifs numériques 3AN, moins les moins-values 3VH) : 79,6 Md€. Elle comprend les
revenus des 2,54 millions de foyers qui optent pour le barème, d'où des chiffrages majorants.

**Coût ou rendement d'un changement de taux.** Coût mécanique = écart de taux × assiette. Réaction : l'assiette varie
de e × Δln(1 − t), où e est l'élasticité des revenus du capital au taux net (0,77 chez Lefebvre, Lehmann et Sicsic ;
0,65 au CAE ; 1 en hypothèse haute). Le coût net retranche l'impôt payé, au nouveau taux, sur l'assiette supplémentaire.
La même formule reproduit le chiffrage du CAE (30 → 33 %, 57 Md€, e = 0,65 : 1,16 Md€ recalculé, 1,2 publié).

**Premières années contre régime permanent.** La réaction mesurée en 2013 et 2018 est pour l'essentiel un déplacement
dans le temps : les bénéfices gardés dans les sociétés sont distribués plus tôt ou plus tard. Si le nouveau taux est
permanent, la date de la distribution ne change pas la valeur actualisée de l'impôt : seule la part π de la réaction
qui, sans la réforme, aurait échappé définitivement à l'impôt (purge au décès, holdings jamais vidées) rapporte
durablement. Coût permanent = coût mécanique − π × (nouveau taux × réaction).

**Perte sèche.** Formule de Harberger appliquée au seul volet réel : la part π de la réaction compte comme perte sèche
évitée, au coin moyen ; la recette perdue doit être levée ailleurs, au « prix d'un milliard » μ − 1 (0,04 / 0,08 / 0,17,
perte sèche d'un point de taux pour tous du barème fusionné, `synthese/sorties/architectures_ircsg.txt`, [PRIX]).

**Expiration du report de l'apport-cession à toute transmission.** Recette annuelle ≈ stock de plus-values en report
÷ délai moyen jusqu'à la transmission × taux. L'auteur prend 153 Md€, 25 ans et 31,4 %. Ce contrôle fait varier les
trois et confronte le résultat à la méthode de l'évaluation préalable (moyenne des reports 2022-2024 des plus de 60 ans).

**Alignement des prélèvements sociaux.** L'amendement sans exclusions (1,4 point sur toute l'assiette) était chiffré à
2,8 Md€, le texte voté à 1,5 Md€ : l'écart, 1,3 Md€, est le produit de 1,4 point sur l'assiette restée à 17,2 %.

**Cas types.** Calculs sur les taux légaux pour une personne seule, avec le barème de l'IR des revenus de 2024 (celui
du dépôt) ; voir § 6.

---

## 2. Chiffres clés vérifiés

| Chiffre de la partie actuelle | Recalcul | Statut | Commentaire |
|---|---|---|---|
| IS + PFU : 48,6 % (IS 25 %) ; 49,1 % (25,825 %) | 48,55 ; 49,12 | OK | — |
| Avec CEHR 4 % : 52,1 % ; à la CDHR : 54,5 % | 52,08 ; 54,46 | OK | « Jusqu'à 54,5 % » ne vaut que pour l'IS à 25,825 % : 60,8 % pour les sociétés à 36,125 % (déjà relevé, `verif_is_pfu.md` E8). |
| Holding : 1,25 % ; 26,8 % | 26,75 | OK | 26,0 % en intégration fiscale (quote-part 1 %) ; 25,9 % sans contribution sociale. Taux tant que le bénéfice reste dans la holding (H7). |
| Salaire : 55,4 % hors cotisations | 9,7 + 49 × 0,932 = 55,37 | OK | Comparaison non homogène (H16). |
| 100 € → 68,6 € ; 105 € → 72,0 € | 68,6 ; 72,03 | OK | Mécanisme (nouvelle vue), pas une mesure. |
| Assiette 79,6 Md€ ; IR à 12,8 % ≈ 10,2 Md€ | 79,61 ; 10,19 | OK, majorant | Acompte 2CK 7,67 Md€ ↔ 59,9 Md€ de dividendes et intérêts. Base 2024 gonflée (H6). |
| PFU à 25 % : ≤ 5,1 Md€ mécanique | 5,10 | OK, majorant | Base 2025 : 4,64. |
| PFU à 25 % : 3,2 à 3,9 Md€ après réaction | log : 3,32 / 3,73 / 3,94 ; linéaire : 3,24 / 3,67 / 3,89 (e = 1 / 0,77 / 0,65) | À PRÉCISER | 3,2 vient de l'approximation linéaire, le script de perte sèche donne 3,3. Surtout, c'est le coût **des premières années** ; régime permanent 3,7 à 5,1 selon π (H2). Base 2025 : 3,0 à 3,6. |
| Hausse 31,4 → 33 % : un peu moins des deux tiers | 63 % (e = 0,77) ; 51 à 68 % (e = 1 à 0,65) | OK | Rendement net 0,8 Md€. |
| CAE : 1,2 Md€ nets pour 30 → 33 % | 1,16 (formule CAE) ; 1,17 (log) | OK | Assiette du CAE 57 Md€ ; sur 79,6 Md€, 31,4 → 34,4 % rapporte 1,45 Md€ (1,16 à 1,59). Rendement des premières années (H2). |
| Taux maximisant la recette 57 % sans réponse croisée | 1/(1 + 0,767) = 56,6 % | OK | Cohérence interne : le 57 % est exactement l'élasticité directe. |
| Coût d'un euro levé à 31,4 % : ≈ 1,5 € (revue) | 1,54 (e = 0,77) ; 1,42 à 1,84 | OK | Pas une perte sèche (H2, H3). |
| Perte sèche du PFU à 25 % : +0,3 (0,15 à 0,6) | +0,41 (0,20 à 0,87) si π = 0 | **ERREUR, corrigée** | § 5. Négative dès que π ≥ 0,5. |
| Entrées en report : 33,6 (2023) ; 22,2 Md€ (2024) | 33 636 et 22 172 M€ (tableau DGFiP, AN n° 3056) ; 3WH : 22,17 | OK | — |
| Stock : 153 (2023) ; 173 Md€ (2024) | 152 869 et 173 268 M€ ; 8UT : 173,27 Md€, 117 112 foyers | OK mais **majorant** | Note 462 du rapport : la case 8UT contient d'autres reports. Évaluation préalable du PLF 2027 : **127 Md€ en 2023**. |
| Reports expirés : 0,4 à 1,5 Md€ par an (2022-2024) | 0,635 ; 0,418 ; 1,514 | OK | Évaluation préalable : 0,5 Md€ en 2021. |
| 84 foyers : 23,5 Md€, plus des deux tiers | 70 % | OK (citation) | **Incohérence de sources** : le même rapport donne 18,8 Md€ pour tout le top 0,01 % du RFR en 2023 ; compatible seulement si une partie des 84 foyers n'est pas dans ce top 0,01 % (RFR sans la plus-value mise en report ?). Non résolu. |
| Art. 5 : 0,5 Md€ en 2027 | « 500 M€ (200 M€ au titre de l'IR et 300 M€ au titre des prélèvements sociaux) », EP § 4.2.1, « en tenant compte de l'étalement » | **VÉRIFIÉ** (était SECONDAIRE) | — |
| Art. 5 : au moins 2 Md€ par an en régime de croisière | 153 / 25 × 31,4 % = **1,92** ; grille 1,1 à 3,6 | **À CORRIGER** | « De l'ordre de 2 Md€ (1,5 à 3) », hors réactions (H10, H11). |
| 90 à 100 M€ par gros apporteur | 280 M€ × 30 / 31,4 / 35,4 % = 84 / 88 / 99 M€ | ARRONDI | « 85 à 100 M€ » si les prélèvements sociaux sont ceux de l'année d'apport (17,2 %) (H10). |
| Alignement des prélèvements sociaux : 1,3 Md€ | 1,30 ; contrôle par l'assiette du prélèvement de solidarité (15,3 Md€ / 7,5 % = 204 Md€, PLF 2027 état A l. 1427) : 1,36 | OK, consolidé | Assiettes cohérentes : 200 (amendement), 204 (prélèvement de solidarité 2027), 190 (CRDS 2024). Incidence non vérifiée (H13). |
| CEHR : 1,412 Md€, 96,7 % au top 0,1 % | Texte du rapport n° 3056 (DLF), revenus de 2023 | VÉRIFIÉ (source parlementaire) | Part payée sur les revenus du capital inconnue (H14). |
| CDHR : 0,6 Md€ en 2027 | PLF 2027, état A, l. 1440 : 600 000 000 € | VÉRIFIÉ | — |
| CDHR : taux effectif 18,9 % | Rapport n° 3056 (rec. 15-16) | VÉRIFIÉ (source parlementaire) | Taux personnel effectif d'un rentier à la CDHR ≈ 37,5 % plutôt que 38,6 %. |
| Exil : 0,02 à 0,23 % du top 1 % par point | CAE Focus 118 | VÉRIFIÉ (contrôle antérieur) | Effet sur le PFU à 25 % : 0,02 à 0,25 Md€ de recette gardée à long terme, au plus (§ 3, H12). |
| 2,5 millions d'optants | 2OP : 2 540 106 | OK | — |

**Ordres de grandeur.** Aucun chiffre absurde. Repères : IR au PFU ≈ 10 Md€ (majorant) ; prélèvements sociaux sur
l'assiette du PFU ≈ 14,8 Md€ ; sur tout le capital ≈ 37 Md€ (204 Md€, dont 107 à 18,6 % et 97 à 17,2 %) ; CEHR 1,4 ;
CDHR 0,4 à 0,6 ; reports d'apport-cession expirés 0,4 à 1,5 Md€ de plus-values par an, pour 22 à 34 Md€ d'entrées.
Un PFU à 25 % coûterait ainsi un tiers à la moitié de l'IR au PFU, et l'expiration à toute transmission rapporterait,
en régime de croisière, à peu près autant que la CEHR.

---

## 3. Hypothèses fortes

| # | Hypothèse | Où elle joue | Ce qu'elle change si elle est fausse | Appui |
|---|---|---|---|---|
| H1 | **Élasticité e = 0,77 (0,65 à 1)**, appliquée à toute l'assiette (dividendes, intérêts, plus-values) | Coût du PFU à 25 % ; rendement d'une hausse ; taux maximisant la recette ; coût d'un euro levé | e = 0,5 : coût premières années 4,2 Md€ ; e = 1,2 : 3,0. Mesurée sur des foyers qui ont aussi des revenus d'activité (rentiers exclus), surtout sur la réforme de 2013 ; variantes de 0,22 à 1,17 dans l'étude. Les intérêts réagissent sans doute moins. | Lefebvre, Lehmann et Sicsic (IZA DP 16112, vérifié) ; CAE 0,65 |
| H2 | **La réaction des dividendes est surtout un calendrier** (part π qui échappe définitivement à l'impôt faible) | Coût permanent d'une baisse (3,7 à 5,1) ; perte sèche (signe) ; rendement durable d'une hausse | Si π = 0 : coût permanent 5,1, perte sèche +0,4 ; une **hausse** rapporterait à long terme presque son rendement mécanique (2,4 Md€ pour 3 points), ce qui affaiblit « une hausse rapporterait peu ». Si π = 1 : coût 3,7 et la baisse **réduirait** la perte sèche (−1,2). π n'est mesuré nulle part. | IPP n° 46 (« optimisation fiscale ») ; 2013-2018 un seul épisode ; 2024-2025 (H5) |
| H3 | **Aucune réaction réelle** (investissement, salaires, activité) | Perte sèche du PFU limitée au coût du financement ; « ne rapporterait rien en activité » | Une réaction réelle donnerait un gain d'activité à la baisse. Seul effet réel trouvé : créations d'entreprises un peu plus rapides après 2018, inséparables de la baisse de l'IS. | IPP n° 46 ; France Stratégie 2023 ; Yagan 2015 (vérifiés) ; IPP n° 47 (secondaire) |
| H4 | **Prix d'un milliard μ − 1 = 0,04 / 0,08 / 0,17** | Perte sèche de la recette à lever ailleurs | Repris du modèle IR-CSG (élasticités du revenu réel 0,05 à 0,25) ; proportionnel : doubler μ − 1 double la perte sèche du financement. | `revue/methode_v2.md` |
| H5 | **La réaction dépend du taux attendu** : stabilité du taux = principal service | Argument central de la partie (« ne plus le changer ») | Si la réaction tenait au taux permanent, un PFU stable garderait une assiette durablement plus faible à taux élevé (coût de la stabilité). L'anticipation est désormais **documentée** : dividendes reçus par les ménages +13,9 Md€ en 2024, « possiblement par anticipation » de la CDHR, −10,5 Md€ en 2025 (Insee) ; dividendes de décembre 2024 +138 % (DGFiP) ; acompte CDHR 0,37 au lieu de 1,9 Md€. Bach et al. ne la jugent que « suggérée » pour 2013. | Insee IP 2105 (vérifié) ; rapport n° 3056 |
| H6 | **L'année 2024 est représentative** (assiette 79,6 Md€) | Tous les chiffrages du PFU | Elle ne l'est pas : avec des dividendes 2025 inférieurs de 14 %, assiette ≈ 72,5 Md€ ; PFU à 25 % : 4,6 mécanique, 3,0 à 3,6 après réaction ; hausse et alignement à réduire d'autant. Le rapport des 2042 au compte national n'est pas fait. | Calcul ; Insee ; rapport n° 3056 (61,0 → 74,9 → 64,3 Md€) |
| H7 | **Le bénéfice gardé en holding sera un jour distribué** (26,8 % = report, pas taux final) | « C'est un report, pas un taux final » ; argument contre l'impôt de 25 % sur les holdings | Si les héritiers ne distribuent jamais (pacte Dutreil, holding transmise, purge des plus-values sur les titres de la holding au décès), 26,8 % est un taux final pour cette part : c'est le constat de régressivité de l'IPP (26 % pour les 0,0002 %). Aucune donnée ne dit quelle part finit distribuée. | Hypothèse ; IPP n° 92 (secondaire) |
| H8 | **Composante du PFU baissée et CDHR** : le chiffrage traite le PFU comme un taux unique | Coût et bénéficiaires du PFU à 25 % ; « 44 % du gain au 1 % » | Baisser la part IR (12,8 → 6,4 %) : la CDHR reprend toute la baisse pour ses redevables (cas types § 6) ; reprise de l'ordre de 0,7 à 1,2 Md€ si ses redevables étaient des rentiers purs (2 × le rendement de la CDHR) ; coût net plutôt 2 à 3 Md€ tant qu'elle dure, gain concentré sous les seuils de 250 / 500 k€. Baisser les prélèvements sociaux : pas de reprise, mais la sécurité sociale perd la recette. Le CAE (Focus 147) signale le même biais pour le chiffrage d'un retour au barème. Base des redevables de la CDHR non publiée. | Calcul (ordre de grandeur) ; BOFiP CDHR ; CAE 147 |
| H9 | **Les optants pour le barème** n'ont pas été retirés de l'assiette | 5,1 Md€ « au plus » | Ampleur inconnue ; vraisemblablement des foyers modestes à petits montants, donc quelques % de l'assiette. | Hypothèse |
| H10 | **Apport-cession : stock, délai, taux, comportements** — 153 Md€, transmis en 25 ans, imposés à 31,4 %, sans réaction | « Au moins 2 Md€ par an » ; « 90 à 100 M€ » | Stock : 127 Md€ (EP) → 1,6 Md€. Délai : 15 ans → 2,5 à 3,2 ; 35 ans → 1,1 à 1,4 (stock de 127 ou 153 Md€). Taux : l'IR est celui de l'année d'apport (12,8 % depuis 2018, barème avec abattements pour 2013-2017, BOFiP) et les prélèvements sociaux sont peut-être ceux de l'année d'apport (17,2 %, non tranché) → 30 % plutôt que 31,4 %. Les cases 3WG (6,5 Md€ « après abattement », 4 498 foyers) et 3WH (22,2 Md€ avant abattement) suggèrent des abattements importants sur une partie des entrées (non résolu). Réactions non chiffrées : donations avancées avant le 1er octobre 2026, moins d'apports une fois la purge supprimée, départs (l'exit tax est adaptée par l'art. 5, f bis). Étalement : 41 % de l'impôt (la part IR) payable sur cinq ans. À très long terme, si les entrées restaient à 25 Md€ par an et étaient toutes transmises, 7 à 8 Md€ par an : borne, pas prévision. | Rapport n° 3056 ; EP PLF 2027 ; BOFiP BOI-RPPM-PVBMI-30-20-20191220 (lu par résumé) |
| H11 | **Lecture du 0,5 Md€ de l'évaluation préalable** | Recoupement du régime de croisière | Trois lectures : 1/5 d'une année pleine (étalement appliqué à tout) → 2,5 Md€ et 8 Md€ de plus-values transmises par an ; un trimestre de transmissions (octobre-décembre 2026) sans étalement → 2,0 ; un trimestre avec étalement de la seule part IR (texte de l'art. 1681 G) → 3,0, mais partage IR/PS 60/440, incompatible avec 200/300. Les deux premières concordent avec 2 à 2,5 Md€. L'EP elle-même parle d'« ordre de grandeur ». | EP PLF 2027 § 4.2.1 et 4.3 (vérifié) ; calcul |
| H12 | **Exil faible** | PFU à 25 % ; hausse ; art. 5 | Mesuré pour le top 1 % des revenus du capital : la baisse de 6,4 points garderait 0,13 à 1,5 % de ce groupe, soit 0,02 à 0,25 Md€ de recette (hypothèse : 66 Md€ d'assiette au top 1 %). Rien pour le top 0,01 %, qui porte l'essentiel de l'art. 5. | CAE Focus 118 (vérifié) ; calcul |
| H13 | **Alignement des prélèvements sociaux** : les deux chiffrages LFSS ne diffèrent que par les exclusions ; « payé surtout par la classe moyenne épargnante » | 1,3 Md€ ; qui paie | Le montant est consolidé par l'assiette du prélèvement de solidarité. L'incidence ne l'est pas : l'assiette restée à 17,2 % est faite surtout de revenus fonciers (≈ 41 Md€ bruts) et d'assurance-vie, détenus d'abord par les déciles supérieurs et les retraités. « Classe moyenne épargnante » est à démontrer ou à retirer. Petit épargnant type : +21 € par an sur 60 000 € d'assurance-vie. | LCP, La finance pour tous (secondaires) ; PLF 2027 état A |
| H14 | **CEHR gardée en majoration du PFU « maintient le taux actuel »** | Coordination avec l'impôt fusionné | Vrai si le seuil reste apprécié sur le revenu total ; s'il ne portait que sur les revenus du capital, la majoration baisserait pour les revenus mixtes. La part de la CEHR payée sur le capital est inconnue (hypothèse de 50 à 80 % → 0,7 à 1,1 Md€). Tant que la CDHR existe, un rentier n'y gagne rien de toute façon. | Rapport n° 3056 ; calcul |
| H15 | **Transmission du report aux héritiers sans effacement** : « rapporte moins et plus tard » | Proposition retenue | Non chiffré : dépend du rythme de vente des titres de la holding par les héritiers, inconnu. Si les holdings familiales ne sont jamais cédées, la recette est nulle. Solidité juridique non expertisée (l'EP écarte une option proche : « imposer à l'héritier les mêmes conditions de maintien du report que celles en vigueur pour la donation »). | EP PLF 2027 § 2.1-2.2 |
| H16 | **Comparaison bénéfice distribué (49,1 %) / salaire (55,4 % hors cotisations)** | « Proche du taux marginal supérieur sur un salaire » | Les 100 € de bénéfice avant IS correspondent à un coût du travail, cotisations patronales comprises ; avec les cotisations sans contrepartie au-delà des plafonds, le taux sur le salaire serait nettement plus élevé (non calculé ici, taux non revérifiés). La conclusion « l'intégration fonctionne pour le bénéfice distribué » est donc favorable au capital. | Calcul ; à faire avec les taux vérifiés |
| H17 | **Taux de 2013 jugé provisoire** | Lecture de 2013 | « Suggérée » seulement par Bach et al. ; explication alternative sans anticipation dans le même texte. | Vérifié (contrôle antérieur) |

---

## 4. Chiffres non vérifiés sur source primaire, ou vérifiés ici

| Chiffre | Statut avant | Statut après ce contrôle | Source |
|---|---|---|---|
| Art. 5 : 0,5 Md€ en 2027 (200 IR + 300 PS) | SECONDAIRE | **VÉRIFIÉ** | EP PLF 2027, § 4.2.1, p. 46 ; méthode § 4.3, p. 46-47 |
| Stock de plus-values en report | SECONDAIRE (153) | **VÉRIFIÉ, avec deux valeurs** : 152,9 Md€ (8UT, majorant) et 127 Md€ (EP) pour 2023 ; 173,3 (8UT) pour 2024 | AN n° 3056, tableau et note 462 ; EP § 1.1 ; 2042 (8UT) |
| Entrées 2021 et 2022 ; expirés 2021 | — | VÉRIFIÉ : 16 et 18 Md€ ; 0,5 Md€ | EP § 1.1 (concorde avec le tableau AN) |
| CDHR 2025 : « 0,4 au lieu de 1,9 Md€ » | NON VÉRIFIÉ (titre de presse) | **VÉRIFIÉ (source parlementaire, chiffre DGFiP provisoire)** : rendement prévu 2 Md€ dont 1,9 d'acompte ; acompte constaté 370 M€ (−81 %) | AN n° 3056, p. du § sur la CDHR (ligne 4364 de la copie) |
| Dividendes reçus par les ménages 61,0 / 74,9 / 64,3 Md€ (2023-2025) | — | **VÉRIFIÉ en variation** (+13,9 Md€ en 2024, −10,5 en 2025) ; niveaux cités par le rapport n° 3056 | Insee Première n° 2105, mai 2026 |
| Revenus de capitaux mobiliers +32 % en 2024 ; décembre +138 % | — | SECONDAIRE (DGFiP citée par le rapport n° 3056) | AN n° 3056 |
| CEHR 1,412 Md€ ; 96,7 % au top 0,1 % | SECONDAIRE | VÉRIFIÉ dans le texte du rapport (donnée DLF) | AN n° 3056 |
| Quote-part mère-fille : gain de 1,7 Md€ ; intégration 1 % | SECONDAIRE | VÉRIFIÉ dans le texte du rapport | AN n° 3056 |
| CSG déductible 6,8 % en cas d'option (2026) | NON VÉRIFIÉ | SECONDAIRE : fraction déductible inchangée, la hausse de 1,4 point n'est pas déductible | Recherche web (Weblex, Que Choisir, cabinets) ; texte non lu |
| Taux appliqué à la plus-value d'apport à l'expiration du report | — | PARTIEL : IR de l'année d'apport (12,8 % depuis 2018 ; barème et abattements pour 2013-2017) ; prélèvements sociaux non tranchés | BOFiP BOI-RPPM-PVBMI-30-20-20191220 § 190-280, lu par résumé automatique ; Cons. const. 2016-538 QPC cité |
| CAE : 1,2 Md€ (30 → 33 %, 57 Md€, e = 0,65) ; 0,6 Md€ (31,5 → 33 %, part IR) ; Montaigne 3,2-3,6 et −0,7 | TEXTE LU | VÉRIFIÉ et reproduit (1,16) ; le CAE 2026 qualifie lui-même le 3,2 de majorant (CDHR ignorée) | Focus 124, encadré 4 ; Focus 147, annexe |
| Rendement de l'alignement des prélèvements sociaux (1,3 Md€) | CALCUL fragile | CALCUL consolidé (assiette 204 Md€ du prélèvement de solidarité 2027) ; sources LCP non primaires | PLF 2027 état A l. 1427 |
| 84 foyers, 23,5 Md€ ; 8 400 bénéficiaires, 700 000 € de revenu moyen | SECONDAIRE (CPO via AN) | SECONDAIRE ; incohérence avec le top 0,01 % du tableau DGFiP (18,8 Md€) non résolue | AN n° 3056 ; rapport du CPO inaccessible |
| Holdings : 85-90 % des foyers tout en haut ; taux de 26,2 % pour les 0,0002 % | SECONDAIRE | inchangé (note IPP n° 92 non téléchargée) | IPP via AN n° 3056 |
| OCDE 49 % à cinq salaires moyens | SECONDAIRE | inchangé (oecd.org inaccessible) | France Stratégie 2023 |
| Gouvernement 2017 : 44 % du gain au 1 % | VÉRIFIÉ | Vérifié mais **périmé** (CDHR, PFU à 31,4 %) | Communication Éblé |
| Taux de l'IS réduit (15 % jusqu'à 42 500 €) dans le cas du dirigeant | — | NON REVÉRIFIÉ ici | Droit courant ; à reprendre de la partie IS |
| Barème de l'IR pour les cas types | — | Barème des revenus de 2024 (OpenFisca, `ir_csg/exercices.py`) ; indexation 2026 non reprise | — |
| RFR comprenant les dividendes avant abattement de 40 % (CEHR, CDHR en cas d'option) | — | NON VÉRIFIÉ (hypothèse des cas types au barème) | art. 1417 du CGI non relu |
| Sort de l'art. 5 au Sénat | — | NON VÉRIFIÉ (examen à partir du 20 novembre) | — |

---

## 5. Erreurs corrigées

**E1. `synthese/perte_seche_autres.py`, fonction `pfu` : recette perdue indépendante de π (corrigée, relancée).**

- *Problème.* π est défini comme la part de la réaction qui échappe définitivement à l'impôt ; la part 1 − π est donc
  un calendrier, qui ne rapporte rien durablement quand le taux est permanent. Le script comptait pourtant toute la
  réaction comme recette (recette perdue 3,7 Md€ pour e = 0,77), même pour π = 0. Le texte de la partie raisonne
  d'ailleurs dans le bon sens (« si une partie était une évasion définitive que la baisse ferait cesser, la recette
  perdue serait moindre ») ; le script le contredisait.
- *Correction.* Recette perdue en régime permanent = (t0 − t1)·B − π·t1·ΔQ ; celle des premières années (toute la
  réaction comptée, rattrapage compris) est imprimée à part entre crochets. Le bloc foncier et IS du même script n'est
  pas touché (un autre agent l'a modifié en parallèle ; sa modification est conservée).
- *Ce qui change* (e = 0,77, μ − 1 = 0,04 / 0,08 / 0,17) :

  | π | Recette perdue | Perte sèche avant | Perte sèche après |
  |---|---|---|---|
  | 0 | 3,7 → **5,1** Md€ | +0,15 / +0,30 / +0,63 | **+0,20 / +0,41 / +0,87** |
  | 0,5 | 3,7 → **4,4** | −0,62 / −0,47 / −0,14 | **−0,59 / −0,42 / −0,02** |
  | 1 | 3,7 (inchangé) | −1,39 / −1,24 / −0,91 | inchangé |

  Le chiffre de la partie, « environ +0,3 Md€ de perte sèche (0,15 à 0,6) », devient **« environ +0,4 Md€ (0,2 à 0,9)
  si la réaction n'est qu'un report »**, avec la mention que le signe s'inverse si la moitié au moins de la réaction
  était une sortie définitive de l'optimisation. À reporter aussi dans `revue/methode_v2.md` § 4 (« +0,3 Md€ (0,15 à
  0,6) »), non modifié ici.

**Erreurs et imprécisions du texte, à corriger à la réécriture (pfu.tex non modifié) :**

- E2. « Au moins 2 Md€ par an » : le calcul de l'auteur donne 1,92 sur un stock majorant ; écrire « de l'ordre de
  2 Md€ par an (1,5 à 3), hors réactions », et citer le stock de 127 Md€ de l'évaluation préalable à côté de 153 / 173.
- E3. « 3,2 à 3,9 Md€ après réaction » : écrire « 3,3 à 3,9 Md€ les premières années ; 3,7 à 5,1 ensuite »
  (cohérence avec le script) et dire que l'assiette de 2024 est gonflée.
- E4. « 90 à 100 M€ chacun » : « 85 à 100 M€ ».
- E5. « Le gain irait d'abord au centile le plus aisé (44 %…) » : chiffre de 2017 ; préciser la composante baissée et
  l'effet de la CDHR (H8).
- E6. « Payés surtout par la classe moyenne épargnante » (alignement des prélèvements sociaux) : non démontré (H13).
- Rappels de `verif_is_pfu.md` encore valables : « jusqu'à 54,5 % » (60,8 % pour les sociétés à 36,1 %) ; les
  « environ 450 » entreprises sont tous les redevables de la contribution exceptionnelle, pas ceux au-delà de 3 Md€.

---

## 6. Calculs manquants pour la nouvelle architecture, et faisabilité

Premiers résultats dans `verif_pfu_sortie.txt` (§ 9 et 10). « Faisable » : avec les données du dépôt ou des sources
déjà lues ; « partiel » : ordre de grandeur sous hypothèses ; « non » : il faut des données non publiées (POTE).

| Bloc de la charte | Calcul | Faisable ? | Ce qu'il faut / ce qu'on a |
|---|---|---|---|
| 1. Situation actuelle | Recette : IR au PFU ≈ 10 Md€ (majorant) ; prélèvements sociaux 14,8 sur l'assiette du PFU, ≈ 37 sur tout le capital ; CEHR 1,4 ; CDHR 0,4-0,6 | Oui | Graphique de décomposition ; dire 2024 contre 2025 |
| | Assiette par nature (dividendes 50, intérêts 10, plus-values 19, apport-cession 22 en report) | Oui | Cases 2042 |
| | Qui paie : concentration (96 / 62 / 33 % des dividendes aux top 1 / 0,1 / 0,01 %, 2021 ; 70 % des plus-values au top 0,01 %) | Oui (parts) | France Stratégie 2023 |
| | Qui paie par décile de niveau de vie | Non | POTE ou Ines ; seul l'Insee (2021) répartit le *gain* de 2018 (80 % aux 15 % les plus aisés) |
| | Série des dividendes 2012-2025 (2013, 2018, 2024-2025) : la réaction au taux attendu en une figure | Oui | Série Insee des dividendes reçus par les ménages (à télécharger sur insee.fr, accessible) |
| | Taux comparés en Europe : personnel (Tax Foundation : France 34 % en 2025, 6e sur 35 ; 35,4 % en 2026) ; intégré recalculé avec l'IS à 25,8 % (51,0 % en 2025 avec la CEHR, 52,1 % en 2026, contre 39,2 % en moyenne européenne en 2025) | Oui | `donnees/dividendes_taux_combine.csv` porte la France à 57,85 % avec l'IS à 36,1 % : à recalculer |
| 3. Réforme naïve | Changer le taux : coût / rendement selon e, π, base 2024 ou 2025 (fait, § 2) | Oui | — |
| | Par composante (IR ou prélèvements sociaux) et effet de la CDHR | Partiel | Cas types faits ; agrégat de reprise par la CDHR = ordre de grandeur (0,7-1,2 Md€) faute de l'assiette de ses redevables |
| | Retour au barème : rendement statique | Partiel | Ordre de grandeur grossier **jusqu'à ≈ 12 Md€** sur la base 2024 (hypothèses : dividendes du top 1 % au TMI de 45 %, plus-values sans abattement), contre 3,2-3,6 Md€ chez Montaigne / CAE (actualisation du coût ex ante de 2018, que le CAE qualifie de majorant) et −0,7 si l'assiette revient à son niveau de 2017. Après réaction (e = 0,65 à 1) : 3 à 6 Md€ ; avec la baisse de 40 % des dividendes de 2013 : ≈ 4. L'écart entre ces chiffres est le message : le rendement d'un retour au barème dépend presque entièrement de la réaction. Un chiffrage propre exige POTE (TMI et ancienneté des titres, d'où les abattements). |
| | À qui : cas types | Oui (faits, ci-dessous) | — |
| 4. Proposition contre aujourd'hui | Taux inchangé ; CEHR en majoration du PFU ; report transmis aux héritiers ; prélèvements sociaux alignés ou non | Partiel | Cas types : oui. Recette du report transmis : non (rythme de vente des héritiers inconnu, H15) ; scénario possible (par ex. 2 à 5 % du stock transmis vendu chaque année) |
| 5. Arbitrages | Taux (25 / 31,4 / 33 %) | Oui | — |
| | Apport-cession, trois traitements | Partiel | Expiration à toute transmission : 1,5 à 3 Md€/an (fait). Expiration quand la holding vend : non chiffrable (fréquence des cessions par les holdings inconnue). Report transmis : scénario seulement. Cas type de l'entrepreneur : fait |
| | CEHR gardée ou non sur le capital | Partiel | Part de la CEHR payée sur le capital inconnue (DGFiP) ; cas types : oui |
| | Alignement des prélèvements sociaux | Oui (montant) ; partiel (qui paie) | Détention d'assurance-vie et de revenus fonciers par décile : enquête Patrimoine de l'Insee, non présente dans le dépôt |
| 6. Transition | Profil de recette de l'art. 5 avec étalement de la part IR sur cinq ans ; facture par gros apporteur (85-100 M€) ; application aux transmissions depuis le 1er octobre 2026, sur un stock d'apports faits sous l'ancienne règle | Partiel | Profil : scénario faisable. Constitutionnalité du traitement du stock et du report transmis : non expertisée |

**Cas types (premier calcul ; personne seule ; barème des revenus de 2024 ; droit 2026) — impôt sur les revenus du
capital seulement :**

| Cas | Aujourd'hui | PFU à 25 % (part IR à 6,4 %) | Retour au barème | Remarque |
|---|---|---|---|---|
| Petit épargnant : pension imposable 22 000 €, 800 € de dividendes, 300 € d'intérêts | 282 € (25,7 %, option pour le barème) ; PFU 345 € | 275 € | 282 € | Le PFU ne le concerne guère ; l'alignement des prélèvements sociaux lui coûterait 21 € par an sur 60 000 € d'assurance-vie |
| Cadre : 95 000 € nets imposables, 6 000 € de dividendes, 4 000 € de plus-values | 3 140 € (31,4 %) | 2 500 € (−640) | 4 697 € (47,0 %, +1 557) | C'est lui qu'un retour au barème frappe le plus, en points |
| Dirigeant de PME : bénéfice de 400 000 € | Tout distribué : 197 100 € d'IS et d'impôt personnel (49,3 %, dont 4 185 € de CDHR) ; gardé en holding : 99 550 € (24,9 %) | — | — | L'écart de 24 points est le cœur du problème des holdings |
| Entrepreneur qui cède (plus-value 7,5 M€) | Cession directe : 2,35 M€ (2,65 avec CEHR) ; apport-cession : 0, purgé au décès | — | — | Art. 5 : 2,35 M€ à la transmission (IR de 0,96 M€ étalable) ; report transmis : 0 tant que les héritiers ne vendent pas |
| Rentier : 400 000 € de dividendes | 154 400 € (38,6 %, CDHR) | 154 400 € (inchangé) | 154 400 € (la CDHR joue encore) | — |
| Rentier : 3 M€ de dividendes | 1,158 M€ (38,6 %) | 1,158 M€ (inchangé) | 1,360 M€ (45,3 %) | PFU à 25 % par les prélèvements sociaux : 32,2 % |

Hypothèses des cas types à signaler : barème non indexé pour 2026 ; CSG déductible de 6,8 % (secondaire) ; RFR avec
dividendes bruts (non vérifié) ; IS à 15 % jusqu'à 42 500 € (non revérifié) ; holding imposée à 25 % sur la quote-part ;
pas de quotient ni de lissage de la CEHR pour revenus exceptionnels.

---

## Sources consultées pour ce contrôle

- Assemblée nationale, rapport n° 3056 (commission d'enquête, 8 juillet 2026), texte intégral (copie locale).
- PLF 2027, texte de l'art. 5, évaluation préalable (p. 42-47) et état A (copies locales).
- CAE, Focus n° 124 (encadré 4 et annexe) et n° 147 (annexe), copies locales.
- Insee Première n° 2105, « Les comptes de la Nation en 2025 » (mai 2026) :
  https://www.insee.fr/fr/statistiques/fichier/version-html/8996855/IP2105.pdf
- BOFiP BOI-RPPM-PVBMI-30-20-20191220 (lu par résumé automatique) :
  https://bofip.impots.gouv.fr/bofip/3623-PGP.html/identifiant=BOI-RPPM-PVBMI-30-20-20191220
- BOFiP BOI-IR-CDHR-10-20260630 (copie locale).
- Recherche web sur la CSG déductible en 2026 (résumés : weblex.fr, quechoisir.org, legalplace.fr), source secondaire.
- Totaux DGFiP de la déclaration 2042, revenus 2024 (`donnees/ir_2042_cases_revenus2024.csv`).
