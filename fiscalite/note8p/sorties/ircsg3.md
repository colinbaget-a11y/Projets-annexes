# Bloc IR-CSG-CRDS, v3 : un barème continu, et où va l'argent de l'élargissement

Compte rendu pour l'assembleur (révision v3, 18/11/2026). Chiffres : `sorties/ircsg3.json`, `sorties/ircsg3_calculs.txt`.
Scripts (python3, depuis `fiscalite/`) : `note8p/calculs/ircsg3_droit.py` (droit 2025 simulé, validé sur OpenFisca),
`ircsg3_modele.py` (foyers purs v2 + familles de 1 à 4 enfants + frais réels + barème continu), `ircsg3_cascade.py`
(décomposition), `ircsg3_baremes.py` (candidats), `ircsg3_proposition.py` (tout le reste), `ircsg3_figures.py`.
Les scripts v2 (`ircsg_*.py`) sont réutilisés, pas modifiés. Statuts : [E] empirique, [S] simulation, [H] hypothèse, [C] choix.

**Changements de méthode décidés par l'auteur et appliqués.** (1) Cadre standard de perte sèche : chacun réagit à sa
rémunération nette, tous prélèvements (CSG comprise) pleinement pris en compte aujourd'hui comme demain ; un jeu
d'élasticités central (méthode v2), bornes basse/haute sur les seules élasticités ; plus aucune « perception de la CSG ».
La note de saillance n'a pas été attendue (`sorties/saillance.md` n'existait pas) et n'est pas utilisée. (2) Frais
professionnels : forfait de 10 % supprimé, **frais réels gardés** (35,2 Md€ déclarés en 2024, cases 1AK et 1BK [E],
répartis au prorata des revenus d'activité [H]) ; ils coûtent environ 7,8 Md€ par rapport à la v2, qui ne les déduisait
pas. (3) Familles de 1, 2, 3 et 4 enfants (Insee, RP 2022 : 43,5 / 38,6 / 13,1 / 4,8 % des familles avec enfants de moins
de 25 ans [E] ; même répartition pour couples et parents isolés, à tout revenu [H]).

## 1. Où vont les recettes (graphique F)

**La recette à tenir de la v2 était nette des niches.** Le modèle part de l'« impôt net » de l'IRCOM (DGFiP : après
réductions et crédits d'impôt, restitutions comprises). Le nouvel impôt, sans niche, n'a donc qu'à rapporter l'impôt
net : la suppression des réductions, crédits et exonérations finance déjà la réforme, par construction, sans être
comptée une seconde fois. Ce que la v2 ne montrait pas, c'est combien. La v3 simule le droit 2025 sans niche sur les
foyers du modèle (`ircsg3_droit`, écart moyen à OpenFisca de 0 à 4 € par foyer pour les salariés, 14 à 22 € pour les
retraités, à cause des seuils de CSG) puis retire les mesures une à une. Ordre : niches, avantages des retraités,
unité d'imposition, assiette ; puis les coûts. L'ordre change le montant de chaque marche (le quotient familial,
mesuré après l'individualisation, vaut plus que mesuré avant), pas le total.

| Étape (Md€ 2025, statique) | Total | Actifs | Retraités | D1-D5 | D10 | 1 % |
|---|---|---|---|---|---|---|
| Charge observée du périmètre (IR barème net, CSG, CRDS) | 229,9 | | | | | |
| 1. Réductions, crédits, exonérations, demi-parts, frais réels au-delà du forfait | +27,1 | +19,0 | +8,1 | +3,8 | +13,4 | +3,2 |
| 2. Abattement de 10 % sur les pensions | +7,3 | 0 | +7,3 | +1,3 | +1,1 | +0,1 |
| 3. Abattement des personnes âgées (157 bis) | +0,6 | 0 | +0,6 | +0,5 | 0 | 0 |
| 4. CSG des retraités alignée (9,2 % + 0,5 %) | +7,9 | 0 | +7,9 | +5,3 | +0,5 | 0 |
| 5. Fin du quotient conjugal | +12,1 | +8,2 | +4,0 | +0,1 | +6,8 | +1,7 |
| 6. Fin du quotient familial | +16,2 | +16,2 | 0 | +0,2 | +8,2 | +1,2 |
| 7. Fin de la CSG déductible | +24,1 | +17,8 | +6,3 | +1,6 | +11,4 | +3,4 |
| 8. Fin du forfait de 10 % (frais réels gardés) | +16,9 | +16,9 | 0 | +1,2 | +8,0 | +1,5 |
| **Élargissement total** | **+112,2** | **+78,1** | **+34,2** | | | |
| 9-10. CEHR du barème absorbée ; invalidité-dépendance gardée | −1,6 | | | | | |
| 11. Franchise de 6 000 € par enfant | −18,1 | −18,1 | 0 | −0,6 | −8,3 | −1,4 |
| 12. Nouveau barème (C2) | −92,5 | −72,1 | −20,3 | −13,4 | −35,8 | −8,8 |
| **Variation nette** | 0 | **−12,1** | **+13,8** | 0,0 | +5,4 | +0,9 |

Lecture de l'étape 1 [S]/[E] : 27,1 Md€ d'écart entre le droit simulé sans niche et l'impôt observé, contre 30,4 Md€
dans les Voies et moyens (PLF 2026, t. II, coût 2025 : réductions et crédits 15,5 dont emploi à domicile 7,0, dons 2,2,
garde d'enfants 1,8, Pinel-Duflot 1,5, Girardin 0,8 ; exonérations salariales 9,3 dont épargne salariale 2,9 et heures
supplémentaires 2,2 ; demi-parts spéciales 2,9 ; foncier 2,2 ; indépendants 0,6), somme que l'annexe elle-même dit
« dépourvue de réelle signification » (interactions). L'ordre de grandeur concorde ; le partage fin de l'étape 1 n'est
pas identifiable dans le modèle. On n'ajoute aucun montant des Voies et moyens au calcul : il n'y a pas de double compte.
Deux points restent : la réduction pour revenus de source étrangère (3,8 Md€, DGFiP n° 41) est dans l'impôt net mais
ne peut être supprimée (conventions) ; si la moitié porte sur des revenus du barème, la recette à tenir monte de 1,9 Md€
(+0,18 point sur le bas et le milieu du barème). L'épargne retraite déductible (10,8 Md€) est gardée à toutes les
étapes : elle est réintégrée à la sortie (rente imposée), la retirer taxerait deux fois la même épargne.

**Réconciliations demandées.** (a) 11,3 contre 12,9 Md€ : en v2, les actifs payaient 11,30 Md€ de moins ; la figure de
bouclage ajoutait la CEHR absorbée (0,58) et l'invalidité-dépendance (1,03) : 12,91 = 12,88 payés en plus par les
retraités. En v3 : actifs −12,15, CEHR −0,58, invalidité −1,03, soit −13,76 = +13,76 des retraités. (b) Les 4,0 Md€
d'IR non attribués (IR imputé au capital par la convention de 12,8 %, 12,4 Md€, moins 8,4 Md€ d'IR au PFU mesuré par
le bloc capital) : **convention retenue**, ils restent au bloc capital (IR des dividendes et intérêts imposés au barème
par option, hors de notre périmètre) [H]. Sensibilité : s'ils relevaient du barème, +4 Md€ à tenir, +0,38 point sur
le bas et le milieu, gain au Smic ramené de 28 à 23 € par mois.

**La question de l'auteur : comment élargir de 112 Md€, prendre 14 Md€ aux retraités, et ne rendre que quelques euros
aux salariés modestes ?** Parce que l'élargissement ne tombe presque pas sur eux et que le barème le rend surtout au
milieu et en haut. Les cinq premiers déciles ne portent que 14 Md€ de l'élargissement (dont 7 sur les retraités
modestes : CSG et abattement) ; le dixième le plus aisé en porte 49 (niches, quotients, CSG déductible, forfait, dont
la valeur croît avec le taux marginal). Un barème à recette égale rend ensuite l'argent là où il a été pris : avec l'ancien barème (5/20/28/45,
passé dans la même cascade), 48 % de la baisse de barème (47,7 sur 100 Md€) allait au dixième supérieur (gagnant net de
2,9 Md€ dans la v2 publiée), et le salarié au Smic, qui n'avait ni niche ni quotient à perdre, ne récupérait que l'équivalent de sa CSG déductible et de
son forfait. En v3, le dixième supérieur reçoit 39 % de la baisse de barème et paie au total 5,4 Md€ de plus.

## 2. Barèmes candidats [C]/[S]

Forme retenue, inspirée du tarif allemand (§ 32a EStG, tarif 2025 : zone 2 de 12 097 à 17 443 €, impôt
(932,30·y + 1 400)·y avec y = (revenu − 12 096)/10 000 ; zone 3 jusqu'à 68 480 €, (176,64·z + 2 397)·z + 1 015,13 ; puis
0,42·revenu − 10 911,92 et 0,45·revenu − 19 246,67 au-delà de 277 826 € ; lu sur finanz-tools.de, qui cite la loi du
30/12/2024, le site du ministère étant indisponible) : le taux marginal monte en ligne droite (14 % → 24 % → 42 %), d'où
un impôt polynomial par zones. Ici : taux marginal affine entre six points en revenu après cotisations par adulte, impôt
= intégrale. Calage à recette constante par le point où le plafond est atteint (Zp).

| Barème (recette constante) | 0 / 1 / 1,5 / 2 / 3,5 Smic → plafond | Zp | Smic | 1,5 S | 2 000 € net | 3 S | 120 k€ | 250 k€ | Retraité 12 / 16 / 20 / 30 / 60 / 100 k€ (€/an) | Gain d'efficacité (bas–haut) | 10 % / 1 % (Md€) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 plafond 45 | 2/16/23/29/37 → 45 % | 152 k€ | −28 | −47 | −45 | −123 | −55 | −363 | +766/+1 254/+1 000/+597/−972/−1 103 | 2,55 (1,13–5,64) | +5,3 / +0,2 |
| **C2 plafond 48** | 2/16/23/29/36 → 48 % | 163 k€ | −28 | −47 | −45 | −129 | −81 | −183 | +766/+1 254/+1 000/+597/−1 054/−1 414 | 2,51 (1,10–5,49) | +5,4 / +0,9 |
| C3 plafond 50 | 2/16/23/29/37 → 50 % | 295 k€ | −28 | −47 | −45 | −123 | −81 | −542 | +766/+1 254/+1 000/+597/−972/−1 306 | 2,64 (1,17–5,85) | +5,3 / +0,5 |
| C4 montée précoce | 0/16/24/30/38 → 48 % | 95 k€ | −44 | −59 | −58 | −111 | +153 | +215 | +601/+1 068/+809/+466/−804/+860 | 1,37 (0,51–2,66) | +10,4 / +2,9 |
| T2 tranches de 3 points (16 taux) | suit C2 | | −28 | −46 | −45 | −129 | −75 | −226 | ≈ C2 | 2,52 | +5,3 / +0,7 |
| Ancienne 5/20/28/45, recalée | | | −2 | −18 | −11 | −140 | −496 | −908 | +600/+1 400/+1 340/+972/−1 331/−5 503 | 3,69 (1,76–8,68) | −3,2 / −3,0 |

Gains des salariés seuls en € par mois (− = baisse d'impôt). Gain d'efficacité : baisse de perte sèche réelle, Md€ par
an, jeu central (bornes : élasticités basses et hautes). Leçons. (1) Le plafond (45, 48 ou 50 %) ne pèse presque rien
sur la recette (1 point de plafond : 0,48 Md€) ni sur l'efficacité ; c'est la pente entre 2 et 5 Smic qui compte.
(2) Une montée précoce (C4) donne 16 € de plus par mois au Smic mais relève le taux marginal des cadres intermédiaires
à 38-45 % dès 70 000 €, fait payer plus le haut (+10 Md€ au dixième) et divise le gain d'efficacité par deux. (3) Les
tranches rapprochées font aussi bien que le continu à 1 point près, avec 16 taux ; le continu se décrit en six nombres.
(4) L'ancienne proposition est plus « efficace » au sens du modèle (+1,2 Md€) parce qu'elle taxe à 28 % de 37 000 à
120 000 € ; mais elle donne 40 % des baisses au dixième supérieur (22 % pour C2), rien au Smic et 5 500 € au retraité à
100 000 €. Sans pondération d'équité, le modèle mène toujours à un barème plat : le choix est un choix de politique.

**Pourquoi le Smic ne gagne « que » 28 € par mois, et pourquoi le financement externe n'y change presque rien.** La
baisse du taux moyen au Smic profite à tous les adultes au-dessus du Smic (55 M d'adultes dans le modèle) : un point de
taux sur le bas et le milieu du barème coûte 10,5 Md€, et 1 Md€ de financement externe ne donne que 1,1 € par mois au
Smic. Pour faire gagner 60 € par mois au Smic à recette constante, il faut porter le taux marginal à 40 % dès 2 Smic
(grille explorée) : le gain d'efficacité devient négatif. Cibler les bas salaires relève des allègements et de la prime
d'activité, pas du barème d'un impôt universel. Bozio et Wasmer (2024, rapport au Premier ministre, lu sur
vie-publique.fr) [E] : entre 1 et 1,6 Smic, 100 € de coût du travail en plus ne laissent que 41 € de salaire net ; le
taux marginal effectif médian culmine à 63 % vers 1,1 Smic, par l'entrée dans l'IR et la dégressivité de la prime
d'activité. C2 supprime la marche d'entrée dans l'IR à 1,1 Smic (10,7 → 23,7 % aujourd'hui) : 16 % au Smic, 23 % à
1,5 Smic, en ligne droite ; la contrepartie est un taux plus élevé entre 0,7 et 1,1 Smic (11 à 17 % contre 10,7 %).

## 3. Recommandation : C2, à recette constante [C]

**Barème.** Taux marginal 2 % au premier euro, 16 % à 19 200 € (1 Smic), 23 % à 28 800 € (1,5 Smic), 29 % à 38 400 €
(2 Smic), 36 % à 67 100 € (3,5 Smic), puis 48 % atteint à 163 400 €, constant au-delà ; ligne droite entre ces points ;
impôt individuel ; franchise de 6 000 € par enfant. Taux marginaux comparés (salarié seul, revenu après cotisations) :
19 200 € : 10,7 → 15,9 % ; 25 000 € : 23,8 → 20,3 % ; 38 400 € : 35,8 → 29,0 % ; 50 000 € : 35,6 → 31,8 % ; 67 000 € :
35,6 → 36,0 % ; 100 000 € : 35,6 → 40,1 % (plus haut qu'aujourd'hui de 67 000 à 101 000 €) ; 120 000 € : 44,6 → 42,6 % ;
300 000 € : 54,9 → 48 %. Pas de saut nulle part.

**Versions financées** (baisse des taux du bas et du milieu, points 0 à 3,5 Smic) :

| Version | Taux 0/1/1,5/2/3,5 Smic | Smic | 1,5 S | 2 000 net | 3 S | 120 k€ | Gain d'eff. | Participation |
|---|---|---|---|---|---|---|---|---|
| F0 (recette constante) | 2,0/16,0/23,0/29,0/36,0 | −28 €/mois | −47 | −45 | −129 | −81 | 2,51 | +419 k |
| F3 (−3 Md€) | 1,9/15,7/22,7/28,7/35,9 | −31 | −53 | −50 | −140 | −98 | 2,73 | +434 k |
| F6 (−6 Md€) | 1,7/15,4/22,4/28,4/35,7 | −35 | −59 | −55 | −152 | −115 | 2,96 | +449 k |

**Nous recommandions F0** (avant la décision de bouclage, § 7). 3 Md€ de financement externe rapportent 0,22 Md€ de perte sèche en moins (7 centimes par
euro) et 3 € par mois au Smic : un mauvais emploi d'un milliard qui manque ailleurs (moindre hausse foncière, transition
de l'amortissement à l'IS). F3 est une option de confort si l'assembleur a une marge sans meilleur usage. Coûts
unitaires : 1 point sur tous les taux 13,7 Md€ ; sur le bas et le milieu 10,5 ; 1 point de plafond 0,48 ; 1 000 € de
franchise par enfant 3,0 Md€.

**Résultats (C2, F0, € par mois pour les actifs, réforme achevée)** [S] : Smic −28 ; 1,5 Smic −47 ; 2 000 € net −45 ;
2 Smic −59 ; 3 Smic −129 ; cadre à 120 000 € brut −81 (−970 €/an, contre −6 533 en v2) ; 250 000 € brut −183
(−2 200 €/an). Mi-temps au Smic −42. Salarié de 63 ans à 35 000 € : l'année de travail en plus est taxée moins.
Déciles (€ par foyer) : −36, +4, +226, +166, −360, −288, −491, +51, −189, +1 276. Actifs −12,1 Md€, retraités
+13,8 Md€ ; 29 % des foyers paient plus de 500 € de plus (majoritairement des retraités et des couples à un revenu).

**Retraités seuls (€ par an)** : 10 000 € +565 ; 12 000 € +766 ; 14 000 € +995 ; 16 000 € +1 254 ; 18 000 € +1 543 ;
20 000 € +1 000 ; 25 000 € +538 ; 30 000 € +597 ; 40 000 € −218 ; 60 000 € −1 054 ; 80 000 € −1 218 ; 100 000 €
−1 414 (v2 : −6 082). Couples de retraités : 30 000 € +1 018 ; 60 000 € −396. Les retraités aisés ne gagnent plus que
peu ; les retraités modestes restent perdants, de 50 à 130 € par mois entre 12 000 et 18 000 € de pension : c'est le prix
de l'égalité pension/salaire (un salarié à 16 000 € paie aujourd'hui 1 700 €, un retraité 0). Seul un taux d'entrée
plus bas pour tous l'atténue (C4 : 165 à 190 € de moins par an) au prix décrit plus haut. **Point d'attention** : le
minimum vieillesse (ASPA, différentiel, non imposable) devrait être calculé sur la pension nette du nouvel impôt, sans
quoi un pensionné proche du minimum passerait sous celui-ci (non chiffré).

**Familles (sans niche)** : couple biactif 2 enfants à 60 000 € −152 €/mois ; mono-actif 2 enfants à 40 000 € −111,
à 60 000 € +99 ; biactif 3 enfants à 60 000 € −221 ; mono-actif 4 enfants à 45 000 € −254 ; parent isolé au Smic,
2 enfants −144. Perdants : couples à un seul revenu élevé (sans enfant à 80 000 € : +442 €/mois, contre +300 en v2 ;
mono-actifs avec enfants au-delà de 55 000 € : +200 à +650 €/mois entre 80 000 et 150 000 €), effet de l'impôt
individuel avec un barème progressif ; étape intermédiaire possible : quotient conjugal plafonné (v2, § 6). Moyennes :
couples avec enfants −797 €/an, parents isolés −843 €/an. Franchise 5 000 € : −0,30 point sur les taux, Smic −31 €/mois,
couple 2 enfants 60 k€ −1 545 €/an ; 7 000 € : +0,28 point, Smic −25, couple −2 022. **6 000 € retenus.**

**Familles avec niches** (perte des avantages / variation d'assiette / gain de barème et franchise = net, €/an ;
droit 2025, paramètres OpenFisca : emploi à domicile 50 % jusqu'à 12 000 € + 1 500 € par enfant, garde 50 % jusqu'à
3 500 € par enfant de moins de 6 ans, dons 66 % ; CGI art. 199 sexdecies, 200 quater B, 200, non relus sur Légifrance) :

| Ménage | Aujourd'hui | Avantages | Assiette | Barème | Net (€/mois) |
|---|---|---|---|---|---|
| Biactif 36+24 k€, 2 enfants, garde 3 500 € et domicile 3 000 € | 2 501 | +3 250 | +3 301 | −5 123 | **+119** |
| Le même sans niche | 5 751 | 0 | +3 301 | −5 123 | −152 |
| Cadres 55+45 k€, 2 enfants, domicile 8 000 €, dons 1 500 € | 9 281 | +4 990 | +8 079 | −10 162 | +242 |
| Biactif 50+30 k€, 3 enfants, dons 1 000 € | 7 624 | +533 | +7 366 | −9 353 | −121 |
| Biactif 40+30 k€, 4 enfants, garde 3 500 € | 4 921 | +1 750 | +5 248 | −8 092 | −91 |
| Parent isolé 1,3 Smic, 2 enfants, garde 2 000 € | 1 679 | +1 000 | +1 233 | −3 043 | −67 |
| Retraité 30 k€, domicile 4 000 € | 1 287 | +2 000 | +1 727 | −1 130 | +216 |
| Retraité 30 k€ sans niche | 3 287 | 0 | +1 727 | −1 130 | +50 |
| Retraités 36+24 k€, domicile 6 000 €, dons 1 000 € | 4 742 | +3 660 | +2 406 | −2 802 | +272 |

Exemple incarné de suppression de niche : le couple biactif qui emploie une garde et une aide à domicile perd 119 € par
mois ; le même couple sans niche gagne 152 €. La garde d'enfants peut passer par la dépense (CMG, crèches), pas par l'impôt.

**Second conjoint.** Prélèvement sur le salaire du second qui reprend un mi-temps au Smic : 11,5 % aujourd'hui (sans
enfant ; 9,5 % avec deux enfants) → 4,9 % ; sur les 1 000 premiers euros : 9,5 % → 2,1 %.

**Attribution de la franchise.** Règle recommandée : répartition libre entre les parents, par défaut sur le revenu le plus
élevé. Avec un taux marginal croissant, c'est le choix qui minimise l'impôt du couple, et le second parent garde
exactement le taux d'une personne seule de même revenu (2 % au premier euro, 9,3 % à 10 000 €) : aucune désincitation.
Une règle « moitié chacun, reliquat transférable » taxerait les premiers euros du second à 22-26 % (perte de la franchise
transférée au taux du premier) : à écarter. Parent isolé dont le revenu est inférieur à la franchise : il ne paie rien
(jusqu'à 6 000 € par enfant) ; le reliquat est perdu, comme l'est aujourd'hui l'avantage de quotient non imputé ; le
rendre remboursable en ferait une prestation familiale (hors bloc).

**Premier enfant (pour la note, à présenter comme une piste, pas un résultat).** La fécondité a reculé de 2,0 enfants
par femme en 2014 à 1,6 en 2024 ; l'Ined (*Population et Sociétés*, juillet 2025, « Les Français·es veulent moins
d'enfants ») relève la baisse du nombre idéal (2,7 en 1998, 2,3 en 2024) et de la préférence pour trois enfants
(environ la moitié des 18-49 ans en 1998, 29 % en 2024) ; nous n'avons pas pu vérifier de série récente des probabilités
d'agrandissement par rang. Fernández-Villaverde et Norrick (NBER WP 35809, 2026) conjecturent que la modernité rend
« le troisième enfant cher et l'absence d'enfant bon marché » ; dans des entretiens, Fernández-Villaverde attribue
l'essentiel de la baisse à la hausse de l'infécondité. Si l'entrée dans la parentalité est la marge décisive, une
franchise plus forte pour le premier enfant serait la mieux ciblée ; la proposition centrale garde une franchise uniforme.

## 4. Efficacité et effets réels (C2, F0) [S]

Perte sèche réelle en moins : 2,5 Md€ par an (1,1 à 5,5 selon les élasticités), dont 0,6 sur les heures et l'effort et
1,9 sur la participation. Effets réels, ordres de grandeur (central ; bas–haut) : revenu réel du travail +0,8 %
(0,3–1,7), soit environ 210 000 équivalents temps plein (90 000–440 000) [H : 26 M d'ETP] ; l'essentiel vient de la
participation des seconds apporteurs et des temps partiels, dont le taux de prélèvement sur le premier salaire baisse
fortement. Élasticités [E] : participation 0,25 (0,10–0,50 ; Chetty et al., *NBER Macro Annual* 2013) ; revenu
d'activité 0,05/0,10 (0,02–0,25 ; Lehmann, Marical et Rioux, *JPubE* 2013). Le revenu déclaré du haut (élasticité du
revenu imposable) n'est pas converti en production. Le nombre de personnes qui entreraient en emploi (419 000 au
central) reste en annexe.

## 5. Trajectoire [C]

Montée en charge sur quatre ans, (1 − λ) × ancien + λ × nouveau, λ = 0,25 à 1 de 2027 à 2030 : recette constante chaque
année (F0 : 0 ; F3 : −0,75, −1,5, −2,25 puis −3,0 Md€ ; F6 : le double). Postes en 2030 (F0) : retraités +13,76,
actifs −12,15, CEHR −0,58, invalidité −1,03. CRDS : extinction après 2033, droit en vigueur, hors bilan.

## 7. Version finale retenue par l'assembleur : C2 financé 5,5 Md€ [C]/[S]

Décision de bouclage (18/11/2026) : le bloc reçoit 5,5 Md€ par an en régime de croisière (fiscalité foncière, niches
de l'IS), en caisse par paliers : 0 jusqu'en 2031, 1,0 (2032), 2,0 (2033), 3,0 (2034), 4,0 (2035), 5,0 (2036), 5,5 dès
2037 ; la fusion garde sa montée en charge 2027-2030 à recette constante. Script : `calculs/ircsg3_final.py` ; chiffres :
clé `final` et table `annuel_final` de `ircsg3.json` (total de chaque année = −financement de l'année),
`sorties/ircsg3_final.txt`.

**Ciblage.** La baisse porte sur les points 0, 1, 1,5 et 2 Smic (poids 1 / 1 / 1 / 0,5 ; −0,53 point), donc aucun taux
marginal n'est relevé entre 0,7 et 1,1 Smic. Pour que le haut ne reçoive rien, le taux au point 3,5 Smic est relevé de
0,36 point, de sorte que l'impôt au point haut (163 400 €) et au-delà est inchangé. Plafond de 48 % et point haut
inchangés. **Barème final** : 1,5 % au premier euro, 15,5 % à 1 Smic (19 200 €), 22,5 % à 1,5 Smic (28 800 €), 28,7 % à
2 Smic (38 400 €), 36,4 % à 3,5 Smic (67 100 €), 48 % à 163 400 € et au-delà.

**Qui reçoit les 5,5 Md€** : actifs 3,7, retraités 1,8 ; dixième le plus aisé 1,0 (des couples dont chaque membre gagne
moins de 163 000 €), centième 0,06. Par foyer : de 10 à 37 € par an aux deux premiers déciles, 77 à 199 € du 3e au 8e,
233 à 235 € aux deux derniers.

**Résultats finaux (€ par mois pour les actifs).** Smic −36 ; 1,5 Smic −60 ; 2 000 € net −57 ; 2 Smic −75 ; 3 Smic −145 ;
cadre à 120 000 € brut −86 ; 250 000 € −183 (inchangé). Mi-temps au Smic −46. Retraités seuls (€/an) : 12 000 € +702 ;
16 000 € +1 170 ; 20 000 € +894 ; 30 000 € +439 ; 60 000 € −1 250 ; 100 000 € −1 490 ; couples de retraités 30 000 €
+860, 60 000 € −706. Familles sans niche (€/mois) : biactif 2 enfants à 60 000 € −170 ; mono-actif 2 enfants à 40 000 €
−121, à 60 000 € +83 ; biactif 3 enfants −236 ; mono-actif 4 enfants à 45 000 € −261 ; parent isolé au Smic −147 ; couple
à un revenu sans enfant à 80 000 € +429. Avec niches : biactif 2 enfants avec garde et emploi à domicile +101 (sans niche
−170) ; cadres avec emploi à domicile et dons +211 ; retraité à 30 000 € avec emploi à domicile +203 (sans niche +37).
Second conjoint (mi-temps au Smic) : 11,5 % → 4,4 % ; premiers 1 000 € : 9,5 % → 1,6 %. Déciles (€/foyer) : −45, −33,
+150, +67, −478, −428, −659, −148, −421, +1 041 ; actifs −15,8 Md€, retraités +11,9 Md€ ; le dixième le plus aisé paie
4,4 Md€ de plus et reçoit 21,6 % des baisses (centième 8,2 %). Perte sèche : −2,8 Md€ par an (1,2 à 6,1), dont 0,7 heures
et effort, 2,1 participation ; travail +0,9 % (0,4–1,9), environ 233 000 ETP (98 000–485 000).

**Cascade finale (graphique F)** : élargissement +112,2 ; CEHR et invalidité −1,6 ; franchise −18,1 ; barème −98,0
(dixième supérieur −36,8, centième −8,8) ; variation nette −3,9 hors CEHR et invalidité, soit −5,5 au total.

**Trajectoire (`annuel_final`, Md€)** : 0 de 2027 à 2031 (fusion à recette constante, λ = 0,25 à 1 de 2027 à 2030) ;
−1,0 (2032), −2,0 (2033), −3,0 (2034), −4,0 (2035), −5,0 (2036), −5,5 dès 2037. Chaque palier abaisse le barème au
prorata (taux = C2 − (financement/5,5) × écart au barème final).

Les figures g1, g2, g3, g3b et F (travail) montrent désormais cette version finale ; les figures de travail A à E
comparent les candidats à recette constante.

## 6. Limites qui peuvent changer la conclusion

1. Frais réels : montant 2024 gardé ; sans forfait, des salariés aujourd'hui au forfait déclareraient leurs frais :
+10 Md€ déclarés = +0,26 point. 2. Imputation de l'étape 1 (niches) au sein des tranches : proportionnelle au droit
simulé ; les gros utilisateurs de niches perdent plus que la moyenne. 3. Familles de 3 enfants et plus : même
répartition à tout revenu [H] ; parents isolés et couples, idem. 4. Couples homogènes, pas de ménages mixtes actifs-
retraités, retraités tous de plus de 65 ans. 5. 4,0 Md€ d'IR non attribué et 3,8 Md€ de réduction pour revenus de
source étrangère (§ 1). 6. Pas de demande de travail ; pas de réaction des retraités. 7. Minimum vieillesse et seuils de
CSG des allocations chômage non traités.

## Titres-messages proposés

g1 « Le taux moyen baisse à tous les niveaux de salaire, et reste progressif » ; g2 « Le taux
marginal monte en ligne droite, sans marche, de 2 % à 48 % » ; g3 « Les familles et les salariés gagnent, les petites
pensions et les couples à un revenu paient plus » ; g3b « Les salariés gagnent à tous les niveaux ; les retraités
modestes paient plus, les aisés gagnent peu » ; F « L'élargissement rapporte 112 Md€ ; le barème en rend 92, la
franchise 18 ».

Sources : Insee, [Familles selon le nombre d'enfants de moins de 25 ans, 2022](https://www.insee.fr/fr/statistiques/2012715) ;
Ined via [Maire-info, 10/07/2025](https://www.maire-info.com/demographie-le-declin-de-la-natalite-fran%C3%A7aise-est-parti-pour-durer-selon-une-etude-article2-29883) ;
[NBER WP 35809](https://www.nber.org/papers/w35809) ; [finanz-tools.de, § 32a EStG 2025](https://www.finanz-tools.de/einkommensteuer/berechnung-formeln/2025) ;
Voies et moyens t. II PLF 2026 (fichier `ir_csg/sorties/depenses_fiscales_ir_plf2026.csv`) ; DGFiP Statistiques n° 41.
