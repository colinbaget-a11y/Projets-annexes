# Bloc IS, version 4 : taux de 25 %, fin du taux réduit, niches et CIR supprimés, déduction immédiate portée de 50 à 100 %

17/11/2026. Scripts `note8p/calculs/is4_reforme.py` (lit `is3.json`, écrit `is4.json` et `is4_calculs.txt`) et
`note8p/calculs/is4_figure_g7.py` (figure g7). Les chiffres de
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
- *Variante non retenue par l'auteur* : garder un crédit réservé aux PME (recette statique 5,1 Md€ au lieu de 7,4).
  C'est la seule option qui préserve la R&D des PME ; les mesures générales du § 3 bis ne la remplacent pas.

**Doctrine (paragraphe proposé).** « Une entreprise doit investir parce que son projet est rentable, non parce que son
comptable lui a trouvé une niche. Sans crédit d'impôt, la recherche reste déduite dès qu'elle est payée : l'impôt ne la
décourage pas, il ne la subventionne plus. Si la collectivité veut payer pour les retombées de la recherche, qu'elle le
fasse au grand jour, par une aide budgétaire ciblée sur les jeunes entreprises et les PME, là où l'effet est mesuré. »
Le TMEI de la R&D passe de −67 % à 0 [S].

## 3 bis. Réinvestir une partie de la recette dans une mesure générale

**Ce qui existe déjà pour la R&D** [E, secondaire : BOFiP et réponse ministérielle ; texte en vigueur non relu sur
Légifrance]. L'art. 236 I permet de déduire immédiatement (ou d'immobiliser, au choix) les dépenses de fonctionnement des
opérations de recherche et de conception de logiciels. La R&D et les logiciels produits en interne sont donc déjà
passés en charges : TMEI nul hors CIR. L'amortissement sur douze mois des logiciels acquis (art. 236 II) a été supprimé
par la LF 2017 (art. 32). Une mesure « pour l'immatériel » ne peut donc porter que sur les incorporels **acquis**.

| Option (coûts bruts, Md€) | Coût de trésorerie | Coût permanent (€ 2027) | Coût actualisé d'une année d'achats | Capital en plus | PIB potentiel | R&D |
|---|---|---|---|---|---|---|
| (a) Logiciels acquis dans la déduction de 50 % (dès 2031) | 2,9 la 1re année | 0,13 | 0,21 | 0,7 Md€ | +0,01 % | aucun effet |
| (b1) Déduction portée à 75 % pour tous (2033) | 4,4 la 1re année | +0,34 | +0,53 | +4,3 | +0,03 % | aucun effet |
| (b2) puis à 100 % (2036), cumul par rapport à 50 % | 7,0 la 1re année du palier | +0,67 (au total 1,35) | +1,07 | +8,6 | +0,05 % | aucun effet |
| (c) Carry-back sur 3 ans, créance remboursable tout de suite | 1,3 à 2,5 [H] | 0,25 à 0,75 [H] | — | non chiffré | non chiffré | faible |

- *(a)* Logiciels acquis : 40 % des 77,5 Md€ d'investissement en logiciels des SNF (2025, Insee 8.212) [H], amortis sur
  3 ans [H]. Durée courte, donc gain faible : coût d'usage −1,1 % à 50 %. Le champ de la v3 citait les logiciels sans les
  chiffrer ; ils le sont désormais. Les brevets et marques acquis, de faible montant, suivent la même règle.
- *(b)* Même méthode que pour les équipements (élasticité 1, de 0,5 à 1,6). La déduction intégrale rend nul le TMEI des
  fonds propres ; le TMEI d'un tiers d'emprunt passe à −13 % (§ 1) : c'est la limite assumée.
- *(c)* Chiffrage grossier : 5 à 10 Md€ de déficits reportés en arrière par an [H]. Le carry-back ne sert qu'aux sociétés
  qui ont déjà payé l'impôt : **il n'aide pas les jeunes entreprises sans bénéfices passés**, celles que le CIR
  remboursable finançait. Non retenu ici ; il relève de la partie « Pour aller plus loin ».
- *Ce qu'aucune option ne fait* : remplacer le CIR des PME. La R&D est déjà déduite au premier euro ; une déduction plus
  rapide des équipements ou des logiciels n'en change pas le coût.

**Paquet recommandé [C]** : (a) + (b) par paliers. Logiciels acquis à 50 % dès l'exercice 2031 ; déduction de 75 % pour
tous en 2033, de 100 % en 2036. Les paliers suivent la montée en charge de la recette du CIR (restitutions des anciennes
créances jusqu'en 2031) et gardent une recette nette positive chaque année.
- *Réinvesti* : 0,94 Md€ par an en régime permanent (€ 2027), sur 5,9 Md€ de CIR prudent (16 %) ; en trésorerie, de
  1,8 à 9,0 Md€ certaines années (caisse 2032-2040).
- *Reste au bouclage* : 8,6 Md€ par an en régime permanent (au lieu de 9,6), au moins 1,9 Md€ chaque année (2034).
- *Effet* : +0,07 % de PIB potentiel en plus (0,04 à 0,12) ; 10 Md€ de capital en plus (équipements et logiciels).

**Bilan honnête, comparé à la suppression sèche du CIR** [S] :

| PIB potentiel, % (long terme) | Suppression sèche | Avec le paquet |
|---|---|---|
| Déduction (équipements, logiciels) | +0,05 | +0,13 (0,06 à 0,20) |
| Perte de R&D des PME | −0,07 à −0,25 | −0,07 à −0,25 |
| **Net** | **−0,02 à −0,20** | **+0,06 à −0,12** |

Le paquet ramène l'effet net vers zéro ; il reste négatif si les retombées de la R&D sont fortes (rendement social double
du rendement privé). La R&D des PME baisse de 2 à 3 Md€ par an dans les deux cas. On l'écrit ainsi.

**Figure g7** : la barre « déduction intégrale » devient une étape de la proposition (paliers 2033 et 2036 ; jusqu'à
7,0 Md€ de surcoût une année, puis 1,35 Md€ par an au total). Titre-message possible : « Financée par la fin du crédit
d'impôt recherche, la déduction intégrale supprime l'impôt sur les machines neuves pour un cinquième du coût d'une baisse
du taux à 22,5 % ».

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

- **Estimation partielle.** Le +0,05 % (0,03 à 0,09) ne mesure que la déduction de 50 % des équipements ; avec le paquet
  (logiciels, 75 puis 100 %), +0,13 %. Ce n'est pas l'effet net de la réforme de l'IS.
- **Fin du taux réduit** : neutre pour les équipements des petites sociétés, défavorable pour leurs bâtiments (coût
  d'usage +6 %) et leur trésorerie ; fin du pic de bénéfices sous le plafond. Faible, probablement négatif, non chiffré.
- **Niches hors CIR** : effets de localisation et de secteur ; gain d'allocation non chiffré.
- **CIR** : −0,07 à −0,25 %, terme dominant et incertain (§ 3).
- **Bilan** : de +0,06 à −0,12 % avec le paquet. Le bloc se justifie par la recette, la neutralité entre actifs et la
  simplification ; il ne promet pas de croissance.

## 6. Pour le bouclage (`is4.json`, table `annuel_caisse`, Md€ courants)

| Caisse | 2029 | 2030 | 2031 | 2032 | 2034 | 2035 | 2037 | 2040 |
|---|---|---|---|---|---|---|---|---|
| Fin du taux réduit (prudent) | 2,22 | 2,29 | 2,35 | 2,42 | 2,57 | 2,65 | 2,81 | 3,07 |
| Déduction de 50 %, départ 2029 | 0 | −3,92 | −7,16 | −5,71 | −3,56 | −2,63 | −1,04 | −0,96 |
| Niches, rendement prudent réalisable | 1,47 | 1,88 | 2,01 | 2,15 | 2,44 | 2,59 | 2,84 | 3,10 |
| Suppression du CIR, réalisable prudent | 4,22 | 4,64 | 4,98 | 6,70 | 7,10 | 7,32 | 7,76 | 8,48 |
| Réinvesti : logiciels acquis | 0 | 0 | 0 | −2,89 | −2,25 | −1,13 | −1,94 | −0,38 |
| Réinvesti : déduction à 75 puis 100 % | 0 | 0 | 0 | 0 | −4,41 | −3,51 | −7,04 | −3,08 |
| **Recette nette du bloc IS, prudent** | **7,91** | **4,89** | **2,18** | **2,67** | **1,89** | **5,29** | **3,40** | **10,23** |

2028 : +1,08 (taux réduit seul). Régime permanent (€ 2027) : 2,15 + 2,18 + 5,92 − 0,67 − 0,94 = **8,6 Md€ par an**. Les
lignes statiques ne sont qu'une borne haute (CIR 7,7 au lieu de 4,2 en 2029). Hors table : fin de la contribution
exceptionnelle (−7 Md€ par rapport à 2026) et extinction du CII, droit en vigueur.

## Limites

Profil d'encaissement du CIR (répartition entre N+1 et N+3) et décotes de réaction [H] ; part des logiciels acquis
(40 %) et leur durée d'amortissement [H] ; carry-back chiffré grossièrement ; art. 236 non relu sur Légifrance ; part de l'investissement des
sociétés déficitaires non mesurée ; montant des charges financières nettes déduites non vérifié ; taux du mécénat (art. 238 bis) non revérifiés ; Voies et moyens du PLF 2027
non lus.

## Références nouvelles

- Sénat, commission des finances, note de présentation « Remboursements et dégrèvements », PLF 2027 : texte lu.
- MESRE-DGRI, *Le crédit d'impôt recherche en 2023* (provisoire, nov. 2025) : texte lu.
- Bloom, Schankerman et Van Reenen (2013), *Econometrica* 81(4) : résumé lu.
- Guides fiscaux sur la règle espagnole de limitation des intérêts (art. 16 LIS, seuil de 1 M€) : secondaires.
