# Vérification des chiffres : note « Fusionner les impôts sur le revenu : une fausse bonne idée ? » et son annexe

Vérification faite le 16 novembre 2026 sur `ir_csg/note-ir-csg.tex`, `ir_csg/annexe-ir-csg.tex` et les notes des figures
`figures/nu/ircsg_v01`, `x01` à `x04` (la figure `x05` n'est pas appelée par la note). Aucun fichier du dépôt n'a été modifié.

**Méthode.** Le modèle (`proposition.py` et ses dépendances), les données et les sorties ont été copiés dans
`/tmp/claude-0/-home-user-Projets-annexes/935fc156-45bd-500a-b52a-e7e4ee23abb6/scratchpad/verif_ircsg/`. Relancé sur cette
copie, `proposition.py` redonne `sorties/proposition.txt` et `proposition_baremes.json` **à l'identique**. Les contrôles
supplémentaires se trouvent dans `scratchpad/verif_ircsg/scripts/` : `agregats.py`, `verif.py`, `haut.py`, `mcf.py`,
`sensib_dwl.py`, `qui_paie.py`, `franchise_masse.py`, `specialise.py` et `specialise_cale.py`. Les cas-types viennent de
`sorties/courbes_openfisca.csv` (OpenFisca-France 176.1) ; ils n'ont pas été recalculés avec `/usr/bin/python3.13`. Deux
documents ont été téléchargés (André et Sireyjol 2021 ; Kleven et Kreiner 2006), rangés chacun dans un dossier
`dl_*` du scratchpad, lus comme pages et jamais exécutés.

Étiquettes : [Pn] renvoie aux lignes de `sorties/proposition.txt`. Le docstring de `proposition.py` annonce « P0 à P9 »,
mais le programme n'écrit que P0 à P7 ; le README dit bien P0 à P7.

---

## 1. Erreurs et absurdités, par gravité

### Grave 1 : la répartition « Qui finance » sous-estime d'un facteur 2,5 environ ce que paient les pensions

**Passage.** Étape 4, « Qui finance » : « les salaires paient 13,3 Md€ de moins, les revenus des indépendants et les loyers
2,6 Md€ de moins ; les pensions paient 13,0 Md€ de plus, les allocations chômage 3,0 Md€ ». Le chiffre « Pensions +13,0 »
revient dans le tableau 3 et dans le README.

**Pourquoi c'est faux.** `bareme_v3.par_type` répartit le nouvel impôt de chaque tranche entre les types de revenu au
prorata du revenu *net*. La franchise de 8 000 € par adulte, réservée aux revenus d'activité, n'entre donc pas dans la
répartition. Il en résulte une absurdité visible dans les sorties : quand la franchise d'activité augmente (P6), ce que
paient en plus les pensions *baisse* (F0 +16,7 ; F4k +14,1 ; F6k +13,6 ; F8k +13,0 ; F10k +12,6 Md€). Dans le même temps, le
retraité seul à 17 000 € paie *plus* (tableau 1 : de +2 520 à +3 540 €). Une franchise réservée à l'activité ne peut pas
alléger la charge reportée sur les pensions.

**Valeur juste.**
- **Borne sûre.** Le barème proposé taxe chaque euro de pension à 17 % au moins, sans franchise. L'impôt sur les pensions
  vaut donc au moins 0,17 × 406 = 69 Md€, contre 41,1 Md€ de charge actuelle dans le modèle (`par_type`). La hausse est
  donc **d'au moins +28 Md€**. Pour le chômage, la même borne donne au moins 0,17 × 37,2 = 6,3 Md€ contre 2,5 aujourd'hui,
  soit **au moins +3,8 Md€** (la note dit +3,0).
- **Dans la représentation du modèle**, si l'on répartit au prorata du revenu *imposable* (après franchise)
  (`qui_paie.py`) : salaires **−32,4**, indépendants et loyers **−4,2**, pensions **+32,0**, chômage **+4,5** Md€. Pour
  contrôle, sans franchise (étape 3), les deux répartitions coïncident exactement : −13,9 / −5,8 / +16,7 / +2,9.
- **Cohérence avec les cas-types.** Au barème proposé, un retraité seul paie entre 18,5 % et 20,5 % de sa pension (12 000 à
  30 000 €). Pour 17,5 millions de pensionnés (cases 1AS et 1BS des déclarations 2042), +13 Md€ ne ferait que 740 € par
  pensionné. Avec +32 Md€, on arrive à environ 1 830 € par pensionné, ce qui est compatible avec les cas-types (+2 830 à
  +3 250 € pour un retraité seul).

**Conclusion touchée.** Le sens du transfert ne change pas (les retraités financent), mais son ampleur est 2,5 fois plus
forte : environ 8 % de la masse des pensions, et non 3 %.

### Grave 2 : avec des foyers « mélangés », la franchise d'activité profite aussi aux retraités ; la recette n'est pas tenue

**Passage.** Tout ce qui suppose une franchise d'activité non nulle : le tableau 1 (prix de la franchise), le barème proposé
(17 / 22 / 24,2 / 50 %), la perte sèche de 9,3 Md€, les 33 % de perdants, le tableau 2 (familles) et la colonne
« Proposition » du tableau 3. L'encadré dit seulement que le décompte des perdants « sous-estime la dispersion réelle ».

**Pourquoi c'est faux.** Dans une tranche de revenu, chaque adulte reçoit la même composition de revenus : une part
d'activité égale à 1 − NL, soit environ 70 % en moyenne. `impot_type` retire donc min(8 000 €, part d'activité) à tous les
adultes, retraités compris. Comme min(F, ·) est concave (inégalité de Jensen), cette franchise moyenne dépasse toujours la
franchise réelle. Dans le modèle, 38,1 millions d'adultes sur 54,7 ont plus de 8 000 € d'activité, et la franchise
accordée atteint **360 Md€** (`franchise_masse.py`). Pour comparaison, les déclarations 2042 comptent environ 30 millions
de salariés (1AJ, 1BJ, PAC). Ce chiffre de comparaison est un ordre de grandeur, pas une microsimulation.

**Ampleur (borne).** Avec des foyers spécialisés, soit tout en activité soit tout en pensions et chômage, dans les mêmes
proportions par tranche, le barème publié rapporte **243,3 Md€, soit 23,2 de plus que la cible** (`specialise.py`). Pour
l'étape 3, sans franchise, l'écart est nul. Pour retrouver 220 Md€ dans cette borne, t1 devrait tomber de 24,2 % à 15,6 %,
sous le taux de 22 % à 20 000 €, donc hors de la famille de barèmes. La perte sèche descendrait à 6,2 Md€, au lieu de 9,3
(`specialise_cale.py`). La réalité se situe entre les deux représentations.

**Conclusions touchées.** La proposition n'est pas démontrée « à rendement inchangé ». Ses taux sont probablement trop
hauts. Le « prix » de la franchise (environ 0,5 Md€ de perte sèche par millier d'euros, tableau 1) est surestimé : à
l'extrême, environ 1 Md€ pour 8 000 €, et non 4,1. Il faut refaire le calcul sur des foyers séparés selon la source de
revenu, ou en microsimulation. La note courte `note-efficace.tex` (`systeme_efficace.impot_franchise`, franchise de
10 000 € sur le travail) repose sur le même mélange et a donc le même défaut ; elle n'a pas été vérifiée ici.

### Moyen 3 : les « parents isolés » sont deux fois trop nombreux dans le modèle, et le quotient familial des enfants est surévalué d'environ 1 Md€

**Passage.** Section famille : « 13,9 Md€ dans notre modèle [...], dont 9,7 pour les couples et 4,2 pour les parents
isolés » ; ligne « Parents isolés » du tableau 2 ; chèque de 772 € par enfant.

**Pourquoi c'est faux.** Le modèle compte 4,0 millions de personnes seules avec un enfant. `ir_actuel` leur accorde à
toutes la case T, soit 2 parts pour un enfant et un plafond de 4 224 €. Or les déclarations 2042 ne comptent que
**1 965 339 cases 0BT** (`donnees/ir_2042_cases_revenus2024.csv`). La dépense fiscale 110110 (demi-part des parents isolés)
vise 1,71 million de ménages pour 865 M€. Les autres sont surtout des concubins, qui n'ont droit qu'à une demi-part par
enfant. L'Insee trouve 2,0 Md€ pour les familles monoparentales en 2017, contre 4,2 dans le modèle.

**Valeur juste (recalcul `verif.py`).** Avec 1,97 million de cases T et les autres foyers à 1,5 part : 3,3 Md€ pour les
parents isolés au lieu de 4,2. Le total passe à **12,9 Md€** au lieu de 13,9, et le chèque à **environ 720 €** au lieu de
772. Le libellé « Parents isolés » couvre aussi des concubins. Enfin, la demi-part des parents isolés (0,87 Md€) est comptée
deux fois : dans le quotient familial des enfants (13,9) et dans les « demi-parts spéciales » (2,9 Md€) des niches
supprimées (annexe).

**Conclusion touchée.** Le montant du chèque et la comparaison avec l'Insee changent. Le classement des quatre variantes ne
change pas : la franchise apporte toujours plus aux familles que le quotient.

### Moyen 4 : la perte sèche est basse par rapport à la littérature, et la marge extensive est absente

**Passage.** Encadré (« environ 18 Md€ par an aujourd'hui ») ; étape 4 (« deux fois moins qu'aujourd'hui ») ; tableau 1
(« chaque millier d'euros de franchise [...] coûte environ 0,5 Md€ de perte sèche »).

**Constats (`mcf.py`).**
- La perte sèche actuelle vaut 18,1 Md€, soit 8,2 % de la recette et 0,62 % du PIB (PIB 2024 : 2 935 Md€, comptes
  nationaux du dépôt).
- Le coût marginal des fonds publics implicite du modèle, pour un point de plus partout, est de **1,10** dans le jeu
  central (1,04 à 1,17 selon les élasticités). Kleven et Kreiner (2006, *JPubE* 90, tableau 3) trouvent pour la France
  **1,21** avec des heures seules (élasticité intensive de 0,1, scénario S3) et **1,72** avec la participation (scénario
  S6), sur le coin fiscal complet. Le coût d'opportunité des fonds publics de 1,2 utilisé dans l'évaluation
  socio-économique française n'a été lu que dans une source secondaire. Le modèle se situe donc au plus bas de la
  fourchette, comme le laisse attendre un coin limité à l'IR et à la CSG.
- Avec 10 points de coin non contributif en plus (hypothèse), la perte sèche imputable à l'IR et à la CSG passerait de 18
  à 35 Md€. Le niveau « 18 → 9 » est donc fragile ; la note le dit, mais seulement à l'étape 4.
- Le code ne contient pas de marge extensive. Or c'est en bas de la distribution qu'elle pèse le plus (Kleven et Kreiner,
  tableau 3). La franchise d'activité, justifiée par le « premier emploi », ne peut donc rien gagner dans ce calcul, et son
  coût de 0,5 Md€ par millier d'euros peut avoir le mauvais signe. Le README range la marge extensive dans « Restent à
  faire », mais la note ne le signale pas au tableau 1.
- Le chiffre « plus de 90 % du gain vient du dixième le plus aisé » est confirmé : **93 %** (8,3 Md€ sur 8,9), dont 4,0
  pour le 1 % du haut. Kleven et Kreiner (tableau 4) donnent pour la France un coût de 14,7 quand on relève le taux du
  dernier décile, ce qui est cohérent avec cette concentration.

### Mineur 5 : périmètre et libellé de la comparaison avec l'Insee

**Passage.** « L'Insee trouvait 13,3 Md€ pour les familles avec enfants en 2017, sur 16,6 Md€ pour l'ensemble des
demi-parts familiales. »

Les deux montants sont exacts : 11,3 pour les couples avec enfants plus 2,0 pour les familles monoparentales, soit 13,3 ; et
11,3 représente 68,2 % de 16,6 (André et Sireyjol 2021, p. 34). En revanche, la « familialisation » de l'Insee comprend
« l'ensemble des dispositifs relatifs aux personnes à charge, et pas uniquement le seul mécanisme des parts », y compris
les majorations de crédits et réductions d'impôt (p. 22 et 29). **16,6 Md€ n'est donc pas « l'ensemble des demi-parts ».**
Le chiffre du modèle comparable aux 13,3 Md€ de l'Insee est 16,2 (13,9 plus garde d'enfants et frais de scolarité), et non
13,9. Le champ de l'Insee est aussi plus étroit : France métropolitaine, ménages ordinaires, 66,2 Md€ d'IR simulé en 2017.
La proximité entre 13,9 et 13,3 est en partie une coïncidence, puisque les parents isolés sont surestimés et les couples
sous-estimés (point 3).

### Mineur 6 : le quotient conjugal est crédité d'un effet qui ne lui revient pas

**Passage.** « Le quotient conjugal, lui, profite surtout aux couples sans enfant (450 € de moins). »

Les −454 € mesurent l'écart avec la charge d'aujourd'hui, pas l'effet du quotient conjugal. Dans la variante « rien »
(impôt individuel), les couples sans enfant gagnent 495 €, donc davantage. À barème égal, le quotient conjugal leur vaut
359 € en moyenne (2,2 Md€, `verif.py`), mais le barème plus haut qu'il impose leur en reprend plus que cela.

### Mineur 7 : choix de code dans le calcul de la perte sèche (fonction `systeme`)

Voir la section 3. Ces choix vont tous dans le même sens et sont petits : ils sous-estiment le gain, qui passerait
d'environ 8,9 à 10 Md€.

### Arrondis douteux et incohérences de détail

| Passage | Écrit | Recalcul / source | Remarque |
|---|---|---|---|
| Étape 2, « 26 % à 30 000 € » | 26 % | t1 = 25,51 % (JSON) | La note de figure `x02` et le README disent 25,5 % ; à harmoniser |
| Très hauts revenus, « IR actuel d'environ 23 % » | 23 % | Au-delà de 3 M€ (convention mixte) : 21,5 % de l'assiette brute, 25,4 % du revenu du barème ; au-delà de 9 M€ : 19,7 / 23,0 % | 23 % ne se retrouve qu'au-delà de 9 M€ et rapporté au revenu fiscal ; préciser le dénominateur |
| Famille, « elle vaut de 1 300 à 1 550 € par enfant » | 1 300 à 1 550 € | 1 275 € à 20 k€, 1 437 € à 45 k€, 1 570 € à 90 k€, 1 598 € à 100 k€ ; moins de 1 275 € sous 20 k€ | Fourchette valable pour un parent entre 20 et 85 k€ environ |
| Section 1, « 40 % au-delà de 110 000 € » | 110 000 € | Saut entre 110 et 115 k€ (31,9 → 40,1 %), vers 113,6 k€ | Acceptable (« vers 114 000 € ») |
| Annexe, OCDE, « écart de 0,1 à 0,4 point » | 0,1–0,4 | Taux moyen d'une personne seule : écart de 0,00 à 0,15 point (médiane 0,08) avec `ocde_taxing_wages_2025_seul.csv` | L'annexe cite *Taxing Wages 2026*, mais le fichier du dépôt porte « 2025 » |
| Annexe, IR au PFU « environ 10,5 Md€ » | 10,5 | Note sous le tableau : 10,2 + 0,4 = 10,6 | Arrondi incohérent à 0,1 près |
| Références, « Gethin et Saez (2026), NBER WP 34217 » | 2026 | Document de travail de septembre 2025, publié dans *QJE* 141(4) en 2026 | Citer soit le document de travail de 2025, soit l'article du *QJE* |
| Annexe, « Part moyenne de la femme : 36 % » | 36 % | Exact pour l'Insee (IP 1492) ; le partage du modèle donne 29,5 % au second revenu | Ce n'est pas un résultat du modèle |

---

## 2. Ordres de grandeur

| Grandeur | Modèle ou note | Repère externe | Verdict |
|---|---|---|---|
| IR 2024 | 91,7 Md€ (IRCOM), dont 80,2 hors capital | DGFiP 92 ; comptes nationaux D51 IR 96,2 (2024, `ntl_france.csv`, ce qui inclut les prélèvements libératoires) | OK |
| CSG | 132,4 dans le champ ; 153 au total (introduction) | Comptes nationaux 2024 : 153,1 | OK ; l'écart de 20 Md€ correspond à la CSG sur le capital et à divers |
| CRDS | 7,4 dans le champ ; 9 au total | Comptes nationaux 2024 : 9,08 ; CADES 9,2 (non vérifié) | OK |
| Salaires (assiette brute) | 994 Md€, soit 1 012 brut | Eurostat D11 reçus par les ménages : 1 137 (`robustesse.txt`, y compris non-déclarants et salaires étrangers) | OK |
| Pensions brutes | 406 Md€ (2024) | DREES : 370 Md€ en 2023 pour les régimes obligatoires de retraite ; ESSPROS 412 en 2023, invalidité comprise ; revalorisation de +5,3 % en 2024 | Plausible, un peu bas (environ −5 % face à ESSPROS revalorisé) |
| Allocations chômage | 37,2 net, 38,7 brut (cases 1xP, préretraites comprises) | Unédic 2024 : 35,9 Md€ d'allocations et d'aides (résumé de recherche) ; s'y ajoutent l'ASS et les préretraites | OK |
| Foyers | 41,6 M | IRCOM 41,6 M ; 9YF : 41,6 M | OK |
| Couples | 13,05 M | Totaux 2042 (couples mariés ou pacsés) | OK |
| Enfants | 18,0 M | 0CF 15,15 + 0DJ 2,01 + 0CH / 2 = 0,84, soit 18,0 | OK |
| Parents isolés | 4,0 M foyers avec case T | 0BT : 1,97 M | **ERREUR** (point 3) |
| Coût du quotient familial | 13,9 Md€ | Insee : 13,3 (2017, champ plus large en dispositifs, plus étroit en population) ; 16,6 pour l'ensemble de la familialisation | Dans la fourchette 13–17, mais par compensation (points 3 et 5) |
| Perte sèche actuelle | 18,1 Md€ = 8,2 % de la recette = 0,62 % du PIB | Coût marginal des fonds publics en France : 1,21 à 1,72 (Kleven et Kreiner 2006) ; modèle : 1,10 | Bas (point 4) |
| Taux marginaux d'aujourd'hui | Personne seule : 31,9 % à 50 k€, 40,1 % au-delà d'environ 114 k€ | OCDE *Taxing Wages* (fichier du dépôt) : 31,96 % à 110 % du salaire moyen, 40,18 % à 250 % ; salaire moyen 45 964 € | OK (écart inférieur à 0,1 point) |
| Taux supérieur actuel | 55 % | OpenFisca : 54,7 % pour une personne seule à 450 k€ | OK |
| Retraité seul à 17 000 €, proposition | +3 250 € (19 % de la pension) | Minimum vieillesse 2026 : 12 523,14 € par an (source de presse) | Exact ; la note signale elle-même le problème du minimum vieillesse |
| Pensions, proposition | +13,0 Md€ | Borne d'au moins +28 Md€ ; environ +32 dans le modèle | **ERREUR** (point 1) |
| Recette de la proposition | 220,1 Md€ | 220 à 243 Md€ selon la composition des foyers | **ERREUR** (point 2) |

**Sommes par décile et par type.** Les déciles n'ont pas tous le même poids (4,03 à 4,27 M de foyers). Pondérées, les
variations par décile s'annulent exactement (0,0 Md€) dans les étapes 1 à 3 et dans la proposition, comme l'exige la
recette constante. La moyenne simple des dix déciles ne s'annule pas (−7 à +13 € par foyer) ; c'est normal. Les
variations par type de foyer (P6) se compensent aussi à 0,1 Md€ près dans les cinq variantes de la note. Par type de
revenu, les quatre lignes s'additionnent à 0 (+0,1 au plus). En revanche, la répartition est fausse dès que la franchise
d'activité n'est pas nulle (point 1).

**Cas-types et moyennes par type de foyer.**
- Couples avec deux enfants : la moyenne de −966 € se situe entre les cas-types à deux revenus (−1 630 à −2 400 €) et le
  couple à un seul revenu (+1 080 €). C'est cohérent.
- Personnes seules sans enfant : la moyenne de +130 €, alors que tous les cas-types salariés gagnent (−14 à −13 171 €),
  s'explique par la part des retraités. C'est cohérent.
- Pensions : la moyenne implicite de +740 € par pensionné ne colle pas aux cas-types (+2 830 à +3 250 €). C'est
  **incohérent** (points 1 et 2).

---

## 3. Calcul de la perte sèche dans `proposition.systeme`

**Formule.** Pour chaque adulte, la perte vaut ½ · e · (part de l'adulte × Z) · τ² / (1 − τ), avec τ = taux marginal sur
l'assiette nette × R. C'est l'approximation de Harberger et Feldstein (1999), écrite correctement : Z est l'assiette brute
de type CSG et τ est rapporté à l'euro brut. Le revenu Z n'est pas corrigé des réactions, ce qui est l'approximation
usuelle.

**Élasticités.** `v.elast` multiplie, selon le rang du foyer, 0,15 / 0,20 / 0,30 / 0,40 (jeu central ; bas
0,05 / 0,05 / 0,15 / 0,20 ; haut 0,25 / 0,35 / 0,50 / 0,70) par la part du revenu brut qui vient du travail (LAB : salaires,
gérants et 70 % des revenus des indépendants et du foncier). C'est conforme à l'encadré. Les pensions et le chômage ne
réagissent pas.

**Taux marginal retenu.** Dans la réforme, le taux est tm(revenu imposable) pour chaque adulte dont la part d'activité
dépasse la franchise, et 0 sinon. Dans la variante quotient, c'est le taux du couple, ou le taux à 1 ou 2 parts quand le
plafond joue : c'est correct. Pour aujourd'hui, `cout_actuel` prend la médiane de quatre profils actifs OpenFisca (IR et
CSG) au revenu fiscal moyen de la tranche, plafonnée à 60 %.

**Défauts relevés dans le code.**
1. **Foyers mélangés et franchise** (grave, point 2) : l'indicateur d'activité `actif = l > F` et la franchise
   `min(F, l)` sont calculés sur une part d'activité moyenne de la tranche, ce qui fait profiter les retraités de la
   franchise.
2. **`par_type`** (grave, point 1) : la nouvelle charge est répartie au prorata du revenu net, sans tenir compte de la
   franchise.
3. **R = ZN/Z au niveau du foyer** au lieu du rapport net/brut propre au travail (0,90). Cela gonfle τ dans les foyers
   riches en pensions. Perte sèche de la proposition : 9,27 → 8,85 avec le rapport du travail (`sensib_dwl.py`).
4. **La CRDS manque dans le taux actuel** (`marges_openfisca.csv` : IR + CSG seulement), alors qu'elle entre dans le
   nouveau taux. Perte sèche actuelle : 18,14 → 18,84 avec 0,5 point de plus.
5. **Taux actuel uniforme dans une tranche** (au revenu moyen), alors que le nouveau taux est calculé point par point.
   Comme la perte croît avec le carré du taux, cela sous-estime légèrement la perte actuelle.
6. **Coin limité à l'IR, à la CSG et à la CRDS, sans marge extensive** (point 4).
7. **Grille.** L'optimum de la proposition bute sur les bornes de la grille (z1 = 45 k€, son minimum ; z2 = 600 k€, son
   maximum). Les barèmes optimaux varient d'un cas à l'autre (z1 = 45 k€ à 4 000 €, 120 k€ à 6 000 €, 45 k€ à 8 000 €), si
   bien que le « prix » de chaque millier d'euros de franchise est bruité : 0,6 ; 0,3 ; 0,5 ; 0,4. La note le dit pour
   l'étape 3 (« le meilleur des barèmes essayés »), pas pour la proposition.
8. **Indicateur `transferts`** : il atteint 32,7 points pour la variante chèque, car l'impôt devient négatif et l'on divise
   par des revenus faibles. Il n'est pas utilisé dans la note, mais il ne doit pas servir à classer cette variante.

Les défauts 3 à 5 jouent tous dans le même sens, contre la réforme, et sont petits (moins de 1 Md€ chacun). Les défauts 1,
2 et 6 changent les conclusions.

---

## 4. Tableau de tous les nombres vérifiés

Statuts : OK ; ERREUR ; ARRONDI (arrondi douteux) ; NV (non vérifiable avec les sources accessibles).

### Titre, introduction

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Sous-titre : « Trois exercices » | 3 étapes + proposition | Structure de la note | OK |
| En-tête : revenus 2024 « publiés en mai 2026 » | — | IRCOM revenus 2024 | NV (date de publication) |
| IR | 92 Md€ | IRCOM 91,7 | OK |
| CSG | 153 Md€ | Comptes nationaux 2024 : 153,1 | OK |
| CRDS | 9 Md€ | Comptes nationaux 2024 : 9,08 | OK |
| Abattement sur les pensions | 10 % | CGI 158-5-a | OK |
| PLF 1978, abattement unique | 5 000 F | Rapport Blin (Sénat, 1977) non consulté | NV |
| « Près de cinquante ans » | 1978 → 2026 = 48 ans | Arithmétique | OK |
| Coût de l'abattement de 10 % | 5,3 Md€ | Voies et moyens PLF 2026 : 5 322 M€ (`depenses_fiscales_ir_plf2026.csv`) | OK |
| PLF 2027, plafond | 3 000 € par foyer, article supprimé en octobre 2026 | Presse (Selectra, Legifiscal, Moneyvox : suppression le 15 octobre) | OK (sources secondaires) |
| Emploi à domicile créé en | 1991 | Non vérifié | NV |
| Coût de l'emploi à domicile | 7 Md€ | 7 029 M€ | OK |
| Insee : 3 enfants, 10 000 € ↔ 6 250 € | 10 000 / 2,4 UC × 1,5 = 6 250 | Échelle OCDE modifiée | OK |

### Encadré

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Recette remplacée | 220 Md€ | 220,09 (`v.CIBLE`) | OK |
| IR / CSG / CRDS | 80 / 132 / 7 | 80,2 / 132,4 / 7,4 | OK |
| Niches supprimées | ≥ 24 Md€ | 15,5 + 5,3 + 2,9 + 0,5 = 24,2 | OK (dont 0,87 compté deux fois, point 3) |
| Tranches IRCOM | 25 | Fichier IRCOM : 25 lignes | OK |
| Enfants à charge | 18 M | 18,0 | OK |
| Élasticités | 0,15 à 0,40 | `ELAST["central"]` | OK |
| Perte sèche actuelle | ≈ 18 (8 à 31) Md€ | 18,14 (8,15 à 31,12) | OK (niveau bas, point 4) |
| Seuil des perdants | 500 € | Définition | OK |

### Section 1 (aujourd'hui) et figure v01

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Taux d'entrée, personne seule | 9,5 % jusqu'à environ 23 000 € | 9,53 % jusqu'à 23 k€ ; 19,9 % à 23 k€, 21,3 % à 24 k€ | OK |
| Saut | 21 % | 21,3 % | OK |
| « 32 % dès 40 000 € » | 32 % | 31,6 % à 40 k€ | OK |
| « 40 % au-delà de 110 000 € » | 40 % | 40,1 % à 115 k€ (saut vers 113,6 k€) | ARRONDI (seuil) |
| Couple avec deux enfants | 9,5 % jusqu'à 60 000 € | 9,5 % jusqu'à 58 k€, 21,2 % à 60 k€ | OK |
| Retraité, 1 000 € de plus | 620 à 770 € | 617 à 774 € | OK |
| Note v01 : seuil de recouvrement | 61 € | CGI 1657 | OK |
| Note v01 : abattement des plus de 65 ans | vers 33 000 € | Saut à 32,5–33 k€ (marginal 44,7 %) | OK |
| Note v01 : creux du couple | 86 000–95 000 € | 20,5 % à 86 k€, 17,6 % à 90 k€, 19,1 % à 95 k€ | OK |

### Étape 1 et figure x01

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Barème | 0, 11, 30, 41, 45 % | LF 2025, revenus 2024 | OK |
| Franchise par enfant | 6 000 € | `ex.FRANCHISE` | OK |
| Taux proportionnel | 3,0 % | 2,99 % [P1] | OK |
| Barème de l'IR seul | 179 Md€ | 178,9 (`verif.py`) | OK |
| « plus du double des 80 Md€ » | — | 178,9 > 160,4 | OK |
| Reste à trouver | 41 Md€ | 220,1 − 178,9 = 41,2 | OK |
| CSG + CRDS | 140 Md€ | 132,4 + 7,4 = 139,9 | OK |
| Effet redistributif | « d'un quart » | 1,26 [P5] | OK |
| Déciles 5 à 7 | 790 à 870 € | −787 / −848 / −872 [P6] | OK |
| Dernier décile | +3 040 € (2,4 points) | +3 038 ; +2,4 | OK |
| Pensions / chômage | +8,8 / +3 Md€ | +8,8 / +3,0 | OK (sans franchise d'activité, répartition valable) |
| Retraité seul à 17 k€ | 1 110 € | +1 114 [P7] | OK |
| Couple, 80 k€, 60/40 | gagne 4 130 € | −4 130 | OK |
| Couple, un seul revenu | +2 590 € | +2 590 | OK |
| Perdants de plus de 500 € | 14 % | 14 % (5,6 M) | OK |
| Taux marginal | 3 → 12 % vers 13 000 € | 2,7 → 12,4 % ; seuil à 12 960 € brut | OK |
| Taux marginal | 29 % vers 33 000 € | 29,3 % ; seuil vers 33 050 € | OK |
| Taux marginal | 40 % vers 95 000 € | 39,5 % ; seuil vers 94 000 € | OK |
| Perte sèche | 18 Md€ | 18,5 [P5] | OK |
| Note x01 : 21 % vers 60 k€, 18 % à 86–95 k€ | — | 21,3 / 17,6 % | OK |

### Étape 2 et figure x02

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Taux de 5 % au premier euro, 13 % à 20 k€ | 5 / 13 % | JSON | OK |
| « 26 % à 30 000 € » | 26 % | 25,51 % (la note de figure dit 25,5 %) | ARRONDI / incohérence |
| 50 % à 250 000 € | — | JSON | OK |
| Seul à 50 k€ : 32 → 24 % | — | 31,9 → 24,4 % | OK |
| Effet redistributif « le même » | — | 0,97 | OK |
| Perte sèche « d'un quart, à 13 Md€ » | — | 13,3 ; −26 % | OK |
| Pensions | +10,9 Md€ | +10,9 | OK |
| Retraité seul à 17 k€ | 1 430 € | +1 428 | OK |
| Déciles 2 à 4 | +90 à +270 € | +92 / +274 / +165 | OK |
| Déciles 5 à 7 | −280 à −430 € | −391 / −277 / −431 | OK |
| Couple, un seul revenu | +1 540 € | +1 541 | OK |
| Perdants | 13 % | 13 % | OK |
| Taux marginaux de 30 à 120 k€ | 25 à 35 % | 25,5 à 35,5 % | OK |

### Étape 3 et figure x03

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Barème | 14 % / 16 % / 18 % à 120 k€ / 50 % à 600 k€ | 0,14 / 0,16 / 0,1799 / 600 k€ | OK |
| « bute sur les bornes » | z1 = 120 k€ et z2 = 600 k€ au maximum de la grille | `GRILLE_EX` | OK |
| Perte sèche | 5 (2 à 9) Md€ | 5,2 (2,2 à 9,0) | OK |
| « plus de trois fois moins » | — | 18,1 / 5,2 = 3,5 | OK |
| Déciles 2 à 4 | +610 à +1 310 € ; 6 à 8 points | +607 / +1 231 / +1 310 ; 7,7 / 7,5 / 6,0 | OK |
| Dernier décile | −5 380 € | −5 376 | OK |
| Perdants | 57 % | 57 % | OK |
| SMIC | +800 € | +802 | OK |
| Personne seule / couple, 80 k€ | −7 120 / −1 030 € ; 7,6 points | −7 122 / −1 028 ; 7,6 | OK |
| Gain avec élasticités basses / hautes | 6 / 22 Md€ | 8,15 − 2,2 = 5,9 ; 31,1 − 9,0 = 22,1 | OK |

### Étape 4, tableau 1 et figure x04

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Franchise d'activité | 8 000 € | `F_RET` | OK |
| « environ 0,5 Md€ par millier d'euros » | — | (10,1 − 5,2) / 10 = 0,49 dans le modèle | OK au calcul ; **surestimé** (points 2 et 4) |
| Tableau 1, perte sèche | 5,2 / 7,7 / 8,3 / 9,3 / 10,1 | [P5] | OK au calcul ; biaisé dès que F > 0 (point 2) |
| Tableau 1, déciles 2 à 4 | +610 à +1 310 / +170 à +790 / +130 à +570 / +210 à +450 / +290 à +390 | [P6] | OK au calcul |
| Tableau 1, perdants | 57 / 43 / 37 / 33 / 32 % | [P5] | OK au calcul |
| Tableau 1, SMIC | +800 / +340 / +120 / −10 / −190 | +802 / +344 / +122 / −14 / −194 | OK |
| Tableau 1, retraité à 17 k€ | +2 520 / +2 740 / +2 960 / +3 250 / +3 540 | +2 524 / +2 741 / +2 958 / +3 251 / +3 544 | OK |
| SMIC « paie ce qu'il paie aujourd'hui » | −14 € | [P7] | OK |
| Au-delà de 8 000 €, la hausse des déciles 2 à 4 « ne baisse plus » | moyenne 338 → 332 € | [P6] | OK |
| Personne seule / couple, 80 k€ | −4 410 / −1 630 € ; 3,5 points (contre 7,6 et 7,5) | [P7] | OK |
| Barème | 17 / 22 / 24 % à 45 k€ / 50 % à 600 k€ | 0,17 / 0,22 / 0,2422 / 600 k€ | OK au calcul ; recette non tenue (point 2) |
| Perte sèche | 9 (4 à 16) Md€ ; « deux fois moins » | 9,27 (3,88 à 15,92) ; 18,1 / 9,3 = 1,96 | OK au calcul (points 2 et 4) |
| Part du gain venant du dernier décile | > 90 % | 93 % (`verif.py`) | OK |
| Perdants | un tiers, contre 57 % | 32,8 % | OK au calcul |
| Salaires / indépendants / pensions / chômage | −13,3 / −2,6 / +13,0 / +3,0 Md€ | Au prorata de l'imposable : −32,4 / −4,2 / +32,0 / +4,5 ; borne : pensions ≥ +28, chômage ≥ +3,8 | **ERREUR** (point 1) |
| Retraité seul : 17 k€ / 30 k€ | 3 250 / +2 830 € | +3 251 / +2 830 | OK |
| Retraité / salarié, 17 k€ | 3 250 / 1 270 € | 3 251 / 1 266 | OK |
| Retraité / salarié, 30 k€ | 6 140 / 3 600 € | 6 144 / 3 596 | OK |
| Impôt sur 10 000 € de pension | 1 800 € | 1 825 | OK (arrondi à la centaine) |
| Minimum vieillesse | 12 523 € | Allocation de solidarité aux personnes âgées 2026 : 1 043,59 € par mois = 12 523,14 € (presse, d'après la Cnav) | OK |
| Note x04 | 17,0 / 22,0 / 24,2 / 45 000 / 600 000 ; 8 000 € ; 6 000 € | JSON | OK |

### Très hauts revenus

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Majoration de la contribution exceptionnelle | 3 puis 4 points | Taux de la contribution sur les hauts revenus | OK |
| Foyers au-delà de 3 M€ | 3 800 | 3 109 + 695 = 3 804 | OK |
| Hausse en convention centrale | 3 à 6 points | +2,8 / +6,2 (`controle_hauts.txt`) | OK |
| IR actuel prêté au revenu du barème | ≈ 23 % | 21,5 % (assiette brute) ou 25,4 % (revenu du barème) au-delà de 3 M€ | ARRONDI |
| Taux marginal actuel | 49 % | 45 % d'IR + 4 % de contribution | OK |
| 250 k€ à 9 M€, capital en haut | −2 à −6,5 points | −6,5 / −6,3 / −4,6 / −2,3 | OK |
| Taux supérieur | 55 → 50 % | OpenFisca 54,7 % | OK |
| Foyers au-delà de 9 M€ | 700, « autant qu'aujourd'hui » | 695 ; +0,3 point | OK |
| Barème en convention « capital en haut » | 25,4 au lieu de 24,2 % ; perte sèche 9,0 ; 34 % de perdants | 25,41 % ; 9,01 ; 33,7 % (`haut.py`) | OK |

### Famille et tableau 2

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Quotient familial des enfants | ≈ 14 ; 13,9 (9,7 + 4,2) | [P0] | OK au calcul ; **4,2 surestimé** → environ 3,3 ; total environ 12,9 (point 3) |
| Insee 2017 | 13,3 sur 16,6 | André et Sireyjol 2021, p. 34 : 11,3 + 2,0 ; 68,2 % | Valeurs OK ; **libellé faux** (point 5) |
| Aide aux familles | 0 / 20,6 / 13,9 / 3,6 | [P4] | OK |
| Perte sèche | 7,8 / 9,3 / 8,2 / 8,1 | [P3, P5] | OK au calcul |
| Perdants | 33 / 33 / 36 / 31 % | 32,7 / 32,8 / 36,0 / 31,2 | OK |
| Personnes seules sans enfant | −200 / +130 / +50 / −90 | −197 / +130 / +52 / −89 | OK |
| Parents isolés | +1 030 / +340 / +510 / +900 | +1 034 / +339 / +511 / +903 | OK au calcul ; population mal définie (point 3) |
| Couples sans enfant | −500 / +360 / +20 / −450 | −495 / +364 / +24 / −454 | OK |
| Couples avec deux enfants | +530 / −970 / −500 / +190 | +530 / −966 / −495 / +190 | OK |
| Personne seule, 80 k€ | −5 910 / −4 410 / −5 020 / −4 970 | −5 905 / −4 408 / −5 024 / −4 968 | OK |
| Couple, 60/40 | +70 / −1 630 / −520 / −240 | +67 / −1 629 / −520 / −235 | OK |
| Couple, un seul revenu | +2 560 / +1 080 / +1 900 / +1 300 | +2 558 / +1 080 / +1 895 / +1 301 | OK |
| Chèque | 772 € | 13,9 Md€ / 18,0 M | OK au calcul ; environ 720 € après correction (point 3) |
| Plafond du quotient | 1 791 € | Paramètres 2024 | OK |
| Variante « rien » | 530 / 1 030 € ; 7,5 points | [P6, P7] | OK |
| Variante chèque | 234 au lieu de 220 Md€ | 234,0 [P4] | OK |
| Variante chèque, personnes seules | +50 € ; +250 € face à « rien » | +52 ; 52 − (−197) = 249 | OK |
| Variante chèque, couples avec enfants | 500 € | −495 | OK |
| Variante quotient | 3,6 Md€ ; +190 € ; « presque proportionnel entre 20 et 100 k€ » | [P4, P6] ; taux marginal de 22 à environ 26,6 % | OK |
| Quotient conjugal | « 450 € de moins » | −454 face à aujourd'hui ; le quotient conjugal seul vaut 359 € | ERREUR d'attribution (point 6) |
| Valeur de la franchise par enfant | 1 300 à 1 550 € | 1 275 à 1 598 € de 20 à 100 k€ | ARRONDI |
| Point d'égalité avec le plafond du quotient | ≈ 170 000 € | 166 k€ | OK |
| Total familles | 20,6 au lieu de 13,9 (16,2) | 13,9 + 1,80 + 0,23 + 0,23 = 16,15 | OK |
| Surcroît de perte sèche | 1,1 à 1,5 Md€ | 9,3 − 8,2 / 8,1 / 7,8 | OK |

### Tableau 3 (synthèse)

| Ligne | Écrit | Recalcul | Statut |
|---|---|---|---|
| Taux marginal, personne seule à 50 k€ | 31,9 / 29,6 / 24,4 / 14,8 / 21,1 | 31,93 / 29,6 / 24,4 / 14,8 / 21,1 (`verif.py`, lissé) | OK |
| Perte sèche | 18 / 18 / 13 / 5 / 9 | 18,1 / 18,5 / 13,3 / 5,2 / 9,3 | OK (proposition : point 2) |
| Effet redistributif | 100 / 126 / 97 / 21 / 75 | 1,26 / 0,97 / 0,21 / 0,75 | OK |
| Perdants de plus de 500 € | 14 / 13 / 57 / 33 | [P5] | OK |
| Perdants de plus de 1 000 € | 11 / 8 / 32 / 11 | [P5] | OK |
| Gagnants de plus de 500 € | 38 / 21 / 17 / 16 | [P5] | OK |
| Déciles 2 à 4 | −80 à −150 / +90 à +270 / +610 à +1 310 / +210 à +450 | [P6] | OK |
| Dernier décile | +3 040 / +760 / −5 380 / −1 440 | +3 038 / +764 / −5 376 / −1 436 | OK |
| Pensions | +8,8 / +10,9 / +16,7 / +13,0 | Les étapes 1 à 3 sont exactes ; **proposition : environ +32** | **ERREUR** (point 1) |
| Retraité seul, 17 k€ | +1 110 / +1 430 / +2 520 / +3 250 | [P7] | OK |
| SMIC | −650 / −370 / +800 / −10 | −646 / −368 / +802 / −14 | OK |
| Personne seule, 80 k€ | −1 910 / −3 390 / −7 120 / −4 410 | [P7] | OK |
| Couple, 60/40 | −4 130 / −2 880 / −1 030 / −1 630 | [P7] | OK |
| Couple, un seul revenu | +2 590 / +1 540 / −690 / +1 080 | [P7] | OK |

### Transition, risque constitutionnel, références

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Taux individualisé par défaut | 1er septembre 2025, LF 2024 art. 19 (loi n° 2023-1322) | Conforme à ce que je sais ; non vérifié en ligne | NV |
| Convergence sur quatre ans | environ 800 € par an | 3 251 / 4 = 813 | OK |
| Décisions du Conseil constitutionnel | 2000-437 DC ; 2012-662 DC | Objets conformes (réduction de CSG ; contribution sur les très hauts revenus d'activité) | OK (de mémoire) |
| Variante quotient | 8,1 Md€ | [P5] | OK |
| Loi n° 77-1467, art. 3 ; rapport Sénat n° 88 | — | Non consultés | NV |
| Martínez, Saez et Siegenthaler, *AER* 111(2) ; Chetty et al., *QJE* 126(2) ; Feldstein, *REStat* 81(4) | — | Références usuelles | OK (de mémoire) |
| Gethin et Saez (2026), NBER 34217 | — | Document de travail de 2025 ; *QJE* 2026 | ARRONDI (année) |

### Annexe

| Passage | Nombre | Source / recalcul | Statut |
|---|---|---|---|
| Dépenses fiscales de l'IR | 44 Md€ | 43,98 (CSV, PLF 2026) | OK |
| Réductions et crédits | 15,5 (7,0 / 2,2 / 1,8 / 1,5 / 1,3) | 15,50 ; 7,03 / 2,20 / 1,80 / 1,46 / 0,83 + 0,43 | OK |
| Abattement sur les pensions / demi-parts / plus de 65 ans | 5,3 / 2,9 / 0,5 (0,4) | 5,32 / 2,85 / 0,48 (0,42) | OK (la demi-part des parents isolés est comptée deux fois, point 3) |
| « jusqu'à 12 Md€ de plus » | 12 | 9,27 + 2,17 + 0,56 = 12,0 | OK |
| Allègement sur les revenus étrangers | 3,8 Md€ | Absent du CSV | NV |
| IR du champ / contribution exceptionnelle / contribution différentielle | 80 ; 1,4 (2023) ; 0,4 (2025) | 80,2 ; le reste n'est pas vérifiable ici | OK / NV / NV |
| CSG + CRDS dans le champ | 132 et 7,4 | 132,4 / 7,4 | OK |
| IR au PFU | ≈ 10,5 (le modèle retire 11,5) | 0,128 × 90 = 11,52 ; note PFU 10,2 + 0,4 = 10,6 | ARRONDI |
| Prélèvements sur le capital | 9,2 / 0,5 / 7,5 % ; ≈ 33 Md€ | Taux de 2024 exacts ; montant estimé | OK / NV |
| CASA / CRDS sur prestations et jeux | ≈ 1 / 0,5 Md€ | Estimations | NV |
| Note de l'annexe : « environ 1 Md€ de trop » | 11,5 − 10,6 = 0,9 | Arithmétique | OK |
| Cases 2042 / IRCOM | 925 / 930 ; 391 / 393 | 925,4 / 930,5 ; 391,5 / 392,8 | OK |
| IR | 91,7 contre 92 | IRCOM | OK |
| CSG sur les salaires | 72,2 + 19,8 = 92,0 ; 91,5 reconstitués | 91,46 | OK (comptes de la Sécurité sociale non consultés) |
| CRDS | 9,2 dont 7,7 ; 7,4 reconstitués | 7,44 | OK (rapport CADES non consulté) |
| Pensions | 412 (2023) ; 406 reconstitués | 406,4 | OK (voir les ordres de grandeur) |
| Seuils de l'IR | 11 497 / 29 315 / 83 823 / 180 294 | LF 2025 | OK |
| Revenu après cotisations | 88,7 % du brut | 88,7 % au SMIC, 88,6 % à 50 k€ | OK |
| OCDE | 0,1 à 0,4 point | 0,00 à 0,15 point (fichier 2025) | ARRONDI / NV (édition citée) |
| Part de la femme dans les revenus du couple | 36 % | Insee Première 1492 : « 36 % » | OK (chiffre Insee, pas résultat du modèle) |

---

## Sources consultées

- André M. et Sireyjol A. (2021), *Économie et Statistique* 526-527, p. 22, 27-29, 30-34 :
  https://www.insee.fr/fr/statistiques/fichier/5430839/02_ES526-527_Andre-Sireyjol_FR.pdf
- Kleven H. et Kreiner C. (2006), *Journal of Public Economics* 90, tableaux 3 et 4 :
  https://www.henrikkleven.com/research/published/kleven-kreiner_jpube2006.pdf
- Insee Première 1492 (Morin, 2014) : https://www.insee.fr/fr/statistiques/1281400
- DREES, *Les retraités et les retraites 2025*, fiche 10 (370 Md€ en 2023) :
  https://drees.solidarites-sante.gouv.fr/sites/default/files/2025-07/Fiche%2010%20-%20Les%20masses%20financi%C3%A8res%20relatives%20aux%20pensions%20de%20retraite.pdf
- Allocation de solidarité aux personnes âgées en 2026 :
  https://www.moneyvox.fr/retraite/actualites/106807/minimum-vieillesse-voici-le-montant-officiel-de-aspa-a-partir-du-1er-janvier-2026
- PLF 2027, abattement des retraités : https://www.legifiscal.fr/actualites-fiscales/4663-plf-2027-abattement-10-retraites-plafonne-3000.html ;
  https://selectra.info/finance/actualites/marche/budget-2027-vote-20-octobre-impot-mesures-votees
- Gethin et Saez, NBER WP 34217 : https://www.nber.org/papers/w34217
- Unédic 2024 (allocations et aides : 35,9 Md€, d'après le résumé de recherche ; non lu à la source) : https://www.unedic.org
- Données du dépôt : `donnees/ir_2042_cases_revenus2024.csv` (0BT, 1AJ, 1AS…), `donnees/ntl_france.csv` (comptes
  nationaux 2024), `ir_csg/sorties/depenses_fiscales_ir_plf2026.csv`, `ir_csg/sorties/robustesse.txt`,
  `ir_csg/sorties/ocde_taxing_wages_2025_*.csv`.

**Non vérifié** : le coût d'opportunité des fonds publics de 1,2 n'a été trouvé que dans une source secondaire ; les
chiffres des comptes de la Sécurité sociale, de la CADES, de la contribution exceptionnelle et de la contribution
différentielle, de l'allègement de 3,8 Md€ et de la note PFU n'ont pas été rapprochés de leurs sources ; les cas-types
OpenFisca n'ont pas été recalculés (seul `courbes_openfisca.csv` a été relu).
