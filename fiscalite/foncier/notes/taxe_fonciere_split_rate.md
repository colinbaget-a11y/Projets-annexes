# Taxe foncière récurrente et impôt à deux taux : revue de littérature

Note de lecture du 15/11/2026, préparée pour la partie « impôts fonciers récurrents » de la note sur la
réforme de la fiscalité immobilière (report d'une partie des DMTO sur la taxe foncière et passage à deux
taux, plus élevé sur le terrain que sur le bâti).

Point de départ : les notes vérifiées d'octobre 2026 du dossier `lvt/notes/` (`theorie_et_split_rate.md`,
`etudes_recentes.md`, `transitions_et_saillance.md`, `etudes_francaises.md`,
`valeur_des_terrains_statistique.md`, `france_institutions_chiffres.md`, et pour Karlsruhe et le
Danemark `sources_video_et_rapports_officiels.md`) et la note `lvt/lvt-brief.tex`. Leurs conclusions sont
reprises sans être refaites ; cette note ajoute ce qui manquait : évaluations régressives aux États-Unis,
sortie d'un gel des évaluations (Philadelphie, council tax anglaise), concurrence fiscale, effets
redistributifs d'un passage au sol, Finlande, état du droit du Bade-Wurtemberg en 2026, dispositifs
français pour les ménages âgés, données et droit français, propositions récentes.

**Statut de lecture.**
- **[TEXTE LU]** : texte intégral (ou passages clés) lu dans cette session ; **[TEXTE LU, note LVT]** :
  lu lors de la vérification d'octobre 2026, non relu ici, conclusion reprise de la note citée.
- **[RÉSUMÉ]** : résumé officiel ou notice seulement.
- **[SECONDAIRE]** : information tirée d'une source tierce (presse, association, cabinet, autre article).
- **[NON VÉRIFIÉ]** : affirmation qu'aucune source primaire n'a confirmée.
- **[CALCUL]** : calcul de l'auteur de la note à partir de chiffres vérifiés.

**Nature des résultats.** Chaque résultat est qualifié : *mécanisme* (se refait au calcul ou découle
d'un modèle), *fait mesuré* (observation sans contrefactuel), *effet causal* (stratégie d'identification
crédible), *ordre de grandeur* (chiffre à retenir pour une simulation).

Les fichiers téléchargés pour cette note sont dans le dossier de travail de la session
(`scratchpad/tf_*`), non conservés.

---

## Synthèse

**Établi.**
- L'impôt sur la propriété (terrain et bâti) est largement capitalisé quand l'écart est permanent et
  visible : quasi complètement pour la council tax anglaise, à 3-4 % d'actualisation (Koster et
  Pinchbeck, 2022). *Causal.* Pour une taxe sur le seul sol, c'est contesté : complète au Danemark selon
  Høj et al. (2018), nulle sur la même réforme selon Nielsson, Wroblewski et Yding (2024, non publié).
- La TFPB est régressive rapportée à la valeur (plus de 0,5 % pour les petits patrimoines, 0,18 % pour le
  millième le plus doté) et progressive rapportée au revenu (André et Meslin, Insee, 2023). *Fait mesuré*,
  dû aux valeurs locatives de 1970.
- Les évaluations de masse sont régressives : aux États-Unis, niveau d'évaluation deux fois plus élevé
  au premier décile de prix qu'au dernier (Berry, 2021) ; charge supérieure de 10 à 13 % pour les
  propriétaires noirs et hispaniques, parce que les évaluations suivent mal le quartier (Avenancio-León
  et Howard, 2022). *Fait mesuré à grande échelle.*
- Un plafond attaché au propriétaire crée un verrou (Proposition 13 : mobilité +25 % à 55 ans quand
  l'avantage devient transférable ; Ferreira, 2010). *Causal.*
- Sortir d'une assiette figée déplace fortement la charge, et les réformes non lissées échouent :
  Pittsburgh 2001, révision française de 1990, council tax figée depuis 1991, Corée 2024, « éléments de
  confort » suspendus en 2025. *Faits observés.*
- L'assiette sol charge les maisons sur grands terrains et les terrains nus, allège les copropriétés
  (Karlsruhe 2025, à recette constante : maisons individuelles +76 %, terrains nus et divers +265 %,
  copropriétés −20 %, commerces −40 %). Le sens entre classes dépend de l'intensité foncière locale (au
  Texas, la charge irait vers le commerce ; Plummer). *Fait mesuré, statique.*
- Le modèle du Bade-Wurtemberg est conforme à la Loi fondamentale selon le BFH (20/05/2026) ; deux
  recours constitutionnels sont pendants.
- Les reports de paiement facultatifs sont très peu utilisés (moins de 1 % des éligibles aux États-Unis) ;
  le Danemark inscrit par défaut.

**Probable.** Le double taux de Pennsylvanie a accru modestement construction et densité (+5 à 6 points de
croissance décennale des pièces, surtout plus de logements ; Banzhaf et Lavery, 2010), sans expliquer le
boom de Pittsburgh (Oates et Schwab, 1997). La part bâti de l'impôt freine l'investissement là où l'offre
est élastique (élasticité d'environ −1 ; Lutz, 2015). En Allemagne, 83 % d'une hausse passe dans les loyers
en trois ans (Löffler et Siegloch, 2024), l'impôt y étant récupérable, ce qu'il n'est pas en France. Des
réévaluations régulières réduisent la régressivité (Philadelphie : PRD de 1,42 à 1,14). La concurrence
par les taux est faible (Finlande, Basse-Saxe : aucune imitation avec des chocs exogènes).

**Plausible, non démontré.** Reporter les DMTO sur une taxe à deux taux augmenterait les transactions,
l'effet propre du second taux restant faible ; le passage au sol pèserait sur les propriétaires âgés de
maisons sur grands terrains des périphéries chères ; une hausse annoncée serait mal capitalisée et
retomberait sur les propriétaires successifs (Bradley ; Elinder et Persson ; Nielsson et al.) ; la
révision à chaque vente votée en commission pour le PLF 2027 (amendement Juvin) créerait un verrou du type
Proposition 13.

**Inconnu.** La valeur du sol parcelle par parcelle en France (pas d'équivalent des Bodenrichtwerte ; au
pays de Galles, confiance « faible » dans les valeurs du sol) ; les effets ex post du modèle badois (aucune
étude au 15/11/2026) ; l'incidence de la TFPB française sur les loyers et la construction ; la répartition
par âge et par revenu d'une bascule française ; le sort de l'amendement Juvin.

### Paramètres pour une simulation française

| Paramètre | Valeurs | Source, statut |
|---|---|---|
| Part du terrain, patrimoine immobilier des ménages (résidu des comptes nationaux) | 44 % fin 2024 ; 49 % en 2019 ; 55 % en 2007 ; 21 % en 1998 | Insee T_8210, calcul note LVT [TEXTE LU, note LVT ; CALCUL] |
| Part du terrain, maison neuve | environ 30 % en 2024 (terrain 95 000 €, 932 m², 102 €/m² ; maison 225 500 €) | SDES, EPTB 2024 [TEXTE LU ; CALCUL] |
| Part du terrain, maison neuve et ancienne | 36 % (neuf), 35 % implicite (ancien) | Combes, Duranton, Gobillon 2019 [TEXTE LU, note LVT] |
| Part du terrain dans la maison médiane vendue en 2024, par département | 10 % (Corrèze), 13-15 % (Lozère, Lot, Cantal, Vosges, Dordogne) ; 64-65 % (Rhône, Haute-Savoie), 75 % (Seine-Saint-Denis) ; médiane des 93 départements 33 %, quartiles 25 % et 41 % | DVF 2024, `lvt/donnees/dep2024.csv` (prix médian du m² de terrain à bâtir × terrain médian ÷ prix médian) [CALCUL] |
| Appartement parisien | 75 % : hypothèse, aucune donnée publique | note LVT |
| Taux neutre d'une taxe sur le sol remplaçant la TFPB | 0,72 % de la valeur des terrains bâtis hors APU ; environ 1 % avec les DMTO ; 0,57 % sur le seul périmètre des ménages (2017) | note LVT [CALCUL] |
| Ratios de taux terrain/bâti pratiqués | Pittsburgh, part municipale : 2:1 (1978), 3,9:1 (1979), 5,1:1 (1980), 5,8:1 (1990) ; tous niveaux confondus, à peine plus de 2:1. Pennsylvanie : ratio moyen 4:1 (Banzhaf-Lavery) ; 7,7:1 chez les adoptants (Hanson) ; Harrisburg 5,3:1 ; Scranton 4,7:1. Projets : Detroit 5:1 ; Cincinnati 4:1. Finlande 2026 : sol 1,30-2,00 %, logements permanents 0,41-1,00 % (assiettes différentes). Bade-Wurtemberg : sol seul | Oates-Schwab, Hanson, Dye-England [TEXTE LU, note LVT] ; vero.fi [TEXTE LU] ; [CALCUL] |
| Taux effectifs sur le sol pratiqués | Bade-Wurtemberg avec un Hebesatz de 270 % (Karlsruhe) : 0,25 % de la valeur de zone pour le logement, 0,35 % pour le reste ; Danemark : au plus 2,4 % de la valeur évaluée (30 ‰ sur 80 %) ; Nouvelle-Galles du Sud : 1,6 % au-delà de 1,075 M AUD, résidence principale exonérée | LGrStG BW [TEXTE LU ; CALCUL] ; tax.dk [TEXTE LU] ; Revenue NSW [TEXTE LU, note LVT] |
| Plafonds de hausse annuelle | Danemark : +4,75 %/an de la taxe foncière, attaché au bien (3,5 % logement social jusqu'en 2040) ; Norvège : 1 ‰ la première année puis +1 ‰/an, plafond 4 ‰ pour le logement ; Estonie 2025 : +50 % ou 20 € ; Michigan : min(inflation ; 5 %), remis à zéro à la vente ; Californie : 2 %, remis à zéro à la vente ; France RVLLP : écart divisé par deux (2017-2025) et lissage sur dix ans (2017-2026) ; Angleterre (proposition IFS) : une bande par an | notes LVT ; KPMG, Cobalt [SECONDAIRE] ; collectivites-locales.gouv.fr, BOFiP [TEXTE LU] ; IFS [TEXTE LU] |
| Reports de paiement | Danemark : prêt d'État par défaut (indefrysning) ; Colombie-Britannique : taux préférentiel +2 points (6,45 %) depuis 2026 ; Irlande : 4 %, report total sous 15 000 € (seul) ou 25 000 € (couple) de revenu ; France : aucun report général, plafonnement de la TFPB à 50 % des revenus sous condition de ressources | notes LVT ; IFS 2020 [TEXTE LU] ; BOFiP [TEXTE LU] |
| Capitalisation | Høj et al. : −4,3 % de prix par point pour mille de taxe (taux implicite 2,3 %) ; Nielsson et al. : nulle, capitalisation complète exclue pour tout taux inférieur à 8 % ; Koster-Pinchbeck : 3-4 % ; TH France : 12 à 48 % | notes LVT ; [TEXTE LU] (Nielsson, introduction) |
| Répercussion sur les loyers | Allemagne 83 % à trois ans ; Berkeley 50 à 89 % ; TH France : 53 % de la suppression captée par les bailleurs | notes LVT |

---

## 1. Les problèmes économiques de l'impôt foncier récurrent

### 1a. Capitalisation et pertes en capital lors d'une hausse

**Mécanisme.** Si l'offre de terrain est fixe et que l'acheteur actualise les impôts futurs, une hausse
permanente de taxe τ (en part de la valeur) réduit le prix de τ/(r+τ) environ ; le propriétaire du jour de
l'annonce supporte toute la perte, les acheteurs suivants ne paient rien de plus. Feldstein (1977) montre
que l'épargne peut se reporter sur le capital productif, ce qui limite la baisse [RÉSUMÉ, note LVT].

**Ce qui est établi ailleurs** (notes LVT, non refait ici) : capitalisation d'environ deux tiers dans le
New Jersey (Oates, 1969), 62 % à 100 % dans la banlieue de Houston selon le taux d'actualisation (Palmon
et Smith, 1998), quasi complète pour la council tax anglaise (Koster et Pinchbeck, 2022, taux net de
croissance de 3,7 %, intervalle 2,3-9,8 %) [TEXTE LU, note LVT].

**Fiche — Danemark, fusion des communes de 2007 (taxe sur le seul terrain).**
- Høj, Jørgensen et Schou (2018), *Fiscal Studies* 39(2) [TEXTE LU, note LVT : document de travail
  2017]. 211 209 ventes de maisons 2001-2008 ; l'harmonisation des taux dans 98 nouvelles communes fait
  monter la grundskyld dans 139 zones et baisser dans 105. Différence de différences à traitement
  continu. Un point pour mille de taxe effective réduit le prix de 4,3 % en 2007 : capitalisation
  complète au taux implicite de 2,3 %, visible dès l'annonce de 2004. *Effet causal.*
- Nielsson, Wroblewski et Yding (novembre 2024), « The Incidence and Efficiency of Land Value
  Taxation », document de travail (Copenhagen Business School, UC Berkeley) [TEXTE LU : résumé et
  introduction, 6 pages de la version en ligne]. Même réforme ; ventes répétées ; instrument construit
  sur la formule de l'État et les taux historiques, second instrument : intensité foncière historique
  de chaque parcelle. Effet nul et précis sur les prix ; la borne inférieure de l'intervalle à 95 %
  exclut tout taux d'actualisation inférieur à 8 %. Pas d'effet sur la construction, sur la mise en
  valeur des terrains nus, sur la mobilité des propriétaires ni sur la propriété ; moins de propriétaires
  âgés s'installent ensuite dans les zones où la taxe a monté. Explication proposée : le contrôle des
  loyers danois autorise la répercussion des hausses d'impôt sur les locataires. Conclusion des auteurs :
  faible coût d'efficacité, mais incidence plus régressive que dans le modèle standard (la charge est
  partagée avec les locataires et les acheteurs futurs). L'explication de l'écart avec Høj et al. par les
  résidences de vacances, mentionnée dans la note LVT, ne figure pas dans les pages lues [NON VÉRIFIÉ].
- **Transposable** : l'ordre de grandeur de la perte à l'annonce dépend entièrement de ce débat. Avec
  Høj et al., une bascule à recette constante ferait perdre 5 à 12 % de leur valeur aux biens les plus
  touchés (biens types de la note LVT) ; avec Nielsson et al., presque rien, mais la charge serait
  supportée par chaque propriétaire successif.

**France.** La suppression de la taxe d'habitation a été capitalisée à 12-17 % (taux d'actualisation de
0,7 %) ou 33-48 % (2 %) selon l'année (Bach et al., IPP, 2023) [TEXTE LU, note LVT]. Le taux de TFPB seul
n'a pas d'effet significatif sur les prix à Dijon et Besançon (Charlot, Paty et Visalli, 2013) [TEXTE LU,
note LVT]. La hausse du taux parisien de 13,5 % à 20,5 % en 2023 n'a fait l'objet d'aucune étude de
capitalisation trouvée.

### 1b. Incidence : propriétaires, locataires, capital

**Trois lectures théoriques** (Zodrow, « The Property Tax as a Capital Tax: A Room with Three Views »,
*National Tax Journal* 54(1), 2001 ; version mise à jour, Baker Institute, 2007) [TEXTE LU] :
- vue traditionnelle (Simon, Netzer) : en économie ouverte, le capital fuit la commune qui taxe, la
  charge retombe sur les occupants en proportion de leur consommation de logement ; impôt plutôt
  régressif ou proportionnel au revenu de cycle de vie ;
- vue « bénéfice » (Hamilton, Fischel) : avec zonage et mobilité à la Tiebout, l'impôt est le prix des
  services locaux, pas un impôt ;
- vue « capital » (Mieszkowski 1972) : la moyenne nationale de l'impôt est supportée par tous les
  détenteurs de capital (« effet impôt sur les profits », progressif par rapport au revenu annuel), les
  écarts entre communes jouent comme des accises locales qui se compensent.
Oates et Fischel (2016), *NTJ* 69(2) : selon la vue retenue, la part nationale est progressive (vue
capital), la part locale n'est pas un impôt (vue bénéfice) [RÉSUMÉ]. *Mécanismes* ; le choix entre vues
est empirique et non tranché. Carroll et Yinger (1994), cités par Zodrow : les bailleurs supportent 84 à
91 cents par dollar de hausse de l'impôt sur le logement locatif dans leur échantillon (Boston) [SECONDAIRE].

**Fiche — Löffler et Siegloch, « Welfare Effects of Property Taxation » (Allemagne).**
- ECONtribute DP 331 (2024) ; versions IZA, CESifo, ZEW 2021 ; aucune publication en revue trouvée
  [TEXTE LU, note LVT].
- Question : qui paie une hausse de la Grundsteuer B ? Données : loyers d'annonce ImmoScout24,
  2007-2015. Identification : environ 5 500 hausses de taux communaux (Hebesatz), surtout motivées par la
  consolidation budgétaire ; études d'événement, effets fixes, instrument tiré des règles de péréquation
  des Länder.
- Résultat : +1 point de taux effectif fait monter le loyer total de 3,4 % en trois ans, soit une
  répercussion d'environ 83 % (environ un tiers à deux ans) ; la recette effective vaut 0,96 de l'effet
  mécanique ; incidence régressive (perte de 1,3 % de la consommation au premier décile contre 0,6 % au
  dernier). *Effet causal.*
- Limites : loyers d'annonce ; l'impôt allemand est récupérable sur le locataire dans les charges ; il
  porte sur terrain et bâti à valeurs figées (1964 ou 1935).
- **Transposable** : en France, la TFPB n'est pas une charge récupérable (décret de 1987, note LVT
  [SECONDAIRE]) ; la répercussion passerait par le loyer à la relocation, freinée là où les loyers sont
  encadrés. L'expérience inverse française (suppression de la TH, payée par le locataire) a profité pour
  53 % environ aux bailleurs (IPP, 2023). Pour un impôt sur le seul terrain, la théorie prédit une
  capitalisation et non une répercussion ; le cas danois (Nielsson et al.) montre qu'une réglementation
  des loyers peut produire l'inverse.

**Autres estimations** : à Berkeley, 50 à 89 cents de répercussion par dollar de choc fiscal sur les
loyers des nouveaux locataires (Baker, 2025, Fed de Philadelphie) [TEXTE LU, note LVT] ; en Corée,
répercussion partielle de l'impôt sur la détention immobilière dans les loyers du haut de gamme (Hong et
Hwang, 2026) [RÉSUMÉ, note LVT].

### 1c. Régressivité par rapport au revenu courant, liquidité, dispositifs pour les ménages âgés

**France, fait mesuré** (André et Meslin, *Insee Analyses* n° 91, 2023, données 2017) [TEXTE LU, note
LVT ; IA 91 rouvert ici] : la TFPB est régressive rapportée au patrimoine (plus de 0,5 % pour les petits
patrimoines, 0,22 % pour le centile le plus doté) mais progressive rapportée au revenu (les 10 % les plus
aisés paient 27 % du total ; plus de 4 % du revenu disponible des 20 % de propriétaires les plus modestes,
moins de 2 % pour le centile supérieur). L'étude ne ventile pas par âge.

**Qui est « riche en patrimoine, pauvre en revenu » en France** [TEXTE LU, note LVT] : près des deux tiers
des propriétaires n'ont plus d'emprunt et plus de la moitié d'entre eux ont 65 ans ou plus (Insee, RPM
2021) ; les retraités détiennent 38,5 % du patrimoine brut, dont près de 64 % en immobilier (COR, 2026).

**Dispositifs français en vigueur (droit 2026)** :
- exonération de TFPB de la résidence principale des plus de 75 ans, et des titulaires de l'ASPA, de
  l'ASI ou de l'AAH, sous le plafond de revenu de l'article 1417 I (12 793 € pour une part en métropole
  pour les impositions de 2026) ; dégrèvement de 100 € pour les 65-75 ans sous le même plafond
  (art. 1390, 1391, 1391 B CGI) [SECONDAIRE : LégiFiscal du 01/07/2026 citant BOI-BAREME-000006 ;
  barème BOFiP non consulté directement] ;
- plafonnement à 50 % des revenus (art. 1391 B ter CGI) : sur réclamation, dégrèvement de la fraction de
  la TFPB de l'habitation principale qui excède 50 % du revenu, pour les foyers sous le plafond de
  l'article 1417 II (30 083 € pour une part en 2026, même source) et non assujettis à l'IFI ; le
  dégrèvement est réduit de l'effet des hausses de taux décidées depuis 2011, si bien que l'État ne
  finance pas les hausses locales ; il est pris en charge par l'État [TEXTE LU : BOFiP BOI-IF-TFB-50-40,
  version du 12/09/2012, qui mentionne encore l'ISF] ;
- **aucun dispositif général de report de paiement** jusqu'à la vente ou la succession n'a été trouvé
  dans le CGI [NON VÉRIFIÉ de manière exhaustive] ; le prêt viager hypothécaire est un produit privé.
- Le seuil de 50 % du revenu est très élevé : il ne traite pas la contrainte de liquidité d'un
  propriétaire dont la taxe passerait de 3 à 8 % de son revenu.

**Ailleurs** (notes LVT) : aux États-Unis, +100 $ de taxe annuelle augmentent de 0,76 point la mobilité à
deux ans des propriétaires de plus de 50 ans (Shan, 2010, variable instrumentale) [TEXTE LU, note LVT],
*effet causal* ; recours aux exonérations de résidence principale environ 90 %, aux « circuit breakers »
environ 40 %, aux reports moins de 1 % (Baer, 1998, cité par Shan) ; Colombie-Britannique : report
massivement utilisé quand il était bon marché, taux relevé en 2026 ; Danemark : prêt de l'État pour
toute hausse future, inscription par défaut sur la déclaration préalable. Au Danemark, les hausses de
taxe foncière n'ont pas fait vendre les propriétaires en place (Nielsson et al.).

**Fiche — IFS, réévaluation de la council tax anglaise** (Adam, Hodge, Phillips et Xu, *Revaluation and
reform: bringing council tax in England into the 21st century*, IFS Report R168, mars 2020) [TEXTE LU] :
voir 1d ; sur les ménages âgés, l'IFS rappelle qu'un report doit porter intérêt (sinon les ménages qui
peuvent payer reportent et placent), être gagé sur le bien, et que le risque principal est politique :
un gouvernement futur peut effacer les dettes reportées, ce qui transforme ex post le report en
exonération ; d'où la recommandation de le réserver aux ménages incapables de payer sur leur revenu.
Exemples cités : Irlande (taux de 4 % ; report total sous 15 000 € de revenu pour une personne seule et
25 000 € pour un couple, report de moitié sous 25 000 et 35 000 €), Colombie-Britannique (1,95 à 3,95 %
en 2020).

### 1d. Évaluations obsolètes ou régressives

**France** [TEXTE LU, note LVT] : valeurs locatives de référence au 1er janvier 1970, une seule
actualisation (1980), puis coefficient national (indexé sur l'inflation depuis 2018) ; l'impôt représente
0,3 % de la valeur au Capitole et plus de 1 % au Mirail à Toulouse (CPO, 2023) ; une révision sur les
loyers relèverait de plus de 15 % les valeurs des logements d'avant 1950 et baisserait de 16 % celles des
années 1960-1970, +9 % pour le décile de niveau de vie le plus aisé, −5,6 % pour le plus modeste (IPP,
2020). Calendrier de la révision : section 3.2.

**Fiche — Berry, « Reassessing the Property Tax »** (Harris School, Université de Chicago, version du
29/07/2021, conférence NBER ; SSRN 3800536) [TEXTE LU] :
- Question : les évaluations des assesseurs sont-elles proportionnelles aux prix ? Données : 26 millions
  de ventes résidentielles 2007-2017 (Corelogic), environ 2 600 comtés (synthèse Lincoln
  [SECONDAIRE]). Méthode : rapport évaluation/prix de vente au moment de la vente, régressions par
  juridiction, tests d'erreur de mesure des prix.
- Résultat : élasticité du taux effectif au prix de −0,37 à l'intérieur d'une juridiction ; le décile de
  prix inférieur subit un niveau d'évaluation double de celui du décile supérieur. Exemples : à Detroit
  en 2010, le logement vendu moyen était évalué à 11 fois son prix, 30 fois dans le quintile inférieur.
  L'erreur de mesure des prix n'explique pas la régressivité ; la cause est l'information : les
  caractéristiques que voit l'acheteur (intérieur, rénovation) ne sont pas observées par l'assesseur,
  d'où des valeurs trop hautes pour les biens moins chers que leurs caractéristiques observables ne le
  laissent prévoir. Les recours, plus fréquents pour les biens chers, aggravent légèrement la
  régressivité (Cook County : 166 000 recours en 2015, environ 80 % aboutissent). *Fait mesuré*,
  mécanisme documenté.
- Limites : critiques de méthode à l'échelle des comtés (Rakow, 2023, sur le comté de Suffolk : années de
  vente et d'évaluation non appariées, exonérations omises) [SECONDAIRE].

**Fiche — Amornsiripanitch, « Why Are Residential Property Tax Rates Regressive? »** (Yale, version du
01/06/2021 ; Fed de Philadelphie 2022) [TEXTE LU : résumé et introduction] : dans de petites zones à taux
et services identiques (« tax code areas », médiane de 65 parcelles), les maisons bon marché paient des
taux effectifs supérieurs de 50 % à ceux des maisons chères ; 30 % de la régressivité s'explique par des
méthodes d'évaluation qui ignorent des caractéristiques valorisées du bien et du quartier ; les
réévaluations peu fréquentes en expliquent **moins de 10 %** ; les recours n'y contribuent pas ; corriger
augmenterait d'environ 15 % la richesse nette des propriétaires modestes. *Décomposition, fait mesuré.*

**Fiche — Avenancio-León et Howard, « The Assessment Gap: Racial Inequalities in Property Taxation »**
(*QJE* 137(3), 2022, p. 1383-1434 ; version de travail de juillet 2021) [TEXTE LU : version 2021] :
- Données : 6,9 millions de logements dans 49 États, 2005-2016 (ATTOM), race du vendeur par les données
  HMDA, 75 000 périmètres d'entités fiscales pour définir des juridictions à taux et services identiques.
- Résultat : rapport évaluation/prix supérieur de 12,7 % pour les propriétaires noirs et de 9,8 % pour
  l'ensemble noirs ou hispaniques ; 300 à 390 $ de plus par an pour le propriétaire minoritaire médian ;
  27 % et 790 $ dans le comté au 90e centile. Un peu plus de la moitié de l'écart est entre quartiers :
  les évaluations suivent bien les caractéristiques du logement mais beaucoup moins celles du quartier,
  que les prix capitalisent ; le reste (5-6 % dans un même îlot) passe par les recours (moins de
  recours, moins de succès, réductions plus faibles). Pas de lien net avec la fréquence de réévaluation,
  sauf l'absence de toute obligation, associée à plus d'inégalité. Un exercice simple fondé sur des
  indices de prix par code postal réduirait l'inégalité jusqu'à 70 %. *Fait mesuré, mécanismes testés.*
- **Transposable** : une assiette « valeur du sol » est par construction une valeur de quartier (valeur
  de zone, coefficient de localisation) ; c'est précisément la composante que les évaluations de masse
  ratent le plus. Une valeur de zone publiée et contestable (modèle allemand) fixe ce risque, mais
  reporte l'erreur sur le découpage des zones.

**Fiche — Philadelphie, sortie d'un gel de trente ans** (Hou, Ding, Schwegman et Barca, « Assessment
Frequency and Equity of the Property Tax: Latest Evidence from Philadelphia », Fed de Philadelphie WP
21-43, révisé en janvier 2025, à paraître au *Journal of Policy Analysis and Management*) [TEXTE LU :
introduction et sections institutionnelles] :
- Contexte : aucune réévaluation complète des années 1980 à 2012 ; valeurs évaluées environ 60 % sous
  le marché ; évaluation fractionnelle à 32 % avec un taux nominal de 9,771 %. L'Actual Value Initiative
  (2013, effet 2014) réévalue tout le parc à la valeur de marché, taux ramené à 1,34 %, nouvelle
  réévaluation en 2019 (et 2023). Elle est accompagnée d'un abattement forfaitaire pour la résidence
  principale (Homestead Exemption) et d'un programme pour les propriétaires occupants de longue date
  exposés à de fortes hausses (LOOP).
- Méthode : différence de différences, données parcellaires appariées aux ventes, Philadelphie contre
  15 villes comparables.
- Résultat : coefficient de régressivité (PRD) 1,42 avant, 1,28 en 2014, 1,14 en 2019 (zone acceptable :
  0,98-1,03) ; taux effectifs en baisse plus forte dans les quartiers à majorité noire, pauvres et non
  gentrifiés ; amélioration de l'uniformité plus faible dans les quartiers défavorisés. *Effet causal
  probable* (un seul traitement).
- **Transposable** : c'est le cas le plus proche de la France (gel long, sortie brutale), et il a tenu
  politiquement avec deux amortisseurs (abattement forfaitaire et protection ciblée des occupants
  anciens).

**Fiche — IFS 2020, council tax figée sur les valeurs d'avril 1991** [TEXTE LU] :
- Constat : 24,5 millions de logements en huit bandes de valeur 1991 ; la bande H paie trois fois la
  bande A pour une valeur au moins huit fois supérieure ; prix à Londres multipliés par plus de six
  depuis 1995, par à peine trois dans le Nord-Est. 31,5 Md£ en 2019-2020, 1 327 £ par ménage en moyenne,
  environ 3 % du revenu disponible.
- Simulation (données administratives de transactions et de caractéristiques, enquêtes ménages) : une
  simple réévaluation change peu les factures moyennes par type de ménage ; une taxe proportionnelle à
  des valeurs à jour réduit les factures de 0,5 à 0,9 % du revenu dans la moitié inférieure et les
  augmente de 0,7 % du revenu pour le décile supérieur ; si les dotations de l'État sont ajustées, les
  factures moyennes baissent de plus de 20 % dans la plupart du Nord et des Midlands et montent à
  Londres et dans sa couronne ; 24 % du quintile le plus pauvre gagneraient plus de 200 £ par an, 4 %
  perdraient autant. Par âge : gain d'environ 140 £/an pour les moins de 35 ans, 70 £ pour les 35-44 ans,
  perte de 40 à 50 £ pour les 45-64 ans et de 30 £ pour les 65 ans et plus. *Ordre de grandeur, calcul
  statique.*
- **Transposable** : la question du financement est décisive. À dotations inchangées, une réforme d'une
  taxe locale ne redistribue qu'à l'intérieur de chaque commune ; seule une péréquation fait apparaître
  les effets entre territoires.

### 1e. Saillance et rejet politique

**Fiche — Cabral et Hoxby, « The Hated Property Tax: Salience, Tax Rates, and Tax Revolts »** (NBER WP
18514, 2012, révisé 2015) [TEXTE LU, note LVT] : la part des emprunteurs qui paient l'impôt foncier
fondu dans leur mensualité (compte séquestre) est instrumentée par la présence locale de banques dont
l'activité de gestion de prêts est surtout hors de l'État. +10 points de paiement par séquestre :
taux plus élevés d'environ 3 millièmes (moyenne 11,5) et probabilité d'un plafond fiscal général réduite
de 37 %. *Effet causal.* Attention : le résumé du PDF de 2015 inverse le signe ; il faut citer le corps du
texte.

**Proposition 13** (Legislative Analyst's Office de Californie, *Common Claims About Proposition 13*,
19/09/2016) [TEXTE LU] : avant 1978, taux moyen de 2,67 % sur la valeur de marché, revalorisée chaque
année (croissance moyenne de 4 % par an, à plus ou moins 5 points près) ; la Proposition 13 plafonne le
taux à 1 %, fixe la base au prix d'achat, revalorisée au plus de 2 % par an et remise à zéro à la vente ;
les recettes baissent d'environ 60 % ; la part des biens vendus chaque année passe de 16 % (1977-1978) à
5 % (2014-2015), la Proposition 13 étant l'un des facteurs ; les 55 ans sont 20 % plus susceptibles de
déménager que les 54 ans en 2014. Les causes du vote (hausse rapide des évaluations en période
d'inflation, réforme des pratiques d'évaluation de 1967, effet de l'arrêt Serrano selon Fischel) ne sont
pas vérifiées ici [NON VÉRIFIÉ].

**Faits observés pertinents pour la France** :
- en France, environ deux tiers des propriétaires paieraient leur taxe foncière en une fois à l'automne
  [SECONDAIRE : Moneyvox, chiffre DGFiP non retrouvé] ; la taxe moyenne d'un propriétaire particulier
  est de 1 117 € en 2025 (DGFiP Statistiques n° 46, 05/05/2026) [TEXTE LU] ;
- l'opération « éléments de confort » (novembre 2025 : 7,4 millions de logements, +63 € en moyenne,
  466 M€) a été suspendue dans la semaine, puis rendue facultative, sur demande des communes, pour une
  application à partir de 2027 [SECONDAIRE : Banque des Territoires, IFRAP du 16/10/2026] ;
- les réformes fondées sur une réévaluation ont échoué ou ont été abandonnées à Pittsburgh (2001), en
  France (1990), en Corée (2022-2024) ; l'Angleterre n'a jamais réévalué depuis 1991 (IFS).

**Transposable** : mensualiser par défaut et afficher la taxe future à la vente réduisent la saillance
(Cabral-Hoxby) et l'erreur d'anticipation (Bradley, 2017 : les acheteurs du Michigan surpaient d'environ
10 000 $ en ignorant la remise à niveau de la base après la vente [RÉSUMÉ, note LVT]). La transparence
démocratique peut s'en trouver réduite : c'est un choix politique, pas un résultat.

### 1f. Effet sur la construction et la densité de la part qui porte sur le bâti

**Mécanisme** (Brueckner et Kim, 2003 [RÉSUMÉ, note LVT]) : taxer le bâti réduit le capital par mètre
carré de terrain (hauteur), ce qui étale la ville, mais renchérit le logement, ce qui réduit la surface
consommée et densifie ; l'effet net est ambigu (étalement si la substitution entre logement et autres
biens est faible). Song et Zenou (2006), *JUE* 60(3) : avec une élasticité de substitution supérieure à 1,
l'impôt foncier réduit la taille des villes ; sur 448 aires urbanisées américaines, les taux effectifs
plus élevés vont avec des villes plus compactes [RÉSUMÉ]. Un impôt sur le seul terrain est neutre pour la
densité s'il est assis sur une valeur indépendante de l'usage (note LVT, §10).

**Effets estimés** :
- New Hampshire, réforme du financement scolaire de 1999 : un allègement moyen égal à 15 % des recettes
  foncières locales augmente l'investissement résidentiel de 11 à 22 % (élasticité d'environ −1), sauf
  dans la couronne de Boston où il est capitalisé dans les prix (Lutz, 2015) [TEXTE LU, note LVT : version
  2009]. *Effet causal.*
- Allemagne : plus de 20 000 changements de Hebesatz 2004-2018, étude d'événement empilée ; +1 % de taux
  réduit la base de 0,11 % et la population de 0,036 %, avec des gains dans les communes voisines
  (Thunecke, 2026) [RÉSUMÉ : page du séminaire Syracuse-Chicago ; texte non trouvé].
- Nouvelle-Zélande : le passage de la valeur du sol à la valeur totale après la fusion d'Auckland a des
  effets sur les agrandissements et transformations, pas sur la construction neuve, sur deux ans (Gemmell,
  Grimes et Skidmore, 2019) [RÉSUMÉ, note LVT].
- Finlande : permettre aux communes de taxer plus lourdement les terrains constructibles non bâtis
  (2001) augmente les mises en chantier de maisons individuelles d'environ 10 % (document de travail
  VATT n° 419) à 12 % (*JUE* 65(3), 2009) dans les communes adoptantes, sans effet sur la taille des
  maisons et avec des indices de densité plus faible (Lyytikäinen, 2009) [RÉSUMÉ, via notices et
  résumés] ; une étude sur Espoo ne trouve pas d'effet (Hannonen, 2008) [SECONDAIRE].
- Danemark : aucun effet de la taxe sur le sol sur la construction ni sur la mise en valeur des terrains
  nus (Nielsson et al., 2024).
- France : aucune étude de l'effet de la TFPB ou de l'exonération de deux ans des constructions neuves sur
  la construction n'a été trouvée.

**Transposable** : alléger la part bâti peut stimuler la construction là où l'offre est élastique ; dans
les zones où le zonage contraint, l'allègement se capitalise. L'instrument « terrain constructible non
bâti » existe en France (majoration facultative de la valeur locative, art. 1396 CGI), sans évaluation.

### 1g. Concurrence fiscale locale

**Mécanisme** : la vue « capital » (1b) prédit que les écarts de taux déplacent le capital vers les
communes moins taxées ; la concurrence par comparaison (« yardstick ») prédit que les élus imitent les
taux voisins. Un impôt sur le seul terrain réduit la première par construction (le terrain ne bouge
pas), mais pas l'exportation de l'impôt vers les propriétaires non résidents (résidences secondaires,
bailleurs, entreprises).

**Fiche — Lyytikäinen, « Tax competition among local governments: Evidence from a property tax reform in
Finland »** (*Journal of Public Economics* 96(7-8), 2012 ; document SERC DP 82, juin 2011) [TEXTE LU :
version 2011] :
- Institution : impôt foncier communal finlandais depuis 1993 ; un taux général s'applique au terrain
  (évalué comme s'il était nu, donc neutre) et aux bâtiments non résidentiels, un taux inférieur aux
  bâtiments résidentiels (fourchettes 1993 : 0,2-0,8 % et 0,1-0,4 %). En 2000, l'État relève les
  planchers à 0,5 % et 0,22 %, ce qui contraint environ 40 % et 30 % des communes.
- Méthode : la hausse imposée aux voisins sert d'instrument au taux des voisins.
- Résultat : aucune interaction ; les coefficients de 0,4-0,5 de la littérature sont exclus ; les
  méthodes spatiales usuelles surestiment l'interaction. *Effet causal (absence d'effet).*
- Limites : l'impôt foncier pèse moins de 5 % des recettes communales finlandaises ; la péréquation
  atténue les incitations ; une hausse imposée par l'État se prête mal à la comparaison par les
  électeurs.

**Autres résultats** : Baskaran (2014), *J. Public Econ.* 118 : pas d'imitation des taux de taxe
professionnelle et foncière en Basse-Saxe après un choc de péréquation en Rhénanie-du-Nord-Westphalie
[RÉSUMÉ]. France : les études qui trouvent de l'imitation portent surtout sur la taxe professionnelle et
utilisent des méthodes spatiales (Leprince, Madiès et Paty, 2007 ; Charlot, Paty et Piguet, 2015, qui
trouvent que la coopération intercommunale réduit la concurrence et relève les taux de taxe
professionnelle) [RÉSUMÉ]. Aucune étude causale sur les taux de TFPB n'a été trouvée.

**France, fait mesuré** [TEXTE LU, note LVT] : depuis la suppression de la TH, la TFPB est le seul levier
de taux des communes ; taux moyen communes et groupements 30,9 % en 2007 (parts départementale et
régionale comprises), 39,7 % en 2024 ; 17 % des communes relèvent leur taux en 2024, 13 % en 2025. Le
taux de TFPB d'une commune ne peut dépasser 2,5 fois le taux moyen départemental ou national s'il est
plus élevé (art. 1636 B septies CGI) [SECONDAIRE : synthèse de recherche citant BOFiP et la fiche des
éléments de référence 2025] ; le taux de CFE suit les variations du taux de TFPB (règles de lien, art. 1636
B sexies) [SECONDAIRE].

---

## 2. Le taux différencié : ce que montrent les expériences

### 2.1 Pittsburgh et les villes de Pennsylvanie

Les fiches détaillées sont dans `lvt/notes/theorie_et_split_rate.md` (§3 à 5) et
`transitions_et_saillance.md` (B12) ; on en reprend l'essentiel.

**Fiche — Oates et Schwab (1997), *National Tax Journal* 50(1)** [TEXTE LU, note LVT] : en 1979-1980,
Pittsburgh porte le taux municipal sur le sol à plus de cinq fois celui du bâti (125,5 contre 24,75
millièmes en 1980) ; comté et district scolaire taxent au même taux, si bien que l'écart total reste à
peine supérieur à 2:1. Permis de construire réels +70 % entre 1960-1979 et 1980-1989, contre −14 % en
moyenne dans 15 villes de la Rust Belt ; Pittsburgh est la seule ville dont l'indicatrice post-réforme est
significative. Les auteurs attribuent le boom à la pénurie de bureaux (vacance inférieure à 1 %) et au
programme Renaissance II ; l'impôt foncier a joué « an important supporting role » en évitant de
relever d'autres impôts. *Comparaison avant-après, un seul traité* : pas d'effet causal propre.

**Fiche — Plassmann et Tideman (2000), *Journal of Urban Economics* 47(2)** [RÉSUMÉ ; résumé de la thèse
de 1997 lu ici] : 15 communes à deux taux contre 204 à taux unique, 1972-1994, permis modélisés en Poisson
à paramètre log-normal (MCMC) : effet positif et significatif sur le nombre de permis ; pas d'effet sur
la valeur par permis ; effet positif sur la valeur totale. Le modèle binomial négatif de la thèse donne un
effet positif non significatif. Dye et England (2010) en tirent un ordre de grandeur de +3 à 4 % de
construction résidentielle. *Effet sensible à la spécification.*

**Fiche — Banzhaf et Lavery (2010), *JUE* 67(2)** [TEXTE LU, note LVT : document de travail 2008] :
secteurs de recensement de Pennsylvanie 1970-2000, premières différences avec effets fixes, appariement.
Le double taux augmente de 5 à 6 points la croissance décennale du nombre de pièces au cours des une ou
deux premières décennies, surtout par davantage de logements (+5 points) plutôt que des logements plus
grands ; avec le ratio des taux, 2:1 donne environ +1 point, 4:1 environ +3 points ; l'appariement donne
+7 à +10 points non significatifs. Les auteurs ne prétendent pas avoir montré une réduction de
l'étalement. Yang (2014, Lincoln) trouve +8,3 points pour les pièces et +8,4 points pour les logements
[TEXTE LU, note LVT] ; Hanson (2021, Lincoln) +60 à 107 établissements à l'adoption, effet qui s'érode
d'environ 5 % par an [TEXTE LU, note LVT].

**Pourquoi Pittsburgh abandonne en 2001** (Hughes, 2006, Lincoln WP06ZK1) [TEXTE LU, note LVT] : gel des
évaluations par le comté d'Allegheny en 1996 ; réévaluation complète ordonnée par un juge en 1997, avec
passage à la valeur de marché pleine ; en janvier 2001, les avis montrent pour la première fois la
décomposition sol et bâti : valeur du sol +81 %, du bâti +43 % ; les taux avaient été fixés sur une part
du sol projetée d'environ 20 %, elle atteint environ 30 % ; la méthode résiduelle d'évaluation du sol est
contestée ; le conseil municipal revient au taux unique dans l'année. Altoona, passée au sol seul en 2011,
revient à l'impôt classique en 2017 (bénéfices non démontrés, confusion, taux sur le sol jugé dissuasif)
[SECONDAIRE, note LVT]. Synthèse de Dye et England (2010) : résultats empiriques « generally
inconclusive » [TEXTE LU, note LVT] ; revue systématique galloise (Goodwin-Hawkins, 2026) : effets
« modestes », limités aux zones urbaines tendues [RÉSUMÉ, note LVT].

**Ce qu'on peut transposer** : l'ordre de grandeur (quelques points de croissance du parc par décennie
pour des écarts de taux effectifs faibles) et surtout la leçon d'échec : ce n'est pas le principe qui a
été rejeté mais une réévaluation brutale après un gel, sans lissage, avec des taux calés sur une base
projetée erronée.

### 2.2 Le Bade-Wurtemberg (Grundsteuer B sur la valeur du sol, depuis 2025)

**Règles de la loi** (Landesgrundsteuergesetz, LGrStG, du 4 novembre 2020, modifiée notamment fin 2021, le 13/06/2023 et le
18/11/2025) [TEXTE LU : version de 2020 sur gesetze-im-internet.de et loi modificative du 18/11/2025
(GBl. n° 113) ; règle des 30 % lue dans le communiqué du BFH] :
- assiette : surface du terrain × Bodenrichtwert de la zone (§ 38 al. 1) ; « maßgebend ist der
  Bodenrichtwert des Richtwertgrundstücks in der Bodenrichtwertzone » ; le bâti est ignoré ; les
  Bodenrichtwerte sont fixés par les comités d'experts (Gutachterausschüsse, § 196 BauGB) comme si le
  terrain était nu, et transmis à l'administration fiscale (§ 38 al. 2) ; à défaut, valeur déduite de
  surfaces comparables (§ 38 al. 3) ;
- preuve d'une valeur inférieure par expertise qualifiée si la valeur typisée dépasse la valeur réelle
  de plus de 30 % (§ 38 al. 4), contre 40 % dans le modèle fédéral ; la loi de 2025 étend une règle
  analogue (40 %) à l'agriculture (§ 33 al. 3) ;
- taux légal (Steuermesszahl) 1,30 ‰ (§ 40 al. 2), réduit de 30 % si le terrain sert majoritairement au
  logement (§ 40 al. 3), de 25 % pour le logement social aidé ou détenu par des sociétés publiques,
  coopératives ou organismes d'utilité publique (al. 4 et 5), de 10 % pour les monuments (al. 6),
  cumulables (al. 7) ; agriculture et forêt 0,55 ‰ (al. 1) ; un al. 8 (abattement sur demande) existe
  depuis 2023, contenu non lu [NON VÉRIFIÉ] ;
- taux communal (Hebesatz) unique pour tous les terrains d'une commune (§ 50 al. 4) : la seule
  différenciation entre logement et autres usages passe par le taux légal ; un taux distinct sur les
  terrains constructibles non bâtis, désignés par arrêté communal, est prévu (§ 50a, « Grundsteuer C »),
  contenu non lu [NON VÉRIFIÉ] ;
- réévaluation générale tous les sept ans (§ 15), première au 1er janvier 2022 pour l'impôt de 2025 ;
  Bodenrichtwerte mis à jour au moins tous les deux ans (§ 196 BauGB, note LVT) ;
- échéances trimestrielles (15 février, mai, août, novembre ; § 52) ;
- aucun dispositif de lissage ou de cas difficiles prévu par le Land (présentation de Karlsruhe, note LVT).
- **Taux effectifs** [CALCUL] : avec le Hebesatz de 270 % de Karlsruhe, 0,25 % de la valeur de zone pour un
  terrain résidentiel (1,30 ‰ × 0,7 × 2,7) et 0,35 % pour les autres ; avec le Hebesatz médian de 290 %
  (30/06/2025, Destatis via Grundradar [SECONDAIRE, note LVT]), 0,26 % et 0,38 %.

**Hebesätze et neutralité** [SECONDAIRE, note LVT] : un registre de taux « neutres en recettes » publié par
le ministère des Finances (fourchettes par commune, non contraignantes) ; selon le Bund der Steuerzahler
(15/09/2025), 720 communes sur 1 101 sont dans la fourchette, 338 au-dessus, 43 en dessous ; taux de moins
de 100 % à plus de 1 000 %.

**Effets constatés en 2025** :
- Karlsruhe (Stadtkämmerei, 07/10/2024, calcul sur les nouvelles bases au Hebesatz neutre de 270 %, recette
  de 60 M€) [TEXTE LU, note LVT] : commerces −40 % (22,36 → 13,37 M€), maisons individuelles +76 %
  (6,29 → 11,05 M€), maisons bifamiliales +105 %, copropriétés −20 %, immeubles locatifs +16 %, divers dont
  terrains nus +265 % ; environ la moitié des biens paient moins ; 24 % de réclamations.
- Part du logement dans l'impôt foncier : Mannheim 56 → 63 %, Fribourg 61 → 70 %, Ravensburg 54 → 70 %
  [SECONDAIRE, note LVT].
- Stuttgart a le coût annexe du logement le plus élevé des capitales régionales en 2025 (2 559 € pour un
  ménage type en maison individuelle), l'impôt foncier en étant la cause principale selon le Bund der
  Steuerzahler (novembre 2025) [SECONDAIRE].
- Aucune étude académique ex post (ZEW, ifo, IW, office statistique) n'a été trouvée.

**Contentieux** :
- Bundesfinanzhof, II R 26/24 (Karlsruhe : terrain d'environ 1 100 m², maison bifamiliale de 1968,
  Bodenrichtwert 510 €/m², valeur fiscale 565 000 €, expertise produite trop tard à 361 000 €) et II R
  27/24 (Stuttgart : 434 m², Bodenrichtwert 1 400 €/m², 607 000 €) ; audience le 22/04/2026, décision
  annoncée le 20/05/2026 (communiqué n° 032/26) [TEXTE LU : communiqué] ; motifs publiés début juillet 2026
  [SECONDAIRE]. Le Land était compétent (art. 105 al. 2 et 72 al. 3 n° 7 GG) ; ne retenir que le sol n'en
  fait pas un autre impôt ; le législateur peut typiser et privilégier la praticabilité ; double fondement
  admis (équivalence : accès aux infrastructures communales ; capacité contributive : rendement potentiel
  reflété dans le Bodenrichtwert) ; la valeur de zone appliquée à toute la parcelle, sans tenir compte du
  bruit ou de l'usage d'une partie du terrain, est justifiée par la gestion de masse ; la règle des 30 %
  évite une imposition excessive ; la réduction pour le logement peut passer par le taux plutôt que par
  l'assiette ; pas de renvoi au BVerfG.
- Recours constitutionnels pendants : 1 BvR 1977/26 et 1 BvR 2005/26, soutenus par le Bund der
  Steuerzahler, Haus & Grund et le Verband Wohneigentum (qualité des Bodenrichtwerte, abattements
  interdits pour les jardins inconstructibles, coût de l'expertise, seuil de 30 %) [SECONDAIRE :
  steuerzahler.de, 14/08/2026]. Un recours contre le modèle fédéral a été déposé le 27/02/2026
  [SECONDAIRE]. Les modèles de Hambourg, de Hesse et de Bavière sont pendants devant le BFH (audiences
  prévues fin 2026 et premier semestre 2027, communiqué du BFH).
- Antécédent : le BVerfG a jugé en 2018 les valeurs unitaires de 1964 et 1935 contraires à l'égalité
  (note LVT) ; aucun équivalent français n'a été trouvé pour les valeurs de 1970.

**Ce qu'on peut transposer** : le droit (typisation par zones publiées, preuve contraire au-delà d'un
seuil, différenciation par le taux) et l'ordre de grandeur du déplacement de charge ; pas d'effet
économique mesuré. Le Land a fait la bascule sans lissage ni registre contraignant : près d'un tiers des
communes ont fixé un taux au-dessus de la fourchette neutre, dont environ 18 % de l'ensemble avec une
hausse de recettes d'au moins 5 % environ (Bund der Steuerzahler [SECONDAIRE, note LVT]).

### 2.3 Danemark (grundskyld) et réforme de 2024

Repris de `transitions_et_saillance.md` (B10) et `etudes_recentes.md` (§1), complété ici.
- La grundskyld est assise sur la valeur du terrain ; depuis 2024, sur 80 % de la valeur évaluée
  (abattement de précaution), avec une taxe sur la valeur du logement occupé par son propriétaire et
  une taxe sur le bâti commercial à côté : le système danois est un système à deux assiettes, pas « sol
  seulement ».
- Taux : au plus 30 ‰ (34 ‰ avant 2024), plus de minimum (16 ‰ avant) ; de 2024 à 2028, chaque commune
  est plafonnée au taux de l'annexe 1 de la loi (ejendomsskatteloven § 28, al. 1) et ne peut dépasser
  son taux de 2023 ; liberté retrouvée en 2029 dans la limite de 30 ‰ [TEXTE LU : Den juridiske
  vejledning 2026-2, C.H.4.3.4.4] ; plafonds communaux de 3,1 ‰ (Frederiksberg) à 17,7 ‰ (Varde)
  [SECONDAIRE : EY, note LVT].
- Effet observé : grundskyld moyenne par logement occupé par son propriétaire de 10 695 DKK en 2023
  (Danmarks Statistik, 23/11/2023) à 7 966 DKK en 2025, « au même niveau qu'en 2024 » (Danmarks
  Statistik, 02/12/2025), soit −25 % [TEXTE LU ; CALCUL] ; impôt de 2025 encore calculé sur des
  évaluations provisoires, à régulariser.
- Transition : rabais garantissant aux propriétaires d'avant 2024 de ne pas payer plus, perdu à la vente ;
  plafonnement de la hausse à 4,75 % par an attaché au bien ; prêt d'État par défaut pour les hausses
  futures (note LVT).
- Fiabilité : en 2011, environ 25 % seulement des maisons vendues étaient évaluées dans la fourchette
  acceptable ; en 2024, l'administration corrigeait encore des cas où la valeur du sol dépassait la
  valeur totale du bien (note LVT).

### 2.4 Finlande : un double taux national depuis 1993

- Terrain évalué selon sa surface et son type, comme s'il était nu ; bâtiments au coût de construction
  moins amortissement (Lyytikäinen, 2012) [TEXTE LU].
- Fourchettes légales 2026 : taux général sur le sol 1,30-2,00 % ; taux général sur les bâtiments
  0,93-2,00 % ; logements permanents 0,41-1,00 % ; autres logements (résidences de loisirs) 0,93-2,00 % ;
  terrains constructibles non bâtis 2,00-6,00 % [TEXTE LU : vero.fi] ; un taux séparé sur le sol existe
  depuis 2024 [SECONDAIRE : extraits de vero.fi].
- Effets : pas de concurrence fiscale mesurable (1g) ; surtaxe des terrains constructibles non bâtis :
  +10 à 12 % de mises en chantier de maisons individuelles (1f).
- **Transposable** : c'est le seul système national européen qui différencie sol, bâti résidentiel et
  terrain constructible non bâti avec des fourchettes votées par les communes ; il pèse peu dans les
  recettes communales.

### 2.5 Estonie, Nouvelle-Zélande, Australie

- **Estonie** (maamaks, sol seul) : fourchettes 2025-2026 de 0,1-1 % pour le résidentiel, 0,1-2 % pour les
  autres terrains [note LVT] ; évaluation de 2022 appliquée depuis 2024, plafonds de taux réduits de 2,5 à
  5 fois ; hausse annuelle plafonnée à 50 % ou 20 € en 2025 ; terrain sous la résidence principale exonéré
  jusqu'à 0,15 ha en zone dense et 2 ha ailleurs [SECONDAIRE : ERR, KPMG, Cobalt, EMTA via extraits].
  Tallinn a un ratio capital/sol plus élevé que Riga, mais les deux villes s'étalent (Wenner, 2018)
  [RÉSUMÉ, note LVT].
- **Nouvelle-Zélande** : les communes taxant la valeur du sol passent de 47 % à 29 % entre 2007 et 2019,
  leur part dans les recettes de 33 % à 12 % ; aucune ne fait le chemin inverse depuis 1989 (Colegrave et
  Winter, 2019 ; McCluskey et al., 2002) [TEXTE LU, note LVT] ; raisons non documentées.
- **Australie** : Nouvelle-Galles du Sud (impôt sur le sol au-delà d'un seuil, résidence principale
  exonérée) ; ACT (bascule sur vingt ans des droits de mutation vers des « rates » sur la valeur du sol,
  élasticité des ventes de 0,6, transition enlisée vers 29 % des recettes propres) ; Victoria (depuis le
  01/07/2024, un bien commercial ou industriel acquitte un dernier droit de mutation à sa première vente,
  puis, dix ans plus tard, un impôt annuel de 1 % de la valeur du sol) [notes LVT : TEXTE LU, SECONDAIRE].

---

## 3. Faisabilité en France

### 3.1 Données de valeur du terrain

| Source | Ce qu'elle donne | Limites pour une assiette « sol » |
|---|---|---|
| DVF (DGFiP, Etalab, ouvert) | toutes les mutations à titre onéreux, prix, parcelles, surfaces, nature (dont « terrain à bâtir ») | ventes seulement (un bien passe sur le marché tous les 19 ans en moyenne, CPO) ; prix du bien entier, pas du sol ; ventes de terrains nus rares en zone dense (presque aucune à Paris, note LVT) ; Bas-Rhin, Haut-Rhin, Moselle et Mayotte absents (absents des données 2024 utilisées par la note LVT [CALCUL]) |
| DV3F (Cerema) | DVF croisé avec les Fichiers fonciers (caractéristiques des parcelles et des locaux, typologie des acteurs) | accès réservé aux acteurs publics de l'aménagement sur engagement annuel ; version ouverte annoncée sans date [SECONDAIRE : documents Datafoncier] |
| Fichiers fonciers (MAJIC, DGFiP-Cerema) | surface de chaque parcelle, locaux, propriétaires | aucune valeur de marché ; la répartition du sol entre lots de copropriété reste à définir (tantièmes) [NON VÉRIFIÉ] |
| EPTB (SDES) | enquête obligatoire et exhaustive auprès des bénéficiaires d'un permis de maison individuelle en secteur diffus : 102 €/m², 932 m², 95 000 € en 2024 | terrains achetés pour une maison neuve seulement ; ni collectif, ni groupé, ni terrain sous bâti existant [TEXTE LU : pages SDES] |
| Comptes de patrimoine (Insee) | terrains bâtis : 6 729 Md€ fin 2024, dont ménages 4 043 Md€ | résidu agrégé (valeur de marché moins bâti à l'inventaire permanent), sans marge d'erreur, révisé de 9 % entre deux publications ; terrains non résidentiels valorisés avec l'indice résidentiel (note LVT) |
| RVLLP (locaux professionnels, depuis 2017) | grille de tarifs au m² par secteur d'évaluation et catégorie, coefficients de localisation de 0,7 à 1,3, environ 3,6 millions de locaux | valeurs locatives du local entier, pas du sol ; utile comme carte de la rente de localisation ; actualisation sexennale des paramètres reportée au 1er janvier 2027 (note LVT) |
| GMBI (déclarations d'occupation depuis 2023) | occupation de chaque local d'habitation | loyers seulement si la déclaration les intègre ; le CPO propose de s'en servir pour une assiette locative ou un modèle d'évaluation automatique [TEXTE LU, note LVT] |

**Constat** : la France a les briques d'une estimation statistique de la valeur des biens (DVF, Fichiers
fonciers, modèle de l'Insee utilisé par André et Meslin) ; elle n'a ni valeurs de zone du sol publiées,
ni comités d'experts chargés de les fixer. Les tests gallois montrent qu'on peut estimer la géographie
relative du sol de façon robuste, mais pas une valeur parcellaire incontestable.

### 3.2 Révision des valeurs locatives des locaux d'habitation : calendrier

[TEXTE LU, note LVT, sauf mention]
- 1990 : révision menée, jamais intégrée.
- LF 2020, art. 146 : révision sur les loyers de 2023 pour des bases appliquées en 2026 ; quatre
  sous-groupes, secteurs d'évaluation, tarifs au m², coefficient de localisation de 0,7 à 1,3, locaux
  exceptionnels à 8 % de la valeur vénale.
- LF 2023, art. 106 : report à 2028.
- LF 2026 (loi n° 2026-103 du 19/02/2026), art. 106 : déclaration des loyers avant le 1er juillet 2028,
  marché de référence au 1er janvier 2028, rapport au Parlement avant le 1er septembre 2029, commissions
  locales en 2030, intégration dans les bases au 1er janvier 2031, première révision sexennale en 2038.
- PLF 2027 (n° 3210), amendement I-CF1872 de M. Juvin du 7 octobre 2026, adopté en commission des
  finances [TEXTE LU : texte de l'amendement] : à compter du 1er janvier 2028, la valeur locative d'un
  logement serait révisée « à l'occasion de chaque mutation à titre onéreux », selon le marché locatif au
  1er janvier de l'année de la vente, avec les règles de la LF 2020 (sous-groupes, tarifs, coefficients de
  localisation, 8 % de la valeur vénale pour les locaux exceptionnels), applicable aux impositions de
  l'année suivante, jusqu'à la révision générale ; l'exposé reconnaît la coexistence de deux bases dans un
  même immeuble et défend sa compatibilité avec l'égalité devant les charges publiques. Un amendement de
  séance (I-3528) étendrait la révision aux successions et donations [SECONDAIRE : Selectra] ; sort en
  séance et au Sénat [NON VÉRIFIÉ].
- **Lecture** : la révision prévue porte sur les loyers, pas sur la valeur vénale ni sur le sol ; la
  révision au fil des ventes ressemble à la base « prix d'achat » de la Proposition 13 : les acheteurs
  paieraient plus que leurs voisins, ce qui est un coût de transaction supplémentaire, à l'opposé du
  report des DMTO sur la détention (verrou documenté en Californie et au Michigan).

### 3.3 Contraintes juridiques

- **Égalité devant l'impôt** (art. 13 DDHC) : le législateur « doit fonder son appréciation sur des
  critères objectifs et rationnels en fonction des buts qu'il se propose » (formule rappelée dans la
  décision n° 2019-796 DC du 27/12/2019, § 4) [TEXTE LU : décision, extraits]. Une assiette « valeur du
  sol » devrait se justifier par un but (efficacité, densification, financement des équipements qui font
  la valeur du sol) ; le BFH a admis pour le Bade-Wurtemberg un double fondement d'équivalence et de
  capacité contributive. Aucune décision du Conseil constitutionnel n'a été trouvée sur l'obsolescence des
  valeurs de 1970 [NON VÉRIFIÉ de manière exhaustive].
- **Libre administration et autonomie financière** (art. 72 et 72-2) : la décision 2019-796 DC valide la
  suppression de la TH ; « aucune exigence constitutionnelle n'impose que la suppression ou la réduction
  d'une recette fiscale » soit compensée par un montant comparable (§ 24) ; une fraction de TVA est une
  ressource propre même si le département n'en fixe pas le taux (§ 35) [TEXTE LU]. Un report des DMTO
  (départements) sur la TFPB (communes) est donc possible juridiquement si la part des ressources propres
  reste déterminante ; il pose surtout une question de financement des départements (le CPO demande une
  compensation par l'État [TEXTE LU : CPO 2023]).
- **Mécanismes de transition et contentieux** : la validation législative rétroactive des modalités de
  calcul du « planchonnement » des locaux professionnels (art. 63 de la LF 2025) a été censurée (décision
  n° 2025-1174 QPC du 28/11/2025, absence de motif impérieux d'intérêt général) après que le Conseil d'État
  a exigé en 2023 un recalcul annuel [SECONDAIRE : Option Finance, cabinets] ; en 2016, la validation
  d'évaluations faites par comparaison avec des locaux-types détruits a aussi été censurée (n° 2015-525
  QPC) [SECONDAIRE : Banque des Territoires]. Les dispositifs de lissage d'une révision sont un nid à
  contentieux s'ils sont mal écrits.
- **Pouvoir de taux** : la commune vote un taux unique de TFPB, plafonné, auquel sont liés d'autres taux
  (1g). Un double taux demanderait une loi définissant deux assiettes et soit deux taux votés, soit un
  rapport légal entre eux (comme le taux légal réduit pour le logement au Bade-Wurtemberg).

### 3.4 Propositions françaises

- **CAE, Note n° 2 (2013), Trannoy et Wasmer** [TEXTE LU, note LVT] : supprimer graduellement les DMTO et
  asseoir la TFPB sur la valeur vénale nette des emprunts, barème relevé sur une dizaine d'années ;
  taxer la plus-value latente lors d'un changement de document d'urbanisme.
- **CPO 2018** : bascule progressive des DMTO vers la TF, rappelée par le CPO 2023 [TEXTE LU : mention dans
  CPO 2023 ; rapport de 2018 non lu].
- **CPO, *Pour une fiscalité du logement plus cohérente*, décembre 2023** [TEXTE LU] : recommandation 3,
  rétablir un lien direct avec les loyers ou les prix, l'option de la valeur vénale « ne saurait être
  complètement écartée » (outils : DVF généralisées, modèles d'évaluation automatique) ; mention de
  l'« impôt foncier à taux fractionné » de l'OCDE (2018) et de la proposition de Trannoy et Wasmer d'une
  taxe plate sur le terrain ; recommandation 8, ne basculer les DMTO vers la détention qu'une fois l'assiette
  rétablie, la bascule « ne saurait être mise en œuvre tant que la fiscalité foncière apparaît décorrélée
  des réalités économiques locales ».
- **IPP** : rapport n° 29 (2020) sur la révision des valeurs locatives ; rapport n° 48 (2023) sur la TH
  [TEXTE LU, note LVT].
- **Trannoy et Wasmer, *Le grand retour de la terre dans les patrimoines* (2022)** : taxe plate sur la
  valeur du terrain [SECONDAIRE, note LVT] ; **Bonnet, Chapelle, Trannoy et Wasmer (2021)**, *EER* :
  premier rang atteint par un impôt foncier positif sans impôt sur le capital [TEXTE LU, note LVT].
- **Bontemps, Cherbonnier et Magnac (TSE, 2023)** : ramener les coûts de transaction de 14 % à 6 %,
  financés par un impôt proportionnel sur la propriété : transactions +21 %, prix +2,4 %, loyers −1,6 %,
  bien-être des nouveaux ménages +0,2 % [TEXTE LU, note LVT].
- **France Stratégie (décembre 2016)** : parmi quatre options, supprimer les DMTO en compensant par la TF
  ou l'impôt sur le revenu [SECONDAIRE : extraits de recherche, page d'origine supprimée].
- **Cour des comptes, *Les taxes foncières* (2023)** : le report de la révision « fragilise les
  fondements des taxes foncières » [via CPO, note LVT] ; **Commission Rebsamen (2021)** : supprimer les
  incitations à la rétention foncière [SECONDAIRE, note LVT].
- **2025-2026** : le rapporteur général du Sénat demande d'accélérer la révision [SECONDAIRE : Public
  Sénat] ; amendement Juvin (3.2) ; aucun rapport parlementaire récent consacré à une taxe sur la valeur du
  sol n'a été trouvé.

---

## 4. Effets redistributifs d'un passage à la valeur du sol, et transitions

### 4.1 Effets redistributifs

**Fiche — trois simulations américaines à recette constante, mêmes méthodes, résultats opposés.**
- England et Zhao (2005), *NTJ* 58(2) ; Lincoln WP04RE2 [TEXTE LU : document de travail]. Dover (New
  Hampshire), évaluations 2002. Une taxe sur le seul sol, sans crédit, augmenterait la facture de 634 $ en
  moyenne pour les 30 % de maisons les moins chères (99 % de perdants), de 311 $ pour les 40 % du milieu,
  et la réduirait de 138 $ pour les 30 % les plus chères. Avec un taux réduit sur le bâti et un crédit
  uniforme de 1 000 $ par avis, 72 % du groupe médian et 80 % du groupe inférieur paieraient moins. Les
  auteurs recommandent un crédit forfaitaire pour corriger cette régressivité.
- Bowman et Bell (2008), *NTJ* 61(4) : à Roanoke (Virginie), la même bascule profite surtout aux quartiers
  les plus pauvres [RÉSUMÉ].
- Plummer (2009, Lincoln WP09EP1 ; *NTJ* 63(1), 2010) [TEXTE LU : document de travail]. Comté de Tarrant
  (Texas), 1997-2006 : taux neutre de 10,3 % de la valeur du sol contre 2,42 % de la valeur totale ; en
  2006, la charge des maisons individuelles baisse de 22 % et celle du collectif de 39 %, celle du commerce
  monte de 34 % et celle des terrains nus de 355 % ; 85 % des maisons individuelles paient moins (−30 % en
  médiane) ; légère progressivité supplémentaire (indice de Suits) ; ce sont les maisons les moins chères
  qui risquent le plus une hausse et dont les taux effectifs varient le plus.
- **Lecture** : le résultat dépend de la corrélation locale entre part du sol et valeur du bien. Là où les
  maisons modestes sont sur de grands terrains peu chers (Dover), la bascule est régressive ; là où le sol
  pèse surtout dans les biens chers et les terrains commerciaux étendus (Texas), elle est progressive. Les
  simulations ignorent les réactions des prix.

**Autres simulations** [notes LVT] : Pays de Galles (2020), le changement de facture est corrélé à 61 %
avec l'indice de défaveur, les zones aisées paient plus ; Detroit (Anderson et Allen, 2022, ratio 5:1 sur
cinq ans), −18 % pour les logements, +90 % pour un corridor de parkings ; Cincinnati (2026, 4:1), terrains
vacants +126 %, quartiers pauvres −17 %, riches +11 % ; Allemagne (Barbosa et Skipka, 2019), part du sol de
33 % dans la valeur des biens des propriétaires, taux neutre de 0,6 %, hausse de 25 % pour le premier
quintile dans un scénario régional ; FMI (Schwerhoff, Edenhofer et Fleurbaey, 2022), corrélation négative
entre valeur du sol détenue et poids social aux États-Unis et en France, les classes moyennes paieraient
plus en part du revenu que les hauts revenus [RÉSUMÉ, texte inaccessible].

**France, ce qu'on peut dire** :
- *Entre territoires* (fait mesuré + calcul) : la TFPB pèse 0,54 % de la valeur des logements dans les 5 %
  de communes les moins chères et 0,20 % dans les 5 % les plus chères ; la part du sol va de 10 % à 75 %
  selon les départements. Une taxe sur le sol à recette constante déplacerait donc la charge des
  territoires ruraux et des villes bon marché vers l'Île-de-France, les métropoles, les Alpes et le
  littoral : maison médiane de Corrèze de 1 040 € à environ 70 €, de Haute-Savoie de 930 € à environ
  1 700 € ; appartement parisien de 730 € à 2 130 € sous l'hypothèse de 75 % de sol (note LVT, calcul).
- *À l'intérieur d'une commune* (par analogie avec Karlsruhe et Dover) : hausse pour les maisons sur
  grands terrains et les terrains nus, baisse pour les copropriétés ; effet sur les commerces ambigu
  (baisse en ville dense, hausse pour les surfaces commerciales étalées).
- *Par revenu* : les ménages aisés détiennent davantage de biens dans les zones chères (IA 91) ; une taxe sur
  le sol serait vraisemblablement plus progressive par rapport au patrimoine que la TFPB actuelle ; par
  rapport au revenu, le signe n'est pas connu (plausible, non démontré).
- *Par âge* : aucune donnée. Par analogie : l'IFS trouve qu'une council tax proportionnelle redistribue
  des ménages âgés vers les jeunes (−30 £ par an pour les 65 ans et plus, +140 £ pour les moins de 35
  ans) ; au Danemark, les hausses n'ont pas chassé les propriétaires âgés en place mais ont réduit leurs
  arrivées. On peut supposer, sans que la littérature l'ait établi, que les perdants âgés seraient les
  propriétaires de maisons sur grands terrains dans les couronnes des métropoles chères.
- *Selon la mise en œuvre* : à dotations inchangées, une taxe communale sur le sol ne redistribue qu'à
  l'intérieur de chaque commune (IFS) ; les écarts entre territoires n'apparaissent que si l'État ajuste
  les dotations ou si le taux est fixé nationalement.

### 4.2 Transitions acceptables : ce qu'on sait

Aucune étude causale ne compare des modes de transition ; on dispose de dispositifs observés et de leur
sort politique.

| Dispositif | Où | Sort observé | Statut |
|---|---|---|---|
| Aucun lissage, réévaluation brutale après gel, taux calés sur une base projetée | Pittsburgh 2001 | abandon du double taux dans l'année | [TEXTE LU, note LVT] |
| Aucun lissage, registre de taux neutres non contraignant | Bade-Wurtemberg 2025 | mis en œuvre ; 24 % de réclamations à Karlsruhe ; un tiers des communes au-dessus de la neutralité ; recours constitutionnels | [TEXTE LU / SECONDAIRE] |
| Réévaluation complète + abattement forfaitaire + programme pour occupants anciens | Philadelphie 2014 | maintenu, réévaluations en 2019 et 2023 | [TEXTE LU] |
| Écart divisé par deux (2017-2025) + lissage des cotisations sur dix ans + coefficients de neutralisation par impôt et collectivité | France, RVLLP 2017 | mis en œuvre ; contentieux sur le calcul annuel du planchonnement, validation censurée en 2025 | [TEXTE LU : collectivites-locales.gouv.fr, BOFiP BOI-IF-TFB-20-30-05 ; SECONDAIRE pour la QPC] |
| Lissage financé par l'administration régionale | Pays de Galles, réévaluation de 2005 | mise en œuvre (l'Angleterre n'a jamais réévalué) | [TEXTE LU : IFS] |
| Rabais garantissant l'ancien impôt, perdu à la vente ; plafond de hausse de 4,75 %/an attaché au bien ; prêt par défaut | Danemark 2024 | mis en œuvre ; verrou probable lié au rabais | [TEXTE LU, note LVT] |
| Montée en charge inscrite dans la loi | Norvège : 1 ‰ puis +1 ‰/an | appliquée (Oslo 2016-2017) | [TEXTE LU, note LVT] |
| Transition longue (vingt ans) | ACT depuis 2012 | enlisée vers 29 % des recettes propres ; recentrée sur les primo-accédants en 2026 | [SECONDAIRE, note LVT] |
| Convergence programmée vers la valeur de marché | Corée 2020 | abandonnée en 2024 après la défaite électorale de 2022 | [SECONDAIRE, note LVT] |
| Bascule bien par bien, à la première vente | Victoria 2024 (commercial) ; amendement Juvin 2026 (révision des valeurs) | trop récent | [SECONDAIRE] ; [TEXTE LU] |
| Plafond attaché au propriétaire | Californie, Michigan, Floride | verrou mesuré (Ferreira ; Wasi et White) ; inégalité entre voisins | [TEXTE LU, note LVT] |

**Leçons tirées de ces cas** (observations, pas effets causaux) :
1. Le lissage doit être attaché au bien (plafond annuel de hausse, en montant ou en pourcentage), pas au
   propriétaire, pour ne pas créer de verrou.
2. Les taux doivent être recalculés sur les valeurs réelles une fois connues, pas sur des projections
   (Pittsburgh) ; un registre de taux neutres non contraignant ne garantit pas la neutralité (BW).
3. Les transitions très longues s'enlisent (ACT) ou sont annulées par l'alternance (Corée) ; les plus
   courtes tiennent quand elles s'accompagnent d'amortisseurs ciblés (Philadelphie, Danemark).
4. Le report de paiement doit être automatique, porter intérêt au coût de financement public, être gagé
   sur le bien et, selon l'IFS, réservé aux ménages incapables de payer sur leur revenu, pour limiter le
   risque d'effacement politique.
5. Toute montée en charge protège les propriétaires du moment aux dépens des autres contribuables (ce
   qu'ils ne perdent pas à l'annonce est la recette à laquelle l'État renonce) ; elle ne protège
   réellement que la trésorerie (note LVT).
6. Les mécanismes de lissage doivent être écrits pour résister au contentieux (planchonnement, 2023-2025).

---

## Sources non vérifiées ou incomplètement vérifiées

- Nielsson, Wroblewski et Yding (2024) : seules les six premières pages de la version en ligne ont été
  lues ; l'explication de l'écart avec Høj et al. par les résidences de vacances n'a pas été retrouvée.
- Plassmann et Tideman (2000) : coefficients de l'article du *JUE* non lus ; seuls le résumé de la thèse
  et des synthèses.
- Thunecke (2026), « Property Taxation and Housing Supply » : résumé seulement, texte introuvable.
- Lyytikäinen (2009), *JUE* 65(3) : 10 % (document de travail) ou 12 % (article) ; texte non lu ; Hannonen
  (2008) sur Espoo : secondaire.
- Bowman et Bell (2008) ; Oates et Fischel (2016) ; Song et Zenou (2006) ; Baskaran (2014) ; Charlot,
  Paty et Piguet (2015) ; Leprince, Madiès et Paty (2007) : résumés seulement.
- Schwerhoff, Edenhofer et Fleurbaey (FMI WP/22/263) : chiffres français non vérifiés (accès refusé).
- Carroll et Yinger (1994) : chiffre repris de Zodrow.
- Rakow (2023), critique de Berry : secondaire.
- Plafonds de revenu 2026 des articles 1417 I et II CGI (12 793 € et 30 083 € pour une part) : LégiFiscal
  citant le BOFiP, barème non consulté ; absence de dispositif général de report de la TFPB : non vérifiée
  de façon exhaustive.
- Plafond de taux de TFPB (2,5 fois le taux moyen, art. 1636 B sexies et septies CGI) et règles de lien :
  secondaire.
- Décision n° 2025-1174 QPC (planchonnement) : texte de la décision non lu ; n° 2015-525 QPC : secondaire.
- Amendement I-3528 (révision à chaque vente, succession ou donation) et sort de l'amendement I-CF1872 en
  séance : non vérifiés.
- France Stratégie (2016), options de réforme de la fiscalité du logement : page d'origine supprimée,
  contenu tiré d'extraits.
- Part des propriétaires payant la taxe foncière en une fois (deux tiers) : presse, chiffre DGFiP non
  retrouvé.
- Bade-Wurtemberg : contenu du § 40 al. 8 et du § 50a LGrStG (Grundsteuer C) ; nombre de communes ayant
  adopté la Grundsteuer C (Tübingen et Wendlingen parmi les premières, presse) ; répartition du sol entre
  lots de copropriété ; date de publication des motifs du BFH ; dépôt et numéros des recours
  constitutionnels (1 BvR 1977/26 et 1 BvR 2005/26, source associative) ; Hebesatz médian de 290 %.
- Danemark : plafonds communaux 2024-2028 (3,1 ‰ à 17,7 ‰, EY) ; taux du prêt de gel (2,66 % en 2025).
- Estonie : plafond de hausse de 50 % ou 20 € et exonération du terrain de la résidence principale
  (cabinets et presse, loi non lue).
- Finlande : date d'introduction du taux séparé sur le sol (2024).
- Proposition 13 : causes du vote (réforme de 1967, arrêt Serrano, inflation).
- Stuttgart, coût annexe du logement (Bund der Steuerzahler, novembre 2025) et immowelt (787 € pour une
  maison sur 508 m² en BW) : sources associative et commerciale.
