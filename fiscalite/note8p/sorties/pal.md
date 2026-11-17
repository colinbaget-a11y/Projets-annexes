# « Pour aller plus loin » : trois prolongements hors scénario central

Compte rendu pour l'assembleur (17/11/2026). Scripts : `calculs/pal_calculs.py` (lance tout), `pal_maires.py`,
`pal_pertes.py`, `pal_revenus.py`, `pal_bareme.py` (barème lu dans `sorties/ircsg4.json`, clé `bareme`, sinon
`ircsg3.json/final`), `pal_figure.py`. Chiffres : `sorties/pal.json`. Annexe : `annexes/annexe_pal.tex`. Brouillon de la
partie : `sorties/pal_section.tex`. Figure : `figures/gpal_revenus_irreguliers.pdf`. Statuts : [E] empirique publié,
[S] simulation des auteurs, [H] hypothèse, [C] choix de politique. Aucune des trois pistes n'entre dans le bouclage ;
aucune n'est financée par la croissance.

**Barème utilisé (piste 3).** Celui de `ircsg4.json` à la date du calcul : 2,12 / 16,12 / 23,12 / 29,38 / 37,01 % aux
points 0 / 19 176 / 28 765 / 38 353 / 67 118 €, 48 % dès 163 425 €. Il diffère du barème cité dans la commande
(1,47 / 15,47 / … %) : l'autre agent l'a recalibré. Relancer `pal_calculs.py` après tout nouveau recalibrage. Les
écarts entre A et B bougent peu : ils viennent de la convexité du barème, pas de son niveau.

---

## 1. Intéresser les maires à construire

**Problème.** Construire coûte à la commune : écoles, voirie, services, opposition des habitants. Les propriétaires
en place, électeurs, ont intérêt à la rareté (Fischel, 2001). Si la commune ne retire presque aucune recette d'un
logement de plus, le refus de construire ne lui coûte rien.

**Droit et faits (vérifiés).**
- *Taxe foncière des logements neufs.* Exonération de deux ans (CGI art. 1383). Depuis 2021, la commune peut limiter
  l'exonération de sa part à 40-90 % de la base ; l'intercommunalité peut toujours la supprimer pour la sienne
  (BOFiP, ACTU-2021-00034 du 20/12/2021) [E]. En 2024, 3 956 communes remettaient en cause ou modulaient l'exonération,
  contre 2 730 en 2017 (Cour des comptes, janvier 2025) ; 41 % des communes franciliennes en 2025 (Institut Paris Région) [E].
- *Suppression de la taxe d'habitation.* Selon la Cour des comptes (« L'évolution de la répartition des impôts locaux
  entre ménages et entreprises et de la (dé)territorialisation de l'impôt », communication à la commission des finances
  de l'AN, janvier 2025 ; lue sur vie-publique.fr, fichier partiel), la recette d'un logement neuf se réduit désormais
  à la taxe foncière, ce qui « a réduit l'incitation des communes à accorder des permis de construire » ; la commission
  Rebsamen avait proposé de permettre aux communes de supprimer totalement l'exonération des logements neufs, sans suite [E].
  Les logements sociaux sont exonérés 15 à 30 ans : perte de 1,04 Md€ pour le bloc communal en 2022, compensée à hauteur
  de 40,7 M€ ; compensation intégrale pendant dix ans pour les agréments 2021-2026 (LF 2022) [E].
- *Compensation de la taxe d'habitation* par l'ancienne part départementale de taxe foncière, corrigée par un
  coefficient (« coco »). Institut Paris Région (Note rapide n° 1054, avril 2026 ; Valentin Sauques) : 100 logements
  identiques rapportent plus de 20 000 € par an d'écart de taxe foncière entre une commune à coco 0,8 et une à 1,2 ;
  dans le quart des communes franciliennes qui ont le plus construit (+11 % de logements en 2016-2024), les recettes de
  fonctionnement ont crû de 26 %, contre 20 % ailleurs ; élasticité moyenne des recettes au parc 0,36 (corrélations,
  pas un effet causal) ; aucun lien net entre construction et DGF [E]. Date exacte (23/04) vue seulement dans un moteur
  de recherche ; la note porte « Avril 2026 ».
- *Taxe d'aménagement* (unique, à la construction) : surface × 892 €/m² en 2026 (1 011 en Île-de-France) × taux
  communal de 1 à 5 % (jusqu'à 20 % dans certains secteurs) ; part départementale ≤ 2,5 % ; abattement de 50 % sur les
  100 premiers m² d'une résidence principale (service-public.fr, vérifié le 01/01/2026) [E]. Produit communal francilien :
  160 M€ en 2024 (250 M€ en 2021) [E, IPR].
- *DGF.* 27,4 Md€ en 2026, dont 19,1 pour le bloc communal [E, d'après l'avis du Sénat sur le PLF 2026 et les
  préfectures, via recherche ; LFI non relue]. La dotation forfaitaire varie avec la population DGF : 64,46 € à
  128,93 € par habitant gagné ou perdu, selon un coefficient logarithmique de la taille (CGCT art. L. 2334-7 ; réponse
  ministérielle au Sénat du 29/09/2021) [E]. Un logement de plus, soit environ 2 habitants [H], vaut 130 à 260 € par
  an, avec retard, et souvent effacés par l'écrêtement.
- *Aide aux maires bâtisseurs* (LF 2025, Fonds vert, enveloppe de 100 M€) : permis délivrés du 1/4/2025 au 31/3/2026,
  chantiers avant le 30/6/2027 ; zones A bis, A, B1, touristiques, OIN, communes SRU ; 1 000 à 2 000 € par logement plus
  un bonus de 1 000 à 1 500 € (Banque des Territoires, 30/04/2025) [E]. Sollicitée « pour plus de 70 000 logements par
  plus de 400 communes » (réponse à la QE n° 7568, AN) ; supprimée pour 2026 (circulaire du 7/4/2026, Maire-info) [E].
  **Non vérifié :** « plus de 45 M€ à 466 communes, opérations de plus de 42 000 logements ». Ces logements sont ceux des
  opérations aidées, pas des logements causés par l'aide : les permis auraient été en grande partie délivrés sans elle.

**L'effet pervers de notre réforme [S].** Avec la double taxe communale à recette constante (scénario B_E10 :
0,569 % du sol, 0,142 % du bâti, contre 0,358 % de la valeur entière aujourd'hui), la recette annuelle qu'un logement
neuf apporte au bloc communal baisse de 60 à 70 % :

| Logement neuf (hypothèses [H]) | Taxe/an aujourd'hui | Après réforme | Valeur actualisée perdue (4 %, 30 ans) |
|---|---|---|---|
| Appartement 65 m², 290 000 €, sol 25 %, densification | 780 € | 310 € (−60 %) | 6 900 € |
| Même appartement, sur un terrain nu | 980 € | 310 € (−68 %) | 10 100 € |
| Maison 100 m², 250 000 €, sol 35 %, terrain nu | 830 € | 230 € (−72 %) | 9 100 € |

(Après réforme : sans exonération de deux ans. Taxe d'aménagement communale à 3 % : 870 à 1 340 €, une fois.)
L'incitation se déplace : la commune gagne désormais quand elle **ouvre des droits à construire**, puisque la valeur du
sol monte. Si l'ouverture multiplie par cinq la valeur du sol d'un logement [H], la part communale sur le sol rapporte
330 € par an et par logement futur, avant toute construction. C'est la bonne décision à récompenser (Glaeser et
Gyourko, 2018), mais à deux conditions : des valeurs actualisées chaque année, et une commune qui ne gagne pas aussi
à la rareté (si elle freine la construction, la valeur des sols déjà bâtis monte aussi). Ce second effet n'est pas
mesuré [H].

**Options comparées.**
1. *Renforcer la part démographique de la DGF* : mal ciblée (récompense la population, pas les logements ; une commune
   dont la taille des ménages baisse perd en construisant), décalée de plusieurs années, brouillée par l'écrêtement ;
   l'IPR n'observe pas de lien construction-DGF. Écartée.
2. *Dotation automatique par logement supplémentaire net* : **retenue [C].**
3. *Territorialiser une partie de la taxe nationale sur le sol* : la commune garde déjà sa part sur le sol (0,569 %),
   qui récompense l'ouverture de droits ; lui rendre 25 % de la part nationale ajouterait 23 € par logement et par an :
   négligeable, et elle rétribuerait aussi la rareté. Écartée.

**Architecture retenue [C].** Une dotation versée à la commune pour chaque logement supplémentaire net (stock de
logements imposés à la taxe foncière, fichier foncier, de l'année N moins celui de N−1 : démolitions et changements
d'usage déduits ; divisions et transformations comptées), en zones tendues (A bis, A, B1), en une fois, l'année
d'entrée au rôle. Pas de bonus densification (le compte net récompense déjà la densification sans critère de plus),
pas de condition environnementale ou de type de logement. En cas de PLU intercommunal, partage fixe commune / EPCI
(à arbitrer ; le NHB anglais versait 80/20 dans les zones à deux niveaux). Financement à enveloppe constante, par un
prélèvement uniforme sur la dotation forfaitaire : les communes qui ne construisent pas y perdent, comme un quart des
autorités anglaises sous le NHB.

| Montant / logement | 150 000 logements | 280 000 (mises en chantier 2025 : 279 700, SDES) | 300 000 |
|---|---|---|---|
| 2 000 € | 0,30 Md€ | 0,56 Md€ | 0,60 Md€ (3,1 % de la DGF du bloc communal) |
| 3 000 € | 0,45 | 0,84 | 0,90 |
| 5 000 € | 0,75 | 1,40 | 1,50 (7,9 %) |

Recommandation : **5 000 € par logement net en zone tendue**, soit à peu près la moitié à trois quarts de la recette
foncière actualisée que notre réforme retire à la commune, ou six à huit ans de cette recette (l'horizon d'un mandat) ;
coût de l'ordre de 0,75 à 1,5 Md€ selon la part des logements en zone tendue (non mesurée ici [H]), soit 4 à 8 % de la
DGF du bloc communal.

**Littérature.** *New Homes Bonus* (Angleterre, 2011) : par logement net supplémentaire (après démolitions), la taxe
d'habitation moyenne nationale pendant six ans, plus 350 £ par logement abordable ; fonds de 200 M£ (2011-12) à près de
1 Md£ (2014-15), financé par redistribution. Évaluation du DCLG (décembre 2014) : incitation jugée « simple, transparente »
et « puissante » par près de la moitié des urbanistes, mais 11 % seulement la disent importante pour le nombre de
logements des plans locaux ; un peu plus d'un tiers en tiennent compte pour les permis ; pas d'estimation causale. Le
NAO (2013) jugeait irréaliste l'effet de +13 % annoncé (« erreur arithmétique substantielle ») et impossible d'isoler un
contrefactuel [E]. Hilber et Vermeulen (2016, *Economic Journal*, 353 autorités 1974-2008) : les contraintes
réglementaires expliquent une large part de la réaction des prix à la demande ; prix du Sud-Est inférieurs d'environ
25 % en 2008 avec la réglementation du Nord-Est [E]. Glaeser et Gyourko (2018, *JEP*) : là où les prix dépassent nettement
le coût de construction, l'écart est une « taxe » réglementaire implicite ; ailleurs, l'offre est élastique [E] :
c'est le fondement du ciblage sur les zones tendues. Fischel (2001, *The Homevoter Hypothesis*) : les propriétaires
électeurs freinent la construction pour protéger la valeur de leur bien [E, thèse appuyée sur des études de cas].
Japon (zonage national) : non examiné faute de source vérifiée dans le temps imparti.

**Croissance.** Plus de logements dans les zones chères, c'est plus de mobilité vers les emplois productifs ; mais
aucune étude ne mesure de façon crédible l'effet d'une dotation par logement sur la construction : **pas de chiffre**.
Limite qui peut changer la conclusion : si l'élasticité des permis à la dotation est faible (cas anglais), la mesure
est surtout une redistribution entre communes, à coût nul pour l'État mais sans gain.

---

## 2. Mieux traiter les pertes des entreprises

**Problème.** L'État prend 25 % des bénéfices l'année même, mais ne rend 25 % des pertes que plus tard, plafonné, ou
jamais si l'entreprise disparaît. L'asymétrie pénalise le risque (Domar et Musgrave, 1944) et l'investissement des
entreprises en perte : notre déduction immédiate de 50 % perd un tiers de sa valeur après un an de pertes et les trois
quarts après trois ans (`is4.json`, « pertes » : 1,60 → 1,07 → 0,41 pour 100 d'achat) [S].

**Droit (BOFiP, novembre 2026).** Report en avant illimité depuis 2004 ; imputation plafonnée à 1 M€ plus 50 % du
bénéfice au-delà (60 % de 2011 à 2012, 50 % depuis les exercices clos au 31/12/2012) (CGI art. 209 I ; BOI-IS-DEF-10-30).
Report en arrière (art. 220 quinquies ; BOI-IS-DEF-20, 20-10, 20-20) : sur option, le seul déficit de l'exercice, sur
le bénéfice de l'exercice précédent, dans la limite de 1 M€ ; créance non imposable, imputable sur l'IS des cinq années
suivantes, remboursée au terme ; remboursement anticipé en procédure collective ; mobilisable auprès des banques. Avant
la LFR 2011-2 (loi 2011-1117), report en arrière sur trois exercices sans plafond. Crise : remboursement immédiat des
créances 2015-2020 (LFR 2020-935, art. 5) ; report du premier déficit clos entre le 30/6/2020 et le 30/6/2021 sur les
trois exercices précédents, sans plafond, conditionné à l'absence de dividendes (LFR 2021-953, art. 1 ; BOI-IS-DEF-20-30)
[E]. Garde-fous anti-« achat de déficits » : perte des déficits en cas de changement d'objet social ou d'activité réelle
(art. 221, 5), transfert sur agrément en cas de fusion (art. 209 II), imputation sur le seul bénéfice propre des
déficits antérieurs à l'entrée dans un groupe intégré (art. 223 I) [E]. Non vérifié sur le texte : un plafond
temporaire de 2,5 Md€ (LF 2025, art. 97, selon Légifiscal) pour les très grands déficits.

**Données.** Déficits nouveaux des sociétés à l'IS : 65 Md€ (2018), 83 (2021), 113 (2022) (DGFiP, *Statistiques*
n° 21, avril 2024) [E]. Report en arrière : 1,2 Md€ et 22 000 entreprises en 2021 ; 0,2 Md€ et 7 800 en 2022 (même
source) [E]. Stock reportable : 315 Md€ fin 2010, dont 160 jugés imputables un jour (53 Md€ de droits) ; consommation
de l'ordre de 25 Md€ par an en 2007-2010 (compte général de l'État 2010, cité par le rapport Carrez n° 3718) [E]. Pas
de chiffre public plus récent trouvé. Rendement du plafonnement de 2011 : 0,5 Md€ en 2011 et 1,5 Md€ en 2012
(évaluation préalable, rapport Marini n° 787) [E]. Coût de l'assouplissement de 2021 : 0,4 Md€ (rapporteur général du
Sénat, 23/06/2021) [E].

**Simulation [S]** (`pal_pertes.py`, IS 25 %, actualisation 5 %). Taux effectif = VA de l'impôt / VA du résultat ;
symétrie = 25 %.

| Profil | Actuel | Indexation (OAT 3,37 %) | Sans plafond | Report arrière 3 ans, remboursé | Remboursement accéléré seul |
|---|---|---|---|---|---|
| Jeune PME : −0,4 M€ × 3 ans puis +0,5 M€ × 9 ans | 26,7 % | 25,6 % | 26,7 % | 26,7 % | 26,7 % |
| Entreprise établie (+3 M€) : −2 M€ × 3 ans puis +2,5 M€ | 26,8 % | 25,9 % | 26,7 % | 25,7 % | 26,5 % |
| Même entreprise, qui disparaît après 3 ans de pertes | l'État porte 3,4 % de la perte | 3,4 % | 3,4 % | 16,3 % | 4,2 % |

Avec une actualisation au taux de l'OAT, l'indexation rétablit exactement la symétrie pour la jeune PME (25,0 %).
Lecture : pour une entreprise qui finit par gagner de l'argent, l'asymétrie coûte 1 à 2 points de taux effectif (3 à
4 points à 8 %) ; seule l'indexation aide la jeune entreprise sans passé bénéficiaire ; le plafond ne joue que pour les
bénéfices au-delà de 1 M€ ; le report en arrière n'aide que celles qui ont déjà payé l'impôt, et c'est le seul
instrument qui rembourse une entreprise qui disparaît.

**Coûts.** (1) *Indexation des nouveaux déficits* : rien les premières années (les déficits indexés ne sont imputés
qu'ensuite), puis, en régime, τ × déficits imputés × ((1+i)^âge − 1) : 1,1 Md€ par an au centre (32 Md€ imputés par
an, âge moyen 4 ans), 0,4 à 2,2 Md€ selon les hypothèses [S/H] ; montée en charge sur quatre à six ans. Pas de coût
sur les déficits jamais utilisés. Pour l'État qui s'endette au taux de l'OAT, le coût actualisé est la valeur du délai
qu'il capte aujourd'hui sur les déficits finalement imputés : un vrai coût, pas un transfert gratuit. (2) *Assouplir
le plafond* : surtout de la trésorerie, au bénéfice des seules entreprises à plus de 1 M€ de bénéfice ; ordre de
grandeur : le rendement de son introduction (1,5 Md€ en 2012) ; part permanente (déficits qu'une entreprise disparue
n'aurait jamais imputés) inconnue. (3) *Report en arrière sur 3 ans et remboursement rapide* : coût de trésorerie très
cyclique (1,2 Md€ en 2021 avec un dispositif de 1 an plafonné, 0,4 Md€ pour l'extension temporaire de 2021) ; coût
permanent = remboursements à des entreprises qui disparaissent ensuite. Le seul remboursement immédiat de la créance
actuelle (1 an, 1 M€) coûte peu : un décalage de trésorerie sur 0,1 à 0,2 Md€ de créances par an en temps normal [S].

**Littérature.** Domar et Musgrave (1944, *QJE*) : avec compensation intégrale des pertes, l'impôt proportionnel peut
accroître la prise de risque ; sans elle, il la réduit [E, théorie]. Auerbach (1986, *RES*) : l'asymétrie fait dépendre
le coût du capital de la situation fiscale future de l'entreprise [E, théorie]. Devereux, Keen et Schiantarelli (1994,
*JPubE*, 597 sociétés britanniques 1973-1986) : l'asymétrie crée de grands écarts de position fiscale, mais sa prise en
compte améliore peu l'explication de l'investissement [E]. Ljungqvist, Zhang et Zuo (2017, *JAR* 55(3) ; 113 changements
de taux d'IS des États américains) : les entreprises réduisent leur risque quand l'impôt monte, pas l'inverse, et les
règles de report des pertes atténuent cette réaction [E]. Langenmayr et Lester (2018, *Accounting Review*) : la prise de
risque croît avec la durée des reports en avant et en arrière, sur données internationales [E]. Dreßler et Overesch
(2013, *ITPF*, multinationales allemandes) : un report en avant limité dans le temps réduit l'investissement des
entreprises à forte probabilité de pertes [E]. Bethmann, Jacob et Müller (2018, *Accounting Review*) : un report en
arrière plus généreux accroît l'investissement des entreprises en perte, mais un tiers seulement du remboursement est
investi, surtout par des entreprises enclines au surinvestissement, et les moins productives sortent plus tard [E] :
argument contre des remboursements inconditionnels. Limites : identification par réformes de taux ou de règles, effets
souvent hétérogènes ; aucune étude française.

**Recommandation [C].** Indexer les **nouveaux** déficits reportables sur le taux de l'OAT à 10 ans, garder le
plafond d'imputation (sa suppression profite aux grands bénéficiaires pour un gain d'incitation faible), et rembourser
la créance de report en arrière existante l'année suivante plutôt qu'au bout de cinq ans. Coût : environ 1 Md€ par an
en régime (0,4 à 2,2), presque rien les premières années. L'indexation récompense les projets qui deviennent
rentables, ne verse rien aux entreprises qui échouent (pas le risque de Bethmann et al.), rend sa valeur à la
déduction de 50 % pour les entreprises en perte ; elle augmente la valeur d'une coquille déficitaire, ce qui suppose de
garder les garde-fous des articles 221, 5, 209 II et 223 I. Elle ne règle pas l'asymétrie pour les échecs : c'est le
prix d'éviter le soutien aux entreprises non viables.

**Croissance.** Effet qualitatif plausible sur la prise de risque et l'investissement des jeunes entreprises
(littérature ci-dessus), non chiffré : les élasticités publiées ne se transposent pas à la France sans hypothèses fortes.

---

## 3. Ne pas pénaliser les revenus irréguliers

**Problème.** Avec un barème progressif annuel, deux personnes au même revenu cumulé paient un impôt différent si
l'une a des revenus irréguliers. Notre barème continu supprime les marches, pas la convexité.

**Exemple [S]** (barème de `ircsg4.json`, personne seule, revenus après cotisations, 250 000 € en cinq ans).

| | An 1 | An 2 | An 3 | An 4 | An 5 | Total | Taux moyen |
|---|---|---|---|---|---|---|---|
| Revenus de B | 10 000 | 20 000 | 30 000 | 70 000 | 120 000 | 250 000 | |
| A (50 000 € par an), impôt | 9 748 | 9 748 | 9 748 | 9 748 | 9 748 | **48 739** | 19,5 % |
| B, impôt annuel | 577 | 1 883 | 3 920 | 16 766 | 36 862 | **60 008** | 24,0 % |
| B, lissage glissant sur 3 ans | 577 | 1 640 | 3 434 | 14 827 | 35 790 | **56 268** | 22,5 % |
| B, option pour 5 ans (quotient pluriannuel) | 577 | 1 701 | 3 373 | 12 502 | 30 586 | **48 739** | 19,5 % |

B paie 11 268 € de plus que A (+23 %) ; le lissage sur 3 ans réduit l'écart à 7 528 € ; l'option pour 5 ans
l'annule. Profil inverse (120, 70, 30, 20, 10 k€) avec l'option pour 5 ans : 36 862, 16 053, 1 136, puis
restitutions de 1 541 et 3 770 € : le mécanisme est symétrique, ce qui oblige à prévoir les restitutions.

**Droit (vérifié).** *Quotient* (CGI art. 163-0 A ; impots.gouv.fr, page modifiée le 07/04/2026) : revenu exceptionnel
par nature et par montant (supérieur à la moyenne des revenus des trois années précédentes), coefficient 4 ; revenus
différés : coefficient = nombre d'années + 1 ; **exclut les revenus « réalisés dans le cadre normal d'une activité
professionnelle », même très variables** [E]. *Étalement agricole* (art. 75-0 A ; BOI-BA-LIQ-10, version du
22/06/2022) : fraction du bénéfice supérieure à 25 000 € et à 1,5 fois la moyenne des trois exercices précédents,
rattachée par septièmes à l'exercice et aux six suivants ; quotient applicable à chaque fraction [E]. *Moyenne
triennale agricole* (art. 75-0 B ; BOI-BA-LIQ-20-10, version du 12/06/2024) : base = moyenne de l'année et des deux
précédentes ; option de trois ans tacitement reconduite ; à la cession, à la cessation ou au décès, l'excédent du
bénéfice sur la moyenne est taxé au taux marginal de la moyenne [E]. *Artistes, écrivains, sportifs* (art. 100 bis ;
BOI-BNC-SECT-20-10-10 et 20-10-20) : moyenne des recettes et des dépenses sur 3 ou 5 ans, sur option, révocable,
l'option continuant à produire ses effets pour les années couvertes ; extension aux salaires par l'art. 84 A [E, 84 A
d'après le Voies et moyens]. *Coûts* (Voies et moyens, tome II, PLF 2026) : étalement agricole (n° 170306) 11 M€ en
2024, 500 entreprises ; art. 84 A et 100 bis (n° 110307) « non chiffré » ; art. 75-0 B référencé (n° 170302) sans
fiche chiffrée ; le quotient n'est pas une dépense fiscale chiffrée [E].

**Architecture proposée [C].** Une option ouverte à tous pour les **revenus professionnels** du nouvel impôt (salaires,
bénéfices non salariés, droits d'auteur), remplaçant 75-0 A, 75-0 B, 84 A, 100 bis et le quotient des revenus
professionnels (le quotient reste pour les revenus différés) :
- option irrévocable pour cinq ans, renouvelable ; impôt cumulé de la période = 5 × impôt du revenu moyen ; chaque année,
  on paie l'impôt cumulé dû sur le revenu moyen des années écoulées, moins ce qui a déjà été payé (restitution possible) ;
- sortie anticipée (cessation, décès, départ à l'étranger) : régularisation immédiate sur les années écoulées (rien de
  plus à calculer que l'année en cours) ; un départ à l'étranger solde la période avant de rendre une restitution ;
- prélèvement à la source : taux personnalisé de l'année calculé, comme aujourd'hui, sur la dernière déclaration,
  mais à partir du revenu moyen de la période ; la déclaration annuelle régularise ;
- revenus du capital et plus-values exclus (prélèvement forfaitaire) ; individuel, donc pas de question de foyer.
Variante plus simple et moins coûteuse : lissage glissant sur 3 ans (réduit l'écart d'un tiers dans l'exemple).

**Budget.** Trois effets à distinguer : (a) un *report de recettes* : une moyenne glissante de type 75-0 B impose
plus tard une partie d'un revenu en hausse, rattrapée à la sortie ; le quotient pluriannuel n'en crée pas (l'impôt
cumulé n'excède jamais celui du revenu moyen), mais ses restitutions avancent la dépense quand les revenus baissent ;
(b) un *coût de transition* : la première vague d'options vient de ceux qui s'attendent à une période irrégulière
(sélection) ; (c) un *coût permanent* : la recette tirée aujourd'hui de la convexité du barème sur les revenus variables
(11 268 € sur cinq ans pour B, soit 4 264 € de moins l'année 4 et 6 276 € l'année 5). Un chiffrage national exige des données
longitudinales individuelles (panel de déclarations) que nous n'avons pas : **pas de chiffrage**. Seuls ordres de
grandeur solides : les régimes actuels coûtent peu (11 M€ pour l'étalement agricole) ou ne sont pas chiffrés. Aux
États-Unis, la suppression de l'*income averaging* général par la loi de 1986 était estimée à 8,6 Md$ sur 1986-1990
(JCT, JCX-24-85, d'après une source secondaire, non relue) [E].

**Littérature.** Vickrey (1939, *JPE* 47(3)) : moyenne cumulative, impôt recalculé sur le revenu cumulé avec intérêts,
neutre au calendrier [E, théorie] ; jamais appliquée à grande échelle. Batchelder (2003, *Harvard Journal on
Legislation* 40) : sur le PSID 1987-1992, l'imposition annuelle pèse surtout sur les ménages modestes à revenus
variables ; propose de lisser le crédit d'impôt sur deux ans [E]. États-Unis : moyenne générale supprimée en 1986
(Tax Reform Act, P.L. 99-514), rétablie pour les agriculteurs et pêcheurs en 1997 (Schedule J, moyenne sur trois
années) [E, IRS]. Australie : moyenne pour les « special professionals » (auteurs, artistes, sportifs, inventeurs) :
le revenu au-delà de la moyenne des quatre années précédentes est imposé comme s'il était étalé sur cinq ans ;
régime distinct pour les agriculteurs (ATO) [E]. Gentry et Hubbard (2000, *AER P&P*) : la convexité du barème réduit
l'entrée dans l'entrepreneuriat (PSID) [E, identification discutée]. Canada : non vérifié.

**Croissance.** Le lissage réduit la pénalité fiscale du risque de revenu (création d'entreprise, carrières à
primes, professions artistiques) ; l'effet n'est pas chiffrable de façon fondée : **pas de chiffre**.

---

## Figure proposée

`gpal_revenus_irreguliers` — titre-message : « À revenu cumulé égal, des revenus irréguliers coûtent 11 000 € d'impôt de
plus en cinq ans ; une option de lissage sur cinq ans efface l'écart. » À placer dans la partie si la place le permet ;
sinon en annexe.

## Limites qui peuvent changer les conclusions
- Maires : aucune élasticité crédible de la construction à une dotation ; part des logements en zone tendue non
  mesurée ; taux communaux moyens (le coco et les taux locaux font varier la perte de recette d'un facteur 2 ou plus).
- Pertes : âge moyen des déficits à l'imputation et volume imputé non publiés ; le coût de l'indexation peut doubler.
- Revenus : coût permanent inconnu sans panel ; risque d'optimisation (déplacement de revenus entre années dans une
  période) limité par l'irrévocabilité, mais réel pour les dirigeants qui fixent leur rémunération.
