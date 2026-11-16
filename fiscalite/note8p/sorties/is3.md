# Bloc IS, version 3 : taux de 25 % maintenu, fin du taux réduit, déduction de 50 %, niches rationalisées

18/11/2026. Scripts : `note8p/calculs/is3_reforme.py` (chiffres, `is3.json`, journal `is3_calculs.txt`),
`note8p/calculs/is3_figure_g7.py` (figure). Ils importent `is/simulation_is.py` sans le modifier et ne réécrivent pas
`is.json`. Droit de 2026 ; bénéfices de l'exercice 2025 (DGFiP n° 51) portés en 2027 ; +3 % par an ensuite. Années =
exercices ; en caisse, un an plus tard (`annuel_caisse`). Statuts : [E] empirique publié, [S] simulation, [H] hypothèse,
[C] choix.

## 1. La proposition [C]

1. **Taux réduit supprimé** : 20 % pour l'exercice 2027, 25 % dès 2028. Une marche intermédiaire suffit à annoncer la
   réforme ; chaque marche de plus coûte environ 1 Md€ de recette sur l'année concernée.
2. **Déduction immédiate de 50 %** des équipements neufs éligibles. La moitié du prix est déduite l'année de l'achat, le
   reste suit le plan ordinaire (linéaire ou dégressif). Elle est introduite à 25 % la première année, puis à 50 %.
   Le départ (2027, 2028 ou 2029) est fixé au bouclage : les trois séries sont dans `annuel`.
   - Champ : machines, matériel, informatique, logiciels acquis.
   - Hors champ : bâtiments, voitures particulières, biens d'occasion.
   - Option : les véhicules utilitaires multiplient tous les coûts par 1,25.
3. **Paquet de niches**, dès les exercices 2028 (§ 4).
4. **Taux normal maintenu à 25 %** (25,8 % avec la contribution sociale de 3,3 %).

## 2. Ce que rapportent et coûtent les mesures (Md€, exercices, + = recette)

| | 2027 | 2028 | 2029 | 2030 | 2032 | 2035 | 2040 | Régime permanent (€ 2027) |
|---|---|---|---|---|---|---|---|---|
| Fin du taux réduit, prudent [S] | +1,08 | +2,22 | +2,29 | +2,35 | +2,50 | +2,73 | +3,16 | +2,15 |
| *idem, statique (borne haute)* | +1,59 | +3,28 | +3,38 | +3,48 | +3,69 | +4,03 | +4,68 | +3,18 |
| Déduction, départ 2027 | −3,69 | −6,75 | −5,38 | −4,28 | −2,48 | −0,85 | −0,99 | −0,67 |
| Déduction, départ 2028 | 0 | −3,80 | −6,95 | −5,54 | −3,45 | −1,01 | −0,99 | −0,67 |
| Déduction, départ 2029 | 0 | 0 | −3,92 | −7,16 | −4,54 | −1,67 | −0,99 | −0,67 |
| Niches, noyau [S] | 0 | +2,80 | +3,36 | +3,55 | +3,96 | +4,65 | +5,39 | +3,67 |
| *Boîte à brevets (hors bouclage prudent)* | 0 | +1,33 | +1,37 | +1,42 | +1,50 | +1,64 | +1,90 | +1,30 |
| *Mémoire : fin de la contribution exceptionnelle (droit en vigueur, non comptée)* | −7,0 | −7,0 | −7,0 | −7,0 | −7,0 | −7,0 | −7,0 | |

**Taux réduit.**
- *Fourchette.* 3,18 Md€ statiques à plein en 2027 (10 points sur 31,8 Md€ de base). La série prudente, retenue,
  repart du dernier chiffre officiel : 2,2 Md€ en 2019 pour 13 points (CPO 2023), ramené à 10 points et actualisé.
- *Ce qui a été retiré.* Le « central » de la v2 (16 % de fuite vers l'IR et les salaires) n'était pas calibré.
- *Le droit.* CGI art. 219 I b, BOI-IS-LIQ-20-10, service-public.fr F23575 : 15 % jusqu'à 42 500 €, chiffre
  d'affaires d'au plus 10 M€, capital détenu à 75 % par des personnes physiques.

**Déduction de 50 %, à 25 %.**
- *Pic et cumul.* Le pic arrive la deuxième année : 6,7, 7,0 ou 7,2 Md€ selon que le départ a lieu en 2027, 2028 ou
  2029. Introduire directement 50 % porterait le pic à 7,4-7,8 Md€. Le coût redescend ensuite à son niveau permanent
  en sept ans.
- *Coût permanent* : 0,67 Md€ de 2027 par an (0,54 à 0,81 selon le plan actuel), soit 0,99 Md€ en 2040.
- *Coût économique d'une année d'achats* : 1,07 Md€ actualisé à 5 % (0,73 au taux de l'État).
- *Nature du coût de départ* : c'est une avance d'impôt que l'État récupère ensuite, pas une perte définitive.
- *Hypothèse non mesurée* [H] : 75 % de l'investissement éligible est fait par des sociétés imposables ; les coûts
  sont proportionnels à cette part.

**Marge de manœuvre en régime permanent** [S] :
- *Calcul* : 2,15 (taux réduit, prudent) + 3,67 (niches, noyau) − 0,67 (déduction) = **5,2 Md€ par an** (€ 2027),
  soit 1,7 point de taux normal.
- *Recettes possibles en plus* : +1,3 Md€ si la base des brevets reste en France, +1,0 Md€ si le taux réduit rapporte
  son statique.
- *Solde du bloc par année*, pour chaque date de départ (`solde_bloc_is`) :

| Départ de la déduction | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|---|
| 2027 | −2,6 | −1,7 | +0,3 | +1,6 | +2,8 |
| 2028 | +1,1 | +1,2 | −1,3 | +0,4 | +1,8 |
| 2029 | +1,1 | +5,0 | +1,7 | −1,3 | +0,5 |

- *Lecture.* Avec un départ en 2028 ou 2029, le bloc a au plus une année légèrement négative ; le bouclage la couvre
  (ou décale d'un an).
- *Usages de la marge, au choix du bouclage.*
  - Absorber le pic de transition.
  - Baisser l'impôt sur le travail, ou relever moins le foncier.
  - Étendre la déduction : véhicules utilitaires (+0,17 Md€ de coût permanent), puis passage progressif à la déduction
    intégrale.
  - Plutôt que baisser le taux : 5 Md€ ne paient que 1,7 point, pour un effet sur le capital domestique bien moindre
    (§ 5).

## 3. Tous les perdants du taux réduit, et pourquoi on l'assume

- **Ampleur.** Sans baisse du taux normal, toute société au taux réduit perd : 10 % de son bénéfice jusqu'à 42 500 €,
  donc 4 250 € par an au plus.
  - 30 000 € de bénéfice : +3 000 € par an (250 € par mois).
  - 42 500 € ou plus : +4 250 €.
- **Nombre.** 760 000 bénéficiaires en 2019 (CPO 2023), au moins 720 000 en équivalent plafond en 2025 (chiffre
  postérieur non publié).
- **Petite société de services** qui achète 10 000 € d'informatique par an : la déduction lui vaut environ 90 € par an.
  Elle perd presque tout l'avantage.
- **Justification [C].**
  - La taille est un mauvais indicateur de besoin : l'avantage va à toute société sous 42 500 €, qu'elle investisse
    ou non, y compris les holdings patrimoniales, les sociétés d'exercice libéral et les SCI à l'IS.
  - Il crée un pic de bénéfices juste sous le plafond (CPO 2016).
  - Il ne favorise pas la croissance des entreprises (OCDE 2015, cité par le CPO).
  - L'euro dépensé ira aux entreprises qui investissent : la déduction et le CIR des PME, qui est maintenu.
- **À la marge, presque neutre pour l'équipement.** Pour une société qui reste sous le plafond, le coût d'usage de
  l'équipement varie de −0,1 % : le taux de 25 % et la déduction se compensent (TMEI de 10,4 % aujourd'hui, 9,9 %
  après). Celui des bâtiments monte de 6 % (TMEI de 13 à 22 %).
- **Effet de trésorerie : pas chiffré.** Moins de trésorerie peut réduire l'investissement des PME contraintes, mais
  la sensibilité de cet investissement à la trésorerie n'est pas estimée en France. On le dit, sans le chiffrer
  (chiffre de la v2 retiré).

## 4. Niches de l'IS : supprimer les niches de convenance, recentrer la R&D

**Source.** Voies et moyens, tome II, PLF 2026 (texte lu ; fiches extraites dans `is3.json`, clé `niches_liste`).
- Dépenses fiscales de l'IS seul : 3,9 Md€ en 2024.
- Dépenses communes à l'IR et à l'IS : 14,1 Md€, dont le CIR.
- Ne sont pas des dépenses fiscales, par construction de la « norme » : taux réduit, régime mère-fille, intégration,
  report des déficits.

**Classement [C] et décision.**

| Dispositif (code VM) | Coût 2026, M€ | Bénéficiaires | Classe | Décision |
|---|---|---|---|---|
| CIR (200302) | 8 041 | 17 593 | externalité R&D | recentrer : plafond de 100 M€ apprécié au niveau du groupe, fin du taux de 5 % au-delà |
| Mécénat des entreprises (210309) | 1 730 | 157 399 | convenance | réduction de 60 % remplacée par la déduction du don comme une charge |
| Crédits culture : audiovisuel, cinéma, tournages étrangers, jeux vidéo, spectacle, musique, théâtre (3201xx) | 706 | ≈ 2 100 | convenance sectorielle | suppression ; la politique culturelle passe, si on la veut, par le budget |
| Zonages : ZRR et ZFRR, ZFU, BER, BUD, ZRD, entreprises nouvelles en zones, Corse | 657 | ≈ 78 000 | convenance territoriale | fermés aux entrants dès 2027, extinction des droits acquis |
| Crédit d'impôt famille (210308) | 223 | 19 540 | utilité sociale | suppression ; la garde d'enfants passe, si on la veut, par la dépense |
| Boîte à brevets à 10 % (210326) | 1 258 (2025) | 1 065 | localisation de revenus | suppression ; recette non comptée au bouclage prudent |
| CII (200310) | 230 | 11 387 | externalité faible | ne pas proroger après 2027 (extinction de droit, non comptée) |
| Suramortissements (39 decies et suivants) | ≈ 220 | | investissement | s'éteignent ; remplacés par la déduction générale ; ne pas créer ceux du PLF 2027 (art. 9 et 10) |
| Taxe au tonnage (320119) | 620 | 78 | régime européen, base mobile | hors paquet |
| Outre-mer (210325, 320136, 210322…) | ≈ 680 | | politique ultramarine | hors paquet, à budgétiser |
| PTZ (210313), HLM (300102), SIIC et SPPICAV | | | logement, transparence | hors paquet |

**Paquet chiffré** [S, statique, en M€ de 2026 portés à +3 % par an] :
- CIR : 0,97 Md€ (569 M€ pour le plafond au niveau du groupe, CPO 2025 ; 400 M€ pour la tranche à 5 %, CAE 2022, sur
  les données de 2019 ; sans le terme croisé, donc prudent).
- Mécénat : 1,01 Md€ (1,73 × (1 − 25/60) ; dons supposés inchangés, donc prudent).
- Culture : 0,71 Md€ (la moitié en 2028, pour les productions engagées).
- Zonages : 0,66 Md€ à terme ; extinction linéaire sur huit ans [H], la durée maximale des exonérations zonées, non
  revérifiée sur chaque texte.
- Crédit famille : 0,22 Md€.
- **Noyau : 3,6 Md€ (2026), soit 2,8 en 2028 et 3,6 en 2030.**
- Brevets : +1,26 Md€ statiques, en borne haute (base mobile, aucune élasticité calibrée), hors bouclage prudent.

**Le CIR : examiner l'efficacité, pas supprimer mécaniquement.**
- **CNEPI (2019)** [E, d'après Trésor-Éco n° 290, Le Gall, Meignan et Roulleau, 2021] : un euro de CIR produit environ
  un euro de R&D privée en plus.
- **Bozio, Irac et Py (2014, Banque de France WP 532)** [E, résumé lu].
  - *Méthode* : réforme de 2008 (passage au volume), doubles différences avec appariement.
  - *Résultat* : effet positif sur la R&D aux marges intensive et extensive, effet sur l'innovation plus faible
    qu'attendu.
- **Bozio, Cottet et Py (2019, rapport IPP n° 22)** [E, page de présentation lue].
  - *Résultat* : R&D +15 à 18 %, soit un multiplicateur de 1,3 à 1,5 ; l'intervalle de confiance n'exclut pas un
    multiplicateur inférieur à 1. Probabilité de déposer un brevet : +5 %.
  - *Conclusion des auteurs* : un effet sur l'innovation « particulièrement limité au regard du coût ».
- **CNEPI (2021) et Bach, Bozio, Guillouzouic, Malgouyres et Serrano-Velarde (2021, rapport IPP n° 33)** [E, via
  Trésor-Éco n° 290 et CAE ; rapport IPP non lu] : effets significatifs sous 250 salariés, aucun effet établi pour
  les ETI et les grandes entreprises.
- **Aghion, Chanut et Jaravel (2022, CAE Focus n° 90)** [texte lu ; corrélations conditionnelles, pas d'identification
  causale].
  - 1 M€ de CIR va avec 1,17 brevet dans une TPE, contre 0,46 dans une grande entreprise.
  - Les 100 premiers bénéficiaires touchent 33 % du CIR.
  - Une vingtaine de groupes reçoivent 400 M€ au taux marginal de 5 % au-delà de 100 M€ de dépenses. C'est une
    subvention inframarginale : le taux marginal est faible justement là où la dépense se ferait de toute façon.
- **Droit récent** [SECONDAIRE, Légifiscal].
  - LF 2025, art. 55 : forfait de fonctionnement ramené de 43 à 40 % ; frais de brevets et dispositif « jeunes
    docteurs » supprimés.
  - LF 2025, art. 56 : CII ramené de 30 à 20 % et prorogé jusqu'au 31/12/2027.
  - LF 2026 : CIR inchangé selon la presse spécialisée (non vérifié au JO).
- **Le recentrage** prend le dispositif là où l'effet n'est pas établi (grands groupes, au-delà du plafond) et garde
  le taux de 30 % là où il est mesuré (PME). On ne chiffre pas de baisse de la R&D des grands groupes : aucun effet
  causal n'y a été mesuré.
- **Variante non retenue** : plafond à 20 M€ de dépenses (CAE : environ 1,75 à 2,5 Md€ redéployables), au risque de
  perdre des laboratoires de groupes mobiles.

**Boîte à brevets.**
- *Le défaut* : elle taxe à 10 % des revenus, pas de la recherche. Son coût a doublé depuis 2021. Le CPO (2025) met
  en doute son efficacité, en citant Alstadsæter et al. (2018) [SECONDAIRE] : les boîtes à brevets déplacent les
  brevets plus que la R&D.
- *Le risque* : la localisation de la base, qu'on ne sait pas chiffrer. D'où une recette laissée hors du bouclage
  prudent.

**Doubles comptes.**
- *Champ du paquet* : le coût entier des dispositifs communs IR-IS (codes 2xxxxx), y compris la part des entrepreneurs
  individuels. Le bloc IR (périmètre des ménages, codes 1xxxxx) ne doit pas les recompter.
- *Mécénat* : celui des ménages relève du bloc IR.
- *Zonages* : seules les exonérations d'impôt sur les bénéfices sont comptées. Celles de CFE et de taxe foncière en
  zone relèvent de la fiscalité locale et ne sont pas comptées ici.
- *Extinctions de droit* (CII, suramortissement 2015-2017, contribution exceptionnelle) : en mémoire, jamais comptées.

**Gains non chiffrés** : moins de recherche de niches, moins de coûts de conseil et de contrôle, une allocation du capital qui suit la rentabilité et non l'éligibilité.

**Exemple : le robot et le comptable.**
- *Le cas.* Une petite entreprise industrielle achète un robot de 500 000 €.
- *Avec le suramortissement « industrie 4.0 »* du PLF 2027 (art. 9, proposé, non voté) : déduction supplémentaire de
  80 %, 120 % en zone d'aide à finalité régionale. L'avantage actualisé atteint 87 000 € (131 000 € en zone),
  soit 17 à 26 % du prix.
- *Avec la déduction générale de 50 %* : 8 000 €.
- *La leçon.* Un robot dont la valeur actuelle nette est de −50 000 € devient « rentable » grâce à la niche : on a
  subventionné un mauvais investissement. La déduction générale ne fait pas cela. Elle vaut la même chose pour toute
  machine, dans tout secteur, sans agrément. Une entreprise doit investir parce que son projet est rentable, non parce
  que son comptable lui a trouvé une niche.

## 5. Effets économiques nets [S, niveau de long terme, pas de taux de croissance]

**Méthode.**
- Le stock de capital suit le coût d'usage (1 − τz)/(1 − τ). Élasticité de 1 pour les équipements (0,5 à 1,6 ; 1,6
  chez Maffini, Xing et Devereux, 2019). Elle s'applique aux 75 % imposables.
- Production Cobb-Douglas, à emploi donné : l'élasticité de la production à chaque capital est la part de son revenu
  (3,4 % pour les équipements).

| | Coût d'usage des équipements | Capital en plus | Investissement en régime établi | PIB potentiel | Coût |
|---|---|---|---|---|---|
| Déduction de 50 % | −2,1 % | 8,4 Md€ (4,2-13,4) | +1,4 Md€/an | **+0,05 %** (0,03-0,09), 1,6 Md€ | 1,07 actualisé par an ; pic 6,7-7,2 |
| Taux à 22,5 % (comparaison) | −0,5 % (bâtiments −1,6 %) | 4,6 (2,3-8,3) | +0,5 | +0,02 % (0,01-0,035) | 7,5 par an |
| Déduction intégrale | −4,2 % | 17,0 (8,5-27,1) | +2,9 | +0,11 % (0,05-0,17) | 2,14 actualisé par an ; 14,8 la 1re année |

- **Par euro de coût économique**, la déduction accumule 7,8 Md€ de capital par Md€ et par an, contre 0,6 pour la baisse
  du taux.
  - *Calcul partiel* : il ignore la localisation et les bénéfices transférés, que seul le taux touche. Le modèle complet
    de Chodorow-Reich, Zidar et Zwick (2024, *JEP*) [E] donne un écart bien plus faible : la déduction livre « la moitié
    du capital pour un tiers du coût ».
  - *Le sens reste le même.*
- **Effets négatifs du financement.**
  - *Taux réduit* : neutre à la marge pour l'équipement des petites sociétés, défavorable pour leurs bâtiments (+6 % de
    coût d'usage), effet de trésorerie non chiffré (§ 3).
  - *Niches* : aucun effet sur le PIB potentiel n'est compté, ni dans un sens ni dans l'autre. Les crédits culture
    déplacent des tournages ; le mécénat réduit les dons ; la boîte à brevets peut faire partir des brevets. Ce sont des
    effets de localisation ou sectoriels, sans élasticité calibrée.
  - *Net* : **environ +0,05 % de PIB potentiel**, effet modeste, qu'il ne faut pas survendre.
- **Le transitoire** (pic d'investissement des premières années) n'est plus chiffré. Le multiplicateur de court terme
  de la v2 a été retiré : il n'élève pas le PIB potentiel.
- **Emprunt.**
  - *Ce qui ne s'aggrave pas* : l'avantage de la dette sur les fonds propres, qui baisse de 2,06 à 1,90 point de coût
    du capital.
  - *Ce qui s'aggrave* : le TMEI d'une machine financée par emprunt passe de −24 % à −37 %.
  - *En financement mixte* (un tiers d'emprunt), il est à peu près nul (−1,7 %). C'est acceptable sans garde-fou ; à
    100 %, il tomberait à −13 %. Le plafonnement de l'art. 212 bis (3 M€ ou 30 % de l'EBITDA) ne touche presque pas
    les PME.
- **Logiciels acquis** (3 ans) : TMEI de 19,5 % à 10,8 %.
- **Bâtiments** : exclus, à 22 %. C'est le premier biais qui reste ; le taux de 25 % ne le corrige pas.
- **Incorporels produits en interne** (R&D) : déduits immédiatement, donc TMEI nul. Avec un CIR à 30 %, ils sont
  subventionnés (TMEI de −67 %) ; au taux de 5 %, la subvention marginale est quasi nulle (−7 %).
- **Pas de neutralité parfaite** : entre actifs, entre dette et fonds propres, entre sociétés imposables et en perte.

**Long terme (souhaitable, non retenu pour son coût) [C].**
- *Passer de 50 à 100 %* en 2035 coûterait 9,4 Md€ la première année, 7,5 la deuxième, puis 0,67 Md€ par an de plus.
  D'un coup en 2027 : 14,8 Md€. Elle exigerait de traiter l'emprunt (TMEI mixte de −13 %) et les pertes.
- *Neutralité dette / fonds propres (ACE)* : non chiffrée, faute d'une donnée vérifiée sur les fonds propres fiscaux.
  Les ACE belge et italienne ont réduit l'endettement, pour un coût élevé (version stock) ; l'italienne a été abrogée
  en 2024.
- *Pertes* (report en arrière remboursable) : non chiffré.
- *La hiérarchie est assumée* : d'abord l'investissement en équipements, au meilleur rendement par euro.

## 6. Cas type : PME, machine de 500 000 € (1er juillet, 7 ans, à 25 %)

| | Linéaire | Dégressif |
|---|---|---|
| Déduction de la 1re année, aujourd'hui | 35 714 € | 80 357 € |
| Avec la réforme | 267 857 € | 290 179 € |
| Trésorerie la 1re année (rendue ensuite) | **+58 036 €** | +52 455 € |
| Avantage actualisé (5 % ; 8 %) | **9 544 € ; 14 155 €** | 6 461 € ; 9 695 € |

À titre de comparaison, sur la même machine marginale, 2,5 points de taux vaudraient environ 2 100 € actualisés : la
baisse du taux paie surtout le bénéfice déjà installé.

## 7. Figure g7_tmei (pleine largeur)

**Titre-message proposé** : « Pour un dixième du coût permanent d'une baisse du taux à 22,5 %, la déduction de 50 %
réduit quatre fois plus l'impôt sur les machines ».

| | TMEI | Coût brut |
|---|---|---|
| Aujourd'hui | 18 % | |
| Taux à 22,5 % | 16 % | 7,5 Md€ par an |
| Déduction de 50 % | 10 % | pic de 6,7 à 7,2, puis 0,67 |
| Déduction intégrale | 0 % | 14,8 la 1re année, puis 1,35 |

Remarque : `calculs/figures_g7_g8.py` réécrit lui aussi g7 (ancienne version à 22,5 %). Ne plus le lancer pour g7, ou
le faire pointer vers `is3.json`.

## 8. Hypothèses retirées (parcimonie) et limites

**Retirés par rapport à la v2.**
- Le « central » du taux réduit (16 % de fuite).
- L'effet de trésorerie du taux réduit (sensibilité de 0,1 à 0,3).
- Le multiplicateur d'investissement de court terme (1,8 à 3,1).
- Le retour par les bénéfices déclarés de la baisse du taux (Beer et al.).
- Les sensibilités de la part imposable (60 à 90 %).

**Non introduits.** Aucune décote comportementale ad hoc sur les niches : la boîte à brevets est exclue du bouclage
prudent plutôt que décotée.

**Limites restantes.**
- Part imposable de 75 % [H].
- Plan d'amortissement actuel [H].
- Élasticité des bâtiments [H], qui ne sert qu'à la comparaison avec le taux.
- Chiffres CIR du CPO et du CAE non actualisés (données 2019 et 2025).
- Coûts des Voies et moyens 2026 (le tome II du PLF 2027 n'a pas été lu).
- Durées d'extinction des zonages.
- Taux du mécénat (60 % jusqu'à 2 M€ de dons, 40 % au-delà, CGI art. 238 bis), non revérifiés sur Légifrance.
- Issue du PLF 2027 (contribution exceptionnelle, art. 9 et 10) inconnue au 18/11/2026.

## Références

- Voies et moyens, tome II, PLF 2026 : texte lu.
- CPO, *Tracer un cadre fiscal et social pluriannuel pour l'industrie* (sept. 2025) : texte lu.
- Aghion, Chanut et Jaravel (2022), CAE Focus n° 90 : texte lu.
- Le Gall, Meignan et Roulleau (2021), Trésor-Éco n° 290 : page lue.
- Bozio, Irac et Py (2014), BdF WP 532 : résumé lu.
- Bozio, Cottet et Py (2019), IPP n° 22 : présentation lue.
- Bach et al. (2021), IPP n° 33 : notice seule.
- Zwick et Mahon (2017), *AER* 107(1) ; Maffini, Xing et Devereux (2019), *AEJ: EP* 11(3) ; Chodorow-Reich, Zidar et
  Zwick (2024), *JEP* 38(3) : lus pour la v2.
- Légifiscal, LF 2025, art. 55-57 : secondaire.
- PLF 2027, art. 9-10 : texte lu (voir `is/notes/is_recherche.md`).
