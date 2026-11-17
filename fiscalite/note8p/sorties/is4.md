# Bloc IS, version 4 : taux de 25 %, fin du taux réduit, niches supprimées (CIR compris), déduction immédiate de 50 %

17/11/2026. Script `note8p/calculs/is4_reforme.py` (lit `is3.json`, écrit `is4.json` et `is4_calculs.txt`). Les chiffres de
la v3 non repris ici (taux réduit, coût de la déduction, TMEI, effets sur le capital, cas types) restent valables
(`is3.json`). Déduction : départ à l'exercice 2029 (25 %), 50 % ensuite [C]. Niches et CIR : exercices 2028 et suivants.
Statuts : [E] publié, [S] simulation, [H] hypothèse, [C] choix.

## 1. Dette : la déduction subventionne l'investissement emprunté, et on le dit

**D'où vient le TMEI négatif.** Une machine de 100 achetée à crédit : avec la déduction de 50 %, l'État en prend
12,5 à sa charge dès la première année (25 % × 50), mais la société continue de déduire les intérêts nominaux sur les
100 empruntés (1,8 d'impôt en moins par an à 7,1 %). L'assiette est différée, les intérêts ne le sont pas : la même
somme est déduite deux fois en valeur actualisée. Le rendement avant impôt minimal d'une machine empruntée passe de 4,0 %
aujourd'hui à 3,65 %, sous le rendement exigé de 5 % : TMEI de −24 % à −37 % [S]. Ce n'est pas propre à la réforme : la
subvention existe déjà avec l'amortissement dégressif ; la déduction l'accroît.

**Deux indicateurs qui disent des choses différentes** [S] :

| Fraction déduite tout de suite | 0 (aujourd'hui) | 50 % | 100 % |
|---|---|---|---|
| Coût du capital, fonds propres | 6,10 % | 5,55 % | 5,00 % |
| Coût du capital, emprunt | 4,04 % | 3,65 % | 3,26 % |
| Avantage de la dette (écart) | 2,06 pt | 1,90 pt | 1,74 pt |
| TMEI emprunt / un tiers d'emprunt | −24 % / 7,6 % | −37 % / −1,7 % | −53 % / −13 % |

- *L'écart baisse* parce qu'une déduction anticipée vaut plus pour qui actualise à un taux élevé (les fonds propres, à
  7,1 %) que pour qui actualise au coût net de la dette (5,3 %). Le choix du mode de financement est donc un peu moins
  faussé.
- *Le niveau baisse sous zéro* pour l'emprunt : des projets dont le rendement social est inférieur au coût du capital
  deviennent rentables. Les deux sont vrais ; on ne peut pas écrire que la réforme ne crée aucune distorsion.
- *En pratique*, une machine est rarement financée à 100 % par emprunt marginal : à un tiers, le TMEI est quasi nul
  (−1,7 %). Au-delà du plafond de l'art. 212 bis, l'intérêt marginal n'est plus déductible et le TMEI de la dette
  rejoint celui des fonds propres (9,9 %) : le problème concerne les sociétés sous le plafond.

**Corrections examinées.**

| Option | Effet sur le TMEI (b = 50 %) | Faisabilité | Coût / recette | Verdict |
|---|---|---|---|---|
| Exclure la part financée par emprunt | neutralise | nulle : l'argent est fongible, traçage impossible | — | écartée |
| Refuser les intérêts « liés » aux actifs déduits | neutralise en principe | même obstacle ; contentieux | — | écartée |
| Abaisser le seuil de l'art. 212 bis de 3 à 1 M€ (ATAD le permet ; l'Espagne applique 1 M€ [E, secondaire]) | aucun pour une PME : 1 M€ de charges nettes = 17 à 25 M€ de dette | simple | recette faible, non chiffrée | ne vise pas la cible ; écartée |
| Rabot général des charges financières nettes | rabot de 21 % : TMEI emprunt ramené à −24 % ; 14 % : mixte nul [S] | simple | recette ≈ 2,5 % des charges nettes déduites par tranche de 10 % (montant non vérifié) | hausse d'impôt sur toute la dette existante : autre réforme |
| Ne déduire que les intérêts réels (i − π) | emprunt −19,5 %, mixte +1,8 % [S] | simple (rabot ≈ π/i, à réviser) | idem, rabot ≈ 28 % aujourd'hui | cap de long terme |
| Ne rien faire | emprunt −37 %, mixte −1,7 % | — | 0 | **recommandé** |

**Recommandation [C].** Ne pas ajouter de garde-fou dans la proposition centrale : les corrections ciblées sont
impraticables, le seuil de l'art. 212 bis ne touche pas la cible, et un rabot général est une réforme à part entière de
la fiscalité de la dette. Écrire la limite : la réforme réduit l'écart dette / fonds propres mais accroît la subvention
à l'investissement emprunté. La neutralité se règle à terme, en même temps que le passage éventuel à la déduction
intégrale (TMEI mixte −13 %) : déduction limitée aux intérêts réels, ou déduction pour fonds propres.

## 2. Pertes : la déduction va d'abord aux sociétés bénéficiaires

- **Droit** [E, service-public.fr F23628 ; BOI-IS-DEF] : report en avant illimité dans le temps, imputable chaque année
  dans la limite de 1 M€ plus 50 % du bénéfice au-delà ; report en arrière sur le seul exercice précédent, dans la limite
  du bénéfice de cet exercice et de 1 M€, sous forme d'une créance remboursable au bout de cinq ans.
- **Ce que vaut la déduction pour une société en perte** [S] : pour 100 d'achat, 1,60 actualisé si la société est
  imposable ; 1,07 après un an de pertes, 0,41 après trois ans, 0,09 après cinq, rien au-delà de la durée du plan. Les
  déficits ne portant pas intérêt, la déduction ne fait qu'avancer une déduction qui attendra de toute façon.
- **Part de l'investissement éligible faite par des sociétés déficitaires : non mesurée.** Aucune source publique
  croisant investissement et situation fiscale n'a été trouvée. Repère : en 2022, 113 Md€ de déficits déclarés pour
  278 Md€ de bénéfices (DGFiP n° 51) [E]. L'hypothèse de 75 % d'investissement imposable [H] laisse 25 % aux
  déficitaires et exonérés ; coûts et effets sur le capital lui sont proportionnels.
- **Hors proposition centrale.** Le traitement des pertes (plafond d'imputation, report en arrière, indexation des
  déficits) est développé dans la partie « Pour aller plus loin » ; il conditionnerait un passage à la déduction
  intégrale.

## 3. Suppression du CIR (décision de l'auteur)

**La mesure [C].** Le crédit d'impôt recherche (CGI, art. 244 quater B) est supprimé pour les dépenses engagées à
compter de 2028. Les dépenses de R&D restent déductibles comme charges ; les équipements de recherche entrent dans la
déduction de 50 %, déjà chiffrée (ils sont dans l'investissement éligible). L'ancien « CIR recentré » (0,97 Md€) disparaît
du paquet : pas de double compte. Le CII s'éteint fin 2027 (droit en vigueur, non compté). Le crédit « recherche
collaborative » (14 M€) suit le CIR.

**Recette statique** [E] : 7,4 Md€ en 2027 (coût projeté ; 7,3 Md€ exécutés en 2025 : Sénat, note de présentation
« Remboursements et dégrèvements », PLF 2027). Borne haute : 8,0 Md€ en 2026 dans les Voies et moyens du PLF 2026.
Créance 2023 : 7,85 Md€, dont 7,32 au titre de la recherche ; PME 2,24, ETI 2,10, grandes entreprises 2,98 (MESRE,
novembre 2025).

**Calendrier d'encaissement** [E pour les règles et la répartition de 2024 ; H pour le profil]. La créance s'impute sur
l'IS de N+1 à N+3, le reliquat est restitué en N+4 ; PME, JEI, entreprises nouvelles et en difficulté sont remboursées
tout de suite (art. 199 ter B). En 2024, sur 7,7 Md€ (CIR et CII), 4,7 ont été restitués et 3,0 imputés. D'où le profil
retenu d'un millésime : 67 % en N+1, 5 % en N+2, 3 % en N+3, 25 % en N+4. Le stock de créances des millésimes 2025-2027
continue d'être imputé ou restitué jusqu'en 2031.

| Caisse, Md€ | 2029 | 2030 | 2031 | 2032 | 2035 | 2040 |
|---|---|---|---|---|---|---|
| Statique (tout le coût de l'année) | 7,7 | 7,9 | 8,1 | 8,4 | 9,2 | 10,6 |
| Mécanique (millésimes 2028 et suivants) | 5,3 | 5,8 | 6,2 | 8,4 | 9,2 | 10,6 |
| **Réalisable prudent (× 0,8), à retenir** | **4,2** | **4,6** | **5,0** | **6,7** | **7,3** | **8,5** |

**Décote de 20 % [H].** Elle couvre : les recettes perdues sur l'emploi de recherche qui disparaît à court terme
(prélèvements sur 2 à 3 Md€ de dépenses de R&D en moins, en partie compensés par l'IS sur des charges déduites en moins) ;
la recréation de soutiens hors de l'impôt (budget, Bpifrance) sous la pression ; le contentieux de transition. Aucune
élasticité ne la calibre ; le central (× 0,9) et la statique bornent la fourchette.

**Effet attendu sur la R&D, présenté honnêtement.**
- *PME* [E] : un euro de CIR produit de 0,9 à 1,5 euro de R&D (CNEPI, cité par le Sénat, PLF 2027 ; Bozio, Cottet et Py,
  2019 : 1,3 à 1,5). Sans CIR, la R&D des PME baisserait de 2,1 à 3,4 Md€ par an, sur 7,5 Md€ déclarés : un quart à
  près de la moitié. Le coût après impôt d'un euro de R&D passe de 0,45 à 0,75 €.
- *ETI et grands groupes* : aucun effet établi (CNEPI 2021, IPP 2021). Ce n'est pas une preuve d'absence d'effet ; ce
  sont aussi les laboratoires les plus mobiles.
- *PIB potentiel, ordre de grandeur non compté* [S] : un stock de R&D des PME réduit de 11 à 19 Md€ (dépréciation de
  15 % [H]) retire 0,07 à 0,12 % de PIB au rendement privé, 0,15 à 0,25 % si le rendement social est double du
  rendement privé, comme le trouvent Bloom, Schankerman et Van Reenen (2013, *Econometrica*) [E, résumé lu]. **C'est
  plus que le gain de la déduction (+0,05 %).** Sur ce point, la littérature contredit la mesure.
- *Variante de repli, à signaler à l'auteur* : supprimer le CIR des ETI et grandes entreprises et garder un crédit
  réservé aux PME. Recette statique 5,1 Md€ (2027) au lieu de 7,4 ; elle prend le dispositif là où l'effet n'est pas
  établi et le garde là où il est mesuré.

**Doctrine (paragraphe proposé).** « Une entreprise doit investir parce que son projet est rentable, non parce que son
comptable lui a trouvé une niche. Sans crédit d'impôt, la recherche reste déduite dès qu'elle est payée : l'impôt ne la
décourage pas, il ne la subventionne plus. Si la collectivité veut payer pour les retombées de la recherche, qu'elle le
fasse au grand jour, par une aide budgétaire ciblée sur les jeunes entreprises et les PME, là où l'effet est mesuré. »
Le TMEI de la R&D passe de −67 % à 0 [S].

## 4. Niches hors CIR et rendement réalisable

| Mesure | Statique 2026 (Md€) | Facteur prudent [H] | Raison |
|---|---|---|---|
| Mécénat : réduction de 60 % remplacée par la déduction | 1,01 | 0,85 | dons moindres = recette en plus ; mais le taux de 40 % au-delà de 2 M€ (non revérifié) et les reports de cinq ans réduisent et étalent le gain |
| Crédits culture | 0,71 | 0,75 | tournages étrangers perdus : TVA et cotisations en moins |
| Zonages fermés aux entrants | 0,66 (à terme) | 0,80 | substitution vers d'autres régimes, extinction lente |
| Crédit famille | 0,22 | 0,90 | les dépenses restent déductibles ; places de crèche réduites |
| **Noyau hors CIR** | **2,60** | **≈ 0,82** | |

En caisse : 1,8 Md€ statiques en 2029 (1,5 prudent), 2,6 (2,2) en 2032, 3,8 (3,1) en 2040. Brevets : 1,3 Md€ statiques,
toujours hors bouclage prudent.

**Chevauchements vérifiés.**
- *CIR et déduction* : les dotations aux amortissements des équipements de recherche entraient dans l'assiette du CIR ;
  le CIR supprimé, la question disparaît. En variante PME, la déduction de 50 % devra être extra-comptable et exclue de
  l'assiette du crédit, comme les suramortissements.
- *Mécénat* : seul le dispositif des entreprises (210309) est compté ici ; celui des ménages relève du bloc IR.
- *Zonages* : seules les exonérations d'impôt sur les bénéfices sont comptées ; celles de CFE et de taxe foncière
  relèvent de la fiscalité locale (bloc foncier), non comptées.
- *Dispositifs communs IR-IS* (codes 2xxxxx) comptés ici en entier, y compris la part des entrepreneurs individuels.

## 5. Gains et rendements : ce que dit le +0,05 % de PIB

- **Estimation partielle.** Le +0,05 % (0,03 à 0,09) de PIB potentiel ne mesure que la déduction de 50 % : coût d'usage
  des équipements −2,1 %, 8 Md€ de capital en plus. Ce n'est pas l'effet net de la réforme de l'IS.
- **Fin du taux réduit** : neutre pour les équipements des petites sociétés (taux de 25 % compensé par la déduction),
  défavorable pour leurs bâtiments (coût d'usage +6 %) et pour leur trésorerie ; elle supprime le pic de bénéfices sous
  le plafond. Signe probablement négatif, faible, non chiffré.
- **Niches hors CIR** : effets surtout de localisation et de secteur (tournages, dons, zones) ; gain d'allocation non
  chiffré.
- **CIR** : négatif, de 0,07 à 0,25 % de PIB selon les externalités (§ 3) ; c'est le terme dominant.
- **Bilan honnête** : avec la suppression totale du CIR, l'effet net du bloc sur le PIB potentiel est plutôt négatif ;
  avec la variante PME, il est proche de zéro ou légèrement positif. Le bloc se justifie par la recette et la
  simplification, pas par la croissance.

## 6. Pour le bouclage (`is4.json`, table `annuel_caisse`, Md€ courants)

| Caisse | 2028 | 2029 | 2030 | 2031 | 2032 | 2035 | 2040 |
|---|---|---|---|---|---|---|---|
| Fin du taux réduit (prudent) | 1,08 | 2,22 | 2,29 | 2,35 | 2,42 | 2,65 | 3,07 |
| Déduction de 50 %, départ 2029 | 0 | 0 | −3,92 | −7,16 | −5,71 | −2,63 | −0,96 |
| Niches, rendement prudent réalisable | 0 | 1,47 | 1,88 | 2,01 | 2,15 | 2,59 | 3,10 |
| Suppression du CIR, réalisable prudent | 0 | 4,22 | 4,64 | 4,98 | 6,70 | 7,32 | 8,48 |
| **Solde du bloc, prudent** | **1,08** | **7,91** | **4,89** | **2,18** | **5,56** | **9,93** | **13,69** |

Régime permanent (euros 2027) : 2,15 + 2,18 + 5,92 − 0,67 = **9,6 Md€ par an**. Fourchette pour le bouclage : prendre les
lignes prudentes ; le statique n'est qu'une borne haute (CIR 7,7 au lieu de 4,2 en 2029). Hors table : fin de la
contribution exceptionnelle (−7 Md€ par rapport à 2026) et extinction du CII, droit en vigueur.

**Figure g7** : inchangée ; son titre-message reste exact (TMEI 18 → 10 % pour 0,67 Md€ permanents, contre 18 → 16 % pour
7,5 Md€). Sa note mentionne déjà l'emprunt (−24 → −37 %).

## Limites

Profil d'encaissement du CIR (répartition entre N+1 et N+3) et décotes de réaction [H] ; part de l'investissement des
sociétés déficitaires non mesurée ; montant des charges financières nettes déduites non vérifié ; taux du mécénat (art. 238 bis) non revérifiés ; Voies et moyens du PLF 2027
non lus.

## Références nouvelles

- Sénat, commission des finances, note de présentation « Remboursements et dégrèvements », PLF 2027 : texte lu.
- MESRE-DGRI, *Le crédit d'impôt recherche en 2023* (provisoire, nov. 2025) : texte lu.
- Bloom, Schankerman et Van Reenen (2013), *Econometrica* 81(4) : résumé lu.
- Guides fiscaux sur la règle espagnole de limitation des intérêts (art. 16 LIS, seuil de 1 M€) : secondaires.
