# Vérification des calculs : notes IS et PFU

Vérification du 16 novembre 2026. Les notes vérifiées sont `is/note-is.tex` (avec la figure `is_01_cout_deduction`) et
`pfu/note-pfu.tex` (avec la figure `pfu_01_taux_cumule`).

**Méthode.** `simulation_is.py` a été relancé sur une copie dans le scratchpad. Sa sortie est identique, octet pour
octet, à `is/sorties/simulation_is.txt`. Les recalculs indépendants sont dans `verif.py` et `verif2.py`, et leurs
sorties dans `verif_sortie.txt` et `verif2_sortie.txt`, tous dans le même dossier du scratchpad
(`/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_is_pfu/`).

Sources internes : `is/donnees/is_chiffres.csv`, `pfu/donnees/pfu_chiffres.csv`, `is/notes/is_recherche.md`,
`pfu/notes/pfu_recherche.md`, `revue/revue_is.md`, `revue/revue_pfu.md`, `donnees/pib_france_cp_meur.json` et
`donnees/ir_2042_cases_revenus2024.csv`.

Sources externes : deux recherches web seulement, dont seuls les résumés ont été lus (liste en fin de rapport).
Aucun fichier n'a été téléchargé et aucun fichier du dépôt n'a été modifié.

**Statuts.**
- OK : le calcul refait ou la source retrouvée donne le même chiffre.
- ERREUR : la valeur juste est indiquée.
- ARRONDI DOUTEUX : l'arrondi est discutable ou ne correspond pas au calcul exact.
- NON VÉRIFIABLE : aucune source dans le dépôt, ou une source qui n'a pas pu être lue.

**Bilan.** Aucun chiffre n'est absurde : les ordres de grandeur tiennent face aux repères externes (§ 2). Sur les
deux notes, environ 140 nombres ont été vérifiés.
- Trois erreurs touchent une conclusion de la note IS : la baisse de taux finale, la borne basse du taux réduit et
  la compensation des petites sociétés pendant la phase à 50 %.
- Les autres problèmes sont des arrondis, un libellé, deux omissions dans la note de figure PFU et des conventions
  du code.

---

## 1. Erreurs et absurdités, par gravité

### Gravité moyenne : erreurs qui modifient une conclusion

**E1. « Baisser le taux normal d'environ un point », « à recette constante sur la durée ».**

*Passage* (IS, § 3, fin) : « Une fois la dette éteinte, l'excédent, de l'ordre de 3 à 6 Md€ par an, permet de
baisser le taux normal d'environ un point : c'est à ce prix que l'ensemble est à recette constante sur la durée. »

*Valeur juste.* L'excédent est bien de 3,3 à 5,8 Md€ en année 20. Mais la baisse de taux que cet excédent finance
durablement, une fois la dette éteinte, se situe entre 0,7 et 1,2 point :
- 0,69 point dans le cas bas (amortissement actuel linéaire, assiette élargie de 3,5 Md€) ;
- 0,87 et 1,02 point dans les deux cas intermédiaires ;
- 1,20 point dans le cas haut (dégressif, 4,4 Md€).

Ce calcul retient une base de 278 Md€ pour un point de taux, puisqu'après la fin du taux réduit les 27 Md€ aujourd'hui
taxés à 15 % passent au taux normal. Avec la base de 251 Md€ que retient le script, la fourchette est de 0,77 à 1,33
point.

Dans le cas bas, si l'on baisse d'un point entier l'année qui suit l'extinction de la dette (année 26), le solde
redevient négatif : −1,2 Md€ l'année suivante, −1,3 Md€ en année 30. La dette remonte à 27,5 Md€ en année 40.

Le scénario S3b du script, avec une baisse d'un point dès l'année 13, ne correspond pas au texte de la note. Ses
résultats ne sont pas repris dans la note : la dette n'est jamais remboursée dans 3 cas sur 4 (133 Md€ en année 40
dans le cas bas).

*Correction proposée* : « de 0,7 à 1,2 point selon le rendement de l'assiette et le régime d'amortissement actuel ».

*Provenance* : `verif.py` et `verif2.py`, avec les fonctions `scenario` et `chemin` de la copie du script.

**E2. Borne basse de la fin du taux réduit : « 2,2 Md€, chiffre officiel de 2019 ».**

*Passages* (IS) :
- tableau 1 : « 2,2 à 2,7 – Chiffre officiel de 2019 ; calcul statique sur 2022 » ;
- § 4 : « Le dispositif a coûté 2,2 Md€ en 2019 » ;
- dans le script, `ELARG_PRUDENT` et `REDUIT = (2.2, 2.7)` alimentent toutes les variantes basses (3,5 Md€).

*Problème.* Le chiffre de 2019 mesure l'avantage par rapport au taux normal de l'époque. Pour les PME, ce taux était
de 28 % sur les 500 000 premiers euros, d'après le BOFiP et l'Insee, que je n'ai vus qu'à travers un résumé de
recherche. L'écart de taux était donc de 13 points, et non de 10.

L'arithmétique du dépôt le confirme :
- 18,2 Md€ de base à 15 % en 2018 (DGFiP, CSV), multipliés par 13 points, donnent 2,4 Md€, proches des 2,2 Md€
  officiels ;
- la même base multipliée par 10 points donne 1,8 Md€.

*Valeur juste.*
- Pour un écart de 10 points, le chiffre officiel de 2019 correspond à environ 1,7 Md€ (2,2 × 10/13), ou 1,8 Md€ sur
  la base de 2018.
- Le seul chiffre comparable est le calcul statique sur 2022 : 2,7 Md€.
- En 2027, ce chiffre serait plutôt plus élevé : jusqu'à 3,0 Md€ avec le plafond de 42 500 €, avant même la
  croissance des bénéfices.
- Une borne basse reste légitime, mais elle doit venir des réactions des sociétés (passage à l'IR, rémunération en
  salaire), qui ne sont pas chiffrées. Elle ne peut pas venir d'un chiffre officiel établi pour un autre écart de taux.

*Conséquence.* Les conclusions restent les mêmes : la variante basse est prudente par construction. Mais le libellé
« chiffre officiel » est faux pour cet usage, et le § 4 met en regard deux chiffres qui ne sont pas comparables.

*Provenance* : CSV IS (lignes 2019 et 2018) ; `is_recherche.md` § 3.2 ; recherche web (taux de 2019).

**E3. Compensation de la petite société pendant la phase à 50 %.**

*Passage* (IS, § 4) : « la déduction immédiate lui avance l'impôt sur ses achats, 4 600 € la première année pour
20 000 € d'équipements ».

*Valeur juste.* Les 4 643 € correspondent à une déduction de 100 %. Or le calendrier de la note ne prévoit que 50 %
de 2027 à 2032, alors que la fin du taux réduit s'applique dès 2027 (scénario S3). Sur ces six années :
- l'avance est de 2 321 € pour 20 000 € d'équipements ;
- l'investissement annuel à partir duquel le gain durable compense la perte de 4 250 € est de 222 600 €, et non de
  110 000 €.

Le seuil de 110 000 € (exactement 111 322 €) n'est atteint qu'avec la déduction totale et un amortissement actuel
linéaire. Si l'entreprise amortit aujourd'hui en dégressif, le seuil monte à 161 000 €.

*Conséquence.* La conclusion « Une petite société industrielle qui investit est en partie compensée » vaut deux fois
moins pendant les six premières années.

*Provenance* : `petite_societe` et `plan('lineaire')` de la copie du script ; `verif.py`.

### Gravité faible : erreurs de libellé, d'arrondi ou d'omission

**E4. Gain de PIB : le stock de 541 Md€ est mal désigné.**

*Passage* (IS, § 2) : « le stock d'équipements des entreprises imposables, 541 Md€ fin 2025, augmenterait de 1 à
6 % ».

*Problème.* Dans le code, 541 Md€ est le stock de toutes les sociétés non financières, et le gain est multiplié par
0,75 pour ne garder que la part des imposables. Le texte mélange les deux.

*Valeur juste.* Deux formulations sont cohérentes :
- « le stock d'équipements des SNF (541 Md€) augmenterait de 1,3 à 5,8 % » ;
- ou : « celui des imposables (environ 405 Md€) de 1,7 à 7,7 % ».

Le gain de PIB (0,04 à 0,2 %) n'en dépend pas et reste juste.

*Provenance* : code, lignes 231 à 238 ; `verif.py`.

**E5. « La dette culmine à 3 à 33 Md€ ».**

*Valeur juste* : 32,49 Md€, donc **3 à 32 Md€**. Le 33 vient d'un double arrondi : 32,49 est affiché 32,5, puis
arrondi à 33. Statut : ARRONDI DOUTEUX.

*Provenance* : scénario S3, cas linéaire avec 3,49 Md€ d'assiette.

**E6. « À partir de la huitième année, … 1,4 à 2,1 Md€ par an ».**

*Valeur juste* : 1,36 à 1,99 Md€ en année 8, soit **1,4 à 2,0**. Le chiffre de 2,1 est celui de l'année 10. La revue
précédente avait déjà relevé ce décalage d'année ; la note a corrigé l'année mais pas le chiffre. Statut : ARRONDI
DOUTEUX.

*Provenance* : `chemin`, avec une déduction de 100 % et une part imposable de 75 %.

**E7. Taux cumulés : arrondis incohérents.**
- Holding : 25,825 + 74,175 × 1,25 % = **26,75 %**, que le CSV PFU donne lui-même. Arrondi au demi supérieur, cela
  donne 26,8 %. La note et la figure affichent 26,7 %.
- Taux à 25 % d'IS : 25 + 75 × 31,4 % = **48,55 %**. Les deux notes l'arrondissent à 48,6 % (au demi supérieur), mais
  la sortie du script affiche 48,5 %, par un artefact de calcul en virgule flottante.

La règle d'arrondi doit être la même partout : 26,8 et 48,6, ou 26,7 et 48,5. Statut : ARRONDI DOUTEUX.

**E8. Note de la figure PFU et texte : le taux maximal est sous-estimé.**

*Passages* :
- note de figure : « Entreprises de plus de 3 Md€ de chiffre d'affaires (contribution exceptionnelle, environ
  450 entreprises) : 56 à 59 % » ;
- texte : « jusqu'à 54,5 % pour un foyer à la CDHR ».

*Valeur juste.* Avec un IS de 36,125 %, on obtient :
- 56,2 % avec le PFU ;
- 58,7 % avec la CEHR ;
- **60,8 % avec la CDHR**.

La fourchette devrait donc être de 56 à 61 %, et le « jusqu'à » du texte ne tient que pour les sociétés à 25,8 %.

Par ailleurs, les « environ 450 » entreprises sont l'ensemble des redevables de la contribution exceptionnelle,
dès 1 Md€ de chiffre d'affaires (`is_recherche.md` § 1.6 : « environ 450 redevables »). Seule une partie d'entre
eux dépasse 3 Md€ et paie 36,1 %. Le nombre exact n'a pas été trouvé.

Le même amalgame figure dans `fiscalite/CLAUDE.md` (« l'IS à 36,1 % ne vise qu'environ 450 entreprises ») ; ce
fichier n'a pas été modifié.

**E9. Coût mécanique du PFU à 25 % : 5,1 Md€ est un majorant, et deux assiettes sont mélangées.**

*Calcul* : 6,4 points × 79,6 Md€ = 5,09 Md€, juste. Mais l'assiette de 79,6 Md€ comprend les dividendes des
2,54 millions de foyers qui optent pour le barème. Le CSV PFU qualifie lui-même de « majorant » l'IR calculé
sur cette assiette. La note devrait le dire.

La note cite aussi le chiffrage du CAE (1,2 Md€ nets pour 3 points), qui porte sur une assiette de 57 Md€. Elle
calcule ses propres chiffres sur 80 Md€. Rapporté à 80 Md€, le chiffrage du CAE donne environ 1,7 Md€. Les deux
chiffres ne sont pas comparables tels quels.

**E10. « Les deux tiers des entrées de 2023 sont concentrés sur 84 foyers ».**

*Valeur juste* : 23,5 / 33,6 = 70 %, soit « plus des deux tiers » ou « sept dixièmes ». Statut : ARRONDI DOUTEUX.

### Cohérence interne et entre les deux notes

**C1. PFU : le coût net d'une baisse permanente est probablement plus élevé que 3,2 à 3,9 Md€.**

La note explique que 2013 et 2018 forment « un seul épisode » : la réaction des dividendes est surtout un
déplacement dans le temps. Or elle calcule le coût net d'une baisse permanente avec des élasticités de 0,65 à 1,
mesurées sur ces épisodes.

À long terme, la réaction de l'assiette serait donc plus faible, et le coût net se situerait entre 3,2 et 5,1 Md€,
plus près de 5,1 si la réaction n'est que temporaire. La conclusion, écarter le PFU à 25 %, en sort renforcée. La
note devrait dire que 3,2 à 3,9 Md€ est le coût des premières années.

**C2. IS : le gain de croissance ne compte que la déduction, pas son financement.**

Le gain de « 0,1 % du PIB » ne vient que de la baisse du coût d'usage des équipements. Le financement, et d'abord
la fin du taux réduit, relève le coût du capital des sociétés sous le plafond :
- pour leurs équipements de 2027 à 2032, l'effet est presque nul (−0,15 %) : la déduction de 50 % compense à peine
  le passage de 15 % à 25 % ;
- pour leurs actifs non éligibles, comme des bâtiments industriels dont les déductions valent 54,8 % du coût
  (Tax Foundation), le coût d'usage monte de 6,6 %.

La note cite elle-même Bernini et Treibich : un taux divisé par deux a accru de 29 % le capital des petites
sociétés. L'effet net du paquet n'est donc pas chiffré et pourrait être nettement inférieur à 0,1 % du PIB. Ce
dernier point est NON VÉRIFIABLE : aucune donnée ne ventile le capital des sociétés sous le plafond.

**C3. PFU, apport-cession : « de l'ordre de 2 Md€ par an » en régime de croisière est probablement un plancher.**

Le calcul est juste : 153 / 25 × 31,4 % = 1,92 Md€. Mais il suppose un stock figé. Or les entrées sont de 22 à
34 Md€ par an, soit 7 à 10,6 Md€ d'impôt potentiel par an si elles finissent par être transmises. Le stock de
153 Md€ ne représente que 5 à 7 années d'entrées au rythme actuel.

Cela ne change pas la position de la note, qui retient le transfert du report sans effacement. Mais cela confirme
que l'article 5 du PLF 2027 pèserait lourdement sur le sommet de la distribution.

**C4. Holding : le taux de 26,75 % est un majorant.**

Le chiffre suppose que la quote-part de 5 % est taxée à 25 %. Deux cas donnent moins :
- une holding intégrée fiscalement (quote-part de 1 %, mentionnée dans `pfu_recherche.md`) paie 0,25 %, soit
  **26,0 %** au total ;
- une petite holding au taux réduit, en droit 2026, paie 0,75 %, soit **26,4 %**. C'est justement le cas que la
  réforme de l'IS supprime.

Les deux notes restent cohérentes entre elles : après la réforme de l'IS, toute holding non intégrée paie 1,25 %.

**C5. Taux cumulés entre les deux notes : cohérents.**
- La note IS donne 41,7 % puis 48,6 % ; la note PFU donne 48,6 % sans la contribution sociale et 49,1 % avec.
- Les deux utilisent le même PFU de 31,4 %.
- Le cas de la petite société n'apparaît que dans la note IS ; ses chiffres (4 250 €, 3 000 €, 110 000 €) sont
  justes, avec la réserve E3.

**C6. Le pic de coût de 2033 n'est dit que par la figure.**

Le passage à 100 % en 2033 fait remonter le coût annuel à 9,3 à 10,8 Md€, plus que la première année de la phase à
50 % (7 à 7,8 Md€). Le texte ne le dit pas ; seule la figure le montre.

**C7. README IS et note : deux fourchettes de points de taux.**

Le README indique « 0,7 à 1 point de taux » et la note « 0,5 à 1 point ». Les deux sont justes, mais pas sur le même
périmètre :
- au taux de 5 % : 0,70 à 1,02 point ;
- au taux de 5 % et de 3,25 % réunis : 0,47 à 1,02 point.

### Code de `simulation_is.py`

Le calcul par millésime est juste.
- `chemin` ne fait porter le nouveau régime que sur les achats postérieurs à la réforme, compare chaque millésime à
  son propre plan ancien, et gère correctement les tranches de tableau.
- `z` actualise de façon cohérente : la déduction de l'année 0 n'est pas actualisée.
- `cout_usage` applique la bonne formule.
- `scenario` compte les intérêts sur la dette de l'année précédente.
- Les sorties publiées sont reproductibles.

Erreurs et conventions à corriger :

1. **Base d'un point de taux après la réforme (ligne 123).** La baisse de taux est calculée sur `BASE_NORMALE`
   (251 Md€), alors qu'après la fin du taux réduit la base au taux normal est de 278 Md€. Le coût d'un point est
   donc sous-estimé de 11 % (voir E1).
2. **Le scénario S3b ne correspond pas au texte (lignes 225 et 226).** Il baisse le taux en année 13 quelle que soit
   la date d'extinction de la dette (année 5 à 25), alors que la note dit « une fois la dette éteinte ». Il manque un
   scénario « baisse l'année qui suit l'extinction » (voir E1).
3. **Années de prix mélangées.** Les ressources (taux réduit 2022 ou 2019, hausse de taux, baisse de taux) sont
   comptées en euros de 2022, sans croissance jusqu'en 2027, alors que les coûts partent de l'investissement de 2027.
   `CROISS_BASE` est défini mais jamais utilisé. La note de figure signale le problème (« plutôt sous-estimés »),
   mais pas le texte sur la dette. L'effet : la dette est surestimée et le coût d'une baisse de taux sous-estimé.
4. **Amortissement dégressif.** Avec la convention de demi-année et 7,5 années restantes, le plan s'étale sur
   8 annuités. En droit français, le plan dégressif s'achève au 7e exercice : c'est ma lecture de la règle des
   « années restant à courir », non vérifiée sur le BOFiP. L'effet est négligeable : z passe de 0,8945 à 0,8966,
   et le coût actualisé de 1,76 à 1,73 Md€.
5. **Libellés trompeurs dans la sortie.**
   - `[SCEN]` annonce un « horizon 30 ans », mais la dette maximale et l'année de remboursement sont cherchées sur
     40 ans (ce qui produit « an 40 » pour S2).
   - `[SOLDE]` « solde annuel positif dès l'année » donne la première année positive, sans voir le retour au
     négatif lors du passage à 100 % (variantes C et D).
6. **Constantes en dur.**
   - `K = 541` n'a pas de source dans le CSV (« lu par la revue »).
   - `PIB25 = 2950`, alors que l'Insee donne 2 991 Md€ pour 2025 dans le dépôt. L'effet sur le gain de PIB est
     inférieur à 0,002 point, et le gain en Md€ ne change pas.
   - `PIB_2027 = 3100`, contre environ 3 170 Md€ à 3 % de croissance par an. Ce chiffre ne sert qu'aux ratios de
     dette sur PIB de la sortie.
   - Les baisses du coût d'usage (0,034 et 0,048) sont saisies en dur, mais elles sont égales aux valeurs calculées.
7. **`petite_societe` ne connaît que la déduction totale et l'amortissement linéaire.** Le calendrier à 50 % et le
   cas dégressif ne sont pas couverts (voir E3).
8. **Dernière ligne `[PME]`.** Elle affiche 48,5 % pour 48,55 % (voir E7).
9. **Conventions acceptables mais à dire.**
   - Les sociétés imposables utilisent toute la déduction tout de suite : il n'y a ni déficits ni plafonnement du
     report. Le coût de la première année est donc plutôt surestimé, et la récupération plus rapide.
   - La semi-élasticité de 1,5 % par point, estimée sur les filiales de multinationales, est appliquée aux
     251 Md€ de bénéfices.
   - Le coût d'usage et le gain de PIB sont calculés avec un taux nominal de 5 %.

---

## 2. Ordres de grandeur face aux repères externes

| Résultat | Repère | Rapport | Jugement |
|---|---|---|---|
| Coût de la déduction totale la première année : 14 à 15,5 Md€ | IS net 2025 : 59,9 Md€ (CSV) | 23 à 26 % | Élevé mais pas absurde. C'est deux fois le rapport britannique (10 Md£ pour 82 Md£ d'IS, soit 12 %), ce qui s'explique en partie par l'*annual investment allowance* britannique (1 M£ déduit tout de suite depuis 2019, résumés de recherche). La part imposable de 75 % décide du chiffre. |
| Déductions supplémentaires la première année : 62 Md€ | Bénéfices imposables 2022 : 278 Md€ | 22 % | Plausible. Une partie deviendrait des déficits reportés (plafond de 1 M€ plus 50 %), ce qui réduirait le coût de la première année. |
| Investissement éligible : 84 Md€ | FBCF des SNF en 2025 : 348,2 Md€ ; PIB : 2 991 Md€ | 24 % ; 2,8 % | Cohérent avec le tableau 8.212 (machines 126,2, dont environ 42 de transport). |
| Stock de 541 Md€ | Stock d'équilibre I/(g + δ) = 84/0,17 = 494 Md€ | 1,1 | Plausible ; source non retrouvée dans le dépôt. |
| Coût permanent : 1,4 à 2,1 Md€ par an ; coût actualisé : 1,8 à 2,6 Md€ | Royaume-Uni : 1 à 3 Md£ par millésime (IFS) | Même ordre | OK. |
| IS à 28 % : 4,4 à 7,5 Md€ | Contribution exceptionnelle (environ 450 groupes) : 7 à 7,5 Md€ ; IS net : 60 Md€ | 7 à 13 % de l'IS | OK. Avec des bases de 2022, le chiffre est plutôt sous-estimé. |
| Gain de PIB : 0,04 à 0,2 % (1,3 à 6 Md€) | Financement : 3,5 à 4,4 Md€ par an | Même ordre | Gain modeste, comme le dit la note, mais calculé sans l'effet du financement (C2). |
| Assiette du PFU : 79,6 Md€ | Repère : 80 Md€ ; acompte de 12,8 % = 7,67 Md€, soit 59,9 Md€ de dividendes et d'intérêts | Cohérent | OK. Le CAE retient 57 Md€ (E9). |
| Dividendes de 2024 : 50,1 Md€ (case 2DC) | France Stratégie : 33,5 Md€ (2021), environ 37 Md€ (2022) | +35 % en deux ans | Plausible, mais la case comprend les dividendes des foyers qui optent pour le barème. Non comparé aux comptes nationaux (NON VÉRIFIABLE). |
| PFU à 25 % : 5,1 Md€ | IR du PFU : environ 10,2 Md€ (majorant) | La moitié | Arithmétique juste ; c'est un majorant (E9). |
| Apport-cession : 90 à 100 M€ par foyer | 23,5 Md€ / 84 foyers = 280 M€ de plus-value chacun | Multiplié par 31,4 à 35,4 % : 88 à 99 M€ | OK, en moyenne sur les 84 foyers. |
| Apport-cession : 2 Md€ par an | Entrées de 22 à 34 Md€ par an | 7 à 10,6 Md€ d'impôt potentiel | Plancher plutôt qu'estimation (C3). |

---

## 3. Tableau des nombres vérifiés

### 3.1 Note IS (texte, tableau 1, figure 1)

| § | Nombre (note) | Recalcul ou source | Statut |
|---|---|---|---|
| Intro | Taux normal de 25 % | CGI (notes) | OK |
| Intro | 50 % de 2027 à 2032, puis 100 % | Script : `pal`, 0,5 si t < 6 | OK |
| Intro | Taux réduit de 15 % | Art. 219 (notes) | OK |
| Intro | 0,1 % du PIB | 0,107 % | OK (C2) |
| 1 | Dernière des 38 pays en 2025 et 2026 | CSV, Tax Foundation | OK |
| 1 | 36,1 % | 25 × (1 + 0,033 + 0,412) = 36,125 | OK |
| 1 | 24,2 % ; quatre taux contre 2,3 en moyenne | `is_recherche.md` § 1.1 | OK |
| 1 | 15e en 2025, 16e en 2026 (récupération des coûts) | CSV et notes | OK |
| 1 | 88 % contre 86 % | 88,0 contre 85,9 | OK |
| 1 | 23,6 contre 22,2 % (13e sur 38) | 23,61 contre 22,24 | OK |
| 1 | 15,0 contre 16,5 % ; 9,8 contre 10,4 % | 14,97 / 16,49 ; 9,82 / 10,40 | OK |
| 2 | Machine de 100 €, 7 ans, 5 %, déductions de 85 à 90 € | z = 84,7 (linéaire) ; 89,5 (dégressif) | OK |
| 2 | L'État rend 25 € ; associé pour le quart | 25 % × 100 | OK |
| 2 | 10 % contre 2,5 % de recette, « quatre fois moins » | 9,9 / 2,5 = 3,96 (notes, tableau 7) | OK |
| 2 | +10 et +17 % ; « deux fois plus » | 10,4 / 16,9 ; +95 % | OK |
| 2 | +11 % (Maffini et al.) | Notes | OK |
| 2 | 12 à 14 % ; 2 390 utilisateurs | DGE (CSV) | OK |
| 2 | L'impôt majore le coût d'usage de 3,5 à 5 % | 3,52 % (dégressif) ; 5,09 % (linéaire) | OK |
| 2 | Élasticité de 0,5 à 1,6 | 1,6 : Maffini (stock) ; 0,5 : hypothèse sans source | NON VÉRIFIABLE (borne basse) |
| 2 | 541 Md€ fin 2025 | Absent du CSV ; cité par la revue (Insee 8.212) | NON VÉRIFIABLE (plausible) |
| 2 | « Des entreprises imposables » ; +1 à 6 % | 1,3 à 5,8 % du stock total, ou 1,7 à 7,7 % de celui des imposables | ERREUR (E4) |
| 2 | Revenu du capital : 3,5 % du PIB | 0,19 × 541 / 2 950 = 3,48 % (3,44 % avec un PIB de 2 991) | OK |
| 2 | Gain de PIB : 0,04 à 0,2 % | 0,044 / 0,201 | OK |
| 2 | 0,1 %, soit 3 Md€ | 0,107 % ; 3,16 Md€ | OK |
| 2 | « Deux fois moins » avec 50 % | 0,02 à 0,10 % | OK |
| 2 | Charges financières : 30 % du résultat brut, au-delà de 3 M€ | Texte non lu dans le dépôt | NON VÉRIFIABLE |
| 2 | Bâtiments : 7,3 contre 12,1 % | 7,33 / 12,09 | OK |
| 3 | 84 Md€ en 2025 | 75,5 + 8,5 (Insee 8.212, notes) | OK |
| 3 | Trois quarts imposables | Hypothèse déclarée | OK |
| 3 | 14 à 15,5 Md€ la première année | 14,02 / 15,52 | OK |
| 3 | 11 à 19 Md€ selon la part imposable | 11,2 / 18,6 | OK |
| 3 | Dès la huitième année, 1,4 à 2,1 Md€ | Année 8 : 1,36 / 1,99 (2,1 = année 10) | ARRONDI DOUTEUX (E6) |
| 3 | 1,8 à 2,6 Md€ actualisés à 5 % | 1,76 / 2,55 | OK |
| 3 | 1,2 à 1,7 Md€ actualisés à 3,25 % | 1,19 / 1,74 | OK |
| 3 | 0,5 à 1 point de taux | 0,47 à 1,02 (2,51 Md€ par point) | OK (C7) |
| 3 | 28 % : 7,5 Md€ | 0,03 × 251 = 7,53 | OK |
| 3 | 4,4 Md€ avec 1,5 % de base en moins par point | 4,37 | OK |
| 3 | Assiette : 3,5 à 4,4 Md€ | 3,49 / 4,39 | OK |
| 3 | 1,4 à 1,7 point | 1,39 / 1,75 sur 251 Md€ (1,26 / 1,58 sur 278 Md€) | OK |
| 3 | CIR : 8 Md€ | 8,068 (2025) | OK |
| 3 | Coût de la boîte à brevets doublé depuis 2021 | 555 M€ en 2021, 1,2 Md€ en 2024 | OK |
| Tableau 1 | Fin du taux réduit : 2,2 à 2,7 (« chiffre officiel de 2019 ») | 2,2 mesuré pour un écart de 13 points ; 1,7 à 1,8 pour 10 points ; 2,7 pour 2022 | ERREUR (E2) |
| Tableau 1 | CIR au niveau du groupe : 0,6 | 0,569 (CPO) | OK |
| Tableau 1 | Exonérations zonées : 0,5 | 0,524 (CPO) | OK |
| Tableau 1 | Brevets : 0,2 à 0,6 ; taux de 17,5 % | 1,258 / 2 = 0,63 ; 10 + 15/2 ; 0,2 est une hypothèse | OK |
| Tableau 1 | Total : 3,5 à 4,4 ; 1,4 à 1,7 point | Voir plus haut | OK |
| 3 | Déduction totale : dette de 19 à 46 Md€ | 19,50 / 45,65 (S4) | OK |
| 3 | Remboursée en 11 à 28 ans | 11 / 28 | OK |
| 3 | 50 % la première année : 7 à 7,8 Md€ | 7,01 / 7,76 | OK |
| 3 | Calendrier : dette de 3 à 33 Md€ | 3,15 / 32,49 | ARRONDI DOUTEUX (E5) : 3 à 32 |
| 3 | Remboursée en 5 à 25 ans | 5 / 25 (S3) | OK |
| 3 | Jamais remboursée sans la fin du taux réduit | S2 : jamais en 40 ans dans les 4 cas | OK |
| 3 | Excédent de 3 à 6 Md€ par an | Année 20 : 3,29 à 5,76 ; à l'extinction : 2,9 à 4,5 | OK |
| 3 | Baisse « d'environ un point », « à recette constante » | 0,69 à 1,20 point (0,77 à 1,33 dans la convention du script) | ERREUR (E1) |
| 4 | 10 M€ ; 75 % ; 42 500 € ; art. 219 | Notes (service-public, évaluations préalables) | OK |
| 4 | Conseil d'État 2025, n° 481538 | Notes | OK |
| 4 | 2,2 Md€ en 2019 ; 760 000 sociétés | CPO 2023 (CSV) | OK (fait), mais voir E2 |
| 4 | 27 Md€ en 2022, soit 2,7 Md€ | 27 × 10 % | OK |
| 4 | 4 250 € par an | 10 % × 42 500 | OK |
| 4 | Le CPO demande la suppression depuis 2016 | Notes | OK |
| 4 | Environ 24 000 € en moyenne en 2018 | 18,2 Md€ / 760 000 = 23 947 € | OK |
| 4 | Bernini et Treibich : +29 % de capital | Revue (résumé seulement) | OK (source secondaire) |
| 4 | Au plus 4 250 €, au plus 10 % du bénéfice | 10 % × min(B ; 42 500) | OK |
| 4 | 2,4 millions de redevables ; 490 000 ; 190 000 | 2,44 M ; 492 800 ; 193 800 | OK |
| 4 | 4 600 € pour 20 000 € la première année | 4 643 € avec 100 % ; 2 321 € avec 50 % (2027 à 2032) | ERREUR (E3) |
| 4 | Gain durable au-delà de 110 000 € par an | 111 322 € (linéaire, 100 %) ; 161 148 € (dégressif) ; 222 645 € (50 %) | OK, avec réserve (E3) |
| 4 | IS en hausse des deux tiers : +3 000 € pour 30 000 € | 4 500 € puis 7 500 €, +66,7 % | OK |
| 4 | Taux cumulé : 41,7 % puis 48,6 % | 41,69 / 48,55 | OK (E7 pour la sortie du script) |
| 5 | Minimum mondial : 15 %, 750 M€, LF 2024 art. 33 | Absents du CSV et des notes lues | NON VÉRIFIABLE |
| 5 | Pilier 2 : 0,5 Md€ en 2026 | CSV (PLF 2027, état A) | OK |
| 5 | 7 Md€, environ 450 groupes ; 5 Md€ par rapport au PLF 2027 | CSV (7,0 ; 5,0) | OK (le chiffre de 450 vaut pour toute la contribution, voir E8) |
| 5 | Contribution sociale de 3,3 % | Notes | OK |
| Figure 1 | Courbes et bandes | Valeurs de `chemin` ; bandes de 3,49 à 4,39 et de 4,37 à 7,53, en hausse de 3 % par an | OK |
| Note fig. 1 | 84 Md€ ; 3 % ; 75 % ; 3,5 à 4,4 ; 4,4 à 7,5 ; 0 à 1,5 % | Voir plus haut | OK |

### 3.2 Note PFU (texte, tableau 1, figure 1)

| § | Nombre (note) | Recalcul ou source | Statut |
|---|---|---|---|
| Intro | 31,4 % en 2026 | 12,8 + 18,6 | OK |
| Intro | Environ 27 % contre 49 % | 26,75 / 49,12 | OK |
| 1 | 12,8 % ; 18,6 % ; 17,2 % ; CSG de 9,2 à 10,6 % | CSV (LFSS 2026, art. 12) | OK |
| 1 | Abattement de 40 % | Droit (notes) | OK |
| 1 | 2,5 millions de foyers optent pour le barème | 2 540 106 (case 2OP) | OK |
| 1 | CEHR : 3 puis 4 % ; 250 000 € (500 000 € pour un couple) | CSV, service-public | OK |
| 1 | Taux marginal de 35,4 % | 31,4 + 4 | OK |
| 1 | CDHR : 20 % ; taux porté à 38,6 % | 20 + 18,6 | OK |
| 1 | Déficit sous 3 % ; 0,6 Md€ attendu au PLF 2027 | CSV (état A, ligne 1440) | OK |
| 1 | 763 000 € ; 25,8 € ; 25 € ; 74,2 € ; 23,3 € | 25,825 ; 74,175 ; 23,29 | OK |
| 1 | 49,1 % ; 48,6 % sans la contribution sociale | 49,12 ; 48,55 | OK (E7) |
| 1 | Jusqu'à 54,5 % pour un foyer à la CDHR | 54,46 ; mais 60,8 % pour les entreprises de plus de 3 Md€ | ARRONDI DOUTEUX (E8) |
| 1 | Salaire : 55,4 % hors cotisations | 9,7 + 49 × (1 − 0,068) = 55,37 | OK |
| 1 | Tax Foundation : 6e sur 35 ; 34 % en 2025 ; moyenne de 21 % | CSV : 6 ; 34,0 ; 20,82 | OK |
| 1 | OCDE : 49 % ; seuls le Danemark et l'Espagne font plus | Notes (54 %, source secondaire) | OK |
| 1 | Holding : 1,25 % ; quote-part de 5 % au taux de 25 % | 5 % × 25 % | OK (C4) |
| 1 | 26,7 % | 26,75 | ARRONDI DOUTEUX (E7) |
| 2 | 2013 ; dividendes −40 % | IPP n° 46 (CSV) | OK |
| 2 | Devait rapporter 0,4 Md€ ; en a coûté 0,9 | CSV | OK |
| 2 | 100 € ; 68,6 € ; 5 % ; 105 € ; 72,0 € | 100 × 0,686 ; 105 × 0,686 = 72,03 | OK |
| 2 | Dividendes de 14 Md€ puis 23 Md€ | France Stratégie (CSV) | OK |
| 2 | +15 % dès 2018 | 15,3 % | OK |
| 2 | 0,4 au lieu de 0,9 ; 0,74 au lieu de 1,05 ; gain de 0,36 | CSV | OK |
| 2 | Taux intégré de 57,6 à 60,1 % en 2013 (IPP) | Cité seulement par `revue_pfu.md` ; absent des notes et du CSV | NON VÉRIFIABLE |
| 2 | 2021 : 96 % ; 62 % ; 33 % ; environ 4 000 foyers | CSV ; notes (« 4 000 foyers ») | OK |
| 2 | Parts en hausse de 5 à 10 points depuis 2017 | Notes, France Stratégie | OK |
| 2 | 44 % du gain au 1 % le plus aisé | CSV (communication Éblé) | OK |
| 2 | Taux maximal de 57 % ; 43 % | 56,6 / 42,9 | OK |
| 2 | PFU de 31,4 à 38,6 % | Voir plus haut | OK |
| 2 | Élasticité de 0,77 | CSV | OK |
| 2 | De 31,4 à 33 % : « un peu moins des deux tiers » du rendement | 62,9 % avec ε = 0,77 | OK |
| 2 | CAE : 3 points rapportent 1,2 Md€ nets | CSV (Focus 124 ; assiette de 57 Md€) | OK (E9) |
| 2 | Départs : 0,2 % par an ; 0,02 à 0,23 % par point | CSV (CAE, Focus 118) | OK |
| 2 | Recommandation 13 du rapport n° 3056 | Notes | OK |
| 3 | Assiette d'environ 80 Md€ : 50 + 10 + 19 | 79,63 = 50,14 + 10,43 + 1,35 + 18,78 + 0,37 − 1,44 | OK |
| 3 | 6,4 points : 5,1 Md€ | 5,09 | OK (majorant, E9) |
| 3 | Élasticité de 0,65 à 1 : 3,2 à 3,9 Md€ nets | 3,24 / 3,91 | OK (C1) |
| 3 | 96 % des dividendes | Voir plus haut | OK |
| 3 | 3 à 4 Md€ perdus | Voir plus haut | OK |
| 3 | 44 % contre 55 % | 44,37 / 55,37 | OK |
| 3 | Directive 2011/96/UE ; quote-part de 5 % | Notes | OK |
| 3 | 85 à 90 % des grandes fortunes détiennent une holding | Audition rapportée (source secondaire) | OK (source) |
| 3 | 1,25 % deviendrait 25 % | Voir plus haut | OK |
| 4 | 31,4 % sur la plus-value ; 70 % de réinvestissement | CSV (LF 2026, art. 11, source secondaire) | OK |
| 4 | Report effacé faute de vente pendant six ans | Notes (« 6 ans, ou 11 ans dans certains cas ») | OK |
| 4 | 33,6 Md€ (2023) ; 22,2 Md€ (2024) ; 18,8 Md€ | CSV (3WH : 22,17 ; 3VG : 18,78) | OK |
| 4 | Stock de 153 Md€ | CSV (rapport AN, source secondaire) | OK |
| 4 | « Les deux tiers » sur 84 foyers | 23,5 / 33,6 = 70 % | ARRONDI DOUTEUX (E10) |
| 4 | 0,4 à 1,5 Md€ de reports expirés par an | 0,418 (2023) ; 1,5 (2024) | OK |
| 4 | Rendement de 0,5 Md€ en 2027 | CSV (source secondaire) | OK |
| 4 | Stock transmis en 25 ans : environ 2 Md€ par an | 153 / 25 × 31,4 % = 1,92 | OK (calcul ; C3) |
| 4 | Étalement sur cinq ans | Notes | OK |
| 4 | 90 à 100 M€ chacun pour les 84 foyers | 279,8 M€ × 31,4 à 35,4 % = 88 à 99 M€ | OK |
| 4 | 31,4 % ; 34,4 % ; 35,4 % ; 250 000 € ; 500 000 € | 31,4 + 3 ; 31,4 + 4 | OK |
| 4 | CDHR : plancher de 20 % | Voir plus haut | OK |
| 4 | CEHR : 1,4 Md€ | 1,412 (CSV) | OK |
| 4 | Recommandations 14 à 17 | Notes | OK |
| 4 | 2,5 millions de foyers | Voir plus haut | OK |
| 4 | Alignement à 18,6 % : environ 1,3 Md€ | 2,8 − 1,5 (CSV, sources secondaires, « fragile ») | OK |
| 4 | Irlande : 20 % sur les revenus passifs | Notes (source secondaire) | OK |
| 4 | Abattements de 2013 à 2017 | Notes | OK |
| Tableau 1 | −40 % ; +15 % | Voir plus haut | OK |
| Figure 1 | 49,1 ; 52,1 ; 54,5 ; 44,4 ; 55,4 | 49,12 ; 52,08 ; 54,46 ; 44,37 ; 55,37 | OK |
| Figure 1 | 26,7 | 26,75 | ARRONDI DOUTEUX (E7) |
| Note fig. 1 | 25,8 ; 12,8 ; 18,6 ; 4 % ; 20 % ; 95 % ; 1,25 % ; 45 % ; 9,7 dont 6,8 | Droit et calculs vus plus haut | OK |
| Note fig. 1 | Plus de 3 Md€ de chiffre d'affaires, environ 450 entreprises : 56 à 59 % | 56,18 à 58,74 ; 60,78 avec la CDHR ; les 450 sont tous les redevables (≥ 1 Md€) | ARRONDI DOUTEUX, incomplet (E8) |

---

## 4. Ce qui n'a pas pu être vérifié

- **Le stock d'équipements de 541 Md€ et l'investissement de 2025 (75,5 et 8,5 Md€).** Le tableau Insee 8.212 n'a pas
  été relu. Les chiffres viennent des notes et de la revue.
- **Le PIB nominal 2027 et le taux d'emprunt de l'État de 3,25 %.** Ce sont des hypothèses du script.
- **Le taux normal de 2019 pour les PME (28 % jusqu'à 500 000 €).** Il n'a été vu que dans un résumé de recherche
  (BOFiP BOI-IS-LIQ-10, Insee ENTFRA21 F3.7). Il est corroboré par l'arithmétique du dépôt (E2).
- **Le nombre d'entreprises au-dessus de 3 Md€ de chiffre d'affaires.** Introuvable dans le dépôt.
- **Le taux intégré de 57,6 à 60,1 % en 2013.** Il n'est cité que par la revue, d'après l'IPP n° 46.
- **Le minimum mondial (15 %, 750 M€, LF 2024 art. 33) et le plafonnement des charges financières (30 %, 3 M€).**
  Textes non lus.
- **La règle exacte de fin du plan dégressif.** Elle relève de ma lecture du BOFiP, non relue sur le texte.
- **Les dividendes déclarés de 2024, comparés aux comptes nationaux.** Comparaison non faite.
- **Le Royaume-Uni.** L'*annual investment allowance* de 1 M£, permanente depuis avril 2023, et le coût de
  9 à 10 Md£ par an n'ont été vus que dans des résumés de recherche (gov.uk, IFS). Le chiffre de 10 Md£ figure
  aussi dans le CSV, d'après l'IFS.

## Sources externes consultées (résumés de recherche seulement)

- [BOFiP, IS – Liquidation et taux – Taux normal (BOI-IS-LIQ-10)](https://bofip.impots.gouv.fr/bofip/2066-PGP.html/identifiant=BOI-IS-LIQ-10-20170301)
- [Insee, Références, fiche 3.7 (ENTFRA21)](https://www.insee.fr/fr/statistiques/fichier/5758766/ENTFRA21_F3.7.pdf)
- [Legifiscal, taux de l'IS](https://www.legifiscal.fr/reperes-fiscaux/taux-impot-societe-is.html)
- [gov.uk, Legislating the Annual Investment Allowance at £1m](https://gov.uk/government/publications/legislating-the-annual-investment-allowance-at-1m/legislating-the-annual-investment-allowance-aia-at-1m)
- [gov.uk, Capital allowances: full expensing](https://gov.uk/government/publications/capital-allowances-full-expensing/capital-allowances-full-expensing-for-companies-investing-in-plant-and-machinery-from-1-april-2023-until-31-march-2026)
- [IFS, Full expensing and the corporation tax base](https://www.ifs.org.uk/sites/default/files/2023-10/Full-expensing-and-the-corporation-tax-base.pdf)
