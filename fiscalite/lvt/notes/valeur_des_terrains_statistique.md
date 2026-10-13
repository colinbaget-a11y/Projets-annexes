# Agent F : la « valeur des terrains bâtis » (AN.2111) est-elle un objet statistique robuste ?

Date de vérification : 13/10/2026. Les PDF et leurs extractions texte sont dans `scratchpad/lit/agentF/`. Le script de calcul est `scratchpad/scripts/agentF_landgdp.py`.

Légende :
- **[TI]** : texte intégral téléchargé et lu ; les passages cités ont été vérifiés dans le texte extrait.
- **[R]** : résumé ou notice seulement.
- **[S]** : source secondaire.
- **[C]** : calcul de l'agent à partir de données vérifiées.
- **NON VÉRIFIÉ** : non confirmé.

---

## 1. Insee : comment sont estimés les « terrains bâtis » dans les comptes de patrimoine

### 1.1 Base 2020 : fiche méthodologique n° 24 (juillet 2026) [TI]

**Référence** : Insee, « Fiche méthodologique – La refonte du compte de patrimoine non financier en base 2020 », juillet 2026, 6 p.
- https://gestion-metadonnees-api.insee.fr/api/documents/document/2891/file
- Également listée comme « Fiche méthodologique n° 24 » sur https://www.insee.fr/fr/metadonnees/source/serie/s2144/documentation-methodologique (URL du fichier : https://insee.fr/fr/metadonnees/source/fichier/fiche_methodologique_refonte_compte_patrimoine.pdf).
- Fichier local : `agentF/insee_doc2891.txt`.

**Passages clés (verbatim)** :

- *Méthode résiduelle, ancrée sur l'ENL* : « L'actif résidentiel est un actif composite : il comprend d'une part les logements, qui sont des actifs fixes produits, et d'autre part les terrains sous-jacents, qui sont des actifs non produits. Les Enquêtes Nationales sur le Logement (ENL) […] permettent d'estimer, à certains points de référence, la valeur totale de l'actif résidentiel. Le partage entre les logements et les terrains est ensuite obtenu en déduisant de la valeur totale la valeur des logements qui est obtenue désormais par la méthode de l'inventaire permanent. »
- *Points d'ancrage anciens* (note 3) : « Ajout de l'ENL 2013, précédemment la dernière estimation disponible était l'ENL 2006. »
- *Inventaire permanent (MIP) pour les « murs », durée de vie 70 ans* : « le traitement de l'actif logement (au sens "les murs") est également revu afin d'adopter la méthode de l'inventaire permanent […] en initialisant une méthode d'inventaire permanent avec une durée de vie de 70 ans. »
- *Pourquoi la valeur des terrains est révisée* : « La valeur des terrains est révisée principalement dans cette version pour deux raisons : (i) la prise en compte les dernières enquêtes nationales sur le logement et donc la révision du total de l'actif logement et terrains sous logement ; (ii) la modification de la méthode utilisée pour mesurer l'actif logement (cf supra) qui a un impact direct, sur la valeur déduite des terrains. »
- *Méthode hybride* : le niveau 2022 publié auparavant est conservé, puis les évolutions de la nouvelle méthode sont appliquées à partir de 2023. « La série d'indice de prix des terrains sous logements (dérivée du partage murs/terrains) est conservée jusqu'en 2022 et uniquement raccordée en évolution à partir de 2023. »
- *Terrains non résidentiels* (point important) : l'indice de prix des terrains sous logements « est également mobilisé pour la valorisation des autres terrains bâtis ainsi que de la composante urbanisable des terrains non bâtis ». La note 4 précise : « Les terrains non bâtis sont valorisés avec une partie urbanisable, via le prix des logements et une partie non urbanisable, via le prix des terres agricoles et des forêts. »
  - **Conséquence** : les terrains sous bâtiments non résidentiels ne sont pas estimés par un résidu propre. Ils sont valorisés avec l'indice des terrains résidentiels, lui-même issu du résidu.
- *Révision des niveaux reportée* : « La révision complète du partage murs/terrains sera réalisée dans le cadre de la prochaine base », dont la publication est « prévue pour mai 2030 ».
- *Ampleur de la révision non publiée* (note 5) : « La révision présentée sur la période 1978-2022 n'intègre pas les effets de la refonte sur les actifs fixes et les terrains […] il convient de se reporter à la publication Insee Méthodes associée à venir. »
  - L'ampleur de la révision du niveau des terrains bâtis due à la refonte n'est donc **pas publiée à ce jour** (NON VÉRIFIÉ / non disponible).
- Aucune déclaration chiffrée d'incertitude (intervalle de confiance, par exemple) dans la fiche.

**Ce que l'Insee ne documente pas publiquement (NON VÉRIFIÉ)** :
- La manière dont la valeur totale de l'actif résidentiel est interpolée ou extrapolée entre deux ENL et après 2013 (indices Notaires-Insee ? parc × prix ?).
- La nature exacte de la valeur issue de l'ENL (valeur déclarée par les propriétaires ?).
- **Indice indirect** : l'Insee Première n° 2028 attribue la baisse de 2023 « principalement » à « la baisse du prix des biens immobiliers (-3,9 % selon l'indice INSEE-Notaire) », ce qui suggère que les indices Notaires-Insee pilotent la valeur totale. La méthode exacte reste NON VÉRIFIÉE.

### 1.2 Base 2010 : dossier « Les comptes nationaux passent en base 2010 » (Insee, 2014) [TI]

URL : https://www.insee.fr/fr/statistiques/fichier/2832834/comptes-nationaux-base-2010.pdf (fichier local : `agentF/comptes-nationaux-base-2010.txt`).

- *Logements : MIP « modifié », calé sur l'Enquête Logement* : « Le patrimoine en logements (hors frais liés) constitue un cas particulier : il est évalué à partir d'une méthode d'inventaire permanent modifiée visant à intégrer l'estimation directe du patrimoine total en logements de la France métropolitaine par l'Enquête Logement (EL) ». Le dossier décrit ensuite le taux de renouvellement et le taux d'amortissement « comme fonction linéaire du taux de renouvellement du capital ». Hypothèses du MIP standard : lois de mortalité log-normales et amortissement linéaire.
- *Terrains : surfaces Teruti-Lucas × prix différenciés* : « La nomenclature de l'enquête Teruti Lucas a changé avec pour conséquence une modification de la valorisation des terrains. En effet cette enquête permet de ventiler les terrains en divers types d'utilisation, auxquels des prix différenciés sont appliqués. La mise à jour de cette ventilation s'est effectuée au profit des terrains bâtis et au détriment des terrains cultivés. » Et : « Le prix de fin d'année des terrains sous logements a été revu à la baisse pour l'ensemble des années étudiées. »
- *Révision de niveau* (tableau, année 2010, Md€) : « Terrains » 5 613 (base 2005) → 5 715 (base 2010) ; « dont terrains sous construction » 5 171 → 5 101. « Constructions » 5 973 → 5 601, dont logements 3 928 → 3 741.
  - Le changement de méthode sur les constructions (frais liés) a pesé −372 Md€.
- *Autre mention* : « L'évaluation des terrains, poste le plus important du patrimoine, a été revue grâce à la reconstitution des séries longues sur l'utilisation des sols. »
- *Source de la méthode antérieure* citée par ce dossier : « Comptes de patrimoine et de variations de patrimoine », Note de la base 2000 n° 10, Insee, 2008. **Non lue** (non trouvée en ligne).
- *Insee Méthodes n° 106* : https://www.epsilon.insee.fr/jspui/bitstream/1/7267/1/imethode106.pdf, cité par Cavailhès, « Fonciers en débat », 20/11/2019. **Non lu** (le serveur epsilon.insee.fr a renvoyé une erreur 502 via le proxy).

### 1.3 Ce que dit le guide Eurostat-OCDE (2015) sur la France [TI]

- Tableau 4A.1 (enquête OCDE 2011) : pour la France, « All land including land underlying buildings and structures ».
  - Sources de prix : « Price index of existing dwellings ; Selling value of lands from annual survey led by the Ministry of Agriculture ».
  - Méthode : « Residual approach for land underlying buildings ».
  - Valeur des terrains publiée séparément : « Yes ».
- §6.189 : « Only a few countries currently use the residual approach (Australia, Belgium, France, Italy and the Netherlands) or the LSR approach (Canada) ».
- Tableau 6.20 (hypothèses de durée de vie, amortissement linéaire) pour la France : logements individuels 90 ans ; bâtiments industriels 90 ; commerces 75 ; hôpitaux 75 ; écoles 75 ; routes 120 ; retraits log-normaux.
  - La base 2020 « tardive » est passée à **70 ans** pour les logements (fiche 2026).
- §6.217 : « For France, most assumptions about the service lives of non-residential assets were set in 1996 […]. For dwellings, estimates of the stock of housing from the National Housing Survey, conducted about every five years, have been used to refine the PIM estimates. »

### 1.4 Niveaux publiés et révisions entre millésimes [TI + C]

- **Insee Première n° 2028** (11/12/2024), https://www.insee.fr/fr/statistiques/8305990, fin 2023 :
  - terrains bâtis S1 = **6 346 Md€** (ménages 3 829), soit −13,7 % sur 2022-2023 ;
  - logements = 6 018 Md€ ;
  - « la diminution des prix des terrains (-13,7 %) l'a emporté sur la hausse du prix des bâtiments (+3,8 %) ».
- **Insee Première n° 2081** (06/11/2025), https://www.insee.fr/fr/statistiques/8661938, fin 2024 :
  - terrains bâtis S1 = **6 729 Md€** (−2,7 %), ménages 4 043 ;
  - logements = 5 977 Md€ ;
  - « la valeur des terrains baisse (-2,7 %, après ‑8,6 %) » ;
  - Définitions : « Les plus ou moins‑values latentes sur l'immobilier sont imputées aux terrains sous-jacents. »
- **Tableau Insee T_8201** (fichier du 17/10/2025, base 2020 ; lu dans `lit/agentC/T_8201.xlsx`), N2111N (terrains supportant des bâtiments et ouvrages) :
  - 2022 = 7 566,7 ; 2023 = 6 917,9 ; 2024 = 6 728,9 Md€ ;
  - N211N (tous terrains) : 2022 = 9 104,5 ; 2023 = 8 383,0 ; 2024 = 8 229,8.
- **[C] Révision d'un millésime à l'autre** : le niveau 2023 des terrains bâtis passe de 6 346 (déc. 2024) à 6 918 Md€ (oct. 2025), soit **+572 Md€ (+9 %)**. La baisse 2023 passe de −13,7 % à −8,6 %.
- **[C] Eurostat** (nama_10_nfa_bs, mis à jour le 28/09/2026, donc probablement le millésime 2026 post-refonte) : France, N211N S1 = 9 512 (2022) ; 8 667 (2023) ; 8 597 (2024) ; 8 652 (2025) Md€.
  - Ces niveaux sont supérieurs de 3 à 4,5 % à ceux du T_8201 de 2025 pour 2022-2024. Le raccordement à l'évolution n'empêche donc pas des écarts de niveau d'un millésime à l'autre (cause précise NON VÉRIFIÉE).
- **[C] Ratio au PIB** (PIB Eurostat B1GQ) : terrains bâtis 2024 = 6 729 / 2 935 = **229 % du PIB** ; 2022 = 7 567 / 2 654 = 285 % du PIB.
- Fiche RPM « Patrimoine des ménages en comptabilité nationale » (Insee Références, éd. 2018, base 2010) : la part des terrains bâtis dans le patrimoine immobilier des ménages « est passée de moins de 20 % fin 1998 à plus de 50 % fin 2007, avant de redescendre à 45 % fin 2016 ».
  - URL : https://www.insee.fr/fr/statistiques/fichier/3549498/REVPMEN18_F2.2_patri-men-comptaNat.pdf [TI]

---

## 2. Doctrine internationale

### 2.1 SCN 2008 [TI] (https://unstats.un.org/unsd/nationalaccount/docs/SNA2008.pdf ; local `agentF/SNA2008.txt`)

- **§10.175** : « Land consists of the ground, including the soil covering and any associated surface waters, over which ownership rights are enforced and from which economic benefits can be derived by their owners by holding or using them. The value of land excludes any buildings or other structures situated on it or running through it […] ».
- **§10.176** : « land improvements and the costs of ownership transfer on land are treated as fixed assets and shown separately ».
- **§10.44** : les améliorations de la terre à l'état naturel sont « treated as the creation of a new fixed asset and are not regarded as giving rise to an increase in the value of the natural resource ».
- **§13.44** : « In principle, the value of land […] is the value of land excluding the value of improvements, which is shown separately under fixed assets, and excluding the value of buildings on the land […]. Land is valued at its current price paid by a new owner, excluding the costs of ownership transfer ».
- **§13.46** : « For land underlying buildings, the market will, in some instances, furnish data directly on the value of the land. More typically, however, such data are not available and a more usual method is to calculate ratios of the value of the site to the value of the structure from valuation appraisals and to deduce the value of land from the replacement cost of the buildings or from the value on the market of the combined land and buildings. When the value of land cannot be separated from the building […] the composite asset should be classified in the category representing the greater part of its value. »
- **Remarque** : le SCN définit la valeur du sol **en l'état** (prix payé par un nouveau propriétaire pour le terrain sous le bâtiment existant). Il ne parle ni de « highest and best use » ni de valeur « as if vacant ».

### 2.2 Eurostat-OCDE (2015), *Compilation guide on land estimation* [TI]

- **Référence** : Luxembourg, Office des publications de l'UE, ISBN 978-92-79-43301-6, doi:10.2785/59489.
- PDF : https://unstats.un.org/unsd/nationalaccount/consultationDocs/KS-GQ-14-012-EN-N.pdf (local `agentF/eurostat_oecd_land_guide.txt`).

**Définitions et nomenclature**
- AN.2111 se subdivise en AN.21111 (terrains sous logements) et AN.21112 (sous autres bâtiments et ouvrages).
- §2.13 : séparer la valeur du sol de celle des bâtiments.
- §2.14 : « Separate estimates, even if they are rough, are clearly to be preferred above registration of the combined value under the more valuable asset. »
- §2.15-2.16 : les améliorations de la terre (AN.1123) et les coûts de transfert sont exclus du terrain.

**Méthodes**
- **Directe** (surface × prix, éq. 1). §5.15 : si le prix de transaction manque, utiliser par exemple « publicly-appraised market-price equivalent, property tax information converted to a market price, […] generalised standard land values ».
- **Résiduelle** (LV = CV − C, éq. 2-3 ; C issu du MIP).
  - *Forces* (§6.103-6.105), notamment : « the value of land underlying constructions, calculated as a residual, can be an important benchmark to verify assumptions underlying the PIM ».
  - *Faiblesses* :
    - §6.108 : « Every bias in the PIM and/or in the methodology used to calculate the combined value affects the resulting value of underlying land. »
    - §6.110 : « incorrect assumptions on the length of the service lives and depreciation rates of dwellings and structures can generate inaccurate estimates of net stocks and, as a consequence, of land underlying buildings ».
    - §6.111 : les transferts de bâtiments d'occasion entre secteurs ne sont pas suivis par le MIP, d'où des stocks sectoriels biaisés : « The effect is not negligible. »
    - §6.112 : « Inaccurate and inconsistent estimates of CV and C […] can lead to negative values of land […] This occurred in the United States for some components (Wasshausen, D., 2011) and in Denmark for certain years in the period 1995–2002 […] and in Finland for forestry land ».
    - §6.113 : tester sur un cycle complet et faire des contrôles de plausibilité (ratio LV/CV, comparaisons entre pays).
    - §6.114 : « when C is obtained through the PIM, most of the holding gains and losses for real estate properties will be allocated to land ».
    - §6.115 : le terrain résiduel « could be overestimated » si certains types de bâtiments s'apprécient.
    - §6.117 : les aménités nouvelles sont entièrement attribuées au sol.
  - *Cas du Danemark* : « the residual approach proved problematic for the years 1995 and 1996 with negative values for land […] Prices for real estate decreased strongly, but construction costs did not […] the value of land became negative. »
- **Ratio terrain/structure (LSR)**.
  - §6.119 : « recommended when available data sources permit the derivation of a higher quality estimate for a representative LSR compared to an estimate for total property value ».
  - §6.155 : la méthode « avoids the potential issue of negative values for land ».
  - §6.156 : risque de non-représentativité si les ratios proviennent de constructions neuves.
- **Hédonique**.
  - §6.180 : « Should other — and easier — methods fail, the hedonic approach is probably the only method which will result in reliable figures for the value of land. »
  - §6.181 : « technically difficult », « data intensive », « high risk of multicollinearity », résultats non cohérents avec le MIP, et « not yet been implemented by any country ».
- **Cas allemand** (§4.19) : les Gutachterausschüsse « value single plots and determine the standard land values ».
- Présentation française antérieure : J. Ribarsky (OCDE), « L'évaluation des terrains dans les comptes de patrimoine », ACN 2014, https://www.insee.fr/fr/statistiques/fichier/2387327/ACN2014-Session5-1-texte.pdf [TI].
  - Tableau 1 (calculs BCE, 2011-2012) : part de la valeur des terrains dans le patrimoine brut des ménages : France 33 %, Italie 27 %, Pays-Bas 21 %, Allemagne 16 %.
  - Durées de vie des logements déclarées : de 55-60 ans (Corée, Royaume-Uni, Finlande) à 90 ans (République tchèque), médiane 75 ans.

---

## 3. Littérature académique

| Référence | Lu | Méthode | Résultats clés (vérifiés) |
|---|---|---|---|
| Davis & Heathcote (2007), JME 54(8):2595-2620 | WP FEDS 2004-37 [TI] ; JME [R via IDEAS] | Résidu agrégé US (prix maison − coût de remplacement) | 1970-2003 : terrain sous logements 1-4 unités = **38 %** de la valeur du parc et **50 % du PIB** ; prix du sol « twice as volatile as existing home prices » ; en 2003T3, la valeur de tout le foncier résidentiel ≈ 1 × PIB. URL WP : https://www.federalreserve.gov/pubs/feds/2004/200437/200437pap.pdf |
| Davis & Palumbo (2008), JUE 63(1):352-384 | WP FEDS 2006-25 [TI] | Résidu par aire métropolitaine (AHS, R.S. Means), δ = 1,5 %/an | 46 aires métropolitaines : part du sol **32 % (1984) → ≈ 50 % (2004)** ; San Francisco 88 %, Minneapolis 46 %. Annexe B : « a lower estimate of δ will imply that the value of land, on average, was negative in many Midwestern cities in the mid 1980s ». URL : https://www.federalreserve.gov/pubs/feds/2006/200625/200625pap.pdf |
| Larson (2015), BEA WP2015-3 | [TI] | Hédonique, interpolée sur une mosaïque de parcelles | 48 États + DC : **≈ 23 000 Md$ en 2009**, marge ± 10 % ; terrain développé = 6 % de la surface et 51 % de la valeur. Critique du résidu : valeur du sol négative pour le secteur « Corporate Business » en 2009 ; hausse de 89 % en un trimestre (Massachusetts, 1985) dans Davis-Palumbo ; « the residual approach has low data requirements but somewhat unreliable estimates in downturns ». URL : https://www.bea.gov/sites/default/files/papers/WP2015-3.pdf |
| Albouy, Ehrlich & Shin (2018), REStat 100(3):454-466 | version du 25/10/2017 [TI] ; version publiée [R] | Ventes de terrains CoStar 2005-2010, 324 aires métropolitaines | Sol urbain > **2 × PIB en 2006** (28 000 Md$ → 18 000 Md$, de 2,2 à 1,3 × PIB en 2009). Comparé au résidu : « higher and less volatile » ; coefficient de variation intra-ville 0,24 contre 0,44 pour Davis-Palumbo ; baisse pic-creux 40 % contre 66 % pour le résidu FOF ; résidu FOF 2006 = 16 900 Md$ contre 30 400 Md$ en transactions ; foncier des entreprises négatif (−178 Md$) en 2009. URL : https://aeaweb.org/conference/2018/preliminary/paper/bDtiis2a |
| Bourassa, Hoesli, Scognamiglio & Zhang (2011), RSUE 41(2):134-144 | [R, IDEAS] | Modèle hédonique, Suisse 1978-2008 | « land leverage » = valeur du sol / valeur totale ; l'effet des fondamentaux sur les prix dépend du levier foncier. Pas de chiffre vérifié. |
| Davis, Larson, Oliner & Shui (2021), JME 118:413-431 | WP FHFA 19-01 révisé en oct. 2020 [TI] | Résidu sur 21,4 M d'expertises « cost approach » 2012-2019, maisons d'âge effectif ≤ 15 ans | Part du sol par comté : du 1er au 99e percentile, **7,7 % à 54,3 %**. Modèle d'option de démolition : le résidu est fiable seulement pour les structures de moins de 20 ans environ (voir §4). URL : https://fhfa.gov/document/wp1901.pdf |

**Critique « plug »**
- Davis & Heathcote, cité par Albouy et al. (note 15) : le résidu attache « the label 'land' to anything that makes a house worth more than the cost of putting up a new structure of similar size and quality on a vacant lot ».
- Albouy et al. ajoutent que le résidu attribue au sol les coûts liés aux contraintes réglementaires ou géographiques, et que la méthode « equates the market value of a structure with its replacement value, neglecting adjustment costs in building and irreversibilities in investment (Glaeser and Gyourko, 2005) ».

---

## 4. Trois concepts distincts de « valeur du sol »

**(a) Résidu sous bâtiment existant** = valeur de marché du bien − coût de remplacement net amorti du bâti. C'est le concept des comptes nationaux en pratique (Insee, ONS, Italie, etc.).

**(b) Valeur du site « comme s'il était nu »** au meilleur usage permis. C'est l'assiette de la taxe foncière sur la valeur du sol (LVT).
- **Allemagne**, § 196 (1) BauGB [TI, https://www.gesetze-im-internet.de/bbaug/__196.html] : « In bebauten Gebieten sind Bodenrichtwerte mit dem Wert zu ermitteln, der sich ergeben würde, wenn der Boden unbebaut wäre. »
- **Allemagne**, § 13 (2) ImmoWertV : « Das Bodenrichtwertgrundstück ist ein unbebautes und fiktives Grundstück ».
- **NSW** (fiche Valuer General « Your land value », sept. 2025 [TI], copie hébergée par une commune : https://www.cgrc.nsw.gov.au/wp-content/uploads/2026/05/Your-land-value-fact-sheet.pdf) : « Land value is the market value of your land only ».
  - Les évaluateurs « analyse sales of both vacant land and improved properties and adjust for the added value of any improvements » et tiennent compte de « the land's most valuable use ».
  - La valeur **inclut** « Improvements like draining, excavating, filling and clearing ». Dans le SCN, ces améliorations relèvent au contraire de l'AN.1123 et sont **exclues** du terrain.
  - Le texte de la s. 6A du Valuation of Land Act 1916 n'a **pas pu être lu** (protection Cloudflare) : NON VÉRIFIÉ en verbatim.

**(c) Prix de marché des terrains nus constructibles** (sélection : réseaux, localisation, rareté en centre-ville).
- Davis et al. 2021, note 6 : « We exclude data on vacant land sales due to the difficulty of controlling properly for differences in the characteristics of the vacant land, for example if water and sewer lines are in place. »
- Larson 2015 : « the number of land transactions falls substantially in downturns […] and land-only sales near city-centers where values are the highest are often infrequent ».
- Albouy et al. : « the value of transactional land should reflect available building opportunities, good or bad, while built-on land reflects the structure that is permitted de facto ».

**Pourquoi (a) ≠ (b)**

- **Davis, Larson, Oliner & Shui (WP FHFA 19-01)** : modèle d'option de démolition-reconstruction.
  - Citation : « A common concern about this residual method […] is that it assumes that the sum of the replacement cost of the housing structure and the value of the land (if it were vacant) is equal to the market value of housing. We show this assumption does not hold when a housing structure has become functionally obsolete and is due to be torn down ».
  - Dans le calibrage, la part « correcte » du sol (valeur du terrain nu / valeur du bien) passe de 30 % (bien neuf) à 100 % (bien à démolir), alors que la part résiduelle plafonne à environ 60 %.
  - Au moment de la démolition, la valeur du bien vaut 30, mais le terrain résiduel vaut 30 − 10,8 = 19,2 (biais à la baisse).
  - Les deux mesures coïncident à peu près jusqu'à 20 ans d'âge (41,6 % contre 39,2 %).
- **Clapp & Salavei (2010)**, « Hedonic pricing with redevelopment options: A new approach to estimating depreciation effects », JUE 67(3):362-377, doi:10.1016/j.jue.2009.11.003 [R, Fairfield digital commons].
  - Valeur = valeur d'usage + option de reconfiguration. L'âge réduit la valeur d'usage mais augmente la valeur d'option. L'intensité (valeur du bâti / valeur du sol) a un effet négatif. Données de Greenwich (Connecticut).
  - La référence « Clapp, Bardhan & Zhou » est **NON VÉRIFIÉE** (non trouvée). Il existe en revanche Clapp, Jou & Lee, « Hedonic models with redevelopment options under uncertainty » (SSRN 1814225), non lu.
- **Dye & McMillen (2007)**, « Teardowns and land values in the Chicago metropolitan area », JUE 61(1):45-63 [R] : « sales price of teardown property is approximately equal to its land value ».
- **Droit allemand : la valeur « comme si nu » est corrigée de l'usage réel quand c'est l'usage du marché.**
  - § 40 (5) ImmoWertV : « Die tatsächliche bauliche Nutzung kann insbesondere in folgenden Fällen den Bodenwert beeinflussen » (écart important entre usage réel et usage permis).
  - § 43 ImmoWertV : pour un « Liquidationsobjekt » dont la libération du terrain est différée, on retient un « nutzungsabhängiger Bodenwert ». Les coûts de démolition (« Freilegungskosten ») sont actualisés et déduits.
  - Le droit de l'évaluation reconnaît donc explicitement l'écart entre (a) et (b).

---

## 5. Comparaisons internationales (terrains / PIB)

**[C] Eurostat**, `nama_10_nfa_bs` (N211N = **tous terrains**, et pas seulement AN.2111, qui n'est pas diffusé dans ce jeu de données) / `nama_10_gdp` (B1GQ), mise à jour du 28/09/2026. Script : `scripts/agentF_landgdp.py`.

Économie totale S1 (pays qui publient ce secteur) :

| Pays | Année | Terrains (Md€) | % du PIB |
|---|---|---|---|
| FR | 2024 | 8 597 | 293 |
| FR | 2022 | 9 512 | 358 |
| UK | 2019 | 6 504 | 257 |
| NL | 2024 | 2 457 | 220 |
| AT | 2023 | 1 022 | 213 |
| DE | 2024 | 7 653 | 174 |
| SE | 2024 | 978 | 174 |
| CZ | 2024 | 365 | 114 |
| SK | 2024 | 116 | 89 |
| FI | 2024 | 211 | 76 |

Ménages et ISBLSM (S14_S15), 2023 sauf mention : ES 292 % ; LU 167 % ; BE 190 % ; FR 174 % ; NL 161 % ; IT 142 % ; DE 110 % ; SE 86 % ; IE 68 % ; PL 59 % ; FI 48 % ; DK 42 %.

**Lecture** : avec 229 % du PIB pour les seuls terrains bâtis en 2024 (293 % pour l'ensemble des terrains), la France est **au sommet** des pays européens qui publient, avec le Royaume-Uni (257 % en 2019) et l'Espagne (ménages seuls, 292 % en 2023). Elle se situe nettement au-dessus de l'Allemagne (174 %) et des Pays-Bas (220 %).

**Mise en garde** : les méthodes diffèrent selon les pays.
- *Allemagne* : méthode directe, surfaces × Bodenrichtwerte moyens. Note Bundesbank/Destatis, « Sektorale und gesamtwirtschaftliche Vermögensbilanzen », mise à jour de nov. 2025 [TI] : « der Gesamtwert des Grund und Bodens […], der im Rahmen eines Projekts auf der Grundlage der Flächenerhebung nach Art der tatsächlichen Nutzung und durchschnittlicher Bodenrichtwerte ermittelt wurde ». Référence : Schmalwasser & Brede, WiSta 6/2015, p. 43-58 (non lu). La valeur allemande est donc une valeur « as if vacant » (concept b) alors que la valeur française est un résidu (concept a).
- *Royaume-Uni*, ONS [TI via WebFetch] :
  - « In the UK we use the residual method to measure land underlying buildings. »
  - En 2020, « land was the most valuable asset in the economy, estimated at £6.3 trillion », dont terrains sous logements £5,4 tn, soit 86 % des actifs non produits (article du 10/03/2022 : https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/articles/improvingestimatesoflandunderlyingdwellingsinthenationalbalancesheetuk/2022).
  - Estimation préliminaire 2025 : actifs non produits (= terrains) £6,9 tn pour une valeur nette de £13,3 tn (bulletin du 10/06/2026).
- *États-Unis* : pas de compte officiel des terrains au BEA. Les Financial Accounts de la Fed fournissent un résidu implicite. Ordres de grandeur académiques : sol résidentiel ≈ 1 × PIB en 2003 (Davis-Heathcote) ; sol urbain > 2 × PIB en 2006 (Albouy et al.) ; ensemble des terrains ≈ 23 000 Md$ en 2009 (Larson).
- *Méthodes déclarées en 2011* (tableau 4A.1 du guide) : Australie = prix × quantité puis résidu pour le résidentiel, valeurs des Valuers-General pour le commercial ; Canada = LSR ; Autriche, Rép. tchèque, Allemagne = méthode directe.
- Les données OCDE (tableau 9B) n'ont pas été consultées : NON VÉRIFIÉ.

---

## 6. Bodenrichtwerte (Allemagne)

- **Base légale** : § 196 BauGB [TI].
  - « Auf Grund der Kaufpreissammlung sind flächendeckend durchschnittliche Lagewerte für den Boden […] zu ermitteln (Bodenrichtwerte). »
  - Valeur « wenn der Boden unbebaut wäre » dans les zones bâties.
  - Zones de valeur (Richtwertzonen) homogènes par type et intensité d'usage.
  - « Die Bodenrichtwerte sind jeweils zu Beginn jedes zweiten Kalenderjahres zu ermitteln, wenn nicht eine häufigere Ermittlung bestimmt ist. »
  - Publication et transmission électronique à l'administration fiscale (§ 196 (3)).
- **ImmoWertV 2021** [TI, https://www.gesetze-im-internet.de/immowertv_2022/] :
  - § 14 (1) : « Bodenrichtwerte sind vorrangig im Vergleichswertverfahren […] zu ermitteln. »
  - § 14 (2) : « in Gebieten ohne oder mit geringem Grundstücksverkehr können Kaufpreise und Bodenrichtwerte aus vergleichbaren Gebieten oder aus vorangegangenen Jahren herangezogen werden […] Darüber hinaus können deduktive oder andere geeignete Verfahrensweisen angewendet werden. »
  - § 14 (3) : dans les zones bâties, l'état et la structure du bâti dominant peuvent être pris en compte.
  - § 15 (1) : les zones sont délimitées de sorte que les écarts de valeur liés à la localisation ne dépassent « grundsätzlich nicht mehr als 30 Prozent ».
  - § 13 (2) : une seule valeur par zone, « Bodenrichtwertspannen sind nicht zulässig ».
- **Source des données** : chaque vente de biens immobiliers passe par un notaire, qui la transmet au Gutachterausschuss (guide Eurostat-OCDE §4.19).
- **Évaluations de précision** :
  - Kolbe, Schulz, Wersing & Werwatz (2015), *Computational Statistics* 30:767-790, doi:10.1007/s00180-015-0559-9 [TI, postprint TU Berlin].
    - Méthode : lissage adaptatif (AWS) des ventes de terrains nus à Berlin, 1996-2009.
    - Résultats : « overall the estimated land values are close to BRW » ; meilleur R² entre AWS et BRW = 0,783. Divergences locales (bord de lac, etc.).
    - Les auteurs notent que les BRW « rely heavily on local surveyors' knowledge and expertise ».
  - Helbing, Shen, Odening & Ritter (2017), SFB 649 DP 2017-002, publié dans la *German Journal of Agricultural Economics* 66(3) [R] : dans le Mecklembourg-Poméranie-Occidentale (2013-2015), les BRW agricoles « underestimate location values of arable land by 11.5 percent on average », écart attribué à la hausse rapide des prix.
  - Aucune évaluation nationale systématique de la précision des BRW urbains n'a été trouvée : NON VÉRIFIÉ.
- **Points NON VÉRIFIÉS** : nombre de Gutachterausschüsse ; couverture complète de BORIS-D ; fréquence annuelle dans la plupart des Länder (la loi impose au minimum une mise à jour tous les deux ans).
