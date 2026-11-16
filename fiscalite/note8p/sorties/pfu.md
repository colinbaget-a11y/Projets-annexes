# Bloc « fiscalité du capital » : compte rendu pour l'assembleur

Chiffres : `note8p/calculs/pfu_transmission.py` → `sorties/pfu.json` (table `annuel` 2027-2040, `cout_par_point`) et
`sorties/pfu_calculs.txt`. Ce script lit `pfu/sorties/calculs_pfu.json` et copie les jeux d'hypothèses de
`pfu/calculs_pfu.py`, sans rien modifier dans `pfu/`. Figure : `figures/g9_exemple_pv`. Annexe :
`annexes/annexe_pfu.tex`. Unités : Md€ au niveau du PIB de 2025, sans croissance (même convention que l'ancienne note
fusionnée). Signe + : recette en plus par rapport au droit de 2026.

## 1. Choix faits

1. **PFU maintenu à 31,4 %** [C] : 12,8 % d'IR et 18,6 % de prélèvements sociaux, après la hausse de 1,4 point de
   la CSG du capital votée en LFSS 2026 (art. 12) [V]. **Un point de PFU vaut 0,67 Md€ à comportements inchangés**,
   sur l'assiette des revenus de 2025 (67,0 Md€). Il vaut 0,44 Md€ les premières années une fois les dividendes
   ajustés (e = 0,77 ; 0,38 à 0,48), et 0,44 à 0,67 Md€ en régime permanent [S]. Une baisse par la part d'IR serait
   reprise par la CDHR à hauteur de 0,10 à 0,17 Md€ par point, tant que celle-ci existe. Une baisse à 25 % coûterait
   4,3 Md€ à comportements inchangés et 3,1 Md€ les premières années.
2. **Fin de l'effacement de la plus-value à la donation et au décès** [C]. Le donataire ou l'héritier reprend le
   prix d'acquisition historique. Rien n'est dû à la transmission : l'impôt n'est payé que si le bénéficiaire vend.
   Les droits de mutation afférents à la plus-value latente (droits × plus-value / valeur) s'ajoutent au prix repris.
   C'est la règle américaine des donations, 26 U.S.C. § 1015(d)(6) [V]. Le report d'apport-cession (art. 150-0 B
   ter) passe au bénéficiaire sans s'effacer. Le champ couvre les valeurs mobilières et droits sociaux de
   l'art. 150-0 A : ni l'immobilier, ni l'assurance-vie, ni le PEA.
3. **Plus-values acquises avant l'annonce : option 1 retenue** [C]. L'héritier reprend le prix historique pour tous
   les titres. La règle s'applique aux transmissions faites à partir du jour de l'annonce (au plus tard le
   1er janvier 2027).
4. **CEHR et CDHR sur le capital** : le chiffrage porte sur leur maintien (0 dans la table). Leur sort relève du bloc
   IR-CSG (voir le § 6).

## 2. L'exemple : titres acquis 100 000 €, valant 1 000 000 €, un enfant (droit de 2026)

Calcul hors CEHR et CDHR l'année de la vente, qui peuvent s'y ajouter. Figure g9. Proposition de titre : « Transmettre
efface aujourd'hui la moitié de l'impôt ; avec la réforme, l'héritier paie à peu près ce qu'aurait payé le parent en
vendant ».

| Situation | Impôt sur la plus-value | Droits de succession | Total |
|---|---|---|---|
| Il vend (PFU 31,4 % sur 900 000 €), puis transmet le produit | 282 600 € | 128 182 € | **410 782 €** (41 %) |
| Même vente par un dirigeant de PME partant à la retraite (abattement de 500 000 € sur la seule part d'IR, art. 150-0 D ter, prorogé jusqu'au 31/12/2031 [S]) | 218 600 € | 147 382 € | 365 982 € |
| Il transmet aujourd'hui : droits sur 1 M€, plus-value effacée, l'héritier revend sans impôt | 0 | 212 962 € | **212 962 €** (21 %) |
| Réforme sans correction : l'héritier reprend 100 000 € | 282 600 € | 212 962 € | 495 562 € |
| **Réforme retenue** : 191 666 € de droits ajoutés au prix repris | 222 417 € | 212 962 € | **435 379 €** (44 %) |
| Variante exactement neutre, non retenue : impôt latent déduit de l'assiette des droits | 282 600 € | 128 182 € | 410 782 € |
| Titres sous pacte Dutreil (75 % exonérés), aujourd'hui | 0 | 28 194 € | 28 194 € (3 %) |
| Titres sous pacte Dutreil, réforme | 274 632 € | 28 194 € | 302 827 € (30 %) |

Lecture : aujourd'hui, transmettre plutôt que vendre fait économiser 198 000 €. Avec la réforme, l'héritier paie
24 600 € de plus que si son parent avait vendu. Ce reste de double imposition vient de ce que la correction utilise
le taux moyen des droits (21 %) et non leur taux marginal (30 %). Nous l'acceptons pour trois raisons. La correction
se calcule à partir de la seule déclaration de succession. Elle ne coûte rien tant que l'héritier ne vend pas. Elle a
un précédent étranger appliqué depuis 1976. La variante neutre, elle, réduit les droits dès le décès (0,7 à 3 Md€ par
an, chiffrage de pfu/), même si les titres ne sont jamais vendus. **C'est une hausse effective de l'impôt sur les
patrimoines transmis**, très forte pour les entreprises sous pacte Dutreil (de 3 % à 30 %), qui reste inférieure à la
charge d'un parent qui vend de son vivant (41 %).

## 3. Recettes de la fin de l'effacement, 2027-2040 (Md€ au niveau du PIB de 2025) [S sur hypothèses H]

| | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bas | 0 | 0,21 | 0,47 | 0,53 | 0,58 | 0,63 | 0,68 | 0,73 | 0,77 | 0,82 | 0,87 | 0,91 | 0,95 | 1,00 |
| **Central** | 0 | **0,86** | **1,91** | 2,10 | 2,29 | 2,47 | 2,64 | 2,80 | 2,96 | 3,11 | 3,26 | 3,40 | 3,53 | **3,66** |
| Haut | 0 | 2,56 | 5,65 | 6,15 | 6,62 | 7,06 | 7,47 | 7,86 | 8,22 | 8,57 | 8,89 | 9,19 | 9,48 | 9,74 |
| Option 2 (jour V), central | 0 | 0,13 | 0,38 | 0,56 | 0,74 | 0,92 | 1,10 | 1,28 | 1,47 | 1,65 | 1,84 | 2,02 | 2,20 | 2,39 |
| dont reports d'apport-cession, central | 0 | 0,08 | 0,21 | 0,27 | 0,32 | 0,37 | 0,41 | 0,46 | 0,50 | 0,55 | 0,59 | 0,62 | 0,66 | 0,70 |

- **Rien en 2027** : les plus-values mobilières n'ont pas de prélèvement à la source et se paient au solde de l'IR de
  l'année suivant la vente [S]. Les héritiers vendent 30 % des titres dans l'année (central), puis 4 % par an.
- Cumul 2027-2040 : 35 Md€ au centre (9 à 97). Le régime de croisière, quand toutes les cohortes ont fini de vendre,
  s'établit vers 6,7 Md€ par an au centre et n'est pas atteint en 2040.
- Hypothèses inchangées par rapport à pfu/ : 1 450 Md€ de titres couverts, 2,3 % transmis par an, 55 % de
  plus-value latente. Repère : 44 % de plus-value latente dans les successions américaines de 2010 qui ont choisi la
  reprise du prix (Gordon, Joulfaian et Poterba, 2016) [E], ce qui laisse penser que le centre est plutôt haut. Le
  calibrage repose sur l'encours de titres de la Banque de France fin 2025, pas sur les flux de 2024 gonflés par la
  CDHR (vérifié dans `calculs_pfu.py`). Les chiffrages du PFU utilisent l'assiette de 2025, qui est peut-être
  déprimée à l'inverse.
- **Pour le bouclage** : n'utiliser ces recettes qu'une fois constatées. Une utilisation prudente reprendrait au plus
  la ligne basse avec deux ans de décalage.

**Options pour les plus-values acquises avant l'annonce.**
- Option 1, prix historique pour tout (retenue) : 35,0 Md€ cumulés.
- Option 2, valeur au jour de l'annonce pour les titres détenus à cette date : 16,7 Md€, soit un coût de 18,3 Md€ sur
  2027-2040 (3,4 à 57). Sur 2027-2031, 1,8 contre 7,2 Md€.

L'option 1 ne réclame aucun impôt sur un fait passé : le fait générateur reste la vente future. Elle taxe une
plus-value déjà accumulée, peu sensible à l'impôt, ce qui en fait la moins distorsive des deux. Elle évite aussi
d'évaluer tous les titres non cotés à une date de référence. Son risque est constitutionnel (atteinte à des attentes
légitimes) et n'a pas été expertisé ; l'option 2 sert de repli.

**Date d'effet.** Elle doit coïncider avec l'annonce. Une année d'écart laisserait passer une cohorte de donations
anticipées, soit environ 6,7 Md€ d'impôt latent au centre.

## 4. Interactions vérifiées

- **Droits de succession** : aucune réforme générale. La seule interaction est la correction du prix (§ 2), qui
  réduit la recette de 10 % au centre (5 à 15 %, taux moyen effectif [H] ; repère : 21,2 Md€ de DMTG en 2025 pour
  environ 300 Md€ transmis par an).
- **Pacte Dutreil** (LF 2026 : engagement individuel porté de 4 à 6 ans, biens somptuaires exclus [S]) : la
  plus-value latente suit les titres. Comme rien n'est dû à la transmission, la réforme ne contredit pas l'objectif du
  pacte. Elle supprime en revanche le cumul « 75 % d'exonération des droits + effacement » quand l'héritier vend après
  l'engagement. Si le pacte est réformé ailleurs, la correction s'ajuste d'elle-même : elle ne porte que sur les
  droits effectivement payés.
- **Report d'apport-cession** : transmis sans effacement, il prend fin aux mêmes événements que chez l'apporteur.
  **PLF 2027, art. 5** : adopté en première lecture à l'Assemblée le 16/10/2026 sous une forme amendée (successions
  exclues ; donation visée seulement si la holding a vendu dans les huit ans). La première partie a ensuite été
  rejetée le 04/11/2026 (scrutin n° 9759) [S]. Rien n'est donc en vigueur, et la table part du droit de 2026. Si la
  version du Gouvernement (expiration à toute transmission, environ 1,7 Md€ par an au centre) était votée, il faudrait
  retirer la ligne « reports » de notre recette.
- **Donation avant cession** : ce montage, qui efface la plus-value aujourd'hui, est fermé.
- **Exit tax** (art. 167 bis) : la plus-value reprise entre dans sa base. Le dégrèvement après 2 ans (5 ans au-delà
  de 2,57 M€) [S] devient la principale sortie restante, d'où la recommandation d'un délai long pour les grosses
  participations. Les amendements de l'Assemblée du 30/10/2026 (15 ans) sont tombés avec le rejet de la première
  partie [S]. Des héritiers non résidents qui vendent des titres de portefeuille échapperaient en général à l'impôt
  français (non vérifié sur les conventions).

## 5. Effets économiques et risques

- **Verrouillage** [S, mécanique ; E pour le sens]. On mesure le rendement supplémentaire qu'un autre placement doit
  offrir pour qu'il vaille la peine de vendre (plus-value égale à 90 % de la valeur, rendement de 5 %). Pour un
  détenteur qui attend son décès dans 10 ans, il passe de 3,6 points aujourd'hui à 1,5 point avec la réforme (de 7,2
  à 1,7 à 5 ans). Pour un héritier, il passe de 0 à 1 à 1,5 point. La réforme déplace donc le verrouillage plus
  qu'elle ne le supprime : elle retire la prime à garder jusqu'à la mort, là où le coin est le plus fort, et laisse
  chez l'héritier le verrouillage ordinaire de tout détenteur. Auten et Joulfaian (2001, *JPubE* 81(2)) montrent que
  l'effacement accroît le verrouillage aux âges élevés [E]. L'effet net sur la réallocation du capital n'est pas
  chiffré, et aucun effet sur le PIB n'est revendiqué.
- **Perte sèche** : pas de chiffrage, aucune élasticité ne s'applique. Pour les plus-values passées, la mesure est
  proche d'un impôt sur un stock. Pour les plus-values futures, elle rétablit la neutralité entre vendre et garder.
  Son effet sur l'épargne en vue de la transmission n'est pas mesuré [H].
- **Risques** : héritiers qui ne vendent pas (le jeu bas divise la recette de 2040 par 3,7) ; départs à l'étranger ;
  report vers l'assurance-vie (IR effacé au décès) ; risque constitutionnel de l'option 1 et de l'effet dès
  l'annonce ; preuve du prix des titres très anciens (règle de repli à prévoir).
- **Littérature sur le taux du PFU** [E] :
  - IPP, note n° 46 (2019) : le PFU de 2018 a fait monter les dividendes versés de 15 %, et la réforme a coûté
    0,4 Md€ au lieu de 0,9 ; en 2013, les foyers au prélèvement libératoire avaient déclaré 40 % de dividendes en
    moins.
  - France Stratégie (2023) : aucun effet détecté sur l'investissement ni sur les salaires des entreprises exposées
    (identification « imprécise »).
  - Yagan (2015, *AER*) : la baisse américaine de 2003 n'a eu aucun effet sur l'investissement.
  - **Boissel et Matray (2022, *AER*)**, qui trouvaient que la hausse de 2013 avait accru l'investissement, **ont été
    rétractés par leurs auteurs** (*AER* 113(7), 2023) après le commentaire de Bach, Bozio, Guillouzouic et
    Malgouyres (2023). À ne pas citer comme résultat.

## 6. CEHR et CDHR sur les revenus du capital (revenus de 2025, DGFiP n° 53, provisoire)

- **CEHR** : 1,39 Md€ au total, dont 0,7 à 1,1 Md€ sur le capital [H : 50 à 80 %].
- **CDHR** : 0,62 Md€, presque entièrement due au capital [H : 80 à 100 %, soit 0,5 à 0,6].
- **Les maintenir sur le capital** (sous forme de majoration de 3 puis 4 points du PFU, appréciée sur le même revenu
  de référence, si le bloc IR-CSG les supprime sur le barème) coûte 0. Le taux supérieur sur le capital reste à
  35,4 %, sans interférence avec le plafond de 50 % des revenus du barème.
- **Supprimer la CEHR sur le capital** coûte 0,7 à 1,1 Md€ avant la reprise par la CDHR des foyers à son plancher.
- **Supprimer la CDHR** coûte 0,6 Md€, mais sa fin est déjà inscrite dans le droit (au retour du déficit sous 3 % du
  PIB) : c'est une évolution du droit en vigueur, pas une mesure.
- La CRDS (0,5 point du PFU, 0,33 Md€ sur son assiette) s'éteint fin 2033. Sans décision, le PFU passera à 30,9 %.

## 7. Long terme (non retenu)

Indexer le prix d'acquisition sur l'inflation ferait porter l'impôt sur le seul gain réel. À 2 % d'inflation, 16 à
23 % des plus-values imposées sont inflationnistes, ce qui représente une perte d'environ 0,6 à 0,9 Md€ par an [H],
davantage avec la réforme, qui fait entrer des gains détenus longtemps. Il faut y ajouter la complexité (les
abattements pour durée de détention de 2013-2017 ont été supprimés pour cette raison). Les distorsions restent entre
les titres détenus en direct, l'assurance-vie (IR effacé au décès), le PEA et l'immobilier (exonéré après 22 ou
30 ans). Orientation de long terme, non retenue.

## 8. Limites qui peuvent changer la conclusion

Aucune statistique ne mesure les plus-values effacées. La recette repose sur cinq hypothèses (part transmise,
plus-value latente, rythme de vente des héritiers, stock de reports, taux moyen des droits), et la fourchette va de 1
à 10 Md€ en 2040. Les recettes des revenus de 2025 sont provisoires. Ni la constitutionnalité de l'option 1 ni l'effet
dès l'annonce n'ont été expertisés.

## Références vérifiées

- Auten et Joulfaian (2001), *Journal of Public Economics* 81(2), 213-229 (résumé lu).
- Gordon, Joulfaian et Poterba (2016), *AER P&P* 106(5), 662-667 (résumé lu).
- Bach, Bozio, Fabre, Guillouzouic, Leroy et Malgouyres (2019), note IPP n° 46.
- France Stratégie (2023), rapport final du comité d'évaluation.
- Yagan (2015), *AER* 105(12).
- Lefebvre, Lehmann et Sicsic (2025).
- Rétractation de Boissel et Matray, *AER* 113(7), 2053-54 (2023) ; Bach et al., *AER* 113(7), 2048-52.
- 26 U.S.C. § 1015.
- Datan, scrutin n° 9759 (04/11/2026).
- Legifiscal et Boursedescrédits sur l'art. 5 du PLF 2027 (secondaires).
- CMS et Deloitte sur le pacte Dutreil (secondaires).
