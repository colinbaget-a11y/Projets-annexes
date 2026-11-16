# Bloc IS : fin du taux réduit, déduction immédiate de 50 %, baisse du taux normal

17/11/2026. Scripts : `note8p/calculs/is_reforme.py` (chiffres, `is.json`, journal `is_calculs.txt`),
`note8p/calculs/is_figure_g7.py` (figure). Ils importent `is/simulation_is.py` sans le modifier. Droit de 2026 ; bases de
bénéfices de l'exercice 2025 (DGFiP n° 51) portées en 2027. Statuts : [E] empirique publié, [S] simulation, [H] hypothèse,
[C] choix. Années = exercices ; en caisse, tout arrive environ un an plus tard (`annuel_caisse`).

## 1. Choix faits [C]

1. **Taux réduit de 15 % supprimé en deux temps.** Il passe à 20 % pour les exercices 2027, puis il est aligné sur le taux
   normal dès 2028.
2. **Déduction immédiate de 50 % des équipements neufs**, à 25 % en 2027 puis 50 % dès 2028. La moitié du prix est
   déduite l'exercice de l'achat ; l'autre moitié suit le plan ordinaire, linéaire ou dégressif. C'est bien la définition
   de la variante « 50 % » de nos programmes (`plan_bonus` dans `simulation_is.py`, `chemin` dans `calculs_note_is.py`) :
   rien à corriger. Champ : machines, matériel et informatique des sociétés à l'IS (84 Md€ d'investissement des SNF en
   2025, 89 en 2027). En sont exclus les bâtiments, les voitures particulières, les biens d'occasion, la cession-bail et
   les achats intragroupe.
3. **Baisse du taux normal**, de 25 % à 24, 23 ou 22 %. Le taux et le calendrier sont fixés au bouclage. Pas de dette :
   les séries de `annuel` se combinent année par année.

## 2. Le taux réduit : ce qu'il est, ce qu'il coûte, pourquoi le supprimer

**Droit 2026, vérifié.** CGI art. 219 I b ; BOFiP BOI-IS-LIQ-20-10 (version du 21/06/2023) ; service-public.fr F23575
(vérifiée le 17/02/2026, après la LFI 2026 du 19/02/2026).
- Taux de 15 % sur les 42 500 premiers euros de bénéfice par période de douze mois (exercices clos depuis le
  31/12/2022).
- Chiffre d'affaires d'au plus 10 M€.
- Capital entièrement libéré, détenu de manière continue à 75 % au moins par des personnes physiques, directement ou par
  une société qui remplit elle-même ces conditions.
- Pour un groupe fiscal, on retient la somme des chiffres d'affaires. Pour une filiale, le Conseil d'État retient le
  chiffre d'affaires du groupe (13/03/2025, n° 481538).
- Contexte : la LFI 2026 a gardé 42 500 € ; le relèvement à 100 000 €, voté à un stade du débat, n'est pas dans la loi
  promulguée. Un amendement au PLF 2027 portant le plafond à 49 000 € aurait été adopté en commission (source
  secondaire, Fiscalonline, 9/10/2026). Notre réforme va dans l'autre sens.

**Ce qu'il coûte.** Le taux réduit n'est plus classé comme dépense fiscale depuis 2006.
- Derniers chiffres officiels : 2,2 Md€ et 760 000 bénéficiaires en 2019 (CPO 2023, d'après les Voies et moyens).
- Base imposée à 15 % : 30,6 Md€ en 2025. Il y a donc au moins 720 000 sociétés en équivalent plafond ; le nombre réel
  est plus élevé.
- Rendement de la suppression à plein, en 2027 : 3,18 Md€ statiques ; **2,67 au centre** [S/H] (2,15 à 3,18). La borne
  basse vient du chiffre de 2019. Le centre suppose que 16 % de l'avantage fuit vers l'IR ou vers les salaires.
- Avantage maximal : 4 250 € par société et par an.

**Pourquoi le supprimer.**
- La petite taille est un mauvais indicateur des difficultés de financement. L'avantage va à toute société sous
  42 500 €, qu'elle investisse ou non : holding patrimoniale, société d'exercice libéral, société civile immobilière à
  l'IS.
- Il réduit à peine le taux implicite des PME hors microentreprises (−0,7 point, CPO 2023).
- Il crée un pic de bénéfices déclarés juste sous le plafond (CPO 2016, liasses de 2012).
- Il ne favorise pas la croissance des entreprises (OCDE 2015, cité par le CPO).
- Ses recettes servent mieux les entreprises qui investissent, prennent des risques et grandissent.

**Rester proportionné.** 4 250 € par an ne freinent pas l'économie. L'argument est la neutralité et la recette, pas un
gain macroéconomique.

**Le risque, à dire.** Bernini et Treibich (2016, *Industrial and Corporate Change*, résumé seul lu) trouvent qu'en
2001-2003, diviser par deux le taux des PME a accru leur capital de 29 %. Si une partie de l'effet passe par la
trésorerie, perdre 2,7 Md€ de trésorerie peut réduire leur investissement de 0,3 à 0,8 Md€ par an. Ce chiffre suppose
0,1 à 0,3 € d'investissement par euro de trésorerie, sensibilité non estimée en France [H]. C'est moins que
l'investissement que suscite la déduction.

## 3. La déduction immédiate de 50 %

### Coûts : ne pas confondre avance de trésorerie et coût permanent

| Md€ (part imposable 75 %, plan actuel moitié linéaire, moitié dégressif) | 50 % (calendrier retenu) | 100 % dès 2027 (abandonné) |
|---|---|---|
| Coût brut annuel | 2027 : 3,7 ; 2028 : 6,7 (pic) ; 2029 : 5,4 ; 2030 : 4,3 ; 2032 : 2,5 ; 2034 : 1,0 | 2027 : 14,8 ; 2030 : 7,5 ; 2034 : 1,7 |
| Coût permanent, une fois la transition passée (euros de 2027) | **0,67** (0,54 à 0,81) ; 0,99 en 2040 (courants) | 1,35 (1,08 à 1,61) |
| Coût actualisé d'une année d'achats (5 % ; 3,25 %) | 1,07 ; 0,73 | 2,14 ; 1,45 |
| Cumul 2027-2036 | 30 | 60 |

Les bornes viennent du plan actuel (tout dégressif ou tout linéaire). Avec une part imposable de 60 à 90 %, tout varie
dans la proportion (pic de 2028 : 5,4 à 8,1).

- **Le coût de départ est une avance.** L'État rend tout de suite l'impôt qu'il aurait perçu sur les annuités futures,
  puis le récupère, car les biens achetés après la réforme n'ont plus que la moitié de leur plan à déduire. Il ne
  reste ensuite que le coût permanent, τ·s·b·I·(1 − z(g)). Ce coût n'existe que parce que l'investissement croît.
- **Les « environ 5 Md€ » de l'ancienne variante 50 % étaient une dette de transition, pas un coût annuel.** Financée
  par 4,2 Md€ d'assiette par an, elle accumulait au plus 5,2 Md€ d'avances (en 2029), remboursés ensuite. Son coût
  permanent est de 0,67 Md€ par an. Dans le nouveau scénario, il n'y a pas de dette : le profil annuel ci-dessus est
  couvert chaque année au bouclage.
- **Le calendrier 25 % puis 50 %** coupe par deux le coût de 2027 (3,7 au lieu de 7,4). Attendre le 1er janvier 2028
  pour acheter fait gagner 0,25 × 0,25 × (1 − z), soit environ 0,8 % du prix : c'est moins qu'un mois de rendement
  d'une machine. Il faut voter le calendrier en une fois.
- **Véhicules utilitaires.** Les inclure (hypothèse : la moitié des 42 Md€ de matériel de transport) multiplie tous les
  coûts par 1,25. C'est le choix le plus neutre entre l'industrie et le transport ou le BTP, à arbitrer au bouclage.

### La moitié du gain, pour la moitié du coût

Déduire 50 % divise exactement par deux la baisse du coût d'usage obtenue par la déduction intégrale : −2,1 % contre
−4,2 % [S]. Le capital supplémentaire, le gain de production, le coût de transition et le coût permanent sont tous
divisés par deux. Le rendement par euro est donc le même (0,28 Md€ de capital par Md€ dépensé sur dix ans). La variante
50 % n'est pas plus efficace que la variante 100 % : elle demande seulement un ticket d'entrée deux fois plus petit,
compatible avec un budget sans dette.

### Ce que dit la littérature [E] et ce qu'on peut en transposer

- **Zwick et Mahon (2017, *AER* 107(1)).**
  - *Question et données* : effet du *bonus depreciation* américain (déduction immédiate partielle de 30 à 50 % en
    2001-2004 et en 2008-2010) ; déclarations de plus de 120 000 sociétés.
  - *Identification* : comparaison d'industries dont les équipements ont des durées différentes, donc plus ou moins
    touchées par la mesure.
  - *Résultat* : +10,4 % et +16,9 % d'investissement éligible. Les petites entreprises réagissent 95 % de plus.
    L'effet n'existe que chez les entreprises imposables, qui en tirent une trésorerie immédiate. Peu d'achats sont
    simplement avancés.
  - *Limites* : mesure temporaire et anticyclique ; effets relatifs entre industries, pas d'équilibre général.
- **Maffini, Xing et Devereux (2019, *AEJ: Economic Policy* 11(3)).**
  - *Question et identification* : effet des *first-year allowances* britanniques (40 % la 1re année au lieu de 25 %),
    permanentes ; doubles différences autour du relèvement des seuils de PME en 2004.
  - *Résultat* : taux d'investissement +2,1 à 2,6 points, soit +11 % à la moyenne (version de travail), en 12 à 18 mois.
    Effet du coût du capital, pas de la trésorerie. Élasticité du stock de capital au coût d'usage d'environ 1,6.
  - *Limites* : entreprises moyennes seulement ; chiffre de 11 % lu dans la version de travail.
- **Chodorow-Reich, Zidar et Zwick (2024, *JEP* 38(3), 61-88), « Lessons from the Biggest Business Tax Cut in US
  History ».**
  - *Le paquet TCJA* : recette de l'IS −40 % ; investissement corporel +8 à 14 % (consensus « autour de 11 % ») ; PIB de
    long terme +0,9 % ; salaires +750 $ par salarié. Les entreprises dont le coin fiscal baisse plus investissent plus.
  - *La déduction immédiate seule* (passage de 50 à 100 % de *bonus*) : +1,7 % de capital en dix ans pour 12,4 % de
    recette. Elle livre « la moitié de l'accumulation de capital pour un tiers du coût de la baisse du taux ».
  - *Risque pro-dette* : « an overly generous expensing regime without interest limitations can lead to negative
    effective marginal rates ».
  - *Plafonnement des intérêts* (Goodman, Isen, Richmond et Smith, 2024, cités par les auteurs) : aucun effet mesurable
    sur l'investissement, et il rapporte.
  - *Limites* : les effets agrégés viennent d'un modèle calé sur des réponses entre entreprises.
- **Transposition à la France.**
  - L'écart de départ est plus petit : le dégressif français (coefficient 2,25) avance déjà les déductions ; z moyen de
    0,87 à 5 %.
  - Les PME françaises, plus contraintes en financement, sont proches des petites entreprises de Zwick et Mahon.
  - Les sociétés en perte ne réagissent pas (voir § 5).
  - Nous retenons donc une élasticité du stock de 0,5 à 1,6 (centre 1) et un investissement de court terme de 1,8 à
    3,1 fois la baisse du coût d'usage, ordre de grandeur des 8 à 14 % obtenus pour environ 4,5 points de terme fiscal.

## 4. La baisse du taux normal

**Un point coûte 2,99 Md€ en 2027**, statique, sur toute la base une fois le taux réduit aligné. C'est bien le chiffre de
nos sorties.
- Il vaut ensuite 3,08 en 2028, 3,27 en 2030 et 4,39 en 2040 (+3 % par an [H]).
- Si la baisse touchait 2027, avant l'alignement, le point vaudrait 2,67.
- Chaque point réduit aussi le coût de la déduction d'1/25 (+0,27 Md€ en 2028, +0,04 en 2040).
- Le retour par les bénéfices déclarés (Beer, de Mooij et Liu, 2020 : semi-élasticité d'environ 1 sur les filiales de
  multinationales) réduirait le coût de 0 à 23 %. On ne le compte pas, car c'est une borne haute si on l'applique à tous.

**Attractivité.**
- Avec la contribution sociale de 3,3 %, le taux facial des grands groupes passerait de 25,8 % à 24,8 % (24 %), 23,8 %
  (23 %) ou 22,7 % (22 %). La moyenne OCDE est de 24,2 % (Tax Foundation, fiche France 2026, ITCI). Ces taux ne comptent pas la
  contribution exceptionnelle, éteinte après l'exercice 2026 dans le droit en vigueur.
- Taux moyen effectif d'un projet rentable (rendement de 20 %, notre convention) : 22,9 % aujourd'hui ; 21,0 % à 23 % ;
  19,1 % avec la combinaison à 23 %. L'OCDE donne pour la France 23,6 % en 2025, contre 22,2 % en moyenne.
- Les choix d'implantation réagissent au taux moyen effectif : semi-élasticité médiane de l'investissement direct
  étranger de −2,5 % par point (Feld et Heckemeyer, 2011, *J. Econ. Surveys*, méta-analyse de 704 estimations, résumé
  lu, biais de publication signalé).
- Ces effets ne sont pas traduits en PIB, par prudence. C'est l'argument propre au taux : la déduction n'aide ni les
  bénéfices mobiles, ni les bâtiments, ni l'immatériel acheté, ni les services peu équipés.

## 5. Taux marginal effectif (TMEI) et risque pro-dette

Convention Devereux-Griffith de nos scripts : équipement de 7 ans, rendement réel exigé 5 %, inflation 2 %,
dépréciation 14 %, pas d'impôt personnel. Les niveaux ne se comparent pas à ceux de l'OCDE ; les écarts, si [S].

| Configuration | TMEI, fonds propres | TMEI, emprunt | TMEI, 1/3 emprunt | Avantage de la dette (points de coût du capital) | Bâtiment | TMEA (20 %) |
|---|---|---|---|---|---|---|
| Aujourd'hui (25 %) | 18,0 % (20,7 linéaire ; 15,1 dégressif) | −24 % | 7,6 % | 2,06 | 22,0 % | 22,9 % |
| Taux à 23 % | 16,4 % | −21 % | 6,7 % | 1,86 | 20,2 % | 21,0 % |
| Déduction de 50 % | 9,9 % | −37 % | −1,7 % | 1,90 | 22,0 % | 20,8 % |
| **23 % + 50 %** | **8,9 %** | −33 % | −1,8 % | 1,73 | 20,2 % | 19,1 % |
| Déduction intégrale (repère) | 0 | −53 % | −13 % | 1,74 | 22,0 % | 18,8 % |
| Petite société sous le plafond, aujourd'hui | 10,4 % | −13 % | 3,8 % | 1,15 | 13,0 % | 13,7 % |

- **La réforme ne crée pas de distorsion pro-dette nouvelle.** L'avantage de la dette (fonds propres moins emprunt) vaut
  (ρ − i(1−τ)) × (1 − τz)/(1 − τ). Il diminue quand la déduction augmente et quand le taux baisse : 2,06 → 1,73 point.
- **Elle subventionne davantage la machine marginale financée par emprunt.** Son TMEI passe de −24 % à −33 % : la
  déduction des intérêts s'ajoute à une déduction rapide du prix. Le plafonnement de l'art. 212 bis (charges
  financières nettes au-delà du plus élevé de 3 M€ et de 30 % de l'EBITDA fiscal) ne touche presque aucune PME.
- **En financement mixte (1/3 de dette), le TMEI devient à peu près nul (−1,8 %).** C'est acceptable, sans garde-fou
  supplémentaire. Ce serait moins vrai à 100 %, où le TMEI mixte tombe à −13 %.
- **Petite société qui reste sous 42 500 €.** Avec 23 % et la déduction, son équipement est un peu moins taxé
  (10,4 → 8,9 %) ; ses bâtiments le sont plus (13,0 → 20,2 %).

**Biais sectoriel.** La déduction favorise les activités à équipements lourds. Les services investissent surtout en
logiciels, déjà vite amortis : les logiciels acquis le sont sur 2 ou 3 ans depuis l'abrogation de l'art. 236 II par la
LF 2017, et les logiciels créés sont déductibles immédiatement (art. 236 I). Ils investissent aussi en bâtiments, que
seule la baisse du taux aide. La combinaison corrige donc une partie du biais. Inclure les logiciels acquis coûte peu ;
inclure les véhicules utilitaires coûte 25 % de plus (§ 3).

**Pertes, vérifiées sur le BOFiP.**
- Report en avant sans limite de durée, imputable à hauteur de 1 M€ plus 50 % du bénéfice au-delà
  (BOI-IS-DEF-10-30).
- Report en arrière sur le seul exercice précédent, dans la limite de 1 M€. Il donne une créance, remboursable au bout de
  cinq ans (BOI-IS-DEF-20-10, version du 12/08/2026 ; délai de cinq ans d'après des sources secondaires).
- La déduction ne vaut rien tout de suite pour une jeune entreprise en perte. C'est aussi pourquoi notre coût ne porte
  que sur les sociétés imposables (75 % [H]).

## 6. Cas types (`is.json`, clé `cas`)

**PME industrielle : une machine de 500 000 € achetée le 1er juillet** (exercice civil, durée d'usage de 7 ans).

| | Linéaire (1/7, prorata) | Dégressif (2,25/7 = 32,1 %) |
|---|---|---|
| Déduction de la 1re année aujourd'hui | 35 714 € | 80 357 € |
| Avec la réforme (250 000 € + plan ordinaire sur le reste) | 267 857 € | 290 179 € |
| Impôt économisé la 1re année à 25 % | 8 929 → 66 964 € | 20 089 → 72 545 € |
| Avantage de trésorerie la 1re année (rendu ensuite) | **+58 036 €** (+53 393 € à 23 %) | +52 455 € |
| Avantage actualisé (5 % ; 8 %) | **9 544 €** ; 14 155 € | 6 461 € ; 9 695 € |

- **Comparaison avec la baisse du taux** (plan moyen, 5 %). Pour une machine marginale, qui rapporte juste son coût du
  capital, deux points de taux valent 1 707 € actualisés ; la déduction de 50 % en vaut 8 003.
- Pour une machine très rentable (rendement réel brut de 20 %), deux points valent 11 350 €. Mais la baisse du taux paie
  aussi tout le bénéfice déjà installé de l'entreprise : c'est là qu'est son coût.

**Petite société de services qui investit peu** (10 000 € d'informatique par an ; la déduction lui rapporte environ 80 €
par an). Variation d'IS par an (+ = perte) :

| Bénéfice | IS actuel | à 24 % | à 23 % | à 22 % |
|---|---|---|---|---|
| 30 000 € | 4 500 € | +2 700 € | +2 400 € | +2 100 € |
| 42 500 € | 6 375 € | +3 825 € | +3 400 € | +2 975 € |
| 60 000 € | 10 750 € | +3 650 € | +3 050 € | +2 450 € |
| 150 000 € | 33 250 € | +2 750 € | +1 250 € | −250 € |
| 300 000 € | 70 750 € | +1 250 € | −1 750 € | −4 750 € |

**Il y a des perdants.** Toute société éligible au taux réduit perd si son bénéfice est inférieur à 4 250/(0,25 − τ) :
**425 000 € à 24 %, 212 500 € à 23 %, 141 667 € à 22 %**. Cela concerne la grande majorité des sociétés aujourd'hui au
taux réduit. La perte est au plus de 4 250 € moins la baisse du taux sur leur bénéfice ; elle est la plus forte vers
42 500 € de bénéfice. Les sociétés qui investissent récupèrent une avance de trésorerie : environ 0,11 € d'impôt en moins
la 1re année pour 1 € d'achats, à 25 %.

## 7. Effets réels (ordres de grandeur [S], niveau de long terme, pas de taux de croissance)

| | Capital en plus (Md€) | Investissement des premières années | Investissement en régime établi | PIB potentiel de long terme |
|---|---|---|---|---|
| Déduction de 50 % | 8,4 (4,2 à 13,4) | +2,5 à 4,3 Md€/an | +0,6 à 2,0 Md€/an | +0,05 % (0,03 à 0,09), 1,6 Md€ |
| Taux à 23 % | 3,7 (1,8 à 6,6), dont bâtiments 1,9 | +0,5 à 0,9 | +0,2 à 0,6 | +0,016 % (0,008 à 0,028) |
| 23 % + 50 % | 11,2 (5,6 à 18,7) | +2,7 à 4,7 | +0,7 à 2,4 | +0,06 % (0,03 à 0,10), 1,9 Md€ |
| Déduction intégrale (repère) | 17,0 (8,5 à 27,1) | +5,0 à 8,7 | +1,3 à 4,1 | +0,11 % (0,05 à 0,17) |

**Méthode.**
- Le stock de capital suit le coût d'usage (1 − τz)/(1 − τ), avec une élasticité de 0,5 à 1,6 pour les équipements
  (541 Md€) et de 0,25 à 1 pour les bâtiments (400 Md€ [H]), sur les 75 % imposables.
- Le PIB vient d'une fonction Cobb-Douglas : l'élasticité de la production à chaque capital est la part de son revenu
  ((r + δ)K/Y : 3,4 % pour les équipements, 1,1 % pour les bâtiments ; part totale du capital d'environ 1/3), à emploi
  donné.
- L'investissement des premières années, plus fort, est transitoire. Il n'élève pas durablement le PIB au-delà de l'effet
  de niveau du stock.

**Rendement par euro.**
- Sur dix ans, la déduction accumule 0,28 Md€ de capital par Md€ dépensé, contre 0,05 pour la baisse du taux : 5 fois
  plus dans notre calcul partiel (équipements et bâtiments seulement), 1,5 fois dans le modèle complet de
  Chodorow-Reich et al.
- La baisse du taux paie surtout l'impôt sur les profits déjà installés et les rentes, mais elle seule agit sur la
  localisation (§ 4).
- Perte sèche évitée sur les équipements : 0,03 à 0,08 Md€ par an pour la déduction de 50 % ; c'est un indicateur
  d'efficacité, pas du PIB.

**Bonne utilisation des ressources ?** Oui pour la déduction. Son coût économique est d'environ 1,1 Md€ actualisé par
année d'achats (0,67 Md€ par an de coût permanent). Elle réduit de moitié le TMEI des équipements. Elle passe par les
entreprises imposables, celles qui réagissent. Son effet reste modeste (+0,05 % de PIB) ; il ne faut pas le survendre.
La baisse du taux est un moins bon instrument pour le capital domestique, mais elle est le seul pour l'attractivité et
pour les secteurs peu équipés.

## 8. Pour le bouclage

**Table `annuel`** (exercices, Md€, + = recette ; extraits) :

| | 2027 | 2028 | 2029 | 2030 | 2033 | 2035 | 2040 |
|---|---|---|---|---|---|---|---|
| Fin du taux réduit (central) | +1,33 | +2,75 | +2,83 | +2,92 | +3,19 | +3,38 | +3,92 |
| Déduction de 50 % (25 % puis 50 %) | −3,69 | −6,75 | −5,38 | −4,28 | −1,58 | −0,85 | −0,99 |
| Un point de taux normal (base totale) | −2,99 | −3,08 | −3,17 | −3,27 | −3,57 | −3,79 | −4,39 |
| Interaction par point (la déduction coûte moins) | +0,15 | +0,27 | +0,22 | +0,17 | +0,06 | +0,03 | +0,04 |
| *Mémoire : fin de la contribution exceptionnelle (droit en vigueur, non comptée)* | −7,0 | −7,0 | −7,0 | −7,0 | −7,0 | −7,0 | −7,0 |

**Contribution exceptionnelle.** Elle a été prorogée pour le second exercice clos à compter du 31/12/2025 (LFI 2026,
art. 12, BOI-IS-AUT-60), puis elle s'éteint. Il ne faut pas financer deux fois la même mesure : son extinction n'est pas
dans nos chiffres.

**Solde de l'IS avant les recettes foncières** (`scenarios_solde_is`).
- Taux à 23 % dès 2028 : −2,4 (2027), −9,6 (2028), −7,6 (2030), −5,4 (2033), −5,8 Md€ (2040).
- Taux à 24 % : −6,8 en 2028, puis −1,4 en 2040.
- Taux à 22 % : −12,4 en 2028, puis −10,1 en 2040.
- **Pour lisser, baisser le taux par étapes, à mesure que le coût de la déduction reflue.** Avec 1 point en 2029, 2 en
  2031 et 3 en 2033, le solde reste entre −2,4 et −6,8 Md€ jusqu'en 2033 ; il rejoint ensuite le régime établi du taux
  choisi (−1,4 / −5,8 / −10,1 en 2040 pour 24 / 23 / 22 %).
- À long terme, la fin du taux réduit paie la déduction et environ deux tiers de point de taux.

## 9. Limites qui peuvent changer la conclusion

- **Part imposable de 75 %** [H] : aucune statistique ne la mesure ; les coûts sont proportionnels (60 à 90 %).
- **Plan actuel** [H] : le mélange linéaire / dégressif n'est pas publié (bornes : 0,54 à 0,81 de coût permanent).
- **Croissance des bases et de l'investissement de 3 % par an** [H] ; bénéfice fiscal 2026-2027 de +2 % par an [H]
  (tome I des Voies et moyens du PLF 2027 non publié).
- **Rendement du taux réduit** [H] : 2,15 à 3,18. Pas de ventilation publiée de la base à 15 % par type de société.
- **Élasticités** [E transposées] : effet proportionnel. Si la réponse passe surtout par la trésorerie (Zwick et
  Mahon), elle dépend de la situation fiscale et de la taille.
- **TMEI** [S] : il est sensible au taux d'intérêt (rendement réel de 5 %) et à l'inflation. Avec une inflation plus forte,
  l'emprunt est encore plus subventionné.
- **Non vérifié sur source primaire** :
  - durée d'usage type des machines (7 ans retenus ; 5 à 10 ans selon les biens) ;
  - nombre de bénéficiaires du taux réduit après 2019 ;
  - coût budgétaire de l'ACE belge ;
  - délai de remboursement de la créance de report en arrière (source secondaire) ;
  - amendement de 49 000 € (source secondaire).

## Pour aller plus loin

- **Déduction intégrale à terme.** Elle se justifie si les ressources le permettent : 1,35 Md€ par an de coût permanent,
  mais 14,8 Md€ la première année d'un passage d'un coup. Il faudrait alors traiter de façon cohérente :
  - le financement par emprunt (TMEI mixte de −13 %), par exemple en retirant la déduction des intérêts sur les biens
    déduits, ou en abaissant le seuil de 3 M€ de l'art. 212 bis ;
  - les pertes : report en avant revalorisé, ou report en arrière élargi.
- **Neutralité entre dette et fonds propres.**
  - L'ACE belge (intérêts notionnels, 2006) a réduit l'endettement de 2 à 7 % (Princen, 2012, CESifo WP 3713), mais son
    coût a été élevé et largement capté par les groupes (non chiffré ici).
  - L'ACE italienne, incrémentale (2011), a réduit l'endettement des bénéficiaires à moindre coût (Branzoli et Caiumi,
    2020, *International Tax and Public Finance*). Elle a été abrogée à partir de 2024.
  - Non retenue : coûteuse pour un effet incertain sur l'investissement.
- **Autres pistes.** Amortissement « neutre », qui revalorise les annuités ; logiciels acquis inclus ; plafonnement plus
  strict des intérêts, dont l'effet sur l'investissement est nul aux États-Unis.
- **Exemple étranger.** L'Allemagne a voté en 2025 un dégressif de 30 % pour 2025-2027, puis une baisse du taux de l'IS
  d'un point par an de 2028 à 2032, de 15 à 10 %. C'est la même logique : d'abord l'investissement, ensuite le taux
  (KPMG, IHK München ; texte du BGBl. non lu).

## Figure

**g7_tmei** (pleine largeur). Titre-message proposé : « Pour un coût permanent neuf fois moindre, la déduction de 50 %
baisse cinq fois plus le taux effectif sur les machines que le passage du taux à 23 % ». Les barres donnent le TMEI d'un
équipement financé par fonds propres ; à droite, le coût brut pour l'État (pic et coût permanent). La note donne le
TMEI d'un équipement financé par emprunt. Gain de trésorerie et avantage actualisé : cas type de la machine (§ 6).

## Références vérifiées

- Zwick et Mahon (2017), *AER* 107(1), 217-248 : texte lu.
- Maffini, Xing et Devereux (2019), *AEJ: EP* 11(3), 361-389 : version de travail Dondena WP 85 lue.
- Chodorow-Reich, Zidar et Zwick (2024), *JEP* 38(3), 61-88 : NBER WP 32672 lu.
- Beer, de Mooij et Liu (2020), *J. Econ. Surveys* 34(3) : vérifié dans `revue/verif_litterature_is_pfu.md`.
- Feld et Heckemeyer (2011), *J. Econ. Surveys* 25(2), 233-272 : résumé.
- Bernini et Treibich (2016), *ICC* 25(5), 829-845 : résumé.
- Princen (2012), CESifo WP 3713 : résumé.
- Branzoli et Caiumi (2020), *ITPF* 27(6) : notice.
- CPO (2016, 2023) : d'après `is/notes/is_recherche.md`.
- Textes : CGI art. 39 A, 209 I, 212 bis, 219 I b, 220 quinquies, 236 ; BOFiP BOI-IS-LIQ-20-10, BOI-BIC-AMT-20-20-30,
  BOI-IS-DEF-10-30, BOI-IS-DEF-20-10, BOI-IS-AUT-60 ; service-public.fr F23575.
